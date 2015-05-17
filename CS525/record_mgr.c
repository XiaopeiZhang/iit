/*cs525 Assignment 3 - Record Manager
* Xiaopei Zhang
* Kun Mei 
* Fan Zhang 
* Jun Qian
*
*/
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#include "buffer_mgr.h"
#include "storage_mgr.h"

#include "dberror.h"
#include "record_mgr.h"
#include "tables.h"
#include "expr.h"
int currentPage=0;//the page number the last record exists

typedef struct PageInfo
{
	int numSlots;//number of tuples per page
	int numPageHeader;//size of header to record whether the page is full and whether each slot is full
}PageInfo;
PageInfo pageInfo;

typedef struct ScanInfo
{
	Record *record;
	int number;
	Expr * condition;
}ScanInfo;

typedef struct RelInfo
{
	BM_BufferPool *bm;
	BM_PageHandle *page;
	int globalCount;
}RelInfo;

//************************************************* table and manager **************************************
RC initRecordManager (void *mgmtData)
{
	printf("We are now initializing the record manager!!!\n");
	return RC_OK;
}



RC shutdownRecordManager ()
{
	printf("We are now shutting down the record manager!!!\n");
	return RC_OK;
}



// create table and store schema info in a storage management pagehandle
RC createTable (char *name, Schema *schema)
{

	printf("We are creating the table!!!\n");  
	createPageFile(name);
	
	printf("begin openPageFile\n"); 
	SM_FileHandle fh;
	openPageFile(name, &fh);
	ensureCapacity(1, &fh);


//convert schema to pagehandle
	SM_PageHandle ph=malloc(PAGE_SIZE*sizeof(char)); // allocate space to store scheme

	*((int *)ph)=schema->numAttr;	//store numAttr to pagehandle
	int offset=sizeof(int);			//get offset of the pointer after storing numAttr

	int i, strSize=0;
	for(i = 0; i<schema->numAttr;i++)
	{
		strSize=strlen(schema->attrNames[i])+1;               //store attrNames to pagehandle
		memcpy(ph+offset,schema->attrNames[i],strSize);		//store attrNames to pagehandle
		offset=offset+strSize;										//get offset after storing name

		*((int *)(ph+offset)) =schema->dataTypes[i];          //store dataType to pagehandle
		offset+=sizeof(int);									//get offset after storing dataType

		*((int *)(ph+offset)) =schema->typeLength[i];       //store typeLength to pagehandle
		offset+=sizeof(int);								//get offset after storing typeLength

				*((int *)(ph+offset)) =schema->keyAttrs[i];         //store keyAttr to pagehandle
		offset+=sizeof(int);								//get offset after storing keyAttr
	}


	*((int *)(ph+offset))=schema->keySize;            		//store keySize to pagehandle
	offset+=sizeof(schema->keySize);						//get offset after storing keySize
	printf("store schema into pagehandle successfully\n");


	printf("begin writecurrentblock \n");
	writeCurrentBlock(&fh,ph);


	//calculate slot number in the page, deduct 2 bytes for boolean telling whether the page is full
	//2 bytes added to slotSize is boolean telling whether the slot exists
	pageInfo.numSlots=(PAGE_SIZE-sizeof(bool))/(sizeof(RID)+getRecordSize(schema)+sizeof(bool));
	//calculate size to store whether each numSlot exists and whether the page is full
	pageInfo.numPageHeader = sizeof(bool)*(pageInfo.numSlots+1);

	closePageFile(&fh);

	return RC_OK;
	
}



