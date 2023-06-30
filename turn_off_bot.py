import discord
from discord import Intents
import asyncio


# Set the Discord bot token
bot_token = "MTA4ODg1MTE1NjA4NTc4NDU4Nw.GRVcFc.rlcjEZihHK62zwMZxOvN1-ZGpCHwgB0k115Jik"

intents = discord.Intents.default()

# Create a Discord client
client = discord.Client(intents=intents)


# Event listener for when the bot is ready
@client.event
async def on_ready():

    # Set the ID of the Discord channel to send messages to
    channel_id = 1088430354160959488

    # Find the channel to send messages to
    channel = client.get_channel(channel_id)

    await channel.send("Boss Hunt Bulagan bot shutting down...!")

# Start the bot
client.run(bot_token)