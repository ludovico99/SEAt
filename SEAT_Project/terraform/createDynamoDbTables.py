import boto3
import json

def createTables():

    dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
    client = boto3.client ('dynamodb',region_name='us-east-1')

   
    notExists = {}
    tables = {'utenti':{"username":'S'},
    'dettagliLido':{"username":'S'},
    'postazioniPerFila':{"lidoId":'S', "numeroFila":'N'},
    'prenotazione':{"prenotazioneId":'N',"ombrelloneId":'S'},
    'recensioni':{"recensioneId":'N'},
    'pricePerPiece':{"lidoId":'S', "pezzo":'S'},
    'pricePerRow':{"lidoId":'S', "row":'S'},
    'pricePerSeason':{"lidoId":'S', "season":'S'},
    'storiaUtente':{"userId":'S'}
    }
    existing_tables = client.list_tables()['TableNames']
    for table_name in tables: 
        if table_name in existing_tables:
            continue                
        
        else :
            count = 0
            notExists[table_name] = table_name
            keySchema = []
            attributeDefinitions = []

            for key in tables[table_name]:
               
                if count == 0:
                    keySchema.append({'AttributeName': key,'KeyType': 'HASH'})
                else :
                    keySchema.append({'AttributeName': key,'KeyType': 'RANGE'})
                attributeDefinitions.append({'AttributeName': key,'AttributeType': tables[table_name][key]})
                count += 1
            
            dynamodb.create_table(
                TableName=table_name,
                KeySchema= keySchema,
                AttributeDefinitions=attributeDefinitions,
                BillingMode= "PAY_PER_REQUEST",
            )

            waiter = dynamodb.get_waiter('table_exists')
            waiter.wait(TableName=table_name)
            
    return notExists


print(json.dumps(createTables()))