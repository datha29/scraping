import os,uuid
from dotenv import load_dotenv
CURRENT_DIR = os.getcwd()

load_dotenv()
class MONGO:
    """Store the MongoDB releated cridential"""
    CONN_STIRNG =  os.getenv('MONGO_CONN_STIRNG')
    DATABASE = os.getenv('MONGO_DATABASE')
    COLLECTION =  os.getenv("MONGO_COLLECTION")

class PUBSUB:
    """Store the Pub-Sub releated cridential"""
    PROJECT_ID = "jiox-328108"
    QUEUEIN = os.getenv("QUEUEIN")
    SUBSCRIPTION_ID_DICT = {"local":"pie-ds-crawler-sub" ,"dev":"pie-ds-process-full-article-dev-sub"}
    SUBSCRIPTION_ID = SUBSCRIPTION_ID_DICT[QUEUEIN]
    # PATH = "/Users/administrator/Downloads/GCP_Key_pub_sub.json"
    TIMEOUT = 30
    QUEUEOUT = os.getenv("QUEUEOUT")
    PUBLISHING_ID_DICT = {"dev":"pie-ds-full-article-dev"}
    PUBLISHING_ID = PUBLISHING_ID_DICT[QUEUEOUT]

class GCP:
    """Store the Path GCP file path"""
    GCP_KEY_FILENAME = "GCP_Key_pub_sub.json"
    RELATIVE_PATH = "src/news_extraction"

class REQUESTS:
    """Store the Header """
    HEADER = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8'
    }


# class JIOCRAWLER:
#     HEADER = {
#         "referer": "https://jionews.com/",
#         "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
#         "accept": "*/*",
#     }

class JIOCRAWLER:
    HEADER = {
        "referer": "https://jionews.com/",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'accept-charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        "accept-encoding": "gzip, deflate, br, compress"
    }



class GCPKEY:
    GCP_CREDENTIALS_DATABASE = os.getenv("GCP_CREDENTIALS_DATABSE")
    GCP_CREDENTIALS_COLLECTION = os.getenv('GCP_CREDENTIALS_COLLECTION')

class COMMON:
    """Common Data"""
    NOISE_LIST = [",",'[]',"\xa0","'",'"','()',"'",'{}','<>','@','<','#','$','%','^','&','*','~','\n','/n','\r','<div','>','\ud83d\udd34','"\u003cp\u003e\u0026nbsp;','\\','[',']','\n','\t','...','\'','   ','div itemprop="articleBody" class="sp-cn ins_storybody" id="ins_storybody',' div itemprop="articleBody" class="spcn ins_storybody" id="ins_storybody"','_rrCode = window._rrCode || ;_rrCode.push(function{ (function(d,t){ var s=d.createElement(t); var s1=d.createElement(t); if (d.getElementById(jsw-init)) return; s.setAttribute(id,jsw-init); s.setAttribute(src,https:www.jiosaavn.comembed_sembed.js?ver=+Date.now); s.onload=function{document.getElementById(jads).style.display=block;s1.appendChild(d.createTextNode(JioSaavnEmbedWidget.init({a:"1", q:"1", embed_src:"https:www.jiosaavn.comembedplaylist85481065","dfp_medium" : "1",partner_id: "ndtv"});));d.body.appendChild(s1);}; if (document.readyState === complete) { d.body.appendChild(s); } else if (document.readyState === loading) { var interval = setInterval(function { if(document.readyState === complete) { d.body.appendChild(s); clearInterval(interval); } }, 100); } else { window.onload = function { d.body.appendChild(s); }; } })(document,script); });']
    DATA_DIR_PATH = CURRENT_DIR + "/data/"
    CONFIG_DIR_PATH = CURRENT_DIR + "/config/"
    SRC_DIR_PATH = CURRENT_DIR + "/src/"
    JIO_MONGO_CONN=os.getenv("JIO_MONGO_CONN")
class TRANSLATOR:
    endpoint = "https://api.cognitive.microsofttranslator.com/translate"
    subscription_key = os.getenv('MS_TRANSLATOR_SUBSCRIPTION_KEY')
    headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Ocp-Apim-Subscription-Region': "jioindiawest",
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }
class LANGUAGECODES:
    lang = {
            "english": {"l2":"en","l3":"eng"},
            "hindi": {"l2":"hi","l3":"hin"},
            "tamil": {"l2":"ta","l3":"tam"},
            "bangla": {"l2":"bn","l3":"ban"},
            "gujarati": {"l2":"gu","l3":"guj"},
            "marathi": {"l2":"mr","l3":"mar"},
            "kannada": {"l2":"kn","l3":"kan"},
            "urdu": {"l2":"ur","l3":"urd"},
            "punjabi": {"l2":"pa","l3":"pun"},
            "telugu": {"l2":"te","l3":"tel"},
            "odia": {"l2":"or","l3":"odi"},
            "assamese": {"l2":"as","l3":"ass"},
            "malayalam": {"l2":"ml","l3":"mal"}
        }


STORAGEDETAILS = {
    "stage":{
        "db": "pie-ds-staging",
        "collection": "article_crawler"
    },
    "dev":{
        "db": "pie-ds-development",
        "collection": "article_crawler"
    },
    "prod":{
        "db": "pie-ds-production",
        "collection": "article_crawler"
    }
}
