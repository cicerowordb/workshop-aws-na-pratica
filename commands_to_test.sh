#!/bin/bash

###################################################
# Commands to test running from your own computer #
# Use command `python` or `python3` according to  #
# your Python installation.                       #
# Change messages at the end of `main.py` file    #
# according to your needs.                        #
# Running this way require all AWS Resources to   #
# created BEFORE running the code. Change the     #
# name of each resource in the `main.py` code.    #
###################################################

###################################################
# Comandos para testes rodando do seu próprio     #
# computador. Use o comando `python` ou `python3` #
# de acordo com a sua instalação de Python.       #
# Mude a mensagem no fim de `main.py` de acordo   #
# com duas necessidades.                          #
# Rodar dessa forma requer todos os recursos AWS  #
# antes de rodar o código. Mude o nome de cada    #
# recurso no código `main.py`.                    #
###################################################


# Export images list / Exportar a lista de imagens
  export IMAGE_DICT='{
    "info": "https://cdn-icons-png.flaticon.com/512/720/720257.png",
    "warning": "https://cdn-icons-png.flaticon.com/512/1680/1680012.png",
    "error": "https://cdn-icons-png.flaticon.com/512/564/564619.png",
    "email": "https://cdn-icons-png.flaticon.com/512/552/552486.png",
    "task": "https://cdn-icons-png.flaticon.com/512/906/906334.png",
    "other": "https://cdn-icons-png.flaticon.com/512/178/178158.png",
    "AcademiaDevOps": "https://academiadevops.dev.br/logo-devops.png"
}'

# Export Telegram data, change it with valid information
# Exportar dados do Telegram, mude para informações válidas
  export DESTINATION_LIST='[
    {
        "name": "AcadDevOps001Bot",
        "bot_token": "0123456789:AABBCC0123456789abcdefghijkl-ABCDEF",
        "chat_id": "012345678"
    },{
        "name": "AcadDevOps002Bot",
        "bot_token": "0123456789:AABBCC0123456789abcdefghijkl-ABCDEF",
        "chat_id": "012345678"
    },{
        "name": "AcadDevOps003Bot",
        "bot_token": "0123456789:AABBCC0123456789abcdefghijkl-ABCDEF",
        "chat_id": "012345678"
    },{
        "name": "AcadDevOps004Bot",
        "bot_token": "0123456789:AABBCC0123456789abcdefghijkl-ABCDEF",
        "chat_id": "012345678"
    }
]'

# Install Python libraries in the local directory
# Instalar as bibliotecas Python no diretório local
python3 -m pip install -r requirements.txt -t .

# Run the code / Rodar o código
python3 main.py


###################################################
# Commands to deploy this application in AWS      #
# Check `cloudformantio.yml` and change S3        #
# bucket's name and DynamoDB table's name before  #
# start.                                          #
###################################################


# Install Python libraries in the local directory
# Instalar as bibliotecas Python no diretório local
python3 -m pip install -r requirements.txt -t .

# Update code (change S3 bucket name)
# Atualizar o código (mude o nome do bucket S3)
rm lambda_function.zip
zip -r lambda_function.zip $(ls -1|grep -Ev '(secret|.old|commands_to_test.sh|requirements.txt|__pycache__|.zip)')
aws s3 cp lambda_function.zip s3://cicerow-config

# Run CloudFormation Deployment
# Rodar a implantação do CloudFormation
aws cloudformation deploy \
    --template-file cloudformation.yaml \
    --stack-name telegram-messages \
    --capabilities CAPABILITY_NAMED_IAM

aws cloudformation describe-stacks
aws cloudformation describe-stacks|grep -A1 '"OutputKey": "AcessURL",'

# Run Tests / Rodar os testes
LAMBDA_URL="https://g49ja46gfa.execute-api.us-east-1.amazonaws.com/default/telegram"
TITLE="AcademiaDevOps"
MESSAGE="Workshop+AWS+Na+Pratica.+Vem+aprender+AWS+com+a+gente."

curl "$LAMBDA_URL"'?title='$TITLE'&message='$MESSAGE
curl "$LAMBDA_URL"'?title='$TITLE'&message='$MESSAGE'&level=info'

# Delete Stack / Apagar Stack
aws cloudformation delete-stack --stack-name telegram-messages
