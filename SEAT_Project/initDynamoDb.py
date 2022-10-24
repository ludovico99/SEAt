import boto3

dynamodb = boto3.resource('dynamodb')

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

# table = dynamodb.create_table(
#     TableName='magazzino',
#     KeySchema=[
#         {
#             'AttributeName': 'lidoId',
#             'KeyType': 'HASH'
#         },
        
#     ],
#     AttributeDefinitions=[
#         {
#             'AttributeName': 'lidoId',
#             'AttributeType': 'S'
#         },
#     ],
#     BillingMode= "PAY_PER_REQUEST",   
# )


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
    TableName='payment',
    KeySchema=[
        {
            'AttributeName': 'username',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'cardId',
            'KeyType': 'RANGE'
        },
        
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'username',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'cardId',
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

# table = dynamodb.create_table(
#     TableName='postazioni',
#     KeySchema=[
#         {
#             'AttributeName': 'lidoId',
#             'KeyType': 'HASH'

#         },

#         {
#             'AttributeName': 'numeroFila',
#             'KeyType': 'RANGE'

#         },

#          {
#             'AttributeName': 'numeroColonna',
#             'KeyType': 'RANGE'

#         },
        
#     ],
#     AttributeDefinitions=[
#         {
#             'AttributeName': 'lidoId',
#             'AttributeType': 'S'
#         },

#         {
#             'AttributeName': 'numeroFila',
#             'AttributeType': 'N'
#         },
#          {
#             'AttributeName': 'numeroColonna',
#             'KeyType': 'N'

#         },
#     ],
#     BillingMode= "PAY_PER_REQUEST",   
# )

waiter = dynamodb.get_waiter('table_exists')
waiter.wait(TableName="storiaUtente")



#PRENOTAZIONE: "prenotazioneID", lidoId, userId, fromDate, toDate, ombrelloneId (1x2), nSdraio, nLettini, nSedie, costo
#DETTAGLILIDO: "username", tipoUtente, nome, luogo, ristorazione, bar, campi, animazione, palestra, totaleSdraio, totaleLettini, totaleSedie
#POSTAZIONI PER FILA: "lido,numeroFila", nOmbrelloni
#STORIAUTENTE: userId, mediaDistanza, varianzaDistanza, mediaDifferenzaBudget, varianzaDifferenzaBudget, counter, nRistorazione, nBar, nCampi, nAnimazione, nPalestra

#RECENSIONI: recensioneId, lidoId, valutazione, commento
#UTENTI: username, password, tipoUtente, email
#PRICEPERPIECE: lidoId, pezzo, costo
#PRICEPERROW: lidoId, numeroFila, incr
#PRICEPERSEASON: lidoId, season, incr


#PAYMENT: username, cardId, cvc, Credito



#SPIEGAZIONE:
#TOTALE OMBRELLONI = Sommare il valore di nOmbrelloni per ogni fila di quel lido
#TOTALE POSTAZIONI PER FILA =  IL totale postazioni per fila è presente in postazioniPerFila

