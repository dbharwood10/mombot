import discord
import random
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import pymongo
from pymongo import MongoClient



load_dotenv()

# Create an instance of commands.Bot with intents
intents = discord.Intents.default()
intents.messages = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

morning_phrases = ["Good morning!", "Rise and shine!", "It's a new day!"]
afternoon_phrases = ["Good afternoon!", "Hope your day is going well!", "Don't forget that Mom loves you!"]
evening_phrases = ["Good evening!", "Time to relax and unwind."]
night_phrases = ["Good night!", "Sweet dreams!"]

def get_time_of_day():
    now = (datetime.utcnow() + timedelta(hours=-5))
    hour = now.hour

    if 6 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 20:
        return "evening"
    else:
        return "night"

async def send_random_interaction(channel):
    time_of_day = get_time_of_day()
    guild = channel.guild
    user = random.choice(guild.members)

    if time_of_day == "morning":
        phrase = random.choice(morning_phrases)
    elif time_of_day == "afternoon":
        phrase = random.choice(afternoon_phrases)
    elif time_of_day == "evening":
        phrase = random.choice(evening_phrases)
    else:
        phrase = random.choice(night_phrases)

    await channel.send(f"{user.mention}, {phrase}")

@bot.command(name='set_interaction_channel')
async def set_interaction_channel(ctx):
    # Allow a user with appropriate permissions to set the interaction channel
    if ctx.message.author.guild_permissions.administrator:
        channel_id = ctx.message.channel.id
        os.environ['CHANNEL_ID'] = str(channel_id)
        await ctx.send(f"Interaction channel set to {ctx.message.channel.mention}")
    else:
        await ctx.send("You don't have the required permissions to set the interaction channel.")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    # Run the background task every x minutes
    send_interaction_task.start()

@tasks.loop(minutes=60)
async def send_interaction_task():
    channel_id = int(os.getenv('CHANNEL_ID'))
    if channel_id:
        channel = bot.get_channel(channel_id)
        if channel:
            await send_random_interaction(channel)

# Run your bot
bot.run(os.getenv('BOT_TOKEN'))
