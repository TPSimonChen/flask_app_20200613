# -*- coding: utf-8 -*-
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel access token (long-lived)
line_bot_api = LineBotApi('ujVtViOq0YUDhIwJ78/VA1QtRS2o3ufyMTAv8GcXxQTBQqpMCuzeeZbosqpWXAIA2d6SSp7MKId4I5IVsBpUnjQ2gJeCGbs0P4ZqSWCTalgX6gFZWQSpBr+g9dCuLUHzDEFwJoOdWOgENnyO74l0FQdB04t89/1O/w1cDnyilFU=')

# Channel secret 
handler = WebhookHandler('14c752c97c71ab7fa5d9263def3b8f56')


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

def getNews():
    """
    建立一個抓最新消息的function
    """
    import requests
    import re
    from bs4 import BeautifulSoup

    url = 'https://www.ettoday.net/news/focus/3C%E5%AE%B6%E9%9B%BB/'
    r = requests.get(url)
    reponse = r.text

    url_list = re.findall(r'<h3><a href="/news/[\d]*/[\d]*.htm" .*>.*</a>',reponse)

    soup = BeautifulSoup(url_list[0])
    url = 'https://fashion.ettoday.net/' + soup.find('a')['href']
    title = soup.text


    tmp = title + ': ' +url
    return tmp
    
def movie():
    from bs4 import BeautifulSoup
    import requests
    
    target_url = 'http://www.atmovies.com.tw/movie/next/0/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('ul.filmListAll a')):
        if index == 20:
            break
        title = data.text.replace('\t', '').replace('\r', '')
        link = "http://www.atmovies.com.tw" + data['href']
        content += '{}\n{}\n'.format(title, link)
    return content

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 傳送新聞
    if event.message.text == '傳送新聞':
        message = TextSendMessage(getNews())
    # 傳送圖片
    elif event.message.text == '傳送圖片':
        message = ImageSendMessage(
            original_content_url='https://i.imgur.com/QPJ8A1b.png',
            preview_image_url='https://i.imgur.com/QPJ8A1b.png'
        )
    # 傳送貼圖
    elif event.message.text == '傳送貼圖':
        message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )
    # 傳送電影 
    elif event.message.text == '傳送電影':
        message = TextSendMessage(movie()) 
    # 傳送按鈕介面訊息
    elif event.message.text == '快速選單':
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/vkqbLnz.png',
                title='Menu',
                text='Please select',
                actions=[
                    MessageTemplateAction(
                        label='發生地點',
                        text='傳送位置'
                    ),
                    MessageTemplateAction(
                        label='看新聞',
                        text='傳送文字'
                    ),
                    URITemplateAction(
                        label='URL',
                        uri='https://tw.appledaily.com/local/realtime/20180817/1412804'
                    )
                ]
            )
        )
    # 傳送多重圖片訊息
    elif event.message.text == '多項傳送':
        message = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/N3oQXjW.png',
                        action=PostbackTemplateAction(
                            label='postback1',
                            text='postback text1',
                            data='action=buy&itemid=1'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/OBdCHB9.png',
                        action=PostbackTemplateAction(
                            label='postback2',
                            text='postback text2',
                            data='action=buy&itemid=2'
                        )
                    )
                ]
            )
        )
    else:
        message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

    
if __name__ == '__main__':
    app.run(debug=True)