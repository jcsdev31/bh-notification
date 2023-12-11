import discord
import config
from constants.bosses import mvps, minis, is_announced
from BossHuntGPT import setup
import asyncio
import waitlist as wl

# Function to get the emoji based on the status
def get_status_emoji(status):
    if status == 0:
        return "🔴"
    elif status == 1:
        return "🟠"
    elif status == 2:
        return "🟡"
    elif status == 3:
        return "🟢"
    else:
        return ""

class CommandCenter:
    admin_id = "<@1043418696560951306>"
    channel_id = 1178294879449784380
    guild_id = 1096915549302313011
    channel = None
    guild = None
    emojis = None
    active_instance = None
    
    def __init__(self):
        self.channel = client.get_channel(self.channel_id)  # Initialize instance variable in the constructor
        self.guild = client.get_guild(self.guild_id)
        self.emojis = self.guild.emojis
    
class Discord:
    guild = None
    category = None
    roles_channel = None
    bot_announcements = None
    bot_guide = None
    live_notifications = None
    drop_database = None
    boss_channels = {}
    
    def __init__(self, guild_id):
        self.guild = client.get_guild(guild_id)
    
    async def setup_guild(self):
        await self.setup_category()
        await self.setup_roles_channel(None)
        await self.setup_bot_announcements()
        await self.setup_bot_guide()
        await self.setup_live_notifications()
        await self.setup_drop_database()
        
    async def setup_category(self):
        category_name = "MVP/Mini Notification"
        self.category = discord.utils.get(self.guild.categories, name=category_name)
        
        if not self.category:
            await cc.channel.send("***Category not found! Creating new category ...***")
            self.category = await self.guild.create_category_channel(category_name)
        
    async def setup_roles_channel(self, position):
        roles_channel_name = "get-bh-roles"
        self.roles_channel = discord.utils.get(self.category.channels, name=roles_channel_name)
        
        if not self.roles_channel:
            await cc.channel.send("***get-bh-roles not found! Creating new get-bh-roles ...***")
            overwrites = {
                self.guild.default_role: discord.PermissionOverwrite(send_messages=False, add_reactions=False, view_channel=True),
                self.guild.me: discord.PermissionOverwrite(send_messages=True, add_reactions=True)
            }
            if position is None:
                self.roles_channel = await self.category.create_text_channel(name=roles_channel_name, overwrites=overwrites)
            else:
                self.roles_channel = await self.category.create_text_channel(name=roles_channel_name, overwrites=overwrites, position=position)
            
            await setup_roles(self.guild)
            
            # Send a message to the channel
            message_bot_unlock = await self.roles_channel.send('***React "<:bhbot:1180746269640114198>" to unlock the bot!***')
            await message_bot_unlock.add_reaction("<:bhbot:1180746269640114198>")
            print('bh bot role message sent')
            
            # Send a message to the channel
            message_mvp = await self.roles_channel.send("React to your preferred MVP to get notified with that specific boss")
            print('mvp role message sent')
            
            for mvp in mvps:
                # Add the reaction to the message
                await message_mvp.add_reaction(getEmoji(mvp))
                print(f"{mvp} added as reaction")
                await asyncio.sleep(1)
                
            message_mini = await self.roles_channel.send("React to your preferred MINI to get notified with that specific boss")
            print('mini role message sent')
            
            for mini in minis:
                # Add the reaction to the message
                await message_mini.add_reaction(getEmoji(mini))
                print(f"{mini} added as reaction")
                await asyncio.sleep(1)
    
    async def setup_bot_announcements(self):
        bot_announcements_name = "bot-announcements"
        self.bot_announcements = discord.utils.get(self.category.channels, name=bot_announcements_name)
        
        if not self.bot_announcements:
            await cc.channel.send("***bot-announcements not found! Creating new bot-announcements ...***")
            role_name = "BH Bot"
            bh_bot_role = discord.utils.get(self.guild.roles, name=role_name)
            overwrites = {
                self.guild.default_role: discord.PermissionOverwrite(send_messages=False, add_reactions=False, view_channel=False),
                bh_bot_role: discord.PermissionOverwrite(view_channel=True),
                self.guild.me: discord.PermissionOverwrite(send_messages=True, add_reactions=True, view_channel=True)
            }
            self.bot_announcements = await self.category.create_text_channel(name=bot_announcements_name, overwrites=overwrites)
        
    async def setup_bot_guide(self):
        bot_guide_name = "bot-guide"
        self.bot_guide = discord.utils.get(self.category.channels, name=bot_guide_name)
        
        if not self.bot_guide:
            await cc.channel.send("***bot-guide not found! Creating new bot-guide ...***")
            role_name = "BH Bot"
            bh_bot_role = discord.utils.get(self.guild.roles, name=role_name)
            overwrites = {
                self.guild.default_role: discord.PermissionOverwrite(send_messages=False, add_reactions=False, view_channel=False),
                bh_bot_role: discord.PermissionOverwrite(view_channel=True),
                self.guild.me: discord.PermissionOverwrite(send_messages=True, add_reactions=True, view_channel=True)
            }
            self.bot_guide = await self.category.create_text_channel(name=bot_guide_name, overwrites=overwrites)
            
            await self.bot_guide.send(""":red_circle: **= LONGER TIME**
:orange_circle:  **= SHORT TIME**
:yellow_circle:  **= REFRESHING SOON**
:green_circle:  **= APPEARED**
:star2:  **= BANNER DETECTED**
:space_invader:  **= VOID DETECTED**""")
        
            roles_channel_link = self.roles_channel.jump_url
        
            await self.bot_guide.send(f"""***==============================***
***== HOW TO UNLOCK THE BOT ==***
***==============================***
1. Go to {roles_channel_link}
2. Click/Tap the <:bhbot:1180746269640114198> to unlock the update channels
3. React to the MVP/MINI that you want to receive notifications from
**NOTE:** 
*DO NOT SPAM REACT THE BOSSES FOR THE BOT TO REGISTER YOUR ACTION. IF YOUR REACT DIDN'T GIVE YOU THE ROLE AFTER 5 SECONDS, TRY IT AGAIN*""")
        
            await self.bot_guide.send("""***==============================***
***== SETUP THE NOTIFICATION ==***
***==============================***""")
        
            await self.bot_guide.send(""":mobile_phone:**PHONE**:mobile_phone: 
Long tap the server icon on the left sidebar, tap Notifications, then tap **"Only @mentions"**""")
        
            image_path_1 = 'bot-guide/mobile1.jpg'
            image_path_2 = 'bot-guide/mobile2.jpg'
            image_path_3 = 'bot-guide/pc.PNG'
            
            file_1 = discord.File(image_path_1)
            file_2 = discord.File(image_path_2)
            file_3 = discord.File(image_path_3)
            
            await self.bot_guide.send(files=[file_1, file_2])
            
            await self.bot_guide.send(""":computer: **PC** :computer:
Right click the server icon on the left sidebar, hover over Notification Settings, click **"Only @mentions"**""")
        
            await self.bot_guide.send(files=[file_3])
    
    async def setup_live_notifications(self):
        live_notifications_name = "live-notifications"
        self.live_notifications = discord.utils.get(self.category.channels, name=live_notifications_name)
        
        if not self.live_notifications:
            await cc.channel.send("***live-notifications not found! Creating new live-notifications ...***")
            role_name = "BH Bot"
            bh_bot_role = discord.utils.get(self.guild.roles, name=role_name)
            overwrites = {
                self.guild.default_role: discord.PermissionOverwrite(send_messages=False, add_reactions=False, view_channel=False),
                bh_bot_role: discord.PermissionOverwrite(view_channel=True),
                self.guild.me: discord.PermissionOverwrite(send_messages=True, add_reactions=True, view_channel=True)
            }
            self.live_notifications = await self.category.create_text_channel(name=live_notifications_name, overwrites=overwrites)
    
    async def setup_drop_database(self):
        drop_database_name = "drop"
        self.drop_database = discord.utils.get(self.category.channels, name=drop_database_name)
        
        if not self.drop_database:
            await cc.channel.send("***drop not found! Creating new drop ...***")
            role_name = "BH Bot"
            bh_bot_role = discord.utils.get(self.guild.roles, name=role_name)
            overwrites = {
                self.guild.default_role: discord.PermissionOverwrite(send_messages=False, add_reactions=False, view_channel=False),
                bh_bot_role: discord.PermissionOverwrite(view_channel=True),
                self.guild.me: discord.PermissionOverwrite(send_messages=True, add_reactions=True, view_channel=True)
            }
            self.drop_database = await self.category.create_text_channel(name=drop_database_name, overwrites=overwrites)
    
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
    print(f'Logged in as {client.user.name}')
    global cc, active_guilds, bosses
    
    bosses = list(mvps.keys()) + list(minis.keys())
    
    cc = CommandCenter()
    active_guilds = []
        
    await cc.channel.send(f"***Instance {wl.instance_id} has connected! Awaiting commands...***")

