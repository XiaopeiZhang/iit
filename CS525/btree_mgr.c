//Xiaopei Zhang, Kun Mei, Fan Zhang, Jun Qian
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#include "buffer_mgr.h"
#include "storage_mgr.h"

#include "dberror.h"
#include "btree_mgr.h"
#include "tables.h"
#include "expr.h"

int lastPage=0;
const RID INIT_RID={-1,-1};
int scanCount=0;

typedef struct Node
{
	int mother;
	bool leaf;
	RID left;
	int value1;
	RID mid;
	int value2;
	RID right;
}Node;

typedef struct TreeInfo
{
	BM_BufferPool *bm;
	BM_PageHandle *page;
	int root;
	int globalCount;//the num of values one tree has
	int maxCount;//the max num of value one node has
}TreeInfo;

// ************************************** init and shutdown index manager ************************************
extern RC initIndexManager (void *mgmtData)
{
	printf("We are now initializing the index manager!!!\n");
	return RC_OK;
}

extern RC shutdownIndexManager ()
{
	printf("We are now shutting down the index manager!!!\n");
	return RC_OK;
}

// ******************************** create, destroy, open, and close an btree index *******************************
extern RC createBtree (char *idxId, DataType keyType, int n)
{
	printf("We are now creating the Btree!!!\n");
	createPageFile(idxId);

	SM_FileHandle fh;
	openPageFile(idxId, &fh);
	ensureCapacity(1, &fh);

	SM_PageHandle ph=malloc(PAGE_SIZE*sizeof(char));

	//index manager only handles integer values
	if(keyType!=DT_INT)
	{
		printf("The values are not integers!!!\n");
		return RC_RM_UNKOWN_DATATYPE;
	}

	
	*((int *)ph)=n;

	writeCurrentBlock(&fh,ph);

	closePageFile(&fh);

	return RC_OK;
}

extern RC openBtree (BTreeHandle **tree, char *idxId)
{
	printf("We are now opening the Btree!!!\n");
	TreeInfo* trInfo=malloc(sizeof(TreeInfo));
	trInfo->bm=MAKE_POOL();
	trInfo->page=MAKE_PAGE_HANDLE();
	trInfo->globalCount=0;
	trInfo->root=0;

	initBufferPool(trInfo->bm,idxId, 10, RS_FIFO, NULL);//we assmume that data would not require more than 10 pages

	pinPage(trInfo->bm, trInfo->page,1);


//create a btree handle and assign it back to tree pointer
	BTreeHandle* treeTemp;
	treeTemp=(BTreeHandle*)malloc(sizeof(BTreeHandle));
	treeTemp->keyType=DT_INT;
	trInfo->maxCount=*((int *)trInfo->page->data);
//	printf("max %d\n", trInfo->maxCount);
	treeTemp->idxId=idxId;
	treeTemp->mgmtData=trInfo;

	*tree=treeTemp;
	unpinPage(trInfo->bm, trInfo->page);
 
	return RC_OK;
}

extern RC closeBtree (BTreeHandle *tree)
{
	printf("We are closing Btree!!!\n");
	lastPage=0;
	scanCount=0;
	free(tree);
	free(((TreeInfo* )(tree->mgmtData))->page);
	shutdownBufferPool( ((TreeInfo* )(tree->mgmtData))->bm );

	return RC_OK;
}

extern RC deleteBtree (char *idxId)
{
	printf("We are deleting Btree!!!\n");
	if(remove(idxId)!=0)		//check whether the name exists
		return RC_FILE_NOT_FOUND;
	return RC_OK;

}


// ************************************* access information about a b-tree *************************************
extern RC getNumNodes (BTreeHandle *tree, int *result)
{
	*result=lastPage+1;
	return RC_OK;
}

extern RC getNumEntries (BTreeHandle *tree, int *result)
{
	TreeInfo* trInfo=(TreeInfo*) (tree->mgmtData);
	*result=trInfo->globalCount;
	return RC_OK;
}

extern RC getKeyType (BTreeHandle *tree, DataType *result)
{
	return RC_OK;
}


// ********************************************** index access *********************************************
extern RC findKey (BTreeHandle *tree, Value *key, RID *result)
{
	TreeInfo* trInfo=(TreeInfo*) (tree->mgmtData);
	int index, findKey=key->v.intV;
	Node* node;
	bool find=false;

	for(index=1;index<=lastPage;index++)
	{
		pinPage(trInfo->bm, trInfo->page, index);
		node=(Node*)trInfo->page->data+sizeof(bool);
		int v1=node->value1;
		int v2=node->value2;
//		printf("key:%d, v1:%d, v2:%d\n",findKey,v1,v2 );
		if(findKey==v1)
		{
			find=true;
			*result=node->left;
			break;
		}
		if(findKey==v2)
		{
			find=true;
			*result=node->mid;
			break;
		}
		unpinPage(trInfo->bm, trInfo->page);
	}

	if(find==false)
		return RC_IM_KEY_NOT_FOUND;

	return RC_OK;
}

