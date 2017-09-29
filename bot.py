import websocket
import json
import requests
import urllib
import os
import logging
import inspect


# Suppress InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

###VARIABLES THAT YOU NEED TO SET MANUALLY IF NOT ON HEROKU#####
try:
        MESSAGE = os.environ['WELCOME-MESSAGE']
        TOKEN = os.environ['SLACK-TOKEN']
        UNFURL = os.environ['UNFURL-LINKS']
except:
        MESSAGE = 'Manually set the Message if youre not running through heroku or have not set vars in ENV'
        TOKEN = 'Manually set the API Token if youre not running through heroku or have not set vars in ENV'
        UNFURL = 'FALSE'
###############################################################

def parse_join(message):
    logger = logging.getLogger("slack-bot")
    m = json.loads(message)
    if (m['type'] == "member_joined_channel"):
        if(m['channel'] == "C4XU7ULUA"):
            x = requests.get("https://concur-blue.slack.com/api/im.open?token="+TOKEN+"&user="+m["user"]["id"])
            x = x.json()
            x = x["channel"]["id"]
            if (UNFURL.lower() == "false"):
              xx = requests.post("https://concur-blue.slack.com/api/chat.postMessage?token="+TOKEN+"&channel="+x+"&text="+urllib.quote(MESSAGE)+"&parse=full&as_user=true&unfurl_links=false")
            else:
              xx = requests.post("https://concur-blue.slack.com/api/chat.postMessage?token="+TOKEN+"&channel="+x+"&text="+urllib.quote(MESSAGE)+"&parse=full&as_user=true")
            #DEBUG
            logger.info '\033[91m' + "HELLO SENT" + m["user"]["id"] + '\033[0m'
            #

#Connects to Slacks and initiates socket handshake
def start_rtm():
    r = requests.get("https://concur-blue.slack.com/api/rtm.start?token="+TOKEN, verify=False)
    logger = logging.getLogger("slack-bot")
    text = r.text
    logger.info text
    r = r.json()
    r = r["url"]
    return r

def on_message(ws, message):
    parse_join(message)

def on_error(ws, error):
    logger = logging.getLogger("slack-bot")
    logger.error "SOME ERROR HAS HAPPENED", error

def on_close(ws):
    logger = logging.getLogger("slack-bot")
    logger.warn '\033[91m'+"Connection Closed"+'\033[0m'

def on_open(ws):
    logger = logging.getLogger("slack-bot")
    logger.info "Connection Started - Auto Greeting new joiners to the network"


if __name__ == "__main__":
    logger = logging.getLogger("slack-bot")

    r = start_rtm()
    logger.info "WebSocket URL:", r

    logger.info "Started WebSocketApp."
    ws = websocket.WebSocketApp(r, on_message = on_message, on_error = on_error, on_close = on_close)
    logger.info "Finished WebSocketApp."
    #ws.on_open

    logger.info "Started ws.run_forever."
    ws.run_forever()
    logger.info "Finished ws.run_forever."
