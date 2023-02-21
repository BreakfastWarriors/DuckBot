import discord
import discord.ext.commands as disc_cmds
import yaml
import nest_asyncio
import asyncio

from cmd_manager import CommandManager
from listen_manager import ListenerManager

CONFIG_FILE = 'config.yml'


class DuckBot(disc_cmds.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load bot config file
        with open(CONFIG_FILE) as config_file:
            self.config = yaml.safe_load(config_file)
        self.token = self.config['token']
        self.remind_server = self.config['reminder-server']
        self.remind_channel = self.config['reminder-channel']
        if 'unsplash-access' in self.config:
            self.unsplash_access = self.config['unsplash-access']
        else:
            self.unsplash_access = None
        if 'pin-channel' in self.config:
            self.pin_channel_name = self.config['pin-channel']
        else:
            self.pin_channel_name = None


async def main():
    # Create client for bot
    intents = discord.Intents.all()
    client = DuckBot(command_prefix='?', intents=intents)

    # Attach cogs to bot
    await client.add_cog(CommandManager(client))
    await client.add_cog(ListenerManager(client))

    # Connect client to discord
    client.run(client.token)


if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.run(main())