extern RC insertKey (BTreeHandle *tree, Value *key, RID rid)
{
	TreeInfo* trInfo=(TreeInfo*) (tree->mgmtData);
	Node* node;


	if(lastPage==0)
	{//if this is the first value inserted
		lastPage=1;
		trInfo->root=1;

		pinPage(trInfo->bm, trInfo->page, lastPage);
		markDirty(trInfo->bm, trInfo->page);
		
		//set the page to be not full
		*(bool*)trInfo->page->data=false;
		//create the node
		node=(Node*)trInfo->page->data+sizeof(bool);
		node->mother=-1;
		node->leaf=true;
		node->left=rid;
		node->value1=key->v.intV;
		node->mid=INIT_RID;
		node->value2=-1;
		node->right=INIT_RID;

		unpinPage(trInfo->bm, trInfo->page);
	}
	else
	{

		pinPage(trInfo->bm, trInfo->page, lastPage);
		markDirty(trInfo->bm, trInfo->page);


		//if the page is full
		if((*(bool*)trInfo->page->data)==true)
		{
			lastPage++;
			unpinPage(trInfo->bm, trInfo->page);
			pinPage(trInfo->bm, trInfo->page, lastPage);

			//set the page to be not full
			*(bool*)trInfo->page->data=false;
			//create the node
			node=(Node*)trInfo->page->data+sizeof(bool);
			node->mother=-1;
			node->leaf=true;
			node->left=rid;
			node->value1=key->v.intV;
			node->mid=INIT_RID;
			node->value2=-1;
			node->right=INIT_RID;

			unpinPage(trInfo->bm, trInfo->page);
		}
		else//if the page is not full
		{
			node=(Node*)trInfo->page->data+sizeof(bool);
			node->mid=rid;
			node->value2=key->v.intV;
			*(bool*)trInfo->page->data=true;

			unpinPage(trInfo->bm, trInfo->page);
		}
	}

	(trInfo->globalCount)++;		//value number increases by 1
	return RC_OK;
}

extern RC deleteKey (BTreeHandle *tree, Value *key)
{
	TreeInfo* trInfo=(TreeInfo*) (tree->mgmtData);
	int index, findKey=key->v.intV;
	Node* node;
	bool find=false;
	int valueNum=0;
	RID moveRID;
	int moveValue;

	for(index=1;index<=lastPage;index++)
	{
		pinPage(trInfo->bm, trInfo->page, index);
		markDirty(trInfo->bm, trInfo->page);
		node=(Node*)trInfo->page->data+sizeof(bool);
		int v1=node->value1;
		int v2=node->value2;
//		printf("key:%d, v1:%d, v2:%d\n",findKey,v1,v2 );
		if(findKey==v1)
		{
			find=true;
			valueNum=1;
			break;
		}
		if(findKey==v2)
		{
			find=true;
			valueNum=2;
			break;
		}
		unpinPage(trInfo->bm, trInfo->page);
	}

	if(find==false)
		return RC_IM_KEY_NOT_FOUND;
	else//if this value exists
	{
		pinPage(trInfo->bm, trInfo->page, lastPage);
		markDirty(trInfo->bm, trInfo->page);

		if(index==lastPage)
		{//if we are deleting a value in the last page
			node=(Node*)trInfo->page->data+sizeof(bool);
			if(valueNum==2)//if we are deleting the last value
			{			
				node->mid=INIT_RID;
				node->value2=-1;
				*(bool*)trInfo->page->data=false;			
			}
			else
			{
				if((*(bool*)trInfo->page->data)==true)//if we are deleting the second last value
				{
					moveRID=node->mid;
					node->left=moveRID;
					moveValue=node->value2;
					node->value1=moveValue;
					node->mid=INIT_RID;
					node->value2=-1;
					*(bool*)trInfo->page->data=false;
				}
				else//if we are deleting the last value in the first position
				{
					node->left=INIT_RID;
					node->value1=-1;
					lastPage--;
				}
			}
			unpinPage(trInfo->bm, trInfo->page);//unpin the last page
		}
		else
		{//if we are deleting a value not in the last page
			//if the last page is full
			if((*(bool*)trInfo->page->data)==true)
			{
				//set the page to be not full
				*(bool*)trInfo->page->data=false;
				//create the node
				node=(Node*)trInfo->page->data+sizeof(bool);
				moveRID=node->mid;
				moveValue=node->value2;

				node->mid=INIT_RID;
				node->value2=-1;

				unpinPage(trInfo->bm, trInfo->page);

				pinPage(trInfo->bm, trInfo->page, index);
				markDirty(trInfo->bm, trInfo->page);
				if(valueNum==1)
				{
					node=(Node*)trInfo->page->data+sizeof(bool);
					node->left=moveRID;
					node->value1=moveValue;
					unpinPage(trInfo->bm, trInfo->page);
				}
				else
				{
					node=(Node*)trInfo->page->data+sizeof(bool);
					node->mid=moveRID;
					node->value2=moveValue;
					unpinPage(trInfo->bm, trInfo->page);
				}
			}
			else//if the last page is not full
			{
				node=(Node*)trInfo->page->data+sizeof(bool);
				moveRID=node->left;
				moveValue=node->value1;
				node->left=INIT_RID;
				node->value1=-1;
				lastPage--;

				unpinPage(trInfo->bm, trInfo->page);//unpin the last page

				pinPage(trInfo->bm, trInfo->page, index);
				markDirty(trInfo->bm, trInfo->page);
				if(valueNum==1)
				{
					node=(Node*)trInfo->page->data+sizeof(bool);
					node->left=moveRID;
					node->value1=moveValue;
					unpinPage(trInfo->bm, trInfo->page);
				}
				else
				{
					node=(Node*)trInfo->page->data+sizeof(bool);
					node->mid=moveRID;
					node->value2=moveValue;
					unpinPage(trInfo->bm, trInfo->page);
				}
			}
		}
		(trInfo->globalCount)--;		//value number decreases by 1
	}

	return RC_OK;
}

