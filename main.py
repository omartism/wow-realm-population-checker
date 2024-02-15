# This example requires the 'message_content' intent.


import discord
import requests
import os
import json

from discord.ext import tasks

# Retrieving the value of the "PATH" environment variable
discord_token = os.environ["DISCORD_TOKEN"]
blizzard_token = os.environ["BLIZZARD_TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
token_url="https://eu.api.blizzard.com/data/wow/connected-realm/5827"
request_data = {
    "namespace": "dynamic-classic1x-eu",
    "locale": "en_US",
    "access_token": blizzard_token
}

client = discord.Client(intents=intents)

def get_realm_data():
    req = requests.get(token_url, params=request_data)
    print(req.status_code)
    json_string = json.dumps(req.json())
    json_dict = json.loads(json_string)
    return json_dict["population"]["type"]

@client.event
async def on_ready():
    global general_channel_id
    print(f'We have logged in as {client.user}')
    if not auto_send.is_running():
        guilds = client.guilds
        for guild in guilds:
            for channel in guild.text_channels:
                if channel.name == "general" or channel.name == "tel-aviv-meeting-room":
                    general_channel_id = channel.id
        channel = await client.fetch_channel(general_channel_id)
        auto_send.start(channel)

@tasks.loop(seconds=20)
async def auto_send(channel: discord.TextChannel):
    if get_realm_data() != "LOCKED":
        print("SERVER IS UNLOCKED")
        await channel.send('ATTENTION: SERVER IS UNLOCKED')


client.run(discord_token)