import asyncio

from mistralai import Mistral
from config import AITOKEN

client = Mistral(api_key=AITOKEN)


async def gpt_text(req, model):
    completion = await client.chat.complete_async(
        messages=[{"role": "user", "content": req}], model=model
    )
    if completion is not None:
        return completion.choices[0].message.content
