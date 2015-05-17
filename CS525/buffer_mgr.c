#include "buffer_mgr.h"
#include <stdio.h>
#include <stdlib.h>
#include "dberror.h"
#include "storage_mgr.h"


#define maxBufferPoolNum 10
#define currentNum 0


//KUN MEI XIAOPEI  FANZHANG AND QIANJUN
RC ReplacementStra(BM_BufferPool *const bm, BM_PageHandle *const page,const PageNumber pageNum);
int currentBufferPoolNum=0;

//the global variable bufferRecord, which holds all the bufferpool information including readnum,writenum,etc 
typedef struct BufferRecord{ 
    int bufferpoolNumber;
    int readNum;    //read number
    int writeNum; //write number
    int pageAge; //a buffer bool level counter
    int lru_k;
    struct PageFrame *first;
    struct PageFrame  *last;
    int numPages;
    //int BufferNum;//BUfferPool Num
} BufferRecord; 
BufferRecord bufferRecord[maxBufferPoolNum];


typedef struct PageFrame{
    int frameNum;
    int PageNum;
    bool dirty; //store the state of the "dirty"
        int lru_k;
    int clockwise;
    char *data;
   int pageTimeRecord; // record the time record of a page,this value would be refreshed when the page was pinned into the buffer / or used by user(in LRU/LRU-K/CLOCK)
    int fixCount; //fix Count  : evict the page only when fixcount==0
    BM_PageHandle pageHandle;
    struct PageFrame *next;

} PageFrame;







SM_FileHandle *fh;  //initial several variables
char *memPage;
PageFrame *PageFrameArray[100];
// queue *g_queue ;
//int bufferRecord[currentBufferPoolNum].readNum=0;
//nt bufferRecord[currentBufferPoolNum].writeNum=0;
void setBufferRecord(BM_BufferPool *const bm)
{
     bufferRecord[currentNum].numPages=bm->numPages;
        bufferRecord[currentNum].first=PageFrameArray[0];
        bufferRecord[currentNum].last=PageFrameArray[bm->numPages-1];
}

void initPageFrame(BM_BufferPool *const bm){
    PageFrame *PageFrameNode[bm->numPages];  //
	int i;
    for(i=bm->numPages-1;i>=0;i--)
    {
        PageFrameNode[i]=(PageFrame *) malloc (sizeof(PageFrame));  //initialize every page with an array
        PageFrameNode[i]->pageHandle.pageNum=NO_PAGE;;
        PageFrameNode[i]->frameNum=i;
        PageFrameNode[i]-> pageTimeRecord =0;
        PageFrameNode[i]->dirty=0;
        PageFrameArray[i]->lru_k;
        PageFrameNode[i]->fixCount=0;
       PageFrameNode[i]->data=bm->mgmtData+PAGE_SIZE*(i);
        if(i!=bm->numPages-1)
            {   
                PageFrameNode[i]->next=PageFrameNode[i+1]; //pointer to the next page.
                
            }
        else 
            {
                PageFrameNode[i]->next=NULL;
            }

    PageFrameArray[i]=PageFrameNode[i];
     }

      if(PageFrameArray!=NULL)
        {
        setBufferRecord(bm);
        }
       
    }

// int isEmpty(struct queue *q)    //check if the page is empty
// {
//     return q->queueSize ==0 ;
// }

//a method used to search a specific page
PageFrame *checkTargetPage(BM_BufferPool *const bm, BM_PageHandle *const page)
{
    PageFrame *pf;
    pf=bufferRecord[currentNum].first;
    int i;
for(i = 0 ; i<bm->numPages;i++)
    {
        if(PageFrameArray[i]->pageHandle.pageNum==page->pageNum)
            return PageFrameArray[i];
        // pf=pf->next;
           }
    return NULL;
}

// Buffer Manager Interface Pool Handling
void setBuffer(BM_BufferPool *const bm, const char *const pageFileName, const int numPages, ReplacementStrategy strategy, void *stratData)
{
     char* buff = (char *)calloc(PAGE_SIZE*numPages,sizeof(char));
      bm->mgmtData=buff;
    bm->pageFile = (char*)pageFileName;
    bm->numPages = numPages;
    bm->strategy = strategy;
}

void initBufferRecord(int i, int numPages)    /* initialze the global variable bufferRecord, which holds all the bufferpool information including readnum,writenum,etc */
{
    char*cache = (char *)calloc(PAGE_SIZE*numPages,sizeof(char));
    bufferRecord[i].readNum=0;
    bufferRecord[i].writeNum=0;
    bufferRecord[i].pageAge=0;
    bufferRecord[i].lru_k=1;
    
  
}

