import random

import discord
from discord.ext import commands

import config

discord_intents = discord.Intents.all()
discord_intents.members = True

bot = commands.Bot(command_prefix='>', intents=discord_intents)
bot.remove_command('help')


@bot.event
async def on_ready():
    print(bot.user.name, 'Работает!')


@bot.listen()
async def on_message(message: discord.message.Message):
    try:
        if message.author != bot.user and message.content[0] == '!':
            dices = message.content[1:].split('+')
            nums = []
            for dice in dices:
                if len(ns := tuple(dice.split('d'))) == 2:
                    count, num = ns
                    for _ in range(int(count)):
                        nums.append(str(random.randint(1, int(num))))
                else:
                    nums.extend(ns)
            content = f'```md\n#{sum(list(map(int, nums)))}\nDetails:[{message.content[1:]} ({" ".join(nums)})]```'
            await message.reply(content=content, mention_author=False)
    except ValueError:
        print('Неизвестная команда')


if __name__ == '__main__':
    bot.run(config.token)