extern RC openTreeScan (BTreeHandle *tree, BT_ScanHandle **handle)
{
	printf("We are opening tree scan!!!\n");
	TreeInfo* trInfo=(TreeInfo*) (tree->mgmtData);
	Node *node;
	int *values;
	int index,i=0,j=0,temp1,temp2,min;
	values=(int*)malloc(sizeof(int)*(trInfo->globalCount));

	for(index=1;index<=lastPage;index++)
	{
		pinPage(trInfo->bm, trInfo->page, index);
		node=(Node*)trInfo->page->data+sizeof(bool);
		int v1=node->value1;
		int v2=node->value2;
//		printf("v1:%d, v2:%d\n",v1,v2 );
		if(v1!=-1)
		{
			values[i]=node->value1;
			i++;
		}
		if(v2!=-1)
		{
			values[i]=node->value2;
			i++;
		}
		unpinPage(trInfo->bm, trInfo->page);
	}

	//sort
	for(i=0;i<(trInfo->globalCount);i++)
	{
		min=i;
		for(j=i+1;j<(trInfo->globalCount);j++)
		{
			if(values[min]>values[j])
				min=j;
		}
		temp1=values[min];
		temp2=values[i];
		values[min]=temp2;
		values[i]=temp1;
	}
/*
	for(i=0;i<(trInfo->globalCount);i++)
	{
		printf("no.%d:%d\n",i,values[i] );
	}
*/
	BT_ScanHandle *handleTemp;
	handleTemp=(BT_ScanHandle*)malloc(sizeof(BT_ScanHandle));
	handleTemp->tree=tree;
	handleTemp->mgmtData=values;
	*handle=handleTemp;

	scanCount=0;

	return RC_OK;
}

extern RC nextEntry (BT_ScanHandle *handle, RID *result)
{
	printf("We are getting the next entry!!!\n");
	TreeInfo* trInfo=(TreeInfo*) (handle->tree->mgmtData);
	printf("%d\n", trInfo->globalCount);
	int* values=(int*)(handle->mgmtData);
	Value* vl;
	vl=(Value*)malloc(sizeof(Value));
	vl->dt=DT_INT;
	vl->v.intV=values[scanCount];
	RID* rslt;
	rslt=(RID*)malloc(sizeof(RID));

	if(scanCount==(trInfo->globalCount))
	{
		return RC_IM_NO_MORE_ENTRIES;
	}
	else
	{
		findKey (handle->tree, vl, rslt);
		scanCount++;
	}

	*result=*rslt;

	return RC_OK;
}

extern RC closeTreeScan (BT_ScanHandle *handle)
{
	printf("We are closing tree scan!!!\n");
	scanCount=0;
	free(handle->mgmtData);
	return RC_OK;
}

// ******************************************** debug and test functions *************************************
extern char *printTree (BTreeHandle *tree)
{
	return tree->idxId;
}
