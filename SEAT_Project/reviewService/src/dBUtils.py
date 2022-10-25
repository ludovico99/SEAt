import boto3
import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Attr

class DBUtils (object):

    def __init__(self):
        self.dynamoDb = boto3.resource('dynamodb', region_name='us-east-1')

        self.client = boto3.client('dynamodb', region_name='us-east-1')


    def scanDb(self, table, filterAttributeList, filterValueList, op):
        """ scan DynamoDB table with input filters (attribute = value)

        Args:
            table (string): table name
            filterAttributeList (list): list of 'attributes name' to insert in filer
            filterValueList (list): list of value requested for attributes
            op (string): operation to perform (and-or)

        Returns:
            list: data retrieved from table
        """
        lenght = len(filterValueList)
        filterExpression = None
        if len(filterAttributeList)!=0: key_or = filterAttributeList[0]
        
        for i in range(0, lenght):
            
            value = filterValueList[i]
            if i == 0:
                filterExpression = Attr(key_or).eq(value)
            if op=='or':
                filterExpression = filterExpression | Attr(key_or).eq(value)
            else:
                key = filterAttributeList[i]
                filterExpression = filterExpression & Attr(key).eq(value)

        dynamoDbTable = self.dynamoDb.Table(table)
        
        if len(filterAttributeList)!=0:
            response = dynamoDbTable.scan(FilterExpression = filterExpression)
        else:
            response = dynamoDbTable.scan()
        data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = dynamoDbTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])   
        # RITORNA UNA LISTA, OGNI ELEMENTO è LA RIGA DELLA TABELLA --> (recensioniId, lidoId, valutazione, commento)
        return data
    
    
    
    def insertInDb(self, table, reviewDetails):
        """ insert a review in 'recensioni' table

        Args:
            table (string): table name
            reviewDetails (grpc_pb2.reviewDetails): grpc message containing the details to insert

        Returns:
            bool: outcome of the operation
        """
        print(reviewDetails.usernameBeachClub, reviewDetails.star, reviewDetails.reviewDetail)
        try:
            id = uuid.uuid1()
            print('UUID per la recensione: ', str(id.time))
            date = datetime.now().date()
            dynamoDbTable = self.dynamoDb.Table(table)
            dynamoDbTable.put_item(
                Item= {
                    'recensioneId': id.time,
                    'lidoId': reviewDetails.usernameBeachClub,
                    'valutazione': reviewDetails.star,
                    'titolo': reviewDetails.reviewDetail,
                    'commento': reviewDetails.comment,
                    'data': date.strftime("%d/%m/%Y")
                }
            )
        except Exception:
            return False
        return True