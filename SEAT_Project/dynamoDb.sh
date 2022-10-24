names_utenti=(id tipoUtente username password email)
types_utenti=(N N S S S)
names_lido=(id tipoUtente nomeLido luogo numeroCarta)
types_lido=(N N S S N)

aws dynamodb create-table \
    --table-name utenti \
    --attribute-definitions AttributeName=${names_utenti[0]},AttributeType=${types_utenti[0]} \
    --key-schema AttributeName=${names_utenti[0]},KeyType=HASH \
    --billing-mode PAY_PER_REQUEST

aws dynamodb create-table \
    --table-name dettagliLido \
    --attribute-definitions AttributeName=${names_lido[0]},AttributeType=${types_lido[0]} \
    --key-schema AttributeName=${names_lido[0]},KeyType=HASH \
    --billing-mode PAY_PER_REQUEST
