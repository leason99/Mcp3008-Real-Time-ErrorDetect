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

char spidev_path[] = "/dev/spidev0.0";
//myadd
struct msg
{
    long mtype;
    int value[3];
};
struct thread_data
{
    int count;
    int qid;
    int len;
};

//glob argument
int limit = 700;
int samples = 50000;
int chnum = 3;

    //myadd
    int abort_read;
struct thread_data *data_point;
void register_sig_handler();
void sigint_handler(int sig);
void show_elapsed(struct timeval *start, struct timeval *end, int count);
//int loop(int speed, int blocks, int ch);
void loop();
void recValue();

void listener();
void init();
int *getListenerData();

void init()
{
    printf("int: %d  int*: %d", sizeof(int), sizeof(int *));
   //mkfifo("/tmp/data", 0555);

    data_point = malloc(sizeof(struct thread_data));
    data_point->count = 0;
    data_point->len = sizeof(struct msg) - sizeof(long);
    data_point->qid = msgget(IPC_PRIVATE, IPC_CREAT | 0666);

    printf("\n data_point1 qid:%d", data_point->qid);
    Py_RETURN_NONE;
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
    pthread_t id;
    if (pthread_create(&id, NULL, (void *)recValue, NULL) < 0)
    {
        perror("listener thread creat error");
        exit(1);
    }

    Py_RETURN_NONE;
}

void detect(PyObject *self)
{
    int opt, blocks, ch, speed, i;
    struct timeval start, end;
    //myadd
    pthread_t id;

    struct msg pmsg;
    //myadd
    register_sig_handler();
    blocks = 1;
    ch = 0;
    speed = 3600000;

    if (gettimeofday(&start, NULL) < 0)
    {
        perror("gettimeofday: start");
        Py_RETURN_NONE;
    }
    //my code
    if (pthread_create(&id, NULL, (void *)loop, NULL) < 0)
    {
        perror("detect thread creat error");
        exit(1);
    }

    pthread_join(id, NULL);

    //mycode

    if (data_point->count > 0)
    {
        if (gettimeofday(&end, NULL) < 0)
            perror("gettimeofday: end");

        else
            show_elapsed(&start, &end, data_point->count);
    }
    printf("\ndetect return");
    Py_RETURN_NONE;
}

void recValue()
{

    //int pipe = open("/tmp/data", O_WRONLY);
    //printf("recValue write pipe:%d", pipe);
    CirQueue q[3];
    int item = 0;
    int count = 0;
    int achieve = 0;
    char value[4];
    int i=0;
    int w = 0;
    initCirQueue(&q[0]);
    initCirQueue(&q[1]);
    initCirQueue(&q[2]);

    struct msg 
    *pmsg;
    pmsg = malloc(sizeof(struct msg));
    pmsg->mtype = 1;
    FILE *dataFile;
    mkdir("./data", 0777);
    while (1)
    {
        int code = msgrcv(data_point->qid, pmsg, data_point->len, 1, 0);

        if (code < 0)
        {
            printf("rcv error");
            //exit(1);
        }
        else if (code > 0)
        {
            //printf("%u",pmsg->value[0]);

            if (achieve)
            {
                count++;
            }
            else
            {
                if (pmsg->value[0] > limit | pmsg->value[1] > limit | pmsg->value[2] > limit)
                {   achieve = 1;
                    
                    char text[100];
                    time_t now = time(NULL);
                    struct tm *t = localtime(&now);
                    strftime(text, sizeof(text)-1, "./data/%d %m %Y %H:%M:%S.txt", t);
                    dataFile=fopen(text,"w");

                    
                }
            }

            if (isFull(&q[0]) == 1)
            {
                for (i=0;i<chnum;i++){
                    deleteCirQueue(&q[i], &item);
                }
            }
            for (i=0;i<chnum;i++){
                insertCirQueue(&q[i], pmsg->value[i]);
            }
            
            //insertCirQueue(&q, 1);
            if (count >= samples / 2 & q[0].count == samples)
            {
                //reset   
                achieve = 0;
                count = 0;

                
                int *Databuf = malloc(sizeof(int) * samples * chnum);
                //printf("\n count :%d", q[0].count);
                
                for (i = 0; i < chnum; i++)
                {
                    for (w = 0; w < samples; w++)
                    {
                        deleteCirQueue(&q[i], Databuf + w + (i * samples));
                        
                        int value=*(Databuf + w + (i * samples));
                        fprintf(dataFile, "%d,",value );
                        //printf( "%d,",value);
                        //fprintf(dataFile, "sdfdsf,");

                    }
                }
                fclose(dataFile);
                dataFile=NULL;
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
        }
    }
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

    while (!abort_read)
    {

        if (ioctl(fd, SPI_IOC_MESSAGE(blocks), tr) < 0)
        {
            perror("ioctl");
            goto loop_done;
        }

        for (i = 0; i < blocks; i++)
        {
            pmsg->value[i] = (((int)rx[1 + (i * 4)] << 2) | (rx[2 + (i * 4)] >> 6));
        }

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

    return;
}

// We know the diff is never going to be that big so don't worry
// about wrapping issues.
void show_elapsed(struct timeval *start, struct timeval *end, int count)
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
}
void freeme(int *ptr)
{
    printf("freeing address: %p\n", ptr);
    free(ptr);
}