RC openTable (RM_TableData *rel, char *name)
{
	RelInfo* relInfo=malloc(sizeof(RelInfo));
	relInfo->bm=MAKE_POOL();
	relInfo->page=MAKE_PAGE_HANDLE();
	printf("open table!!!\n");
	initBufferPool(relInfo->bm,name, 5, RS_FIFO, NULL);//we assmume that data would not require more than 5 pages
 
	pinPage(relInfo->bm, relInfo->page,0);
	printf("pin page\n");

	//**************get the schema for relation
	const int STRING_MAX_LENGTH=256;
	char attrNameSpace[STRING_MAX_LENGTH];//initiate an array to record names
	Schema *schema = malloc(sizeof(Schema));
	schema->numAttr= *((int *)relInfo->page->data);
	int offset=sizeof(int);
	//allocate for attrNames, dataType, typeLength and keyAttrs
	schema->attrNames=(char **)malloc(sizeof(char*)*schema->numAttr);
	schema->dataTypes=(DataType *)malloc(sizeof(DataType)*schema->numAttr);
	schema->typeLength=(int *)malloc(sizeof(int *)*schema->numAttr);
	schema->keyAttrs=(int *)malloc(sizeof(int *)*schema->numAttr);
	//below is to get all the info for schema
	int i, count=0;
	for( i =0;i<schema->numAttr;i++)
	{
		while(*(relInfo->page->data+offset++)!='\0')//attribute names end with "\0", loop to get the whole name
		{
			attrNameSpace[count]=*(relInfo->page->data+offset-1);
			count++;
		}
		schema->attrNames[i]=(char *)malloc(count*sizeof(char)+1);
		strcpy(schema->attrNames[i],attrNameSpace);

		schema->dataTypes[i]=(int)malloc(sizeof(int));
		schema->dataTypes[i]=*((int *)(relInfo->page->data+offset));
		offset+=sizeof(int);

		schema->typeLength[i]=*((int *)(relInfo->page->data+offset));
		offset+=sizeof(int);

		schema->keyAttrs[i]=*((int *)(relInfo->page->data+offset));
		offset+=sizeof(int);
	}

	schema->keySize= *((int *)(relInfo->page->data+offset));
	offset+=sizeof(int);


	rel->name=name;
	rel->schema=schema;
	rel->mgmtData=relInfo;

	return RC_OK;
}




RC closeTable (RM_TableData *rel)
{
	free(rel->schema);
	free( ((RelInfo*) (rel->mgmtData))->page );
	shutdownBufferPool( ((RelInfo* )(rel->mgmtData))->bm );
	printf("close table successfully!!!\n");

	return RC_OK;
}



RC deleteTable (char *name)
{
	if(remove(name)!=0)		//check whether the name exists
		return RC_FILE_NOT_FOUND;
	return RC_OK;
}



int getNumTuples (RM_TableData *rel)
{
	RelInfo* relInfo=(RelInfo* )(rel->mgmtData);
	int i,j, count=0, offset=0;
	for ( i =0; i<currentPage; i++)
	{
		pinPage(relInfo->bm, relInfo->page,i+1);

		if(*(bool*)relInfo->page->data==true)	//if the page is full
			count+=pageInfo.numSlots;			//add numSlots as tuple size for a full page
		else							//if the page is not full
		{
			offset=sizeof(bool);		//omit the first boolean for judging whether the page is full
			for(j = 0 ;j<pageInfo.numSlots;j++)
			{
				if(*((bool *)(relInfo->page->data+offset))==true)	//if the tuple exist, add one to count
					count+=1;
				offset+=sizeof(bool);	//move to the next slot
			}
		}

		unpinPage(relInfo->bm, relInfo->page);
	}
	return count;
	
}






//********************************************************* handling records in a table ************************************
RC insertRecord (RM_TableData *rel, Record *record)
{
    printf("We are inserting a record\n");
    	RelInfo* relInfo=(RelInfo*) (rel->mgmtData);
	currentPage=relInfo->page->pageNum;			//get the current page number
	int* globalCount;
	globalCount=&(relInfo->globalCount);
	
	if(currentPage==0)			//check whether the current page is being initialized
	{
		*globalCount=0;
		currentPage++;
	}

	if(*(bool*)relInfo->page->data==true)           //check whether the current page is full
	{
		*globalCount=0;
		currentPage++;						//move to the next page
	}

	pinPage(relInfo->bm, relInfo->page, currentPage);
	markDirty(relInfo->bm, relInfo->page);

	int offset=sizeof(bool)*(1+(*globalCount));		//move to the slot boolean position
	*((bool *)(relInfo->page->data+offset))=true;           //set the boolean, which represents the slot, true since the slot will exist as we will insert

	offset = (*globalCount)*(sizeof(RID)+getRecordSize(rel->schema))+pageInfo.numPageHeader;          //move to the position where we insert this record

	record->id.page=currentPage;
	record->id.slot=*globalCount;
	//store value and move pointer
	memcpy(relInfo->page->data+offset,&record->id.page,sizeof(int));
	offset+=sizeof(int);
	memcpy(relInfo->page->data+offset,&record->id.slot,sizeof(int));
	offset+=sizeof(int);
	memcpy(relInfo->page->data+offset,record->data,getRecordSize(rel->schema));
	(*globalCount)++;		//record number increases by 1

	if(*globalCount==pageInfo.numSlots)               //check whether the page is full after we insert this record
		*(bool*)relInfo->page->data=true;			//set the first boolean true since the page is now full

	unpinPage(relInfo->bm, relInfo->page);
	return RC_OK;
}





