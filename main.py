""" Módulo para enviar mensagens a bots ou grupos do Telegram
"""

import requests
from string import Template
from io import BytesIO
from datetime import datetime
import threading

import boto3

from message_and_config import (
    DESTINATION_LIST,
    IMAGE_DICT,
    HTML_RESPONSE,
    TITLE,
    MESSAGE,
)

dynamodb = boto3.client('dynamodb')
s3_client = boto3.client('s3')


def request_get_thread_function(url, response_list):
    """
    Envia a mensagem para o Telegram em threads diferentes
    """
    response_list += [ requests.get(url, timeout=3) ]


def send_message_to_dynamodb_and_s3(query_params, destination):
    """
    Envia uma mensagem e uma imagem para um banco de dados DynamoDB e um bucket S3 da AWS.
    Esta função recebe os parâmetros da consulta HTTP, extrai o título, a mensagem e outros dados relevantes,
    e envia esses dados para um banco de dados DynamoDB e uma imagem para um bucket S3 da AWS.
    Args:
        query_params (dict): Um dicionário contendo os parâmetros da consulta HTTP, incluindo 'message', 'title'
        e outros parâmetros opcionais.
        destination (string): Destino na lista.
        A URL não foi incluída por conter informações sigilosas (bot_token e chat_id).
    Returns:
        None
    Raises:
        Boto3Exceptions: Se ocorrerem exceções ao interagir com o DynamoDB ou o S3.
    """

    if 'message' in query_params and 'title' in query_params:
        message = query_params['message']
        title = query_params['title']
        level = query_params.get('level', 'AcademiaDevOps')

        id = f'{destination}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'
        item={
            'id': {'S': id},
            'title': {'S': title},
            'message': {'S': message},
            'level': {'S': level},
            'destination': {'S': destination},
        }
        dynamodb.put_item(
            TableName='MensagensDoTelegram',
            Item=item
        )

        bucket_name = 'cicerow-config'
        s3_client.upload_fileobj(
            BytesIO(bytes(str(item), encoding='utf-8')),
            bucket_name,
            f'telegram-{id}.txt'
        )


def extract_query_parameters(event):
    """
    Extrai os parâmetros da consulta do evento.
    Args:
        event (dict): O evento recebido pela função Lambda.
    Returns:
        dict: Um dicionário com os parâmetros da consulta.
    """
    if 'queryStringParameters' in event:
        query_params = event['queryStringParameters']
        return query_params
    return {}

def build_message_and_webhook(query_params):
    """
    Constrói a mensagem e a URL do webhook com base nos parâmetros da consulta.
    Args:
        query_params (dict): Os parâmetros da consulta.
    Returns:
        str: A URL do webhook construída com base nos parâmetros.
            Retorna None se os parâmetros estiverem ausentes ou inválidos.
    """
    if 'message' in query_params and 'title' in query_params:
        message = query_params['message']
        title = query_params['title']
        level = query_params.get('level', 'AcademiaDevOps')
        image_url = IMAGE_DICT.get(level, IMAGE_DICT['AcademiaDevOps'])
        caption = f'<b>{title}</b>\n<i>{level}</i>\n{message}'
        url_list = []
        for destination in DESTINATION_LIST:
            url_list += [{
                "name": destination["name"],
                "url": (f'https://api.telegram.org/bot{destination["bot_token"]}/'
                        f'sendPhoto?chat_id={destination["chat_id"]}'
                        f'&photo={image_url}'
                        f'&caption={caption}'
                        f'&parse_mode=html')
            }]
        return url_list
    return None

def lambda_handler(event, context):
    """
    Função Lambda para lidar com eventos e enviar mensagens via webhook.
    Args:
        event (dict): O evento recebido pela função Lambda.
        context (object): O contexto de execução da função Lambda.
    Returns:
        dict: Uma resposta HTTP com status, cabeçalhos e corpo em JSON.
    """
    query_params = extract_query_parameters(event)
    if query_params:
        webhook_url_list = build_message_and_webhook(query_params)
        if webhook_url_list:
            response_text = 'Enviando mensagens para membros da lista:<br>'
            response_list = []
            thread_list = []
            for destination in webhook_url_list:
                thread = threading.Thread(
                    target=request_get_thread_function,
                    args=(destination['url'],response_list)
                )
                thread.start()
                thread_list += [ thread ]
            for thread in thread_list:
                thread.join()

            thread_list = []
            count = 0
            for response in response_list:
                if response.status_code == 200:
                    response_number = 200
                    response_title = 'Mensagem(ns) enviada(s) com sucesso'
                    response_text += f'<li> Mensagem enviada para <b>{webhook_url_list[count]["name"]}</b>.<br>'
                    thread = threading.Thread(
                        target=send_message_to_dynamodb_and_s3,
                        args=(query_params, webhook_url_list[count]["name"])
                    )
                    thread.start()
                    thread_list += [ thread ]
                    count += 1
                else:
                    response_number = 500
                    response_title = 'Erro conectando ao Telegram'
                    response_text += f'<li> ERRO enviando mensagem para <b>{destination["name"]}</b>.<br>'
                    break
            for thread in thread_list:
                thread.join()
        else:
            response_number = 500
            response_title = TITLE['WEBHOOK_ERROR']
            response_text = MESSAGE['WEBHOOK_ERROR']
    else:
        response_number = 400
        response_title = TITLE['PARAMETER_ERROR']
        response_text = MESSAGE['PARAMETER_ERROR']

    response_html = Template(HTML_RESPONSE)
    response_html = response_html.safe_substitute(
        TITLE=response_title,
        MESSAGE=response_text
    )

    return {
        'statusCode': response_number,
        'headers': {'Content-Type': 'text/html'},
        'body': response_html
    }

if __name__ == '__main__':
    event = {
        "queryStringParameters": {
            "title": "Título: Workshop AWS Na Prática: Evento online e gratuito.",
            "message": "Aqui você aprende a fazer uma aplicação usando os serviços AWS para enviar mensagens simultâneas para vários dos seus contatos."
        }
    }
    print(lambda_handler(event, None))
