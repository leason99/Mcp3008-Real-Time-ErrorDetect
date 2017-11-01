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

#include <pthread.h>
#include <sys/msg.h>
#include <sys/ipc.h>
char spidev_path[] = "/dev/spidev0.0";
//myadd
struct msg {
    long mtype;
    char value[1];
    
};

struct thread_data {
    int count;
    int qid;
    int len;
};
 
//myadd

void register_sig_handler();
void sigint_handler(int sig);
void show_elapsed(struct timeval *start, struct timeval *end, int count);
//int loop(int speed, int blocks, int ch);
void loop(void *count);
void recValue();
int dump(int blocks, unsigned char *rx);

int abort_read;
int verbose;

void usage(char *argv_0)
{
    printf("\nUsage: %s <options> [adc-list]\n", argv_0);
    printf("  -b<block>       Blocks per read, default 1, max 1000\n");
    printf("  -c<channel>     Channel, default 0, range 0-7\n");
    printf("  -s<speed>       SPI clock speed, default 3600000\n");
    printf("  -v              Verbose, dumps values from last read\n");
    printf("\nExample:\n\t%s -b100 0 -c1\n", argv_0);

    exit(0);
}

int main(int argc, char **argv)
{
    int opt, blocks, ch, speed, i;
    struct timeval start, end;
    //myadd
    pthread_t id,id2;
    int ret,ret2;
    //myadd

    register_sig_handler();

    blocks = 1;
    ch = 0;
    speed = 3600000;

    while ((opt = getopt(argc, argv, "b:c:hv")) != -1) {
        switch (opt) {
        case 'b':
            blocks = atoi(optarg);

            if (blocks < 1 || blocks > 1000) {
                printf("Valid block range is 1 - 1000\n");
                exit(1);
            }

            break;

        case 'c':
            ch = atoi(optarg);

            if (ch < 0 || ch > 7) {
                printf("Valid channels are 0 - 7\n");
                exit(1);
            }

            break;

        case 's':
            speed = atoi(optarg);

            if (speed < 1000000 || speed > 10000000) {
                printf("Valid speeds are 1000000 to 10000000\n");
                exit(1);
            }

            break;

        case 'v':
            verbose = 1;
            break;

        case 'h':
        default:
            usage(argv[0]);
            break;
        }
    }

    if (gettimeofday(&start, NULL) < 0) {
        perror("gettimeofday: start");
        return 1;
    }
    //my code
    //int count= loop(speed, blocks, ch);
    int qid;
   /*if(qid=msgget(IPC_PRIVATE,IPC_CREAT|0666)<0){

        perror("msgget");
        exit(1);
    }*/


    qid=msgget(IPC_PRIVATE,IPC_CREAT|0666);

    printf("%d",qid);
    struct thread_data data;
    struct msg pmsg;
    data.qid=qid;
    data.count=0;
    data.len=sizeof(struct msg)-sizeof(long);
    ret=pthread_create(&id,NULL,(void *) loop,(void*)&data);
    ret2=pthread_create(&id2,NULL,(void *) recValue,(void*)&data);
    
    pthread_join(id,NULL);
    //mycode
    int count=data.count;
    
    if (count > 0) {
        if (gettimeofday(&end, NULL) < 0)
            perror("gettimeofday: end");
        else
            show_elapsed(&start, &end, count);
    }

    return 0;
}

