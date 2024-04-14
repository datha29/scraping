import asyncio
from typing import AnyStr, List

import aiohttp

from src import CRAWLER_URL


def insert_to_mongo(data:dict,coll_obj):
    url = data["url"]
    coll_obj.update_one({"url":url},{"$set":data},upsert=True)


async def post_task(url, session):
    req = await session.request('POST', url=CRAWLER_URL,data=url)
    data = await req.json()
    return data
    
async def trigger_requests(input_list:List[AnyStr]):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in input_list:
            tasks.append(post_task(url, session,))
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
