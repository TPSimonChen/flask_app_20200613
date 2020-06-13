# -*- coding: utf-8 -*-
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('CtuLJRFCIiDY+wqmCnE1m81le6nVIyRUJUQoBl4+CozbQQbzk6BS6MJUtAJOX2TP2d6SSp7MKId4I5IVsBpUnjQ2gJeCGbs0P4ZqSWCTalhYw3OmFHVncBUJO0eiNzJ/KJb+CGCe0kXSSxv7ba3AbwdB04t89/1O/w1cDnyilFU=')
# Channel access token (long-lived)
handler = WebhookHandler('14c752c97c71ab7fa5d9263def3b8f56')
# Channel secret 



@app.route("/callback", methods=['POST'])
def callback():

    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
 

if __name__ == '__main__':
    app.run(debug=True)