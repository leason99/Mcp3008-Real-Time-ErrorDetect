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
    int value[1];
};
struct resdata
{
    long mtype;
    char value[4];
};
struct thread_data
{
    int count;
    int qid;
    int len;
};

//myadd
int abort_read;
struct thread_data *data_point, *data_point2;
CirQueue DataQueue;
PointerCirQueue *PointerQueue;
void register_sig_handler();
void sigint_handler(int sig);
void show_elapsed(struct timeval *start, struct timeval *end, int count);
//int loop(int speed, int blocks, int ch);
void loop();
void recValue(int *);

void listener(int *listenerData_point);
void init();
int *getListenerData();

void init()
{
    printf("int: %d  int*: %d", sizeof(int), sizeof(int *));
    mkfifo("data", 0555);
    
    PointerQueue = malloc(sizeof(PointerCirQueue));
    initCirQueue(&DataQueue);
    initCirQueue(PointerQueue);
    data_point2 = malloc(sizeof(struct thread_data));
    data_point2->count = 0;
    data_point2->len = sizeof(struct resdata) - sizeof(long);
    data_point2->qid = msgget(IPC_PRIVATE, IPC_CREAT | 0777);
    data_point = malloc(sizeof(struct thread_data));
    data_point->count = 0;
    data_point->len = sizeof(struct msg) - sizeof(long);
    data_point->qid = msgget(IPC_PRIVATE, IPC_CREAT | 0666);

    printf("\ndata_point2 qid:%d  | data_point21 qid:%d", data_point2->qid, data_point->qid);
    Py_RETURN_NONE;
}
void listenerData(int *rs)
{

    struct resdata *lsd;
    lsd = malloc(sizeof(struct resdata));
    lsd->mtype = 10;
    int code = 0;
    printf("\ndata_point2 qid:%d  | data_point21 qid:%d", data_point2->qid, data_point->qid);
    printf("\nlsd mtype:%d  | data_point2->len:%d", lsd->mtype, data_point2->len);
    int qid = data_point2->qid;
    int len = data_point2->len;
    int pipe = open("data", O_RDONLY);
    printf("R pipe:%d",pipe);
    while (read(pipe, lsd->value, 4) <= 0)
    {
        printf("\nwhile");
        sleep(1);
        //code = msgrcv(data_point2->qid , lsd, len, 10, 0);
        /*
        printf("\nmsgrcv code:%d", code);
        //printf("\nlsd->value:%p", lsd->value[0]);

        if (code < 0)
        {
            printf("\nError\n");
        }
        else if (code > 0)
        {
            //int *rs;
            char *r = &rs;
            int x;
            for (x = 0; x < 4; x++)
            {

                *(r + x) = lsd->value[x];
            }
            printf("rs address %p",rs);
            
            return ;
        }


        else
        {
            printf("\nelse_code:%d", code);
        }*/
    }
    char *r = &rs;
    int x;

    for (x = 0; x < 4; x++)
    {

        *(r + x) = lsd->value[x];
    }
    printf("rs address %p",rs);

    return;

    pthread_exit(NULL);
}
int *getListenerData()
{ /*printf("PointerQueueAddress:%p",PointerQueue);
    while (1)
    {
        int **pointer;
        if (PointerQueue->count>0)
        {
            printf("deletePointerQueue");
            deleteCirQueue(PointerQueue, *pointer);

                return *pointer;
        }
        else
        {

            sleep(1);
            printf("empty");
        }
    }

    return NULL;
*/
 /*   int *rs;
    pthread_t id;
    if (pthread_create(&id, NULL, (void *)listenerData, rs) < 0)
    {
        perror("detect thread creat error");
        exit(1);
    }
    printf("creat getListenerData ");
    pthread_join(id, NULL);
*/
    /*
    struct resdata *lsd;
    lsd = malloc(sizeof(struct resdata));
    lsd->mtype = 10;
    int code = 0;
    printf("\ndata_point2 qid:%d  | data_point21 qid:%d", data_point2->qid, data_point->qid);
    printf("\nlsd mtype:%d  | data_point2->len:%d", lsd->mtype, data_point2->len);
    int qid = data_point2->qid;
    int len = data_point2->len;
    while (1)
    {
        printf("\nwhile");

        code = msgrcv(qid, lsd, len, 10, 0);

        printf("\nmsgrcv code:%d", code);
        //printf("\nlsd->value:%p", lsd->value[0]);

        if (code < 0)
        {
            printf("\nError\n");
        }
        else if (code > 0)
        
        {
            int *rs;
            char *r = &rs;
            int x;
            for (x = 0; x < 4; x++)
            {

                *(r + x) = lsd->value[x];
            }
            return rs;
        }

        else
        {
            printf("\nelse_code:%d", code);
        }
    }*/
    struct resdata *lsd;
    lsd = malloc(sizeof(struct resdata));
    lsd->mtype = 10;
    int code = 0;
    //printf("\ndata_point2 qid:%d  | data_point21 qid:%d", data_point2->qid, data_point->qid);
    //printf("\nlsd mtype:%d  | data_point2->len:%d", lsd->mtype, data_point2->len);
    int qid = data_point2->qid;
    int len = data_point2->len;
    int pipe = open("data", O_RDONLY);
    printf("R pipe:%d",pipe);
    while (read(pipe, lsd->value, 4) <= 0)
    {
        printf("\nwhile");
        
        //code = msgrcv(data_point2->qid , lsd, len, 10, 0);
        /*
        printf("\nmsgrcv code:%d", code);
        //printf("\nlsd->value:%p", lsd->value[0]);

        if (code < 0)
        {
            printf("\nError\n");
        }
        else if (code > 0)
        {
            //int *rs;
            char *r = &rs;
            int x;
            for (x = 0; x < 4; x++)
            {

                *(r + x) = lsd->value[x];
            }
            printf("rs address %p",rs);
            
            return ;
        }


        else
        {
            printf("\nelse_code:%d", code);
        }*/
    }
    int *rs;
    char *r = &rs;
    int x;

    for (x = 0; x < 4; x++)
    {

        *(r + x) = lsd->value[x];
    }

    

    printf("rs address %p", rs);

    return rs;
}

