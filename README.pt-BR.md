# Telegram Message Sender

Este é um módulo Python projetado para enviar mensagens e imagens para bots ou grupos no Telegram usando a API do Telegram, AWS Lambda, AWS DynamoDB e AWS S3. Ele é especialmente útil para notificar membros de uma lista de destinatários.

## CloudFormation Template for Telegram Message sender

Todos os recursos necessários para implantar a aplicação na AWS podem ser criados via CloudFormation e estão descritos no arquivo `cloudformation.yaml`


### `TelegramRestApi`
- API Gateway para a aplicação. Essa API é uma das formas mais simples para criar um acesso HTTP/HTTPS para uma aplicação.

### `TelegramRestApiDeployment`
- Configuração de deployment para o API Gateway.

### `TelegramApiGatewayResource`
- Configuração de recurso para o API Gateway.

### `TelegramApiGatewayMethod`
- Método indicado para manipular as requisições HTTP (GET).

### `TelegramFunctionApiGatewayPermission`
- Permissão para invocar a função Lambda.

### `TelegramLambdaFunctionRole`
- Função do IAM para aplicar as permissões necessárias à função Lambda.

### `TelegramLambdaFunction`
- Função Lambda com o código a ser executado. Observe que vamos copiar o código de um bucket S3. Que há um limite de tempo (timeout) para executar a função e que as variáveis de ambiente estão disponíveis configuradas textualmente.

### `TelegramDynamoTable`
- Tabela do DynamoDB para salvar o histórico de mensagens.

## CloudFormation Outputs

Os outputs mostram algumas informações e configurações do que foi criado.

### `RestAPI`
- ID do REST API criado no API Gateway.

### `LambdaFunctionRole`
- Nome da função do IAM criada para a função Lambda.

### `LambdaFunction`
- Nome da função Lambda

### `AcessURL`
- Endpoint de acesso criado, ou seja, a URL usada para disparar a sua função Lambda.

### `DynamoTelegramTable`
- Tabela de histórico de mensagens para o DynamoDB.

## Código em Python

* **Envio Assíncrono**: As mensagens são enviadas de forma assíncrona para destinos diferentes usando threads, melhorando a eficiência do envio e diminuindo o tempo de execução do código.
* **Armazenamento no DynamoDB**: As mensagens enviadas são armazenadas em um banco de dados DynamoDB, facilitando o rastreamento e a análise posterior.
* **Armazenamento no S3**: Uma versão em formato de arquivo de texto da mensagem é carregada para um bucket S3, proporcionando uma cópia de backup e facilitando a gestão de arquivos.

### Configuração

Antes de usar este módulo, é necessário configurar as seguintes variáveis e arquivos:

* **AWS Credentials**: Certifique-se de ter as credenciais AWS configuradas no ambiente onde o script será executado ou as permissões corretas na sua função Lambda.
* **IMAGE_LIST**: Configure essa variável de ambiente com a lista de imagens que pretende usar.
* **DESTINATION_LIST**: Configure essa variável com as informações de acesso aos bots ou grupos destinatários das mensagens.
* **message_and_config.py**: Este arquivo contém informações específicas do projeto, como tokens de bot do Telegram, IDs de chat e configurações relacionadas à mensagem. Um exemplo é fornecido como referência (message_and_config_example.py).

### Utilização

O módulo é projetado para ser utilizado como uma função AWS Lambda. Basta configurar uma função Lambda no AWS Management Console e anexar este script como o manipulador da função.

Ao chamar a função, forneça os parâmetros da consulta, como título e mensagem, para enviar mensagens para os destinos configurados.

Exemplo de chamada da função Lambda:

```python
event = {
    "queryStringParameters": {
        "title": "Título: Workshop AWS Na Prática: Evento online e gratuito.",
        "message": "Aqui você aprende a fazer uma aplicação usando os serviços AWS para enviar mensagens simultâneas para vários dos seus contatos."
    }
}
print(lambda_handler(event, None))
```

Consulte mais detalhes no arquivo `commands_to_test.sh` para execução local ou remota.

### Observações
* Certifique-se de que a tabela do DynamoDB e o bucket S3 especificados no script estejam corretamente configurados e acessíveis.
* Os tokens do bot do Telegram e outros detalhes sensíveis não devem ser expostos no código. Utilize variáveis de ambiente ou métodos seguros de armazenamento de segredos.
* Este módulo é configurado para lidar com eventos da AWS Lambda, mas pode ser adaptado para outros ambientes conforme necessário.
* Consulte a documentação do Telegram Bot API e AWS para obter informações detalhadas sobre como configurar e utilizar os serviços mencionados.

