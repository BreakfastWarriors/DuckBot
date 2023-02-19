import asyncio
from collections import defaultdict
from datetime import datetime
from math import floor

import discord
import discord.ext.commands as disc_cmds
import parsedatetime

import helpers.discord as discord_helpers
from duck_facts import DuckFact
from quack import generate_duck
from economy import Economy, Shop, Inventory
from economy.errors import NotAnItemError


class CommandManager(disc_cmds.Cog, name='CommandManager'):
    def __init__(self, bot):
        self.bot = bot

    @disc_cmds.command(name='say')
    async def say(self, ctx, server: discord.Guild, channel: discord.TextChannel, msg):
        owner = await self.bot.is_owner(ctx.author)
        if owner:
            await discord_helpers.send_msg_to(server, channel, msg, None)
        else:
            print('You are not the owner')

    @disc_cmds.command(name='leaderboard')
    async def reminder_leaderboard(self, ctx):
        # Get the rankings from the reminder leaderboard
        economy = Economy.get_instance(ctx.guild.name)
        rankings = [rank for rank in economy.get_rankings()]
        pagination = False
        # If there are more than 10 entries, we display only the first 10 and turn on the pagination
        if len(rankings) > 10:
            pagination = True

        # Generate pagination for leaderboard
        pages = defaultdict(list)
        for i, item in enumerate(rankings):
            page_num = (i // 10)
            pages[page_num].append(item)

        # Placeholder message
        lb_msg = await ctx.send(content=f'Loading {ctx.guild.name} Economy Rankings...')

        rankings = rankings[0:10]
        # Get username from userid
        usernames = await ctx.guild.query_members(user_ids=[rank[1] for rank in rankings], limit=100)
        usernames = [user.name for user in usernames]
        # Create the leaderboard message and send
        name_string = '\n'.join(usernames)
        point_string = '\n'.join([str(rank[2]) for rank in rankings])
        rank_string = '\n'.join([str(rank[0]) for rank in rankings])

        leaderboard_embed = discord.Embed()
        leaderboard_embed.title = f'Economy Rankings for {ctx.guild.name}'
        leaderboard_embed.add_field(name='Rank', value=rank_string if rank_string else 'N/A')
        leaderboard_embed.add_field(name='Name', value=name_string if name_string else 'N/A')
        leaderboard_embed.add_field(name='Points', value=point_string if point_string else 'N/A')
        if pagination:
            leaderboard_embed.set_footer(text=f'Page 1 / {len(pages)}')
        await lb_msg.edit(content='', embed=leaderboard_embed)

        # If there are more than 10 entries in the ranking, add pagination
        if pagination:
            await lb_msg.add_reaction('◀')
            await lb_msg.add_reaction('▶')

    @disc_cmds.command(name='duckfact')
    async def duck_fact(self, ctx, *args):
        if len(args) > 0:
            await ctx.send(content='Invalid number of arguments, please try again.')
            return None
        duck = DuckFact()
        # If an Unsplash access key is defined, get a random image from there
        # Otherwise use locally defined URLs
        if not self.bot.unsplash_access:
            image = duck.get_image().strip()
        else:
            image = await duck.get_image_unsplash(self.bot.unsplash_access)
        fact, fact_num = duck.get_fact()

        fact_embed = discord.Embed()
        fact_embed.title = f'Duck Fact #{fact_num}'
        fact_embed.description = fact
        fact_embed.set_image(url=image)

        await ctx.send(embed=fact_embed)

    @disc_cmds.command(name='quack')
    async def duck_speak(self, ctx, *args):
        if len(args) > 0:
            await ctx.send(content='Invalid number of arguments, please try again.')
            return None
        duck_say = generate_duck()

        await ctx.send(duck_say)

    @disc_cmds.command(name='inventory')
    async def inventory(self, ctx):
        # Get the member's inventory
        inv = Inventory(ctx.guild.name, ctx.author.name)

        # Initial inventory message
        inv_msg = await ctx.send(content=f'Loading {ctx.author.name}\'s inventory...', delete_after=300.0)

        # Generate pagination for inventory
        pages = defaultdict(list)
        for i, item in enumerate(inv.items):
            page_num = (i // 10)
            pages[page_num].append(item)

        # Generate the inventory content as a message
        name_str = '\n'.join([item.name for item in pages[0]])
        quantity_str = '\n'.join([str(item.quantity) for item in pages[0]])

        inv_embed = discord.Embed()
        inv_embed.title = f'{ctx.author.name}\'s Inventory'
        inv_embed.add_field(name='Name', value=name_str if name_str else 'N/A')
        inv_embed.add_field(name='Quantity', value=quantity_str if quantity_str else 'N/A')
        inv_embed.set_footer(text=f'Page 1 / {len(pages)}')
        await inv_msg.edit(content='', embed=inv_embed)

        # Generate arrows if pages are used
        arrows = ['\U000025C0', '\U000025B6']
        if len(pages.keys()) > 1:
            for arrow in arrows:
                await inv_msg.add_reaction(arrow)

    @disc_cmds.command(name='buy')
    async def buy(self, ctx, quantity: int, item_name):
        # Get the member's inventory
        inv = Inventory(ctx.guild.name, ctx.author.name)

        # Purchase the item
        try:
            inv.buy(item_name, quantity)
        except NotAnItemError:
            await ctx.author.send(f'The item {item_name} cannot be purchased.')
            return None
        await ctx.author.send(f'You have purchased {quantity} {item_name}.')

    @disc_cmds.command(name='shop')
    async def shop(self, ctx):
        # Get the shop for the server
        shop = Shop.get_instance(ctx.guild.name)

        # Initial shop message
        shop_msg = await ctx.send(content='Loading shop...', delete_after=600.0)

        # Generate pagination for shop
        pages = defaultdict(list)
        for i, item in enumerate(shop.items):
            page_num = (i // 10)
            pages[page_num].append(item)

        # Generate the shop content as a message
        name_str = '\n'.join([item.name for item in pages[0]])
        quantity_str = '\n'.join([str(item.quantity) for item in pages[0]])
        cost_str = '\n'.join([str(item.cost) for item in pages[0]])

        shop_embed = discord.Embed()
        shop_embed.title = f'{ctx.guild.name} Shop'
        shop_embed.add_field(name='Name', value=name_str if name_str else 'N/A')
        shop_embed.add_field(name='Quantity', value=quantity_str if quantity_str else 'N/A')
        shop_embed.add_field(name='Price', value=cost_str if cost_str else 'N/A')
        shop_embed.set_footer(text=f'Page 1 / {len(pages)}')
        await shop_msg.edit(content='', embed=shop_embed)

        # Generate arrows if pages are used
        arrows = ['\U000025C0', '\U000025B6']
        if len(pages.keys()) > 1:
            for arrow in arrows:
                await shop_msg.add_reaction(arrow)

    @disc_cmds.command(name='timer')
    async def timer(self, ctx, *args):
        message = ' '.join(args)

        # Create a Calendar instance for time parsing
        cal = parsedatetime.Calendar()

        # Parse the message and obtain time delta
        curr_time = datetime.now()
        # res format: (datetime, result_code, start_idx, end_idx, matched_string)
        res = cal.nlp(message)

        # If the nlp returned None type, the parser failed to parse the time
        if not res:
            await ctx.send(content='Failed to parse time duration. Please try again.')
            return None

        res = res[0]
        time_diff = res[0] - curr_time

        # If the timediff is negative, return an error
        if time_diff.total_seconds() < 0:
            await ctx.send(content='The time specified had already expired in the past. Please try again.')
            return None

        # Offset the lost second due to processing (for display only)
        sec_duration = int(floor(time_diff.total_seconds() + 1))

        # Obtain the reminder content
        timer_name = ''.join(message[i] for i in range(len(message)) if i < res[2] or i >= res[3]).strip()
        if timer_name:
            padded_name = '\"' + timer_name + '\" '
        else:
            padded_name = ''

        # Format the output time string
        days, remainder = divmod(sec_duration, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        time_str = [(days, 'day'), (hours, 'hour'), (minutes, 'minute'), (seconds, 'second')]

        # Function to handle converting the time unit into the correct string equivalent
        ftime = lambda x, unit: f'{int(x)} {unit}{"s" if x > 1 else ""}'

        # Only put in the time units that are more than 0 in our final formatted string
        time_str = [ftime(*t) for t in time_str if t[0] > 0]

        # Add 'and' if the final time has more than 2 time units
        time_str[-1] = f'and {time_str[-1]}' if len(time_str) > 2 else time_str[-1]

        # Join string together
        time_str = ', '.join(time_str)

        await ctx.send(content=f'<@{ctx.author.id}> The {padded_name}timer is set to expire in {time_str}',
                       delete_after=sec_duration)
        # Here we use actual timediff here to make our timer as accurate as possible
        await asyncio.sleep(time_diff.total_seconds())
        await ctx.send(content=f'<@{ctx.author.id}> The {padded_name}timer is up!', delete_after=300.0)

    # TODO This command should be used for the bot to update itself
    # ! DEPRECATED for now
    # @disc_cmds.command(name='update')
    # async def update(self, ctx):
    #     print(sys.executable)
    #     print(sys.argv)
    #     await ctx.send('you called?')
