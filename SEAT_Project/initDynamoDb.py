import boto3
import json

def createTables():

    dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
    client = boto3.client ('dynamodb',region_name='us-east-1')

    try:
        table = dynamodb.create_table(
            TableName='utenti',
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'

                },
                
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                },

            ],
            BillingMode= "PAY_PER_REQUEST",
        )

        table = dynamodb.create_table(
            TableName='dettagliLido',
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'
                },
                
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                },
            ],
            BillingMode= "PAY_PER_REQUEST",   
        )

        table = dynamodb.create_table(
            TableName='postazioniPerFila',
            KeySchema=[
                {
                    'AttributeName': 'lidoId',
                    'KeyType': 'HASH'

                },

                {
                    'AttributeName': 'numeroFila',
                    'KeyType': 'RANGE'

                },
                
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'lidoId',
                    'AttributeType': 'S'
                },

                {
                    'AttributeName': 'numeroFila',
                    'AttributeType': 'N'
                },
            ],
            BillingMode= "PAY_PER_REQUEST",   
        )

        table = dynamodb.create_table (
            TableName='prenotazione',
            KeySchema =[
                {
                    'AttributeName': 'prenotazioneId',
                    'KeyType': 'HASH'

                },  
                {
                    'AttributeName': 'ombrelloneId',
                    'KeyType': 'RANGE'

                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'prenotazioneId',
                    'AttributeType': 'N'

                },
                {
                    'AttributeName': 'ombrelloneId',
                    'AttributeType': 'S'
                },
            ],
            BillingMode = "PAY_PER_REQUEST",   
        )

        table = dynamodb.create_table(
            TableName='recensioni',
            KeySchema=[
                {
                    'AttributeName': 'recensioneId',
                    'KeyType': 'HASH'
                },
                
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'recensioneId',
                    'AttributeType': 'N'
                },
            ],
            BillingMode= "PAY_PER_REQUEST",   
        )

        table = dynamodb.create_table(
            TableName='pricePerPiece',
            KeySchema=[
                {
                    'AttributeName': 'lidoId',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'pezzo',
                    'KeyType': 'RANGE'
                },
                
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'lidoId',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'pezzo',
                    'AttributeType': 'S'
                },
            ],
            BillingMode= "PAY_PER_REQUEST",   
        )

        table = dynamodb.create_table(
            TableName='pricePerRow',
            KeySchema=[
                {
                    'AttributeName': 'lidoId',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'row',
                    'KeyType': 'RANGE'
                },
                
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'lidoId',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'row',
                    'AttributeType': 'S'
                },
            ],
            BillingMode= "PAY_PER_REQUEST",   
        )

        table = dynamodb.create_table(
            TableName='pricePerSeason',
            KeySchema=[
                {
                    'AttributeName': 'lidoId',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'season',
                    'KeyType': 'RANGE'
                },
                
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'lidoId',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'season',
                    'AttributeType': 'S'
                },
            ],
            BillingMode= "PAY_PER_REQUEST",   
        )

        table = dynamodb.create_table(
            TableName='storiaUtente',
            KeySchema=[
                {
                    'AttributeName': 'userId',
                    'KeyType': 'HASH'
                },    
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'userId',
                    'AttributeType': 'S'
                },
            ],
            BillingMode= "PAY_PER_REQUEST",   
        )

        waiter = dynamodb.get_waiter('table_exists')
        waiter.wait(TableName="storiaUtente")

        return {"table_exists":"False"} 

    except client.exceptions.ResourceInUseException as e:

        return {"table_exists":"True"}


print(json.dumps(createTables()))