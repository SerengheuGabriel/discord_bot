import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

from datetime import datetime



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    # response = f'Hi {member.display_name}, welcome to my Hell!'
    # channel = bot.get_channel(756148810224369756)
    # await channel.send(response)
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@bot.event
async def on_member_remove(member):
    response = f"Everybody say peepo bye {member.display_name} 👋!"
    channel = bot.get_channel(756148810224369756)
    await channel.send(response)

@bot.command(name="balu")
async def on_message(ctx, message):
    if message.author == bot.user:
        return

    silly_words = [
        'Wow',
        'Geez',
        'Much dumb',
        'ha ha'
    ]

    response = random.choice(silly_words)
    await message.channel.send(response)

@bot.event
async def on_member_update(before, after):
    response = f'{before.display_name} is now {after.display_name}. Much wow'
    channel = bot.get_channel(756148810224369756)
    await channel.send(response)

@bot.command(name='roll', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@bot.command(name='playlist')
async def playlist(ctx, nr_songs: int):
    i = 0
    songs = []

    channel = bot.get_channel(951515691029233734)

    async for msg in channel.history(limit=10000):
        if i >= nr_songs:
            break
        if msg.author != bot.user:
            content = msg.content
            if 'spotify' in content:
                split_content = content.split(" ")
                #print(split_content[0])
                for element in split_content:
                    if 'spotify' in element:
                        songs.append(element)
                        i += 1

    channel = ctx.author.voice.channel
    await channel.connect()

    for i in songs:
        response = f'.p {i}'
        await ctx.channel.send(response)

    await channel.disconnect()

bot.run(TOKEN)