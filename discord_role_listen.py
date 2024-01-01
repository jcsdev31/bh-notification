import discord
import config
from constants.bosses import mvps, minis

guild = None
emojis = None

def startClient():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.reactions = True
    return discord.Client(intents=intents)
        
# Create a Discord client
client = startClient()

# Event listener for when the bot is ready
@client.event
async def on_ready():
    global guild, emojis
    
    print(f'Logged in as {client.user.name}')
    
    guild = client.get_guild(1096915549302313011)
    emojis = guild.emojis

# Returns a pre-formatted emoji_id
def getEmoji(boss_name):
    formatted_string = boss_name.lower().replace(" ", "")
    
    for emoji in emojis:
        if emoji.name == formatted_string:
            return f"<:{emoji.name}:{emoji.id}>"
    
    print("No emoji matched the provided boss name")
    
@client.event
async def on_raw_reaction_add(payload):
    # Extract relevant information from the payload
    guild_id = payload.guild_id
    channel_id = payload.channel_id
    message_id = payload.message_id
    emoji = str(payload.emoji)
    
    # Fetch the guild, channel, and message objects
    guild = client.get_guild(guild_id)
    channel = guild.get_channel(channel_id)
    message = await channel.fetch_message(message_id)
    member = payload.member
  
    # Get the content of the message
    message_content = message.content
    
    # Check if the reaction is added to the correct message and by a non-bot user
    if message_content == '***React "<:bhbot:1180746269640114198>" to unlock the bot!***' and not member.bot:
        role_name = "BH Bot"
        role = discord.utils.get(guild.roles, name=role_name)

        # Add the role to the member
        await member.add_roles(role)
        print(f"Added {role_name} role to {member.display_name}")
    
    # Check if the reaction is added to the correct message and by a non-bot user
    if message_content == "React to your preferred MVP to get notified with that specific boss" and not member.bot:
        
        for mvp in mvps:
            if emoji == getEmoji(mvp):
                # Replace 'ROLE_NAME' with the actual role name you want to assign
                role = discord.utils.get(guild.roles, name=mvp)

                # Add the role to the member
                await member.add_roles(role)
                print(f"Added {mvp} role to {member.display_name}")
                
    if message_content == "React to your preferred MINI to get notified with that specific boss" and not member.bot:
        
        for mini in minis:
            if emoji == getEmoji(mini):
                # Replace 'ROLE_NAME' with the actual role name you want to assign
                role = discord.utils.get(guild.roles, name=mini)

                # Add the role to the member
                await member.add_roles(role)
                print(f"Added {mini} role to {member.display_name}")

@client.event
async def on_raw_reaction_remove(payload):
    # Extract relevant information from the payload
    guild_id = payload.guild_id
    channel_id = payload.channel_id
    message_id = payload.message_id
    emoji = str(payload.emoji)
    
    # Fetch the guild, channel, and message objects
    guild = client.get_guild(guild_id)
    channel = guild.get_channel(channel_id)
    message = await channel.fetch_message(message_id)
    member = await guild.fetch_member(payload.user_id)

    # Get the content of the message
    message_content = message.content
    
    # Check if the reaction is added to the correct message and by a non-bot user
    if message_content == '***React "<:bhbot:1180746269640114198>" to unlock the bot!***' and not member.bot:
        role_name = "BH Bot"
        role = discord.utils.get(guild.roles, name=role_name)
        
        # Add the role to the member
        await member.remove_roles(role)
        print(f"Removed {role_name} role from {member.display_name}")
    
    # Check if the reaction is added to the correct message and by a non-bot member
    if message_content == "React to your preferred MVP to get notified with that specific boss" and not member.bot:
        
        for mvp in mvps:
            if emoji == getEmoji(mvp):
                # Replace 'ROLE_NAME' with the actual role name you want to assign
                role = discord.utils.get(guild.roles, name=mvp)

                # Add the role to the member
                await member.remove_roles(role)
                print(f"Removed {mvp} role from {member.display_name}")
                
    if message_content == "React to your preferred MINI to get notified with that specific boss" and not member.bot:
        
        for mini in minis:
            if emoji == getEmoji(mini):
                # Replace 'ROLE_NAME' with the actual role name you want to assign
                role = discord.utils.get(guild.roles, name=mini)

                # Add the role to the member
                await member.remove_roles(role)
                print(f"Removed {mini} role from {member.display_name}")
    
    
client.run(config.BOT_TOKEN)