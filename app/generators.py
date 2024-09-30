# from mistralai import Mistral
from openai import AsyncOpenAI
from config import AITOKEN

client = AsyncOpenAI(api_key=AITOKEN)


async def gpt_text(req, model):
    completion = await client.chat.completions.create(
        messages=[{"role": "user", "content": req}],
        model=model
    )
    completion
    if completion is not None:
        return completion.choices[0].message.content