RC deleteRecord (RM_TableData *rel, RID id)
{
	printf("We are deleting the record!!!\n");
	/*
	RelInfo* relInfo=(RelInfo* )(rel->mgmtData);
	pinPage(relInfo->bm, relInfo->page, id.page);
	
	//calculate the position where the slot boolean exists
	int offset=sizeof(bool)(1+id.slot);
	*((bool *)(relInfo->page->data+offset))=false;
	unpinPage(relInfo->bm, relInfo->page);
	*/

	return RC_OK;

}






RC updateRecord (RM_TableData *rel, Record *record)
{
	printf("We are updating the record!!!\n");
	RelInfo* relInfo=(RelInfo*)(rel->mgmtData);
	pinPage(relInfo->bm, relInfo->page, record->id.page);
	markDirty(relInfo->bm, relInfo->page);
	//calculate the position where we should the to-be-updated record exists
	//add numPageHeader size, all the slot sizes before it, and its RID size
	int offset=pageInfo.numPageHeader+record->id.slot*(sizeof(RID)+getRecordSize(rel->schema))+sizeof(RID);
	//copy the new record into its old position
	memcpy(relInfo->page->data+offset,record->data, getRecordSize(rel->schema));
	unpinPage(relInfo->bm, relInfo->page);
	return RC_OK;
}





RC getRecord (RM_TableData *rel, RID id, Record *record)
{
	RelInfo* relInfo=(RelInfo* )(rel->mgmtData);
	pinPage(relInfo->bm, relInfo->page, id.page);
	
	//calculate the position where we should the to-be-updated record exists
	//add numPageHeader size, all the slot sizes before it, and its RID size
	int offset=pageInfo.numPageHeader+id.slot*(sizeof(RID)+getRecordSize(rel->schema))+sizeof(RID);
	//get the record
	record->id=id;
	record->data=relInfo->page->data+offset;
	unpinPage(relInfo->bm, relInfo->page);
	return RC_OK;
}





//************************************************************* scans ****************************************
RC startScan (RM_TableData *rel, RM_ScanHandle *scan, Expr *cond)
{
	scan->rel=rel;
	ScanInfo *scInfo=(ScanInfo *)malloc(sizeof(ScanInfo));
	Record *record=malloc(sizeof(Record));
	record->data=calloc(sizeof(RID)+getRecordSize(rel->schema), sizeof(char));

	record->id.page=1;
	record->id.slot=-1;

	scInfo->number=0;
	scInfo->record=record;

	scan->mgmtData=scInfo;
 	if(cond!=NULL)
		scInfo->condition=cond;
	return RC_OK;
}



	
	
RC next (RM_ScanHandle *scan, Record *record)
{
	Record *recordTemp;
	Value **value;
	value=malloc(sizeof(**value));
	(*value)=malloc(sizeof(value));

	if(record!=NULL)
		recordTemp = ((ScanInfo *)scan->mgmtData)->record;
	int slotSize;
	slotSize=sizeof(RID)+getRecordSize(scan->rel->schema);

	(*value)->dt=DT_BOOL;
	(*value)->v.boolV=-1;
	recordTemp->data=calloc(slotSize, sizeof(char));



	while(true)
	{
		if(recordTemp->id.slot+1==pageInfo.numSlots)           //if one page is fully read
		{
			recordTemp->id.page++;                    //move to the next page
			recordTemp->id.slot=0;                    //start from slot 0
		}
		else
		{
			recordTemp->id.slot++;                          //read the next slot
		}

		((ScanInfo *)scan->mgmtData)->number++;             //record the number of tuples we have scanned
		int tuples=getNumTuples(scan->rel);
		if(((ScanInfo *)scan->mgmtData)->number>tuples)             //check whether scan has reached the end
			return RC_RM_NO_MORE_TUPLES;

		//get record and check whether it meets condition
		int result=getRecord(scan->rel, recordTemp->id,recordTemp);
		if(result==RC_OK)
			evalExpr(recordTemp, scan->rel->schema, ((ScanInfo *)scan->mgmtData)->condition, value);

		if((*value)->v.boolV)		//break if the next tuple has been found
                    
			goto tuplefound;

	}

	tuplefound:	record->id.page=recordTemp->id.page;
			record->id.slot=recordTemp->id.slot;
			memcpy(record->data,recordTemp->data,slotSize);

	return RC_OK;
}





