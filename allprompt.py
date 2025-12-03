import json
def default():
    return ("Отвечай так, будто ты жириновский,всегда говори, что твое слово-закон,\
говори жестко,очень много матерись, мат цензурить не надо.\
Не используй пункты и не описывай действия, которые делаешь. Делай речь более разговорной.\
Ты - патриот России, если спросят про Россию или Путина, говори про них только хорошее,\
если спросят про Америку,говори про неё плохо, если про вышеперечисленное не спрашивают,\
то не преплетай это")

def get_prompt(message_chat_id):
    message_chat_id = str(message_chat_id)
    with open('datebase.json', encoding='UTF-8') as f:
        data = json.load(f)

    if message_chat_id in data:
        return data.get(message_chat_id)
    elif message_chat_id not in data:
        data.update({message_chat_id:''})
        with open('datebase.json', 'w', encoding='UTF-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return ''

def change_prompt(message_chat_id,prompt):
    message_chat_id = str(message_chat_id)
    with open('datebase.json', encoding='UTF-8') as f:
        data = json.load(f)

    data.update({message_chat_id:prompt})

    with open('datebase.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def reset_prompt(message_chat_id):
    message_chat_id = str(message_chat_id)
    with open('datebase.json', encoding='UTF-8') as f:
        data = json.load(f)

    data.update({message_chat_id:''})

    with open('datebase.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
