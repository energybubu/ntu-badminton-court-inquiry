from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from badminton_court import Query, Query_all

from pprint import pprint

import openai, os
app = Flask(__name__)

line_bot_api = LineBotApi('yZwUTzxEf17CtCIgR12stNgdFEd/WsiXEV9E+DLUHH9UDQ4S5iWt9+5Dh6CkMI0fTErnU3ve0IuEPPgBUC2fgIrp7+GeeFiugj6a31Kp+rPyQjOcZSemyo9OcUCbRQOxYgxg79Vb+jmW9/bWSwJjIAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8e5bdf4d1c4e88d5f9a2428bac79712d')
def chat(text):
    ''' create your own api key on openai '''
    openai.api_key = "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"
    response = openai.Completion.create(
        engine = "text-davinci-003", # Choose the best model
        prompt = "What is predicate?", # Enter your question
        max_tokens = 30,
        temperature=0.9,
        top_p=0.75,
        n=1
    )
    return response["choices"][0]['text']
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("Request body: " + body, "Signature: " + signature)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

import datetime
from datetime import date
import requests
def notify(event, user):

    headers = {
        "Authorization": "Bearer " + "F5amfMBnKpxQVcyMa6Q1ZN0dMdnYg5bdmscRHQpbLNj",
        "Content-Type": "application/x-www-form-urlencoded"
    }
 
    params = {"message": f"{user}: {event.message.text}"}
 
    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=params)
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:  
        profile = line_bot_api.get_profile(event.source.user_id)
        user = profile.display_name
        if profile.display_name!="李沅錡": notify(event, user)
        if profile.display_name=="李沅錡":
            print(profile.display_name, "正在節省他的時間")
        elif profile.display_name=="樂":
            print("樂正在使用")
            line_bot_api.push_message(
                event.source.user_id,
                TextSendMessage(text="寶貝！歡迎使用我的機器人！\nI love you ~~"))
        elif profile.display_name=="涂宇杰":
            print("涂宇杰正在使用, 一次50")
            line_bot_api.push_message(
                event.source.user_id,
                TextSendMessage(text="幹嘛，我有說要給你用嗎？\n一次50，月結。"))
        else:
            print(profile.display_name, "正在偷用你的機器人")
    except :
        print("Failed to Notify")
    print("Text:", event.message.text)
    content = "{}: {}".format(event.source.user_id, event.message.text)
    query_date = event.message.text.replace(" ", "").replace("\n", "")
    if query_date=="all" or query_date=="All": 
        arr = Query_all()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='\n'.join(arr)))
    else:
        try:
            todate = datetime.datetime.today()
            print("todate:", todate)
            q_date = datetime.datetime.strptime(query_date, '%Y-%m-%d')
            print("q_date:", q_date)
            dif = (q_date-todate).days
            print("dif: ", dif)
            if dif<-1:
                content = "請輸入一週內的日期。\n\n人要往前看，不要再活在過去了！！"
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=content))
            elif dif>7:
                content = "請輸入一週內的日期。\n\n如果需要占卜的功能，歡迎私訊小編，可以付費解鎖！"
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=content))
            else:
                query_date = q_date.strftime('%Y-%m-%d')
                content = Query(username=os.environ['USER'], password=os.environ['PASSWORD'], assign_date=query_date)

                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=content))
        except:
            text = f"你仔細看看自己打了什麼\n*** ?? ***\n{event.message.text}\n*** ?? ***\n\n請按照以下格式輸入\n\n1.YYYY-MM-DD\n查詢特定日期剩餘場次\n\n2.All/all\n查詢一週內剩餘場次"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=text))
            


import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])