@client.event
async def on_message(message):
    global cc
    
    if message.content.startswith('!set_active_instance'):
        new_instance = message.content.split(' ')[1]
        if cc.active_instance == new_instance:
            await message.channel.send(f'***Instance {wl.instance_id} is already active!***')
        else: 
            cc.active_instance = new_instance
        
            if is_this_instance():
                await message.channel.send(f'***Instance {wl.instance_id} is now active!***')
    
    # CHECK IF COMMAND_CENTER IS DIRECTED TO THIS INSTANCE
    if is_this_instance():
        # print(f"Received message: {message.content}")
        global active_guilds
        if message.author == client.user:
            return

        if message.content.startswith('!start_instance'):
            if not wl.instance_udid:
                await message.channel.send('***Instance UDID not set!***')
            elif not active_guilds:
                await message.channel.send('***No active guilds to send updates to!***')
            else:
                if not wl.is_running:
                    wl.clear_all_json()
                    wl.is_running = True
                    await message.channel.send('***Starting the infinite loop...***')
                    for obj in active_guilds:
                        await obj.live_notifications.send("***Boss Hunt Assistant initializing ...***")
                    await clean_channels()
                    if wl.is_restart:
                        await setup_dc_sidebar()
                    await message.channel.send('***Bot is done setting up!***')
                    await setup()
                else:
                    await message.channel.send('***The loop is already running.***')

        elif message.content.startswith('!stop_instance'):
            if wl.is_running:
                wl.is_running = False
                await alert_shutdown()
            else:
                await message.channel.send('***The loop is not currently running.***')
                
        elif message.content.startswith('!set_active_guild'):
            guild_id = int(message.content.split(' ')[1])
            active_guild = Discord(guild_id)
            await active_guild.setup_guild()
            is_already_active = False
            
            for obj in active_guilds:
                if obj.guild.id == guild_id:
                    await cc.channel.send(f"***{obj.guild.name} (ID: {obj.guild.id}) is already active!***")
                    is_already_active = True
            
            if not is_already_active:
                await wl.set_active_guild(guild_id)
                active_guilds.append(active_guild)
                await cc.channel.send(f"***{active_guild.guild.name} (ID: {active_guild.guild.id}) has been set as an active guild!***")
            
        elif message.content.startswith('!get_active_guilds'):
            count = 1
            for obj in active_guilds:
                await cc.channel.send(f"***Active Guild {count}: {obj.guild.name} (ID: {obj.guild.id})***")
                count += 1
            if count == 1:
                await cc.channel.send("***No active guilds found!***")
            
        elif message.content.startswith('!remove_active_guild'):
            guild_id = int(message.content.split(' ')[1])
            
            for obj in active_guilds:
                if obj.guild.id == guild_id:
                    active_guilds.remove(obj)
                    await cc.channel.send(f"***{obj.guild.name} (ID: {obj.guild.id}) has been set to inactive!***")
        
        elif message.content.startswith('!get_all_guilds'):
            # Access the list of guilds
            for guild in client.guilds:
                await cc.channel.send(f"***Bot is a member of guild: {guild.name} (ID: {guild.id})***")
        
        elif message.content.startswith('!get_active_instance'):
            await cc.channel.send(f"***Active Instance: Instance {wl.instance_id}***")
            
        elif message.content.startswith('!set_instance_udid'):
            wl.instance_udid = message.content.split(' ')[1]
            await cc.channel.send(f"***Instance UDID set to: {wl.instance_udid}***")
            wl.clear_active_guilds()
        
        elif message.content.startswith('!get_instance_udid'):
            if not wl.instance_udid:
                await cc.channel.send(f"***Instance UDID not set!***")
            else:
                await cc.channel.send(f"***Instance UDID: {wl.instance_udid}***")
        
        elif message.content.startswith('!delete_role'):
            if not active_guilds:
                await message.channel.send('***No active guilds!***')
            else:
                role = message.content.split(' ')[1]
                await delete_role(role)
        
        elif message.content.startswith('!reset_all_roles'):
            if not active_guilds:
                await message.channel.send('***No active guilds!***')
            else:
                await reset_all_roles()
                
        elif message.content.startswith('!send_announcement '):
            # Extract the announcement content after the command
            announcement_content = message.content[len('!send_announcement '):]
            await send_announcement(announcement_content)
            await cc.channel.send(f"***Announcement has been sent***")
            
        elif message.content.startswith('!get_all_active_voice_channels'):
            await get_all_active_voice_channels()
            
        elif message.content.startswith('!clear_all_active_voice_channels'):
            await clear_all_active_voice_channels()
            
        elif message.content.startswith('!get_all_active_text_channels'):
            await get_all_active_text_channels()
            
        elif message.content.startswith('!clear_all_active_text_channels'):
            await clear_all_active_text_channels()
        
        elif message.content.startswith('!check_get_roles_channel'):
            await check_get_roles_channel()
            
