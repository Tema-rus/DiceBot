import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv


class DiceBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remove_command('help')

        @self.event
        async def on_ready():
            print(f'{self.user.name} has connected to Discord!')

        @self.listen()
        async def on_message(message):
            if message.author == self.user or not message.content.startswith('!'):
                return
            try:
                nums = []
                for dice in message.content[1:].split('+'):
                    count, num = dice.split('d') if 'd' in dice else (1, dice)
                    nums.extend(str(random.randint(1, int(num))) for _ in range(int(count)))
                total = sum(map(int, nums))
                content = f'```md\n#{total}\nDetails:[{message.content[1:]} ({" ".join(nums)})]```'
                await message.reply(content=content, mention_author=False)
            except ValueError:
                print('Неизвестная команда')


if __name__ == '__main__':
    load_dotenv()
    bot = DiceBot(command_prefix='>', intents=discord.Intents().all())
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))