void listener(int *listenerData_point)
{
    printf("listener");
    pthread_t id;

    int temp;

    printf("%d", listenerData_point);
    if (pthread_create(&id, NULL, (void *)recValue, listenerData_point) < 0)
    {
        perror("listener thread creat error");
        exit(1);
    }
    //pthread_join(id,NULL);

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

void recValue(int *listenerData_point)
{
    printf("\nrecValue");
    
    int  pipe = open("data", O_WRONLY);
    printf("W pipe:%d",pipe);
    CirQueue q;
    int item = 0;
    int count = 0;
    int achieve = 0;
    initCirQueue(&q);
    struct msg *pmsg;
    pmsg = malloc(sizeof(struct msg));
    pmsg->mtype = 1;

    struct resdata *lsd;
    lsd = malloc(sizeof(struct resdata));
    lsd->mtype = 10;

    printf("start while");
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
                if (pmsg->value[0] > 500)
                {
                    achieve = 1;
                }
            }

            if (isFull(&q) == 1)
            {
                deleteCirQueue(&q, &item);
            }

            insertCirQueue(&q, pmsg->value[0]);
            //insertCirQueue(&q, 1);
            if (count >= 25000 & q.count==50000)
            {
                FILE *fp = fopen("test", "wb");

                achieve = 0;
                count = 0;
                int w = 0;
                int item_num = q.count;
                int *Databuf = malloc(sizeof(int) * 50000);
                //printf("\n count :%d", q.count);
                for (w = 0; w < item_num; w++)
                {
                    deleteCirQueue(&q, Databuf + w);

                    fprintf(fp, "%d,", *(Databuf + w));
                    //printf("delet:%d",*(listenerData_point+w));
                    //printf("\ni:%d cout: %d empty: %d |aderss: %d",w,q.count,isEmpty(&q),listenerData_point[w]);
                }

                fclose(fp);
                printf("\ni:%d cout: %d empty: %d |value: %d", w, q.count, isEmpty(&q), *(Databuf + w - 1));
                char *c = &Databuf;
                int x = 0;
                for (x = 0; x < 4; x++)
                {
                    lsd->value[x] = *(c + x);
                }
                write(pipe, lsd->value, 4);
                printf("address %p", Databuf);
                //int code = msgsnd(data_point2->qid , lsd, data_point2->len, 0);
                //printf("send %d", code);

                //PointerinsertCirQueue(PointerQueue, Databuf);
                //printf("PointerQueue count: %d",PointerQueue->count);
                sleep(2);
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
    int blocks = 1;
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
        tx[i * 4] = 0x60 | (ch << 2);
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
        pmsg->value[0] = (((int)rx[1] << 2) | (rx[2] >> 6));
        //printf("\n%d",pmsg->value[0]);
        if (msgsnd(data_point->qid, pmsg, data_point->len, 0) < 0)
        {
            perror("send error");
            exit(1);
        }

        data_point->count += blocks;
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