RC initBufferPool(BM_BufferPool *const bm, const char *const pageFileName,const int numPages, ReplacementStrategy strategy,void *stratData)
{
    //bufferRecord[currentBufferPoolNum].writeNum=0;
    //bufferRecord[currentBufferPoolNum].readNum=0;
  initBufferRecord(currentBufferPoolNum,numPages);
    fh=(SM_FileHandle *)malloc(sizeof(SM_FileHandle));
   
    setBuffer(bm,pageFileName,numPages,strategy,stratData);
    // bm->pageFile=(char *)pageFileName;
    // bm->numPages=numPages;
    // bm->strategy=strategy;
   
    // g_queue= (queue *)malloc(sizeof(queue));
    openPageFile (bm->pageFile, fh);
    initPageFrame(bm);
    return RC_OK;
}


PageFrame *PageFrameInfo(const PageNumber pageNum)
{
     PageFrame *pf=(PageFrame *) malloc (sizeof(PageFrame));
        pf->dirty=0;
    pf->fixCount=1;
    pf->next=NULL;
    pf->pageHandle.pageNum=pageNum;
    return pf;
}

RC pinPageFrame (BM_BufferPool *const bm, BM_PageHandle *const page,const PageNumber pageNum){
    PageFrame *pf;
    pf=bufferRecord[currentNum].first;
      int i;
    int check =0;    //set a flag to test if the given page is located in the buffer
page->pageNum=pageNum;
    //check if the page is in the buffer pool   
    //check the first pageframe
     if(pf->pageHandle.pageNum==pageNum&&!(bufferRecord[currentNum].first==0))
        check=1;
 i=1;
 while(i<bm->numPages&&check==0)
    {
        pf=pf->next;
        if(pf->pageHandle.pageNum==pageNum)
            check=1;
        i++;
    }

    /**f already in the buffer pool, pin it****/
    if(check==1)  //if already in the buffer pool, pin it
    {
        pf->fixCount++;
        page->data=pf->data; //retrive the data from the page
        return RC_OK;
    }
    switch(bm->strategy)            
            {
                case RS_FIFO:
                    //do nothing
                case RS_LRU:
                    bufferRecord[currentBufferPoolNum].pageAge++;
                    pf->pageTimeRecord=bufferRecord[currentBufferPoolNum].pageAge;
                case RS_LRU_K:
                    pf->lru_k++;
                    if (bufferRecord[currentBufferPoolNum].lru_k==pf->lru_k)
                    bufferRecord[currentBufferPoolNum].pageAge++;
                    pf->pageTimeRecord=bufferRecord[currentBufferPoolNum].pageAge;

                case RS_CLOCK:
                    pf->clockwise=1;

            }
    
ReplacementStra(bm,page,pageNum);
}
//if not in the buffer pool, check if in the memory 
RC ReplacementStra (BM_BufferPool *const bm, BM_PageHandle *const page,const PageNumber pageNum){
    PageFrame* pfPtr=bufferRecord[currentNum].first;
 
    PageFrame *newPageFrame;
    newPageFrame=PageFrameInfo(pageNum);

    PageFrame* pfSearch=bufferRecord[currentNum].first;
                      //if the first page in the buff is free(fixCount==0)
            bufferRecord[currentNum].first=pfPtr->next;                   // set the first pointer of queue to the second page
    // else
    //        pfPtr_pre->next=pfPtr->next;                 //else let the previous page's next pointer points to
    newPageFrame->data=pfPtr->data;
                                                            // the next one(skip the page between them)
    // if(pfPtr==bufferRecord[currentNum].last)
    //         bufferRecord[currentNum].last=pfPtr_pre;
       
    if(pfPtr->dirty==1)                               // if the page is dirty, write it to the file
        {
            writeBlock(pfPtr->pageHandle.pageNum,fh, pfPtr->data);
            bufferRecord[currentBufferPoolNum].writeNum++;
        }
     newPageFrame->frameNum=pfPtr->frameNum;
    free(pfPtr);                                      // free the node.
    // bufferRecord[currentNum].numPages= bufferRecord[currentNum].numPages-1;           //decrease the size of queue by one
 
    
    // add the new page to the buffer(the last position of te queue in order to make it FIFO)
    readBlock(pageNum, fh, newPageFrame->data);
    page->data=newPageFrame->data;

    bufferRecord[currentBufferPoolNum].readNum++;
    bufferRecord[currentNum].last->next=newPageFrame;
    bufferRecord[currentNum].last=newPageFrame;
    PageFrameArray[newPageFrame->frameNum]=newPageFrame;
    // bufferRecord[currentNum].numPages= bufferRecord[currentNum].numPages+1;          


    return RC_OK;
}






//inistialize the buffer pool

RC shutdownBufferPool(BM_BufferPool *const bm){
    int  result,i;
    PageFrame *pf;
    pf=bufferRecord[currentNum].first;
    result=forceFlushPool(bm);         //store data into memory
    if (result=RC_OK)
        {
         setBuffer(bm,NULL,0,0,NULL);
          bufferRecord[currentBufferPoolNum].readNum=0;
         bufferRecord[currentBufferPoolNum].writeNum=0;//free(bm->mgmtData);
          closePageFile(fh);
                      for(i=0;i<bm->numPages;i++)
                      {
                                    if(pf->fixCount!=0){
                                    printf("file write failed,some one are still aceesing the buffer\n");
                                    return RC_WRITE_FAILED;
                                     }
                         pf=pf->next;
                        return RC_OK;
                      }
        }     
       else
       {
        return RC_WRITE_FAILED;
       }
    
}

