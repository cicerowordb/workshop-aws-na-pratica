""" Módulo com as mensagens usadas no código
"""

import os
import json

DESTINATION_LIST = json.loads(os.getenv('DESTINATION_LIST'))

IMAGE_DICT = json.loads(os.getenv('IMAGE_DICT'))

HTML_RESPONSE = ('<!DOCTYPE html>'
                 '<html lang="pt-br">'
                 '    <head>'
                 '        <title>Telegram Messages</title>'
                 '        <meta charset="utf-8">'
                 '    </head>'
                 '    <body>'
                 '        <h1>$TITLE</h1>'
                 '        <p>$MESSAGE</p>'
                 '    </body>'
                 '</html>')

TITLE = {
    'PARAMETER_ERROR': 'Nenhum parâmetro encontrado na URL',
    'WEBHOOK_ERROR': 'Não foi possível criar o webhook para cada um dos destinos'
}

MESSAGE = {
    'PARAMETER_ERROR': ('Pelo menos dois parâmetros são necessários para enviar'
                        'uma mensagem usando este serviço:<br>'
                        '<li> <b>title</b>: o título da mensagem.'
                        '<li> <b>message</b>: a própria mensagem.'
                        'Mais um par&acirc;metro pode ser usado opicionamente:'
                        '<li> <b>level</b>: um dos seguintes valores: info, warning, error, '
                        'email, task, other ou AcademiaDevOps. '
                        'Se nenhum deles for usado o último será escolhido por omissão.'),
    'WEBHOOK_ERROR': ('Para criar os webhooks corretamente você precisa criar uma '
                      'variável de ambiente de nome <code>DESTINATION_LIST</code> '
                      'com a lista de destinatários. Esses destinatários precisam '
                      'ter um nome, um token e um chat_id (isso vale para bots e '
                      'grupos, para usuários há algumas diferenças).<br>'
                      'Veja o exemplo a seguir de um comando para exportar essa'
                      'variável de ambiente no Linux:<br>'
                      '<code>'
                      'export DESTINATION_LIST=\'[{<br>'
                      '"name": "AcadDevOps001Bot",'
                      '"bot_token": "0123456789:AABBCC0011223344556677889900-Abcdef",'
                      '"chat_id": "012345678"},{'
                      '"name": "AcadDevOps002Bot",'
                      '"bot_token": "0123456789:AABBCC0011223344556677889900-Abcdef",'
                      '"chat_id": "012345678"},{'
                      '"name": "AcadDevOps003Bot",'
                      '"bot_token": "0123456789:AABBCC0011223344556677889900-Abcdef",'
                      '"chat_id": "012345678"}]'
                      '</code>')
}
