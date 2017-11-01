
#ifndef LFQ
#define LFQ

#define MAX 50000
typedef struct 
{
   int front   ;
   int rear    ;
   int count   ;
   int ele[MAX]    ;
}CirQueue;
typedef struct 
{
   int front   ;
   int rear    ;
   int count   ;
   int *ele[MAX]    ;
}PointerCirQueue;




/*Declaration of circular queue.*/


/*Initailization of circular queue.*/
void initCirQueue(CirQueue * );
/*Check Queue is full or not*/
int isFull(CirQueue * );

/*Check Queue is empty or not*/
int isEmpty(CirQueue * );

/*To insert item into circular queue.*/
void insertCirQueue(CirQueue * , int );
void PointerinsertCirQueue(CirQueue * , int* );

/*To delete item from queue.*/
int deleteCirQueue(CirQueue * , int *);


#endif