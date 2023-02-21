import random
import string
import re

def generate_duck():
    quuuaaaaaaaaaaak = [
        'wak',
        'kwa',
        'quack',
        'quack-quak-quack',
        'quackity',
        'kwak',
        'waaak',
        'honk',
        'honk-gah-quack',
        'quack-waaak-kwak-wak',
        'bok',
        'wok',
        'quuuaaaaaaaaaaak'
    ]
    quackQuackQuack = ['.', '...', '!', '?']
    wok = [15, 30, 75]

    quackity = random.choice(wok)

    # Bwok bwok Bok Cluckity. Bwak Cluck-cluck-cluck... Bok pukaaak
    honkGahQuack = ''
    quackWaaakKwak = False
    for i in range(quackity):
        # Cluck... Bwok cluck
        quack = random.choice(quuuaaaaaaaaaaak)

        # Cluck-a-buh-gawk
        # Note: Cluck cluckity Bwak Cluck-cluck-cluck Puk
        kwa = (i == quackity - 1) or (random.random() > 0.9)
        wak = random.choice(quackQuackQuack) if kwa else ''
        quack = quack + wak

        # Bwok Bok bwak!
        # Note: Bwwwaaaaaaaaaak Bwwwaaaaaaaaaak Pukaaak Bok Puk?
        honk = (i == 0) or quackWaaakKwak or (random.random() > 0.3)
        quack = quack[0].upper() + quack[1:] if honk else quack

        # Cluck... Bwok cluck
        quackWaaakKwak = kwa

        # Cluck Cluckity Bwwwaaaaaaaaaak
        honkGahQuack = honkGahQuack + quack

        # Bwwwaaaaaaaaaak Waaak
        honkGahQuack = honkGahQuack if i == quackity - 1 else honkGahQuack + ' '

    return honkGahQuack



def generate_duck_kr():
    
    quuuaaaaaaaaaaak = [
    '왁',
    '콰',
    '돌팔이 의사',
    '꽥꽥꽥꽥꽥꽥',
    '돌팔이',
    '곽',
    '와악',
    '울리다',
    '빵-가-꽥',
    '꽥꽥-꽥꽥-꽥꽥',
    '복',
    '냄비',
    '쿠우아아아아아아아아악'
    ]
    quackQuackQuack = ['.', '...', '!', '?']
    wok = [15, 30, 75]

    quackity = random.choice(wok)

    # Bwok bwok Bok Cluckity. Bwak Cluck-cluck-cluck... Bok pukaaak
    honkGahQuack = ''
    quackWaaakKwak = False
    for i in range(quackity):
        # Cluck... Bwok cluck
        quack = random.choice(quuuaaaaaaaaaaak)

        # Cluck-a-buh-gawk
        # Note: Cluck cluckity Bwak Cluck-cluck-cluck Puk
        kwa = (i == quackity - 1) or (random.random() > 0.9)
        wak = random.choice(quackQuackQuack) if kwa else ''
        quack = quack + wak

        # Bwok Bok bwak!
        # Note: Bwwwaaaaaaaaaak Bwwwaaaaaaaaaak Pukaaak Bok Puk?
        honk = (i == 0) or quackWaaakKwak or (random.random() > 0.3)
        quack = quack[0].upper() + quack[1:] if honk else quack

        # Cluck... Bwok cluck
        quackWaaakKwak = kwa

        # Cluck Cluckity Bwwwaaaaaaaaaak
        honkGahQuack = honkGahQuack + quack

        # Bwwwaaaaaaaaaak Waaak
        honkGahQuack = honkGahQuack if i == quackity - 1 else honkGahQuack + ' '

    return honkGahQuack



def has_link(message):
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    match = pattern.search(message)
    return bool(match)



async def on_message(message):
        msg = message.content
        rng = random.random()
        kr_count = 0
        korean_range = "[\uac00-\ud7a3\u1100-\u11ff\u3130-\u318f]+"
        
        if message.author.id == 328965253314379778 and not message.author.is_on_mobile() and len(msg) > 5 and len(msg) < 125 and not has_link(msg) and rng <= .95:
            pcheck = 0
            ccheck = 0
            muc = {'m','u','c'}
            for l in msg:
                if l in string.punctuation and l not in ['\'', '\"']:
                    pcheck += 1
                if l.isupper() and l != 'I':
                    ccheck += 1
            if ccheck >=1 and ccheck <= 5 and pcheck >= 2 and not muc:
                say = generate_duck()
                await message.reply(say, mention_author=False)
        elif message.author.id == 130155817524658176 and not has_link(msg) and rng >= .99:
            say = generate_duck()
            await message.reply(say, mention_author=False)
        elif message.author.id == 185665749027782656:
            if re.search(korean_range, msg) is not None:
                print(kr_count)
                say = generate_duck_kr()
                if kr_count%3 == 0:
                    kr_count += 1
                    await message.reply(say, mention_author=False)