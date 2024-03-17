import json

from openai import OpenAI, Stream
from openai.types.chat import ChatCompletionChunk

client = OpenAI()

def call_openai(message:str, temperature: float = 0.0, model: str = "gpt-4", stream=False):
    stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            stream=stream,
            temperature=temperature
        )
    return stream


def call_openai_using_stream(temperature: float = 0.0, model: str = "gpt-4") -> Stream[ChatCompletionChunk]:
    return call_openai(temperature=temperature, model=model, stream=True)



# stream = call_openai_using_stream()

# for chunk in stream:
#     if chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content, end="")


completion = call_openai(message="Can you explain me what is a Large Language Model ? Please provide examples with context.")
print(f"Token usage: {completion.usage.model_dump_json()}") #model_dump_json from pydantic, .usage is a pydantic model
print(f"model response: {completion.choices[0].message.content}")

