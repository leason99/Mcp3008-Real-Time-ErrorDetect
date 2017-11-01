#include <stdio.h>
#include "lfq.h"

/*Declaration of circular queue.*/


/*Initailization of circular queue.*/
void initCirQueue(CirQueue * q)
{
   q->front =  0;
   q->rear  = -1;
   q->count =  0;
}

/*Check Queue is full or not*/
int isFull(CirQueue * q)
{
   int full=0;
    
   if(q->count == MAX)
       full = 1;   

   return full;
}

/*Check Queue is empty or not*/
int isEmpty(CirQueue * q)
{
   int empty=0;
    
   if(q->count == 0)
       empty = 1;  

   return empty;
}

/*To insert item into circular queue.*/
void insertCirQueue(CirQueue * q, int item)
{
   if( isFull(q) )
   {
       printf("\nQueue Overflow");
       return;
   }
    
   q->rear = (q->rear+1)%MAX;
   q->ele[q->rear] = item;
    
   q->count++;
 
   
   
   
   //printf("\nInserted item : %d",item);
}
void PointerinsertCirQueue(CirQueue * q, int* item)
{
   if( isFull(q) )
   {
       printf("\nQueue Overflow");
       return;
   }
    
   q->rear = (q->rear+1)%MAX;
   q->ele[q->rear] = item;
    printf("\nadress: %p",q->ele[q->rear]);
   q->count++;
 
   
   
   
   //printf("\nInserted item : %d",item);
}
/*To delete item from queue.*/
int deleteCirQueue(CirQueue * q, int *item)
{
   if( isEmpty(q) )
   {
       printf("\nQueue Underflow");
       return -1;
   }

   *item    = q->ele[q->front];

   q->front = (q->front+1)%MAX;
    
   q->count--;

   return 0;
}
/*

int main()
{

    int item=0;
    CirQueue q;
 
    initCirQueue(&q);
 
    insertCirQueue(&q, 10); 
    insertCirQueue(&q, 20);
    insertCirQueue(&q, 30);
    insertCirQueue(&q, 40);
    insertCirQueue(&q, 50);
    insertCirQueue(&q, 60);
 
    if ( deleteCirQueue( &q, &item ) == 0 )
        printf("\nDeleted item is : %d",item);
 
     
    if ( deleteCirQueue( &q, &item ) == 0 )
        printf("\nDeleted item is : %d",item);
 
     
    if ( deleteCirQueue( &q, &item ) == 0 )
        printf("\nDeleted item is : %d",item);
 
     
    if ( deleteCirQueue( &q, &item ) == 0 )
        printf("\nDeleted item is : %d",item);
 
     
    if ( deleteCirQueue( &q, &item ) == 0 )
        printf("\nDeleted item is : %d",item);
 
    insertCirQueue(&q, 60);
     
    if ( deleteCirQueue( &q, &item ) == 0 )
        printf("\nDeleted item is : %d",item);
 
 
    if ( deleteCirQueue( &q, &item ) == 0 )
        printf("\nDeleted item is : %d",item);
 
    printf("\n");
    return 0;   
}*/