# Returns a pre-formatted emoji_id
def getEmoji(boss_name):
    formatted_string = boss_name.lower().replace(" ", "")
    
    for emoji in cc.emojis:
        if emoji.name == formatted_string:
            return f"<:{emoji.name}:{emoji.id}>"
    
    print("No emoji matched the provided boss name")
    
# Check if the commands comming from the command center is directed to this instance
def is_this_instance():
    if cc.active_instance and cc.active_instance == wl.instance_id:
        return True
    else:
        return False

async def setup_roles(guild):

    role_name = "BH Bot"
    existing_role = discord.utils.get(guild.roles, name=role_name)

    if existing_role is None:
        # Role doesn't exist, create it
        new_role = await guild.create_role(name=role_name, permissions=discord.Permissions(0))
        print(f'Created role: {new_role.name}')
        await asyncio.sleep(1)
    else:
        print(f'Role {existing_role.name} already exists')

    for boss in bosses:
        role_name = boss

        # Check if the role already exists
        existing_role = discord.utils.get(guild.roles, name=role_name)
        
        if existing_role is None:
            # Role doesn't exist, create it
            new_role = await guild.create_role(name=role_name, permissions=discord.Permissions(0))
            print(f'Created role: {new_role.name}')
            await asyncio.sleep(1)
        else:
            print(f'Role {existing_role.name} already exists')
            
