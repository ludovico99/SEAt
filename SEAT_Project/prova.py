import datetime

# date = datetime.datetime(2022,10,10)

# full_month_name = date.strftime("%B")
# year = date.strftime("%Y")
# print("Full name: ",full_month_name)
# print("Year: ",year)
# print("TYPE Year: ",type(year))


start = datetime.datetime.strptime("21-06-2014", "%d-%m-%Y")
end = datetime.datetime.strptime("07-07-2014", "%d-%m-%Y")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]
print(type(date_generated[0]))
# for date in date_generated:
#     print(date.strftime("%d-%m-%Y"))

# dict={1:[1,2,3],2:[1,2,5,9],3:[1,9,8,2],4:[4,2,1],5:[4,4,2],6:[2,6,7]}
# first = True
# set1 = {}
# for key in dict:
#     if(first==True):
#         print(dict[key])
#         set1 = set(dict[key])
#         first = False
#         print(set)
#         continue
#     set1 = set1.intersection(dict[key])
#     print(set1)

# import boto3
# from boto3.dynamodb.conditions import Attr

# def scanDb(table, filterAttributeList, filterValueList):
#         lenght = len(filterAttributeList)
#         filterExpression = None
        
#         for i in range(0, lenght):
#             key = filterAttributeList[i]
#             value = filterValueList[i]
#             if i == 0:
#                 filterExpression = Attr(key).eq(value)
#             filterExpression = filterExpression & Attr(key).eq(value)
#         response = table.scan(FilterExpression = filterExpression)
#         print (response['Items'])

# filterAttributeList = ['username', 'password']
# filterValueList = ['elisa', 'elisa']
# dynamoDb = boto3.resource('dynamodb')
# table = dynamoDb.Table('utenti')
# scanDb(table, filterAttributeList, filterValueList)


#pip install numpy
# import numpy as np
# corr = np.corrcoef([1.0,0.0,0.33,1.0,0.0],[0.0,1.0,0.0,0.0,1.0])[0,1]
# print("correlazione: ", corr)


# dict = {'ciao':1, 'elisa':2, 'taehyung':3}
# print("before clear: ", dict)
# dict.clear()
# print("- ", dict)


# nOmbrelloni = 3
# nSdraio = 17

# print(nSdraio//nOmbrelloni)
# print(nSdraio%nOmbrelloni)

# def putTransaction (items, table):
#         #[[nomeAttribute, type, value]]
#         transaction = {'Put':{'Item':{},'TableName': table}}

#         for i in range (0,len(items)):
#             attr = {items[i][1]:str(items[i][2])}
#             transaction['Put']['Item'][items[i][0]]= attr
#         print(transaction)
#         return transaction

def updateTransaction (key,updateInfo,table):
        #Key,updateInfo --> [[nomeAttribute, type, value]]
        updateExpression= "SET "
        count = 0
        ExpressionAttributeValues = {}
        for i in range (0,len(updateInfo)):
            count +=1
            updateExpression = updateExpression + updateInfo[i][0]  + " = :val" + str(count) + ","
            ExpressionAttributeValues[":val" + str(count)] = {updateInfo[i][1]:str(updateInfo[i][2])}
    
        if updateExpression[-1] == ',':
            updateExpression = updateExpression[:-1]
        
        transaction = {'Update':{'Key':{},'UpdateExpression': updateExpression,'TableName': table,'ExpressionAttributeValues': ExpressionAttributeValues}}

        for i in range (0,len(key)):
            attr = {key[i][1]:str(key[i][2])}
            transaction['Update']['Key'][key[i][0]]= attr
        
        print (transaction)
        return transaction

updateTransaction ([['username','S',"pippo"],['password','S',1234]],[['prenotazioneId','N',str(10101010)],['lidoId','S',"pippo"],['userId','S',"username"]],"prenotazioni")