RC forceFlushPool(BM_BufferPool *const bm){     //function used to store data into memory
    PageFrame *pf;
    int result;
    pf=bufferRecord[currentNum].first;
    int i;
    openPageFile(bm->pageFile, fh);
    while(pf!=NULL) //loop to check dirty files
    {
        if(pf->dirty==true&&pf->fixCount==0)   //check file if it is dirty
        {
    //    ensureCapacity(pf->pageHandle.pageNum+1,fh);  
        result=writeBlock(pf->pageHandle.pageNum,fh, pf->data);
        bufferRecord[currentBufferPoolNum].writeNum++;
             pf->dirty=0;  //after storing set the dirty flag into 0
        }

        pf=pf->next;
    }
    printf("forceFlushPool Success\n");
    return RC_OK;
}

// Buffer Manager Interface Access Pages
RC markDirty (BM_BufferPool *const bm, BM_PageHandle *const page){
    PageFrame *pf;
    pf=checkTargetPage(bm,page);
    if(pf!=NULL)
     { 
                    pf->dirty=1;
                    return RC_OK;
      }
      else
      {
        //  printf("fail to make dirty this page,please check function markDirty\n");
            return RC_NO_SUCH_PAGE_IN_BUFF;
    }
}

RC forcePage (BM_BufferPool *const bm, BM_PageHandle *const page){
    PageFrame *pf;
    int result=-1;
    pf=checkTargetPage(bm,page);
    if(pf!=NULL)
    {
    result=writeBlock(pf->pageHandle.pageNum,fh, pf->data);
    bufferRecord[currentBufferPoolNum].writeNum++;
    if (result!=0)
        {
            return RC_WRITE_FAILED;
        }
    return RC_OK;
     }
      else
      {
        return RC_WRITE_FAILED;
      }
}




RC pinPage (BM_BufferPool *const bm, BM_PageHandle *const page,const PageNumber pageNum){
    page->pageNum=pageNum;
  
            return pinPageFrame(bm,page,pageNum);
    // else //if(bm->strategy==1)
    //         return pinPage_LRU(bm,page,pageNum);

}

RC unpinPage (BM_BufferPool *const bm, BM_PageHandle *const page){
    PageFrame *pf;
    int check;
    pf=checkTargetPage(bm,page);
    //check the PageFrame founded by check tragert page
    if(pf!=NULL)
       {
        check=(*(pf->data)==*(page->data));
        if (check!=1)
            printf("failed in unpin page, the data is not the same as we expect\n");
        if (pf->fixCount>0)
            pf->fixCount-=1;
        return RC_OK;
     }
    else
         {
            printf("unpin page failed \n");
         return RC_UNPIN_ERROR;
         }
}


// Statistics Interface

PageNumber *getFrameContents (BM_BufferPool *const bm){
    PageFrame *pf;
    pf=bm->mgmtData;
    PageNumber *frameContent;
    frameContent = (int *)malloc(sizeof(int)*bm->numPages);
    int i;
    for(i = 0; i < bm->numPages; i++)
    {
        frameContent[i] = pf[i].pageHandle.pageNum;
    }
    return frameContent;

        PageNumber (*arr)[bm->numPages];
    arr=calloc(bm->numPages,sizeof(PageNumber));
     for ( i =bufferRecord[currentNum].numPages-1;i>=0;i--)
    {
        (*arr)[i]=PageFrameArray[i]->pageHandle.pageNum;
    }
    return *arr;
    
    
    
}
bool *getDirtyFlags (BM_BufferPool *const bm){ 

    PageFrame *pf;
    pf=bm->mgmtData;
    bool *dirtyFlag;
    dirtyFlag = (bool*)malloc(sizeof(bool)*bm->numPages);
    int i;
    for(i = 0; i < bm->numPages; i++)
    {
        dirtyFlag[i] = PageFrameArray[i] ->dirty;
    }
    return dirtyFlag;

    
}
int *getFixCounts (BM_BufferPool *const bm){   
        int *fixCount;
    PageFrame *pf;
    pf=bm->mgmtData;
    fixCount = (int*)malloc(sizeof(int)*bm->numPages);
    int i;
    for(i = 0; i < bm->numPages; i++)
    {
        fixCount[i] = PageFrameArray[i]->fixCount;
    }
    return fixCount; //return the fix number of the page

}
int getNumReadIO (BM_BufferPool *const bm){
    return bufferRecord[currentBufferPoolNum].readNum;
    }
int getNumWriteIO (BM_BufferPool *const bm)
{
    return bufferRecord[currentBufferPoolNum].writeNum;
}