async def delete_role(boss):
    formatted_string = boss.replace("-", " ")
    
    for guild in active_guilds:
        role_name = formatted_string
        
        # Check if the role already exists
        existing_role = discord.utils.get(guild.guild.roles, name=role_name)
        
        if existing_role:
            await existing_role.delete()
            await cc.channel.send(f"***The role {boss} has been deleted for {guild.guild.name}!***")
        else:
            await cc.channel.send(f"***Role {boss} does not exist in {guild.guild.name}***")
            
async def reset_all_roles():
    for guild in active_guilds:
        
        roles_channel_name = "get-bh-roles"
        roles_channel = discord.utils.get(guild.category.channels, name=roles_channel_name)
        
        if roles_channel:
            await roles_channel.delete()
            position = roles_channel.position
            await cc.channel.send(f"***The get-bh-roles has been deleted for {guild.guild.name}!***")
        else:
            await cc.channel.send(f"***get-bh-roles not found! No channel to delete {guild.guild.name}***")
            
        for boss in bosses:
            role_name = boss
            
            # Check if the role already exists
            existing_role = discord.utils.get(guild.guild.roles, name=role_name)
            
            if existing_role:
                await existing_role.delete()
                print(f"***The role {boss} has been deleted for {guild.guild.name}!***")
            else:
                print(f"***Role {boss} does not exist in {guild.guild.name}***")
            
        await guild.setup_roles_channel(position)
        await cc.channel.send(f"***Done resetting all roles and roles-channel for {guild.guild.name}!***")

async def clean_channels():
    for guild in active_guilds:
        for boss_name in bosses:
            for i in range(4):
                channel_name = f"{get_status_emoji(i)}{boss_name}"
                channel = discord.utils.get(guild.guild.channels, name=channel_name)
                if channel:
                    await channel.delete()
                    print(f"{channel_name} voice channel deleted in {guild.guild.name}")
                    break
                channel_name = f"{get_status_emoji(i)}🌟{boss_name}"
                channel = discord.utils.get(guild.guild.channels, name=channel_name)
                if channel:
                    await channel.delete()
                    print(f"{channel_name} voice channel deleted in {guild.guild.name}")
                    break
        