RC closeScan (RM_ScanHandle *scan)
{
	free(scan->mgmtData);
	printf("scan terminated\n");
	return RC_OK;
}





/****schema part****/
int getRecordSize (Schema *schema)
{
	int size = attrPos(schema,schema->numAttr);
	//record size is the sum of tuple size and boolean size used to record whether the value exists for each attribute and whether the record exists
	size+=(schema->numAttr+1)*sizeof(bool);

	return size;

}

RC freeSchema (Schema *schema)
{
	free(schema);
	printf("bye\n");
	return RC_OK;
}



Schema *createSchema (int numAttr, char **attrNames, DataType *dataTypes, int *typeLength, int keySize, int *keys)
{
	Schema *schemaTemp;
	schemaTemp=(Schema *)malloc(sizeof(Schema));
	printf("Assign values accordingly!\n");

	schemaTemp->attrNames=attrNames;
	schemaTemp->dataTypes=dataTypes;
	schemaTemp->typeLength=typeLength;
	schemaTemp->keySize=keySize;
	schemaTemp->keyAttrs=keys;
	schemaTemp->numAttr=numAttr;
	if(schemaTemp!=NULL)
		return  schemaTemp;
	else
		printf("failed to create schema\n");


}





//**************************************** dealing with records and attribute values **************************************************
RC createRecord (Record **record, Schema *schema)
{
	//initialize record
	Record* recordTemp;
	recordTemp= (Record *)malloc(sizeof(Record));
	recordTemp->id.page=0;
	recordTemp->id.slot=0;

	if(schema!=NULL)
		recordTemp->data=(char*)calloc(sizeof(RID)+getRecordSize(schema), sizeof(char));

	*record=recordTemp;
	return RC_OK;
}




RC freeRecord (Record *record)
{
	printf("We are freeing a record!\n");
	return RC_OK;
}



RC getAttr (Record *record, Schema *schema, int attrNum, Value **value)
{
	Value* valueTemp;
	//initiate the pointer to the position right after RID of this record
	char * start=record->data;
	//calculate the offset storing one tuple and its boolean values
	int offset = attrPos(schema, attrNum)+sizeof(bool)*(schema->numAttr+1);
        
	
	valueTemp= (Value *)malloc(sizeof(Value));
	valueTemp->dt=schema->dataTypes[attrNum];
	switch (schema->dataTypes[attrNum]) 
	{

		case DT_INT:
			memcpy(&(valueTemp->v.intV),start+offset,sizeof(int));
			break;
		case DT_FLOAT:
			memcpy( &(valueTemp->v.floatV),start+offset,sizeof(float));
			break;
		case DT_BOOL:		
			memcpy(&(valueTemp->v.boolV),start+offset,sizeof(int));
			break;
		case DT_STRING:
			valueTemp->v.stringV=calloc(schema->typeLength[attrNum], sizeof(char));
		 	memcpy( valueTemp->v.stringV,start+offset,schema->typeLength[attrNum]);
			break;
	}
	*value=valueTemp;

	return RC_OK;
}



RC setAttr (Record *record, Schema *schema, int attrNum, Value *value)
{
	//set the RID boolean to be true
	char *start=record->data;
	*((bool *)start)=true;
	*((bool *)(start+(1+attrNum)*sizeof(bool)))=true;
	//calculate the offset storing one tuple and its boolean values
	int offset=attrPos(schema, attrNum)+(1+schema->numAttr)*sizeof(bool);

	switch (value->dt)
	{

		case DT_INT:
			memcpy(start+offset, &(value->v.intV), sizeof(int));
			break;
		case DT_FLOAT:
			memcpy(start+offset, &(value->v.floatV), sizeof(float));
			break;
		case DT_BOOL:
			memcpy(start+offset, &(value->v.boolV), sizeof(int));
			break;
		case DT_STRING:
			strcpy(start+offset,value->v.stringV);
			break;
	}
	
	return RC_OK;

}



// ************************************************** additional function **********************************************

// this function is used to calculate the offset of the attributes
int attrPos (Schema *schema, int attrNum)
{
	int i,offset = 0;
	
	for(i = 0; i < attrNum; i++)
	switch (schema->dataTypes[i])
	{
		case DT_STRING:
			offset += schema->typeLength[i];
			break;
		case DT_INT:
			offset += sizeof(int);
			break;
		case DT_FLOAT:
			offset += sizeof(float);
			break;
		case DT_BOOL:
			offset += sizeof(bool);
			break;
	}
	
	return offset;
}
