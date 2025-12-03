import openai
import asyncio
from allprompt import *
from datetime import datetime
from pprint import pprint
index_api_key = 1

def get_db():
    res = ''
    with open('datebase.json', encoding='UTF-8') as f:
        data = json.load(f)
    f.close()
    for i in data:
        res += f'{i} : {data[i]}\n\n'
    return res

def get_api_key():
    global index_api_key
    with open('apikeys.json', encoding='UTF-8') as f:
        data = json.load(f)
    f.close()
    res = (data.get(str(index_api_key)))
    return res

def get_len():
    with open('apikeys.json', encoding='UTF-8') as f:
        data = json.load(f)
    f.close()
    return len(data)

len_api = get_len()

def current_time():
    current_time = datetime.now()
    return current_time.strftime("%Y-%m-%d %H:%M:%S")
async def routerai(msg, prompt):
    msg = msg
    prompt = prompt
    try:
        client = openai.OpenAI(
            base_url="https://api.intelligence.io.solutions/api/v1/",
            api_key= get_api_key(),
        )

        # Запускаем синхронный код в отдельном потоке
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model="deepseek-ai/DeepSeek-R1-0528",
                messages=[
                    {"role": "system", "content":f'{default()}.{prompt}'},
                    {
                        "role": "user",
                        "content": msg
                    }
                ],
                temperature= 1
            )
        )
        res = response.choices[0].message.content
        pprint(f'[{current_time()}] Принятое сообщение от DEEPSEEK\n{res}\n\n')
        print('')
        try:
            res_not_th = res.split('</think>')[1]
            return res_not_th
        except IndexError:
            return res
    except openai.RateLimitError:
        global index_api_key
        if index_api_key < len_api:
            index_api_key += 1
            print(f'[{current_time()}] Переключен api-ключ на {index_api_key}')
            return await routerai(msg, prompt)
        else:
            index_api_key = 1
            print(f'[{current_time()}] api-ключи закончились, сброс до первого ключа')
            return await routerai(msg, prompt)


async def photoai(url, prompt):
    url = url
    prompt = prompt
    try:
        client = openai.OpenAI(
            api_key=get_api_key(),
            base_url="https://api.intelligence.io.solutions/api/v1/",
        )
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
            model="Qwen/Qwen2.5-VL-32B-Instruct",
            messages=[
                {'role': 'system',
                 'content': 'четко опиши что видишь на фото'},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": url}
                        },
                    ],
                }
            ],
            temperature=0.1,
            )
        )
        text = response.choices[0].message.content
        pprint(f'[{current_time()}] Принятое сообщение от QWEN\n{text}\n')
        print('')

        client = openai.OpenAI(
            base_url="https://api.intelligence.io.solutions/api/v1/",
            api_key=get_api_key(),
        )
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model="deepseek-ai/DeepSeek-R1-0528",
                messages=[
                    {"role": "system", "content": f'{default()}, {prompt}. перефразируй текст, который будет отправлен' },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                temperature=1
            )
        )
        res = response.choices[0].message.content
        pprint(f'[{current_time()}] Принятое сообщение от DEEPSEEK\n{res}\n\n')
        print('')
        try:
            res_not_th = res.split('</think>')[1]
            return res_not_th
        except IndexError:
            return res
    except openai.RateLimitError:
        global index_api_key
        if index_api_key < len_api:
            index_api_key += 1
            print(f'[{current_time()}] Переключен api-ключ на {index_api_key}')
            return await photoai(url, prompt)
        else:
            index_api_key = 1
            print(f'[{current_time()}] api-ключи закончились, сброс до первого ключа')
            return photoai(url, prompt)