async def update_status(boss, status, is_announced):
    for guild in active_guilds:
        is_update = False
        
        role_name = boss
        
        # Check if the role already exists
        role = discord.utils.get(guild.guild.roles, name=role_name)
        
        for i in range(4):
            channel_name = f"{get_status_emoji(i)}{boss}"
            channel = discord.utils.get(guild.guild.channels, name=channel_name)
            if channel:
                await channel.delete()
                print(f"{channel_name} voice channel deleted in {guild.guild.name}")
                position = channel.position
                is_update = True
                break
            channel_name = f"{get_status_emoji(i)}🌟{boss}"
            channel = discord.utils.get(guild.guild.channels, name=channel_name)
            if channel:
                await channel.delete()
                position = channel.position
                is_update = True
                break
        
        # Define the permissions
        overwrites = {
            guild.guild.default_role: discord.PermissionOverwrite(view_channel=False, connect=False),
            role: discord.PermissionOverwrite(view_channel=True),
            guild.guild.me: discord.PermissionOverwrite(view_channel=True, manage_channels=True, connect=True)
        }
            
        # Create the voice channel within the category
        if is_announced:
            channel_name = f"{get_status_emoji(status)}🌟{boss}"
        else:
            channel_name = f"{get_status_emoji(status)}{boss}"
        
        max_retries = 3
        retry_interval = 5
        retries = 0
        sent = False
        while retries < max_retries and not sent:
            try:
                if is_update:
                    channel = await guild.category.create_voice_channel(name=channel_name, overwrites=overwrites, position=position)
                else:
                    channel = await guild.category.create_voice_channel(name=channel_name, overwrites=overwrites)
                sent = True
                print(f"{channel_name} voice channel created in {guild.guild.name}")
            except Exception as e:
                print(f"Error: {e}")
                retries += 1
                print(f"Retrying ({retries}/{max_retries}) in {retry_interval} seconds...")
                await asyncio.sleep(retry_interval)

        if not sent:
            print("Max retries reached. Message could not be sent.")
        
        # Save boss_name:channel to boss_channels
        guild.boss_channels[boss] = channel
        
async def setup_dc_sidebar():
    for boss, status in mvps.items():
        if not status == -1:
            await update_status(boss, status, is_announced[boss])
    
    for boss, status in minis.items():
        if not status == -1:
            await update_status(boss, status, is_announced[boss])

def set_is_running(new):
    wl.is_running = new
    
async def alert_shutdown():
    
    await cc.channel.send('***Stopping the infinite loop...***')
    for obj in active_guilds:
        await obj.live_notifications.send("***Boss Hunt Assistant turning off ...***")
    await clean_channels()
    print("Bot is done cleaning up!")
    await cc.channel.send('***Bot is done cleaning up!***')
    wl.is_restart = True

async def send_announcement(message):
    for guild in active_guilds:
        role_name = "BH Bot"
        
        # Check if the role already exists
        role = discord.utils.get(guild.guild.roles, name=role_name)
        await guild.bot_announcements.send(f">>> {role.mention} {message}")

async def get_all_active_voice_channels():
    for guild in active_guilds:
        for channel in guild.category.voice_channels:
            print(f"{channel.name} in {guild.guild.name}")
    
    print("get_all_active_voice_channels done!")

async def clear_all_active_voice_channels():
    for guild in active_guilds:
        for channel in guild.category.voice_channels:
            print(f"{channel.name} deleted in {guild.guild.name}")
            await channel.delete()
            
    print("clear_all_active_voice_channels done!")
    
async def get_all_active_text_channels():
    for guild in active_guilds:
        for channel in guild.category.text_channels:
            print(f"{channel.name} in {guild.guild.name}")
    
    print("get_all_active_text_channels done!")

async def clear_all_active_text_channels():
    for guild in active_guilds:
        for channel in guild.category.text_channels:
            print(f"{channel.name} deleted in {guild.guild.name}")
            await channel.delete()
            
    print("clear_all_active_text_channels done!")

async def check_get_roles_channel():
    for guild in active_guilds:
        print(f'Checking get_roles_channel for {guild.guild.name}')
        async for message in guild.roles_channel.history(limit=3):
            print(f'Message: {message.content}')

            reactions = message.reactions

            # Iterate through reactions
            for reaction in reactions:
                print(f'Reaction {reaction.emoji}')

client.run(config.BOT_TOKEN)