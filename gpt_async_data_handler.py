import time
import numpy as np
from matplotlib import pyplot as plt
import asyncio
import openai
import re
import time
import pandas as pd

openai.organization = ""
openai.api_key = ""

def prepare_prompts(data, prompt_template):
    messages_list = []
    for i in range(len(data)):
        text1 = f"\"{data[i]}\""
        prompt = prompt_template + text1

        if len(prompt) > 4000:
            prompt = prompt[:4000]

        messages_list.append(prompt)

    return messages_list


def make_messages_list(txt, system_prompt):
    messages_list = []
    for i in txt:
        message = [{"role": "system", "content": system_prompt}, {"role": "user", "content": i}]
        messages_list.append(message)
    return messages_list


async def dispatch_openai_requests(
        messages_list: list[list[dict[str, any]]],
        model: str, temperature: float,
        max_tokens: int, top_p: float,
) -> list[str]:
    async_responses = [
        openai.ChatCompletion.acreate(
            model=model,
            messages=x,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )
        for x in messages_list
    ]

    return await asyncio.gather(*async_responses)

#Asynchronously execute a single call to the OpenAI API
async def call_api(messages, model, temperature, max_tokens, top_p):
    try:
        response = await dispatch_openai_requests(
            messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )
    except openai.error.RateLimitError:
        raise
    except Exception as e:
        print(e)
        response = [-1]*len(messages)
    return response

#Split the list of all prompts into blocks of 40 and call all 40 prompts asynchronously
async def obtain_responses(messages_list, model, temperature, max_tokens, top_p):
    answers = []
    lst = [messages_list[i:i + 40] for i in range(0, len(messages_list), 40)]
    i = 0
    while i != len(lst):
        try:
            print(i)
            answer = await call_api(lst[i], model, temperature, max_tokens, top_p)
            answers.extend(answer)
            i += 1
            time.sleep(15)
        except openai.error.RateLimitError:
            print("timeout")
            time.sleep(70)
    for i in range(len(answers)):
        try:
            answers[i] = str(answers[i])
        except:
            answers[i] = -1
    return answers


async def process_text(texts, model, temperature, max_tokens, top_p):
    messages_list = prepare_prompts(texts, prompt_template)
    messages_list = make_messages_list(messages_list, system_prompt)
    results = await obtain_responses(messages_list, model, temperature, max_tokens, top_p)

    return results


async def process_dataframe(df, model, temperature, max_tokens, top_p):
    safe = 0
    df_done = pd.DataFrame()
    while (len(df) > 0 and safe < 10):
        texts_to_process = df.loc[df["response"] == -1, 'text'].tolist()
        new_responses = await process_text(texts_to_process,model, temperature, max_tokens, top_p)
        df["response"] = new_responses
        df_done = pd.concat([df_done, df[df["response"] != -1]])
        df = df[df["response"] == -1]
        safe += 1
    return df_done


prompt_template = ""
system_prompt = "You are a helpful AI."

PATH = ""

def main():
    df = pd.read_csv(PATH)
    df["response"] = -1
    df = asyncio.run(process_dataframe(df, model="gpt-3.5-turbo", temperature=0.7, max_tokens = 500, top_p=1.0))
    df.to_csv("result.csv")

if __name__ == "__main__":
    main()
