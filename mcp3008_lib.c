/*
   Copyright (C) 2017, Jumpnow Technologies, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <signal.h>
#include <sys/ioctl.h>
#include <time.h>
#include <sys/time.h>

#include <getopt.h>
#include <errno.h>
#include <linux/spi/spidev.h>
#include <python3.4/Python.h>
#include <pthread.h>
#include <sys/msg.h>
#include <sys/ipc.h>
#include <numpy/arrayobject.h>
#include "lfq.h"
#include <mongoc.h>

char spidev_path[] = "/dev/spidev0.0";
const char *uri_str = "mongodb://192.168.1.171:27017";
mongoc_client_t *client;
mongoc_database_t *database;
mongoc_collection_t *collection;

//myadd
struct msg
{
    long mtype;
    int value[5];
    // ch1,ch2,ch3,sec,usec
};
struct thread_data
{
    int count;
    int qid;
    int len;
};

//glob argument
int limit = 700;
int detectionTimes = 0;
int samples = 50000;
int chnum = 3;
FILE *dataFile;
//myadd

int abort_read;
struct timeval start, end;
int abort_rec;

pthread_t listenerId;
pthread_t detectId;

struct thread_data *data_point;
typedef void (*Func)();
void stop();
void register_sig_handler();
void sigint_handler(int sig);
double show_elapsed(struct timeval *start, struct timeval *end, int count);
//int loop(int speed, int blocks, int ch);
void loop();
void recValue();
void listener();
void init();
int *getListenerData();

void init(int Limit)

{
    printf("%d", Limit);
    limit = Limit;
    detectionTimes = 0;
    abort_read = 0;
    abort_rec = 0;
    register_sig_handler();
    printf("int: %d  int*: %d", sizeof(int), sizeof(int *));
    //mkfifo("/tmp/data", 0555);

    data_point = malloc(sizeof(struct thread_data));
    data_point->count = 0;
    data_point->len = sizeof(struct msg) - sizeof(long);
    data_point->qid = msgget(IPC_PRIVATE, IPC_CREAT | 0666);

    printf("\n data_point1 qid:%d", data_point->qid);
    
    client = mongoc_client_new(uri_str);
    mongoc_client_set_appname(client, "connect-example");
    database = mongoc_client_get_database(client, "mcp3008");
    collection = mongoc_client_get_collection(client, "mcp3008", "device1");
}

int *getListenerData()
{
    char value[4];

    int code = 0;

    int pipe = open("/tmp/data", O_RDONLY);
    printf("R pipe:%d", pipe);
    while (read(pipe, value, 4) <= 0)
    {
        printf("\nwhile");
    }
    int *rs;
    char *r = &rs;
    int x;

    for (x = 0; x < 4; x++)
    {
        *(r + x) = value[x];
    }

    printf("rs address %p", rs);

    return rs;
}

void listener()
{
    printf("start listener");

    if (pthread_create(&listenerId, NULL, (void *)recValue, NULL) < 0)
    {
        perror("listener thread creat error");
        exit(1);
    }

    Py_RETURN_NONE;
}

void detect(PyObject *self)
{
    int opt, blocks, ch, speed, i;

    //myadd
    pthread_t id;
    struct msg pmsg;
    //myadd

    blocks = 1;
    ch = 0;
    speed = 3600000;

    if (gettimeofday(&start, NULL) < 0)
    {
        perror("gettimeofday: start");
    }
    //my code
    detectId = pthread_create(&id, NULL, (void *)loop, NULL);
    if (detectId < 0)
    {
        perror("detect thread creat error");
        exit(1);
    }

    //pthread_join(id, NULL);

    //mycode

    printf("\ndetect return");
}
void stop()
{

    raise(SIGINT);
    //pthread_cancel(detectId);
}

int getDetectionTimes()
{
    return detectionTimes;
}
void recValue()
{
    bson_t  *document, child;
    char buf[16];
    const char *key;
    bson_error_t error;

    //int pipe = open("/tmp/data", O_WRONLY);
    //printf("recValue write pipe:%d", pipe);
    CirQueue q[3];
    int item = 0;
    int count = 0;
    int achieve = 0;
    char value[4];
    int i = 0;
    int w = 0;
    int partialSamples = 0;

    struct timeval startPoint, endPoint;
    initCirQueue(&q[0]);
    initCirQueue(&q[1]);
    initCirQueue(&q[2]);

    struct msg *pmsg;
    pmsg = malloc(sizeof(struct msg));
    pmsg->mtype = 1;
    mkdir("./data", 0777);
    while (!abort_rec)
    {
        int code = msgrcv(data_point->qid, pmsg, data_point->len, 1, 0);

        if (code < 0)
        {
            printf("rcv error");
            sleep(2);
        }
        else if (code > 0)
        {

            if (achieve)
            {
                count++;
            }
            else
            {
                if (pmsg->value[0] > limit | pmsg->value[1] > limit | pmsg->value[2] > limit)
                {
                    achieve = 1;
                    detectionTimes = detectionTimes + 1;
                    char text[100];
                    time_t now = time(NULL);
                    struct tm *t = localtime(&now);
                    strftime(text, sizeof(text) - 1, "./data/%d %m %Y %H:%M:%S.txt", t);
                    dataFile = fopen(text, "w");
                    startPoint.tv_sec = pmsg->value[3];
                    startPoint.tv_usec = pmsg->value[4];
                    document = bson_new();

                    BSON_APPEND_DATE_TIME(document, "time", now);
                    if (q[0].count == samples)
                    {
                        partialSamples = samples / 2;
                    }
                    else
                    {
                        partialSamples = samples - q[0].count;
                    }
                }
            }

            if (isFull(&q[0]) == 1)
            {
                for (i = 0; i < chnum; i++)
                {
                    deleteCirQueue(&q[i], &item);
                }
            }
            for (i = 0; i < chnum; i++)
            {
                insertCirQueue(&q[i], pmsg->value[i]);
            }

            //insertCirQueue(&q, 1);
            if (count >= samples / 2 & q[0].count == samples)
            {
                //reset
                achieve = 0;
                count = 0;

                endPoint.tv_sec = pmsg->value[3];
                endPoint.tv_usec = pmsg->value[4];

                int *Databuf = malloc(sizeof(int) * samples * chnum);
                //printf("\n count :%d", q[0].count);
                BSON_APPEND_ARRAY_BEGIN(document, "languages", &child);
                for (i = 0; i < chnum; i++)
                {
                    for (w = 0; w < samples; w++)
                    {

                        deleteCirQueue(&q[i], Databuf + w + (i * samples));

                        int value = *(Databuf + w + (i * samples));
                        fprintf(dataFile, "%d,", value);

                        int keylen = bson_uint32_to_string(w + (i * samples), &key, buf, sizeof buf);
                        bson_append_int32(&child, key, (int)keylen, value);
                    }
                }
                bson_append_array_end(document, &child);

                double samplerate = show_elapsed(&startPoint, &endPoint, partialSamples);
                BSON_APPEND_DOUBLE(document, "samplerate", samplerate);
                if (!mongoc_collection_insert(collection, MONGOC_INSERT_NONE, document, NULL, &error))
                {
                    fprintf(stderr, "%s\n", error.message);
                }
                bson_destroy(document);
                fprintf(dataFile, "%f", samplerate);

                fclose(dataFile);
                dataFile = NULL;
                printf("\ni:%d cout: %d empty: %d |value: %d", w, q[0].count, isEmpty(&q), *(Databuf + w - 1));
                char *c = &Databuf;
                for (i = 0; i < 4; i++)
                {
                    value[i] = *(c + i);
                }

                //write(pipe, value, 4);

                printf("address %p", Databuf);
                free(Databuf);
                //sleep(2);
            }
        }
        else
        {
            printf("\nno message");
            sleep(1);
        }
    }
    //deleteFailFile();
}
void loop()
{
    int speed = 3600000;
    int blocks = chnum;
    int ch = 0;
    int i;
    //annotation count for thread
    //int count = 0;
    int fd = 0;
    struct spi_ioc_transfer *tr = 0;
    unsigned char *tx = 0;
    unsigned char *rx = 0;
    //myadd
    struct msg *pmsg;
    pmsg = malloc(sizeof(struct msg));
    pmsg->mtype = 1;
    //myadd
    tr = (struct spi_ioc_transfer *)malloc(blocks * sizeof(struct spi_ioc_transfer));
    if (!tr)
    {
        perror("malloc");
        goto loop_done;
    }
    tx = (unsigned char *)malloc(blocks * 4);
    if (!tx)
    {
        perror("malloc");
        goto loop_done;
    }
    rx = (unsigned char *)malloc(blocks * 4);
    if (!rx)
    {
        perror("malloc");
        goto loop_done;
    }

    memset(tr, 0, blocks * sizeof(struct spi_ioc_transfer));
    memset(tx, 0, blocks);
    memset(rx, 0, blocks);

    for (i = 0; i < blocks; i++)
    {
        // tx[i * 4] = 0x60 | (ch << 2);
        tx[i * 4] = 0x60 | (i << 2);
        tr[i].tx_buf = (unsigned long)&tx[i * 4];
        tr[i].rx_buf = (unsigned long)&rx[i * 4];
        tr[i].len = 3;
        tr[i].speed_hz = speed;
        tr[i].cs_change = 1;
    }

    // unset cs_change for last transfer in block or we lose
    // the first read of t
    //the next block
    tr[blocks - 1].cs_change = 0;

    fprintf(stdout, "\n(use ctrl-c to stop)\n\n");

    fd = open(spidev_path, O_RDWR);

    if (fd < 0)
    {
        perror("open()");
        printf("%s\n", spidev_path);
        goto loop_done;
    }
    struct timeval instantTime;
    while (!abort_read)
    {
        pthread_testcancel();
        if (ioctl(fd, SPI_IOC_MESSAGE(blocks), tr) < 0)
        {
            perror("ioctl");
            goto loop_done;
        }

        for (i = 0; i < blocks; i++)
        {
            pmsg->value[i] = (((int)rx[1 + (i * 4)] << 2) | (rx[2 + (i * 4)] >> 6));
        }
        gettimeofday(&instantTime, NULL);
        pmsg->value[3] = instantTime.tv_sec;
        pmsg->value[4] = instantTime.tv_usec;
        //printf("ch1: %d ch2: %d ch3: %d ",pmsg->value[0],pmsg->value[1],pmsg->value[2]);

        if (msgsnd(data_point->qid, pmsg, data_point->len, 0) < 0)
        {
            perror("send error");
            exit(1);
        }

        data_point->count += 1;
    }

loop_done:

    if (fd)
        close(fd);
    if (rx)
        free(rx);
    if (tx)
        free(tx);
    if (tr)
        free(tr);
    //msgctl(data_point->qid, IPC_RMID, NULL);

    return;
}

// We know the diff is never going to be that big so don't worry
// about wrapping issues.
double show_elapsed(struct timeval *start, struct timeval *end, int count)
{
    double diff;
    double rate;

    if (end->tv_usec > start->tv_usec)
    {
        diff = (double)(end->tv_usec - start->tv_usec);
    }
    else
    {
        diff = (double)((1000000 + end->tv_usec) - start->tv_usec);
        end->tv_sec--;
    }

    diff /= 1000000.0;

    diff += (double)(end->tv_sec - start->tv_sec);

    if (diff > 0.0)
        rate = count / diff;
    else
        rate = 0.0;

    printf("Summary\n  Elapsed: %0.2lf seconds\n    Reads: %d\n     Rate: %0.2lf Hz\n\n",
           diff, count, rate);

    return rate;
}

void register_sig_handler()
{
    struct sigaction sia;

    bzero(&sia, sizeof sia);
    sia.sa_handler = sigint_handler;

    if (sigaction(SIGINT, &sia, NULL) < 0)
    {
        perror("sigaction(SIGINT)");
        exit(1);
    }
}

void sigint_handler(int sig)
{
    abort_read = 1;
    if (data_point->qid != NULL)
    {
        if (data_point->count > 0)
        {
            if (gettimeofday(&end, NULL) < 0)
                perror("gettimeofday: end");

            else
                show_elapsed(&start, &end, data_point->count);
        }
        sleep(1);
        //deleteFailFile();
        struct msqid_ds ds;

        while (1)
        {
            if ((msgctl(data_point->qid, IPC_STAT, &ds)) < 0)
            {
                printf("msgctl讀取錯誤。n");
            }

            if (ds.msg_qnum == 0)
            {

                abort_rec = 1;
                break;
            }
        }

        if ((msgctl(data_point->qid, IPC_RMID, NULL)) < 0)
        {
            printf("msgctl刪除錯誤。n");
        }
        else
        {
            data_point->qid = NULL;
        }

        deleteFailFile();
        
        


        /*
    * Release our handles and clean up libmongoc
    */
        mongoc_collection_destroy(collection);
        mongoc_database_destroy(database);
        mongoc_client_destroy(client);
        mongoc_cleanup();
    }
}

void deleteFailFile()
{

    if (dataFile != NULL)
    {

        char proclnk[255];
        char *filepath = malloc(255);
        ssize_t r;
        int fno = fileno(dataFile);
        sprintf(proclnk, "/proc/self/fd/%d", fno);
        r = readlink(proclnk, filepath, 255);
        if (r < 0)
        {
            printf("failed to readlink\n");
            exit(1);
        }
        filepath[r] = '\0';
        printf(filepath);
        remove(filepath);
        fclose(dataFile);
        free(filepath);
    }
}
void freeme(int *ptr)
{
    printf("freeing address: %p\n", ptr);
    free(ptr);
}