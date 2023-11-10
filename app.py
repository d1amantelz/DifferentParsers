import time

import aiohttp
from fastapi import FastAPI

from main import AsyncParser

app = FastAPI()


@app.get("/parse/{num_albums}")
async def parse_albums(num_albums: int):
    start_time = time.time()

    async with aiohttp.ClientSession() as aio_session:
        async_parser = AsyncParser(aio_session)
        await async_parser.download_content(num_albums)

    end_time = time.time()
    elapsed_time = end_time - start_time

    response_data = {
        "message": "Parsing complete!",
        "downloaded_albums": num_albums,
        "execution_time_seconds": round(elapsed_time, 3),
    }

    return response_data


# uvicorn app:app --host 127.0.0.1 --port 8000 --reload
# http://127.0.0.1:8000/parse/<num>