void recValue(void *data){
    struct thread_data *data_point=( struct thread_data*)data;
    struct msg *pmsg;
    pmsg= malloc(sizeof(struct msg));
    pmsg->mtype=1;
    while(1){
        int code=msgrcv(data_point->qid, pmsg, data_point->len,1,0);
        if(code<0){
            perror("rcv error");
            exit(1);
            }
        else if (code>0){
            //printf("%u",pmsg->value[0]);
            }
            else{printf("no message");
        }
    
  
    
            }
}
void loop(void *data)
{   int speed =3600000;
    int blocks=1;
    int ch=0;
    int i;
    //annotation count for thread 
    //int count = 0;
    int fd = 0;
    struct spi_ioc_transfer *tr = 0;
    unsigned char *tx = 0;
    unsigned char *rx = 0;
    //myadd
    struct thread_data *data_point=(struct thread_data*)data;
    struct msg *pmsg;
    pmsg= malloc(sizeof(struct msg));
    pmsg->mtype=1;


    //myadd
    tr = (struct spi_ioc_transfer *) malloc(blocks * sizeof(struct spi_ioc_transfer));

    if (!tr) {
        perror("malloc");
        goto loop_done;
    }

    // use 4 byte increments to keep things better aligned
    tx = (unsigned char *) malloc(blocks * 4);

    if (!tx) {
        perror("malloc");
        goto loop_done;
    }

    rx = (unsigned char *) malloc(blocks * 4);

    if (!rx) {
        perror("malloc");
        goto loop_done;
    }

    memset(tr, 0, blocks * sizeof(struct spi_ioc_transfer));
    memset(tx, 0, blocks);
    memset(rx, 0, blocks);

    for (i = 0; i < blocks; i++) {
        tx[i*4] = 0x60 | (ch << 2);
        tr[i].tx_buf = (unsigned long) &tx[i * 4];
        tr[i].rx_buf = (unsigned long) &rx[i * 4];
        tr[i].len = 3;
        tr[i].speed_hz = speed;
        tr[i].cs_change = 1;
    }

    // unset cs_change for last transfer in block or we lose
    // the first read of t
    //the next block 
    tr[blocks-1].cs_change = 0;

    //count = 0;
    
    fprintf(stdout, "\n(use ctrl-c to stop)\n\n");

    fd = open(spidev_path, O_RDWR);

    if (fd < 0) {
        perror("open()");
        printf("%s\n", spidev_path);
        goto loop_done;
    }

    while (!abort_read) {
        if (ioctl(fd, SPI_IOC_MESSAGE(blocks), tr) < 0) {
            perror("ioctl");
            goto loop_done;
        }
        int16_t a2dVal = 0;
        //printf("%u |%u |%u |%u\n",rx[0],rx[1],rx[2],rx[3]);
        //rx[1] &= 0x03;  // only bits 0-1 are data
        a2dVal = (((int16_t)rx[1] << 2) | (rx[2]>>6));
        pmsg->value[0]=a2dVal;
        
        if(msgsnd(data_point->qid,pmsg,data_point->len,0)<0){
            perror("send error");
            exit(1);
        }
        //msgsnd(data_point->qid,pmsg,data_point->len,0);
        
        //printf("%d\n",a2dVal);
       
        //sleep(1);
        data_point->count+= blocks;
    }

    if (verbose)
        dump(blocks, rx);

loop_done:

    if (fd)
        close(fd);

    if (rx)
        free(rx);

    if (tx)
        free(tx);

    if (tr)
        free(tr);

    return ;
}

int dump(int blocks, unsigned char *rx)
{
    int i, j, val;

    printf("\nLast block of data\n");

    for (i = 0, j = 0; i < blocks; i++, j += 4) {
        val = (rx[j+1] << 2) + (rx[j+2] >> 6);
        printf("%03d: %d\n", i, val);
    }

    printf("\n");
}

// We know the diff is never going to be that big so don't worry
// about wrapping issues.
void show_elapsed(struct timeval *start, struct timeval *end, int count)
{
    double diff;
    double rate;

    if (end->tv_usec > start->tv_usec) {
        diff = (double) (end->tv_usec - start->tv_usec);
    }
    else {
        diff = (double) ((1000000 + end->tv_usec) - start->tv_usec);
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

    if (sigaction(SIGINT, &sia, NULL) < 0) {
        perror("sigaction(SIGINT)");
        exit(1);
    }
}

void sigint_handler(int sig)
{
    abort_read = 1;
}
