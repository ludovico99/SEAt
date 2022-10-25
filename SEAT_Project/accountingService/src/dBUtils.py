import boto3
from boto3.dynamodb.conditions import Attr

class DBUtils (object):

    def __init__(self):
        self.dynamoDb = boto3.resource('dynamodb', region_name='us-east-1')

        self.client = boto3.client('dynamodb', region_name='us-east-1')

    def putTransaction (self, items, table):
        """ Utility function that translates a list in a put transaction (dynamoDB query)

        Args:
            items (List): List of items to be inserted 
            table (string): table's name

        Returns:
            dict[str,[dict[str,any]]]: A transaction in dynamoDB format
        """
        #[[nomeAttribute, type, value]]
        transaction = {'Put':{'Item':{},'TableName': table}}

        for i in range (0,len(items)):

            if items[i][1] == 'BOOL':
                attr = {items[i][1]:items[i][2]}
            else : attr = {items[i][1]:str(items[i][2])}
            
            transaction['Put']['Item'][items[i][0]]= attr
        print(transaction)
        return transaction
    
    def deleteTrasaction (self,key,table):
        """ Utility function that translates a list in a delete transaction (dynamoDB query)

        Args:
            key (List): List of items to be inserted 
            table (string): table's name

        Returns:
            dict[str,[dict[str,172.20.0.3any]]]: A transaction in dynamoDB format
        """
        #key --> [[nomeAttribute, type, value]]
        transaction = {'Delete':{'Key':{},'TableName': table}}

        for i in range (0,len(key)):

            if key[i][1] == 'BOOL':
                attr = {key[i][1]:key[i][2]}
            else : attr = {key[i][1]:str(key[i][2])}

            transaction['Delete']['Key'][key[i][0]]= attr
        print(transaction)
        return transaction

    
    def updateTransaction (self,key,updateInfo,table):
        """ Utility function that translates a list in a update transaction (dynamoDB query)

        Args:
            key (List): List that contains the primary key for the table
            updateInfo (List) : List of items to be inserted
            table (string): table's name


        Returns:
            dict[str,[dict[str,any]]]: A transaction in dynamoDB format
        """
        #Key,updateInfo --> [[nomeAttribute, type, value]]
        updateExpression= "SET "
        count = 0
        ExpressionAttributeValues = {}
        for i in range (0,len(updateInfo)):
            count +=1
            updateExpression = updateExpression + updateInfo[i][0] + " = :val" + str(count) + ","
            if updateInfo[i][1] == 'BOOL':
                attr = {updateInfo[i][1]:updateInfo[i][2]}
            else : attr = {updateInfo[i][1]:str(updateInfo[i][2])}
            ExpressionAttributeValues[":val" + str(count)] = attr
    
        if updateExpression[-1] == ',':
            updateExpression = updateExpression[:-1]
        
        transaction = {'Update':{'Key':{},'UpdateExpression': updateExpression,'TableName': table,'ExpressionAttributeValues': ExpressionAttributeValues}}

        for i in range (0,len(key)):
            if key[i][1] == 'BOOL':
                attr = {key[i][1]:key[i][2]}
            else : attr = {key[i][1]:str(key[i][2])}
            transaction['Update']['Key'][key[i][0]]= attr
        
        print (transaction)
        return transaction



    def executeTransaction (self,transactions):
        """ Function that performs the dynamoDB write transaction

        Args:
            transactions (List): List of transactions

        Returns:
            BOOL,string:  Return a Boolean in order to discriminate the success or failure of the method and an error messag
        """
        try:
            response = self.client.transact_write_items(
                        TransactItems = transactions
                )
            return True, "Transaction has succeded"
        except Exception as e:
            print(repr(e))
            return False, "Transaction has been aborted"


    def scanDb(self, table, filterAttributeList, filterValueList):

        """ scan DynamoDB table with input filters (attribute = value)

        Args:
            table (string): table name
            filterAttributeList (list): list of 'attributes name' to insert in filter
            filterValueList (list): list of value requested for attributes

        Returns:
            list: data retrieved from the table
        """
        
        try:
            length = len(filterAttributeList)
            filterExpression = None
            
            for i in range(0, length):
                key = filterAttributeList[i]
                value = filterValueList[i]
                if i == 0:
                    filterExpression = Attr(key).eq(value)
                filterExpression = filterExpression & Attr(key).eq(value)

            dynamoDbTable = self.dynamoDb.Table(table)

            response = dynamoDbTable.scan(FilterExpression = filterExpression)
            data = response['Items']
            while 'LastEvaluatedKey' in response:
                response = dynamoDbTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                data.extend(response['Items']) 
        except Exception as e:
            print(repr(e))
            return None  
            
        return data

    