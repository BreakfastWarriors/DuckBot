import json
import os
import sqlite3

import discord.ext.commands as disc_cmds
import discord.utils

from daily_reminder import DailyReminder
from quack import on_message as quack_message


class ListenerManager(disc_cmds.Cog, name='ListenerManager'):
    def __init__(self, bot):
        self.bot = bot
        self.daily_reminder = DailyReminder(self.bot)
        self.conn = sqlite3.connect('messages.sqlite')

        # Pull the pin mapping json and load it
        if os.path.isfile('data/pins.json'):
            with open('data/pins.json') as pin_file:
                self.pins = json.load(pin_file)
        else:
            self.pins = {}
        self.pin_channel = None

        self.duck_up = '<:duck_up:1071706220043452518>'
        self.duck_down = '<:duck_down:1071706217845624842>'

    @disc_cmds.Cog.listener(name='on_ready')
    async def on_ready(self):
        self.bot.current_guild = discord.utils.get(self.bot.guilds, name=self.bot.remind_server)
        if not self.bot.current_guild:
            print(f'Warning: remind server {self.bot.remind_server} inaccessible to bot!')

        self.pin_channel = discord.utils.get(self.bot.current_guild.text_channels, name=self.bot.pin_channel_name)
        if not self.pin_channel:
            print(f'Error: the pin channel {self.bot.pin_channel_name} does not exist')

        print('Ready to go!')

    @disc_cmds.Cog.listener(name='on_message')
    async def on_message(self, message):
        c = self.conn.cursor()
        c.execute("INSERT INTO messages VALUES (?,?,?,?,?)",
                  (message.id, message.author.name, message.content, message.channel.name, message.created_at))
        self.conn.commit()

        if 'cum' in message.content and '?cum' not in message.content:
            if os.path.isfile('data/cum.json'):
                with open('data/cum.json') as file:
                    data = json.load(file)

            if message.author.name in data:
                data[message.author.name] += 1
            else:
                data[message.author.name] = 1

            with open('data/cum.json', 'w') as f:
                json.dump(data, f)

        await self.daily_reminder.remind(message)
        await quack_message(message)

    # Bot pin feature
    # Note: we have to use the "raw" version of it because the target message is not necessarily
    # in the bot's message cache
    @disc_cmds.Cog.listener(name='on_raw_reaction_add')
    async def on_pin_reaction(self, reaction_event):
        if reaction_event.emoji.name != '📌' or not self.pin_channel:
            return

        target_msg = await self.bot.current_guild.get_channel(reaction_event.channel_id) \
            .fetch_message(reaction_event.message_id)
        reaction = next((r for r in target_msg.reactions if r.emoji == '📌'), None)
        if not reaction:
            print(f'Warning: 📌 emoji not found among the reactions, message id: {reaction_event.message_id}')

        # Prevent the double-pinning
        # 1. message cannot be already pinned
        # 2. message cannot be on the pin channel
        if reaction.count > 1 or target_msg.channel == self.pin_channel:
            return

        users = [user async for user in reaction.users()]
        pin_requester = users[0].id

        msg_author = target_msg.author.id
        msg_content = target_msg.content
        # Cap the message length at 600
        if len(msg_content) > 600:
            msg_content = msg_content[:600] + '...'
        msg_channel = target_msg.channel
        msg_link = target_msg.jump_url
        msg_attachments = target_msg.attachments
        # msg_id = target_msg.id
        # msg_time = target_msg.created_at
        msg_embed = target_msg.embeds

        # Assemble the pin message
        content = f'📌 by <@{pin_requester}> | <#{msg_channel.id}>'
        embed = discord.Embed()
        # embed.title = msg_author
        embed.description = f'<@{msg_author}>: {msg_content}'

        # Only take the first attachment/embed if there are any
        if msg_attachments:
            attachment_url = msg_attachments[0].url
            embed.set_image(url=attachment_url)

            # Embeds doesn't support videos, show its filename instead
            if 'video' in msg_attachments[0].content_type:
                embed.description += f'\n`<{msg_attachments[0].filename}>`'

        embeds = [embed]

        # Example timestring: 06/14/2022 6:03 PM MST
        # msg_time_mst = (msg_time - datetime.timedelta(hours=7)).strftime('%m/%d/%Y %I:%M %p MST')
        # embed.set_footer(text=f'Message ID {msg_id} · Posted {msg_time_mst}')

        if msg_embed:
            embeds.append(msg_embed[0])

        embed.description += f'\n\n**[Jump to the message]({msg_link})**'

        # Mention the users but do not actually ping them
        pin_msg = await self.pin_channel.send(content=content,
                                              embeds=embeds,
                                              allowed_mentions=discord.AllowedMentions.none())

        # Add the mapping between the target msg and the pin msg
        self.pins[target_msg.id] = pin_msg.id
        with open('data/pins.json', 'w') as outfile:
            json.dump(self.pins, outfile)

        # Add reactions to the pin message
        await pin_msg.add_reaction(self.duck_up)
        await pin_msg.add_reaction(self.duck_down)

    # Pin removal
    @disc_cmds.Cog.listener(name='on_raw_reaction_remove')
    async def on_pin_clear(self, reaction_event):
        if reaction_event.emoji.name != '📌' or not self.pin_channel:
            return

        # Make sure there's no more pin emoji in the message
        target_msg = await self.bot.current_guild.get_channel(reaction_event.channel_id) \
            .fetch_message(reaction_event.message_id)
        reaction = next((r for r in target_msg.reactions if r.emoji == '📌'), None)
        if not reaction:
            if reaction_event.message_id in self.pins:
                pin_msg_id = self.pins[reaction_event.message_id]
                pin_msg = await self.pin_channel.fetch_message(pin_msg_id)

                if not pin_msg:
                    print(f'Error: pin message {pin_msg_id} not found')
                    return

                await pin_msg.delete()
                del self.pins[reaction_event.message_id]
                with open('data/pins.json', 'w') as outfile:
                    json.dump(self.pins, outfile)
