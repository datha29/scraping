import time
import traceback
from typing import Sequence

import uvicorn
from fastapi import BackgroundTasks, Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import AnyUrl, BaseModel

from src import MONGO_COLL_OBJ
from src import MONGO_COLL_OBJ_STAGE
from src.news_extraction.log_handler import LogHandler
from src.news_extraction.scraper import Scraper
from src.tasks import insert_to_mongo, trigger_requests

logger = LogHandler()
app = FastAPI(title="Crawler API")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins,
)

class ListOfUrl(BaseModel):
    urls: Sequence[AnyUrl]


@app.get('/', tags=["Health Check"])
async def health_check():
    return JSONResponse({'msg': 'Crawler is Up!'})


@app.post("/crawl", tags=["Crawl URL"])
async def crawl_article(url: AnyUrl = Body(..., media_type='text/plain'),backgroundTasks:BackgroundTasks=None):
    try:
        url = str(url)
        data = MONGO_COLL_OBJ.find_one({"url": url},{"_id":0})
        if data and len(data)>2:
            return dict(data)
    except Exception as e:
        traceback.print_exc()
    data = {"url": url}
    try:
        start_time = time.perf_counter()
        data,_ = Scraper(data, logger).main()
        data["TT"] = time.perf_counter() - start_time
        data["url"] = url
        backgroundTasks.add_task(insert_to_mongo,data,MONGO_COLL_OBJ)
        backgroundTasks.add_task(insert_to_mongo,data,MONGO_COLL_OBJ_STAGE)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": repr(e)}, 500)
    return JSONResponse(content=jsonable_encoder({"Result": data}))


@app.post("/trigger", tags=["Bulk Ops"])
async def trigger_urls(input: ListOfUrl,backgroundTasks:BackgroundTasks=None):
    try:
        urls = [str(i) for i in input.urls]
        backgroundTasks.add_task(trigger_requests,urls)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": repr(e)}, 500)
    return JSONResponse({"Result": "OK"})


@app.post("/fetch_articles", tags=["Bulk Ops"])
async def fetch_article_body(input: ListOfUrl):
    articles=[]
    try:
        data = [str(i) for i in input.urls]
        cursor = MONGO_COLL_OBJ.find({"url": {"$in":data}},{"_id":0})
        for each in cursor:
            if each and len(each)>2:
                data=dict(each)
                articles.append(data)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": repr(e)}, 500)
    return JSONResponse(content=jsonable_encoder({"Result": articles}))


if __name__ == '__main__':
    uvicorn.run("api:app", host='0.0.0.0', port=9123)
