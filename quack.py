import random
import string

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

async def on_message(message):
        if message.author.id == 328965253314379778 and not message.author.is_on_mobile() and message.channel.name == 'argle-bargle':
            pcheck = 0
            ccheck = False
            for i in message.content:
                if i in string.punctuation:
                    pcheck += 1
                if i.isupper():
                    ccheck = True
            if ccheck and pcheck > 2:
                say = generate_duck()
                await message.reply(say, mention_author=False)