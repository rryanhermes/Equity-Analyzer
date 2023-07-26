import os
import discord

DISCORD_BOT_TOKEN = 'MTEwMzc5MDM5NDIzMzMzMTc1Mg.GaUZ3i.cKJikcv_nnw2QL1HW1xSFstXVy-rFF7di3HXN8'
CHANNEL_NAME = 'sadoon-signals'
SERVER_ID = 916510140298047539

# Set up the Discord client with intents
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# Define a callback function for when the client is ready
@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")

    # Get the server object corresponding to the server you want to access
    server = client.get_guild(SERVER_ID)
    if server is None:
        print(f"Could not find server with ID {SERVER_ID}")
        return

    # Search for the channel with the desired name
    channel = discord.utils.get(server.channels, name=CHANNEL_NAME)
    if channel is None:
        print(f"Could not find channel with name {CHANNEL_NAME}")
        return

    # Get the last 100 messages in the channel
    messages = await channel.history(limit=100).flatten()

    # Print the contents of each message
    for message in messages:
        print(f"{message.author.name}: {message.content}")

# Run the client with your Discord bot token
client.run(DISCORD_BOT_TOKEN)
