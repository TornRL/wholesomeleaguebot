# Made by Torn_RL
# Made for: Wholesome League (On Twitch.Tv/MonkeyShinesTV)

import os
import random
import itertools
from dotenv import load_dotenv
from discord.ext import commands
import discord
import asyncio

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Define intents for the bot
intents = discord.Intents.default()
intents.messages = True
intents.members = True
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Define a queue as a global variable
queue_status = True
limit_queue_status = False
queue = []

# queue max size when a command is active
queue_max_size = 1000  

# User Violations
user_violations = {}

# OTHER DISCORD ROLES TO IGNORE
MOD_ROLE_ID = int(os.getenv('MOD_ROLE_ID'))
TWITCH_MOD_ROLE_ID = int(os.getenv('TWITCH_MOD_ROLE_ID'))
TIER3_ROLE_ID = int(os.getenv('TIER3_ROLE_ID'))
TIER2_ROLE_ID = int(os.getenv('TIER2_ROLE_ID'))
TIER1_ROLE_ID = int(os.getenv('TIER1_ROLE_ID'))
TWITCH_SUB_ROLE_ID = int(os.getenv('TWITCH_SUB_ROLE_ID'))
RISING_STAR_ROLE_ID = int(os.getenv('RISING_STAR_ROLE_ID'))
HAT_TRICK_ROLE_ID = int(os.getenv('HAT_TRICK_ROLE_ID'))
ONES_WINNER_ROLE = int(os.getenv('1S_WINNER_ROLE'))
TWOS_WINNER_ROLE = int(os.getenv('2S_WINNER_ROLE'))
EVENT_WINNER_ROLE_ID = int(os.getenv('EVENT_WINNER_ROLE_ID'))

# ROLE IDs
CASTER_ROLE_ID = int(os.getenv('CASTER_ROLE_ID'))
EU_ROLE_ID = int(os.getenv('EU_ROLE_ID'))
NAE_ROLE_ID = int(os.getenv('NAE_ROLE_ID'))
NAW_ROLE_ID = int(os.getenv('NAW_ROLE_ID'))
OCE_ROLE_ID = int(os.getenv('OCE_ROLE_ID'))
SAM_ROLE_ID = int(os.getenv('SAM_ROLE_ID'))
MENA_ROLE_ID = int(os.getenv('MENA_ROLE_ID'))
ASIA_EAST_ROLE_ID = int(os.getenv('ASIA_EAST_ROLE_ID'))
SOUTH_AFRICA_ROLE_ID = int(os.getenv('SOUTH_AFRICA_ROLE_ID'))
ASIA_SE_ROLE_ID = int(os.getenv('ASIA_SE_ROLE_ID'))

S1_ROLE_ID = int(os.getenv('S1_ROLE_ID'))
S2_ROLE_ID = int(os.getenv('S2_ROLE_ID'))
S3_ROLE_ID = int(os.getenv('S3_ROLE_ID'))
G1_ROLE_ID = int(os.getenv('G1_ROLE_ID'))
G2_ROLE_ID = int(os.getenv('G2_ROLE_ID'))
G3_ROLE_ID = int(os.getenv('G3_ROLE_ID'))
P1_ROLE_ID = int(os.getenv('P1_ROLE_ID'))
P2_ROLE_ID = int(os.getenv('P2_ROLE_ID'))
P3_ROLE_ID = int(os.getenv('P3_ROLE_ID'))
D1_ROLE_ID = int(os.getenv('D1_ROLE_ID'))
D2_ROLE_ID = int(os.getenv('D2_ROLE_ID'))
D3_ROLE_ID = int(os.getenv('D3_ROLE_ID'))
C1_ROLE_ID = int(os.getenv('C1_ROLE_ID'))
C2_ROLE_ID = int(os.getenv('C2_ROLE_ID'))
C3_ROLE_ID = int(os.getenv('C3_ROLE_ID'))
GC1_ROLE_ID = int(os.getenv('GC1_ROLE_ID'))
GC2_ROLE_ID = int(os.getenv('GC2_ROLE_ID'))
GC3_ROLE_ID = int(os.getenv('GC3_ROLE_ID'))
SSL_ROLE_ID = int(os.getenv('SSL_ROLE_ID'))
SSL_2K_ROLE_ID = int(os.getenv('SSL_2K_ROLE_ID'))

WL_LOBBY_ROLE_ID = int(os.getenv('WL_LOBBY_ROLE_ID'))
LOBBY_CHANNEL_ID = int(os.getenv('LOBBY_CHANNEL_ID'))

RANK_EMOJI = {
    "Silver1": "<EmoteID>",
    "Silver2": "<EmoteID>",
    "Silver3": "<EmoteID>",
    "Gold1": "<EmoteID>",
    "Gold2": "<EmoteID>",
    "Gold3": "<EmoteID>",
    "Platinum1": "<EmoteID>",
    "Platinum2": "<EmoteID>",
    "Platinum3": "<EmoteID>",
    "Diamond1": "<EmoteID>",
    "Diamond2": "<EmoteID>",
    "Diamond3": "<EmoteID>",
    "Champ1": "<EmoteID>",
    "Champ2": "<EmoteID>",
    "Champ3": "<EmoteID>",
    "GrandChamp1": "<EmoteID>",
    "GrandChamp2": "<EmoteID>",
    "GrandChamp3": "<EmoteID>",
    "SSL": "<EmoteID>",
    "SSL2K": "<EmoteID>"
}

# Event handler for bot startup
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Event handler for errors
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f'An error occurred: {str(error)}')

@bot.command(name='test_mmr')
async def test_mmr(ctx):
    user_roles = [role.id for role in ctx.author.roles]  # Get the IDs of all roles the user has
    
    # List of rank roles
    rank_roles = ["s1", "s2", "s3", "g1", "g2", "g3", "p1", "p2", "p3", "d1", "d2", "d3", "c1", "c2", "c3", "gc1", "gc2", "gc3", "ssl", "ssl_2k"]
    
    # Check if the user has any of the rank roles
    for rank in rank_roles:
        role_id = int(os.getenv(f"{rank.upper()}_ROLE_ID"))
        if role_id in user_roles:
            # Calculate MMR based on the rank role
            mmr_value = mmr(role_id)
            await ctx.send(f"Your MMR based on your rank role '{rank.upper()}' is {mmr_value}.")
            return
    
    # If none of the rank roles are found
    await ctx.send("You don't have any of the rank roles.")

# help command
@bot.command(name='helpcommand')
async def help_command(ctx):
    # Define the help message
    help_message = "```Available Commands:\n"
    help_message += "!queue - View the players in the queue.\n"
    help_message += "!join - Join the queue with your rank and region.\n"
    help_message += "!leave - Leave the queue.\n"
    help_message += "!helpcommand - Display this help message.\n"
    help_message += "[CASTER] !3 - (3v3) Divide the queue into two balanced teams and display the results.\n"
    help_message += "[CASTER] !2 - (2v2) Divide the queue into two balanced teams and display the results.\n"
    help_message += "[CASTER] !checkin - (3v3) Players need to react to that message to remain in the queue.\n"
    help_message += "[CASTER] !checkin2 - (2v2) Finds the predominant region to play on.\n"
    help_message += "[CASTER] !region - (3v3) Finds the predominant region to play on.\n"
    help_message += "[CASTER] !region2 - (2v2) Finds the predominant region to play on.\n"
    help_message += "[CASTER] !tregion - (Tournaments) Finds the predominant region to play on.\n"
    help_message += "[CASTER] !forceleave <Current Queue Number> - Forcefully remove a member from the queue.\n"
    help_message += "[CASTER] !emptyqueue - Empty the queue.\n"
    help_message += "[CASTER] !blacklist <@member> - Blacklist a user from joining the queue.\n"
    help_message += "[CASTER] !unblacklist <@member> - Remove a user from the blacklist.\n"
    help_message += "[CASTER] !openqueue - Opens the queue.\n"
    help_message += "[CASTER] !closequeue - Closes the queue.\n"
    help_message += "[CASTER] !skipqueue <Current Queue Number> <Move To Spot> - Skips a player in the queue.```\n"

    # Send the help message
    await ctx.send(help_message)

# queue command
@bot.command(name='queue')
async def view_queue(ctx): 
    # Define the channel ID or name where users can join the queue
    allowed_channel_id = # Channel ID
    notes_kick_ban_channel_id = # Channel ID
    notes_channel = ctx.guild.get_channel(notes_kick_ban_channel_id)

    member = ctx.author

    # Check if the command was sent in the correct channel
    if ctx.channel.id != allowed_channel_id:
        user_id = ctx.author.id
        # Track the number of violations for the user
        if user_id not in user_violations:
            user_violations[user_id] = 1
        else:
            user_violations[user_id] += 1
        
        # If the user has violated the channel rule 2 times, blacklist them
        if user_violations[user_id] == 2:
            if ctx.author.id not in blacklisted_users:
                blacklisted_users.append(ctx.author.id)
                queue[:] = [queued_member for queued_member in queue if queued_member[0] != member]
                await ctx.send(f"{ctx.author.name}, you have been blacklisted for the rest of the stream and removed from the queue.")
            else:
                queue[:] = [queued_member for queued_member in queue if queued_member[0] != member]
                await ctx.send(f"{ctx.author.name}, you already blacklisted for the rest of the stream and removed from the queue.")
            return
        
        if user_violations[user_id] >= 3:
            try:
                # Ban the user
                await ctx.author.ban(reason="Violated rules 3 times.")
                
                # Send a message to the #notes-kick-ban channel
                notes_channel = ctx.guild.get_channel(notes_kick_ban_channel_id)
                if notes_channel:
                    await notes_channel.send(
                        f"{ctx.author.name} has been banned after violating the rules by using the WL Bot in the wrong channel more than 3 times."
                    )
                else:
                    await ctx.send("Cannot find the moderation channel.")
                
                await ctx.send(f"{ctx.author.name} has been banned for violating the rules.")
                return
            except discord.Forbidden:
                await ctx.send("I do not have permission to ban this user.")
            except Exception as e:
                await ctx.send(f"An error occurred: {e}")

    if queue:
        response = "**Players in Queue:**\n"
        for index, (member, roles) in enumerate(queue, 1):
            response += f"{index}. {member.display_name}\n"  # Corrected attribute access
    else:
        response = "The queue is currently empty."
    await ctx.send(response)


@bot.command(name='q')
async def view_queue_short(ctx):
    await view_queue(ctx)


blacklisted_users = []

@bot.command(name='blacklist')
async def blacklist_user(ctx, member: discord.Member):
    if discord.utils.get(ctx.author.roles, id=CASTER_ROLE_ID) is None and discord.utils.get(ctx.author.roles, id=MOD_ROLE_ID) is None:
        await ctx.send("You don't have permission to use this command.")
        return

    if member.id in blacklisted_users:
        await ctx.send(f"{member.name} is already blacklisted.")
    else:
        blacklisted_users.append(member.id)
        await ctx.send(f"{member.name} has been blacklisted from joining the queue.")

@bot.command(name='unblacklist')
async def unblacklist_user(ctx, member: discord.Member):
    if discord.utils.get(ctx.author.roles, id=CASTER_ROLE_ID) is None and discord.utils.get(ctx.author.roles, id=MOD_ROLE_ID) is None:
        await ctx.send("You don't have permission to use this command.")
        return

    if member.id not in blacklisted_users:
        await ctx.send(f"{member.name} is not currently blacklisted.")
    else:
        blacklisted_users.remove(member.id)
        await ctx.send(f"{member.name} has been removed from the blacklist.")

@bot.command(name='j')
async def join_queue_short(ctx):
    await join_queue(ctx)

@bot.command(name='join')
async def join_queue(ctx):
    # Define the channel ID or name where users can join the queue
    allowed_channel_id = # Channel ID
    notes_kick_ban_channel_id = # Channel ID
    notes_channel = ctx.guild.get_channel(notes_kick_ban_channel_id)

    # Check if the command was sent in the correct channel
    if ctx.channel.id != allowed_channel_id:
        user_id = ctx.author.id
        # Track the number of violations for the user
        if user_id not in user_violations:
            user_violations[user_id] = 1
        else:
            user_violations[user_id] += 1
        
        # If the user has violated the channel rule 2 times, blacklist them
        if user_violations[user_id] == 2:
            if ctx.author.id not in blacklisted_users:
                blacklisted_users.append(ctx.author.id)
                await ctx.send(f"{ctx.author.name}, you have been blacklisted for the rest of the stream.")
            else:
                await ctx.send(f"{ctx.author.name}, you already blacklisted for the rest of the stream.")
            return
        
        if user_violations[user_id] >= 3:
            try:
                # Ban the user
                await ctx.author.ban(reason="Violated rules 3 times.")
                
                # Send a message to the #notes-kick-ban channel
                notes_channel = ctx.guild.get_channel(notes_kick_ban_channel_id)
                if notes_channel:
                    await notes_channel.send(
                        f"{ctx.author.name} has been banned after violating the rules by using the WL Bot in the wrong channel more than 3 times."
                    )
                else:
                    await ctx.send("Cannot find the moderation channel.")
                
                await ctx.send(f"{ctx.author.name} has been banned for violating the rules.")
                return
            except discord.Forbidden:
                await ctx.send("I do not have permission to ban this user.")
            except Exception as e:
                await ctx.send(f"An error occurred: {e}")
        
        # Create a clickable link to the allowed channel
        allowed_channel = ctx.guild.get_channel(allowed_channel_id)
        await ctx.send(f"You cannot join the queue at this time. Please head over to {allowed_channel.mention} and use this command to join. Repeated cases will lead to further punishments.")
        return
    
    if ctx.guild is None:
        await ctx.send("You can only join the queue in a server.")
        return

    member = ctx.author
    for queued_member, queued_roles in queue:
        if queued_member == member:
            await ctx.send("You are already in the queue.")
            return
    
    if member.id in blacklisted_users:
        await ctx.send("You are blacklisted and cannot join the queue.")
        return
    
    if queue_status == False:
        await ctx.send("You cannot join the queue right now as it's closed.")
        return
    
    if queue_status and len(queue) >= queue_max_size and limit_queue_status == True:
        await ctx.send(f"{ctx.author.name}, the queue is currently full ({queue_max_size} players). Please wait for a spot to open.")
        return

    # Check if the user has any of the rank roles
    rank_roles = ["s1", "s2", "s3", "g1", "g2", "g3", "p1", "p2", "p3", "d1", "d2", "d3", "c1", "c2", "c3", "gc1", "gc2", "gc3", "ssl", "ssl_2k"]
    user_roles = [role.id for role in ctx.author.roles]
    has_rank_role = any(int(os.getenv(f"{rank.upper()}_ROLE_ID")) in user_roles for rank in rank_roles)
    
    # Check if the user has multiple rank roles
    rank_role_ids = [int(os.getenv(f"{rank.upper()}_ROLE_ID")) for rank in rank_roles]
    user_rank_roles = [role.id for role in ctx.author.roles if role.id in rank_role_ids]

    if len(user_rank_roles) > 1:
        await ctx.send(f"{ctx.author.name}, you have more than one rank role. Please ensure you only have one rank role to join the queue.")
        return
    
    # Check if the user has any of the region roles
    region_roles = ["EU", "NAE", "NAW", "OCE", "SAM", "MENA", "ASIA_EAST", "SOUTH_AFRICA", "ASIA_SE"]
    has_region_role = any(int(os.getenv(f"{region.upper()}_ROLE_ID")) in user_roles for region in region_roles)

    # Check if the user has multiple region roles
    region_role_ids = [int(os.getenv(f"{region.upper()}_ROLE_ID")) for region in region_roles]

    user_region_roles = [role.id for role in ctx.author.roles if role.id in region_role_ids]
    if len(user_region_roles) > 1:
        await ctx.send(f"{ctx.author.name}, you have more than one region role. Please ensure you only have one region role to join the queue.")
        return

    # No rank/region role
    if not has_rank_role:
        await ctx.send("You must have one of the rank roles to join the queue.")
        return
    
    if not has_region_role:
        await ctx.send("You must have one of the region roles to join the queue.")
        return
    
    # Store all the roles the user has
    user_roles_list = ctx.author.roles

    queue.append((member, user_roles_list))  # Store the member and their roles in the queue
    await ctx.send(f"{member.name} has joined the queue.")

@bot.command(name='l')
async def leave_queue_short(ctx):
    await leave_queue(ctx)

@bot.command(name='leave')
async def leave_queue(ctx):
    allowed_channel_id = # Channel ID
    notes_kick_ban_channel_id = # Channel ID
    notes_channel = ctx.guild.get_channel(notes_kick_ban_channel_id)

    member = ctx.author

    # Check if the command was sent in the correct channel
    if ctx.channel.id != allowed_channel_id:
        user_id = ctx.author.id
        # Track the number of violations for the user
        if user_id not in user_violations:
            user_violations[user_id] = 1
        else:
            user_violations[user_id] += 1
        
        # If the user has violated the channel rule 2 times, blacklist them
        if user_violations[user_id] == 2:
            if ctx.author.id not in blacklisted_users:
                blacklisted_users.append(ctx.author.id)
                queue[:] = [queued_member for queued_member in queue if queued_member[0] != member]
                await ctx.send(f"{ctx.author.name}, you have been blacklisted for the rest of the stream and removed from the queue.")
            else:
                queue[:] = [queued_member for queued_member in queue if queued_member[0] != member]
                await ctx.send(f"{ctx.author.name}, you already blacklisted for the rest of the stream and removed from the queue.")
            return
        
        if user_violations[user_id] >= 3:
            try:
                # Ban the user
                await ctx.author.ban(reason="Violated rules 3 times.")
                
                # Send a message to the #notes-kick-ban channel
                notes_channel = ctx.guild.get_channel(notes_kick_ban_channel_id)
                if notes_channel:
                    await notes_channel.send(
                        f"{ctx.author.name} has been banned after violating the rules by using the WL Bot in the wrong channel more than 3 times."
                    )
                else:
                    await ctx.send("Cannot find the moderation channel.")
                
                await ctx.send(f"{ctx.author.name} has been banned for violating the rules.")
                return
            except discord.Forbidden:
                await ctx.send("I do not have permission to ban this user.")
            except Exception as e:
                await ctx.send(f"An error occurred: {e}")
        
        # Create a clickable link to the allowed channel
        allowed_channel = ctx.guild.get_channel(allowed_channel_id)
        await ctx.send(f"You cannot join the queue at this time. Please head over to {allowed_channel.mention} and use this command to join. Repeated cases will lead to further punishments.")
        return
    
    # Check if the member is in the queue
    if any(member == queued_member for queued_member, _ in queue):
        # Filter out the member from the queue
        queue[:] = [queued_member for queued_member in queue if queued_member[0] != member]
        await ctx.send(f"{member.name} has left the queue.")
    else:
        await ctx.send(f"{member.name} is not in the queue.")

@bot.command(name='fl')
async def force_leave_short(ctx):
    await force_leave(ctx)

@bot.command(name='forceleave')
async def force_leave(ctx, position: int):
    if discord.utils.get(ctx.author.roles, id=CASTER_ROLE_ID) is None and discord.utils.get(ctx.author.roles, id=MOD_ROLE_ID) is None:
        await ctx.send("You don't have permission to use this command.")
        return
    
    # Check if the position is within the valid range of the queue
    if position < 1 or position > len(queue):
        await ctx.send("Invalid position. Please provide a valid position in the queue.")
        return
    
    # Remove the member from the queue using the specified position
    member_name = queue[position - 1][0].name
    del queue[position - 1]
    
    await ctx.send(f"{member_name} has been removed from the queue.")

@bot.command(name='eq')
async def empty_queue_short(ctx):
    await empty_queue(ctx)

@bot.command(name='emptyqueue')
async def empty_queue(ctx):
    if discord.utils.get(ctx.author.roles, id=CASTER_ROLE_ID) is None and discord.utils.get(ctx.author.roles, id=MOD_ROLE_ID) is None:
        await ctx.send("You don't have permission to use this command.")
        return
    queue.clear()
    await ctx.send("The queue has been emptied.")

@bot.command(name='3')
async def cast3v3(ctx):
    global queue_status, queue_max_size, limit_queue_status

    if discord.utils.get(ctx.author.roles, id=CASTER_ROLE_ID) is None and discord.utils.get(ctx.author.roles, id=MOD_ROLE_ID) is None:
        await ctx.send("You don't have permission to use this command.")
        return
    
    print("Queue length before casting 3s:", len(queue))  # Debugging print
    if len(queue) < 6:
        await ctx.send("Not enough players in the queue to cast 3s.")
        return
    
    # Pop the top 6 players from the queue using FIFO
    players = [member for member, _ in [queue.pop(0) for _ in range(min(6, len(queue)))]]
    
    print("Players popped for casting 3s:", [player.name for player in players])  # Debugging print
    
    # Extract MMR values for each player
    mmrs = [mmr([role.id for role in player.roles]) for player in players]
    
    print("MMRs of popped players 3s:", mmrs)  # Debugging print

    # Adjuct queue limit size when active
    if queue_status and queue_max_size is not None:
        queue_max_size -= 6
        if queue_max_size < 0:
            queue_max_size = 0
    
    # Calculate closest average MMR and divide players into two groups
    group1, group2 = find_closest_average(mmrs)
    
    # Generate random lobby information
    lobby_info = generate_lobby_info()
    
    # Get the WL_LOBBY_ROLE
    wl_lobby_role = discord.utils.get(ctx.guild.roles, id=WL_LOBBY_ROLE_ID)
    if wl_lobby_role is None:
        await ctx.send("Temporary role not found.")
        return

    # Get the target channel
    target_channel = bot.get_channel(LOBBY_CHANNEL_ID)
    if target_channel is None:
        await ctx.send("Target channel not found.")
        return
    
    # Assign the wl_lobby_role to each player and send a message
    for player in players:
        try:
            await player.add_roles(wl_lobby_role)
            print(f"Role given to {player.name}.")
        except discord.Forbidden:
            print(f"Failed to assign role to {player.name}. User might have insufficient permissions.")
    
    # Wait if needed
    await asyncio.sleep(10)

    # Send the lobby information to the target channel
    await target_channel.send(f"{wl_lobby_role.mention}\n**Lobby Information:**\n{lobby_info}")
    
    # Construct the output message with rank emojis
    output = "**BLUE:**\n"
    output += '\n'.join([
        f"{rank_emoji([role.id for role in player.roles])} {player.name}" 
        for player in players if players.index(player) in group1
    ])
    
    output += f"\n\n**ORANGE:**\n"
    output += '\n'.join([
        f"{rank_emoji([role.id for role in player.roles])} {player.name}" 
        for player in players if players.index(player) in group2
    ])
    
    output += "\n==============================================="
    
    print("Constructed output 3s:", output)  # Debugging print
    
    # Send the output message to the target channel
    await target_channel.send(output)

    # Wait for 3 minutes before removing the role
    await asyncio.sleep(180)
    
    # Remove the wl_lobby_role from each player
    for player in players:
        try:
            await player.remove_roles(wl_lobby_role)
            print(f"Role removed from {player.name}.")
        except discord.Forbidden:
            print(f"Failed to remove role from {player.name}. User might have insufficient permissions.")



@bot.command(name='2')
async def cast2v2(ctx):
    global queue_status, queue_max_size, limit_queue_status
    if discord.utils.get(ctx.author.roles, id=CASTER_ROLE_ID) is None and discord.utils.get(ctx.author.roles, id=MOD_ROLE_ID) is None:
        await ctx.send("You don't have permission to use this command.")
        return
    
    print("Queue length before casting 2s:", len(queue))  # Debugging print
    if len(queue) < 4:
        await ctx.send("Not enough players in the queue to cast 2s.")
        return
    
    # Pop the top 4 players from the queue using FIFO
    players = [member for member, _ in [queue.pop(0) for _ in range(min(4, len(queue)))]]
    
    print("Players popped for casting 2s:", [player.name for player in players])  # Debugging print
    
    # Extract MMR values for each player
    mmrs = [mmr([role.id for role in player.roles]) for player in players]
    
    print("MMRs of popped players 2s:", mmrs)  # Debugging print

    # Adjust queue limit size when active
    if queue_status and queue_max_size is not None:
        queue_max_size -= 4
        if queue_max_size < 0:
            queue_max_size = 0
    
    # Calculate closest average MMR and divide players into two groups
    group1, group2 = find_closest_average_2v2(mmrs)
    
    # Generate random lobby information
    lobby_info = generate_lobby_info()
    
    # Get the WL_LOBBY_ROLE
    wl_lobby_role = discord.utils.get(ctx.guild.roles, id=WL_LOBBY_ROLE_ID)
    if wl_lobby_role is None:
        await ctx.send("Temporary role not found.")
        return

    # Get the target channel
    target_channel = bot.get_channel(LOBBY_CHANNEL_ID)
    if target_channel is None:
        await ctx.send("Target channel not found.")
        return
    
    # Assign the wl_lobby_role to each player and send a message
    for player in players:
        try:
            await player.add_roles(wl_lobby_role)
            print(f"Role given to {player.name}.")
        except discord.Forbidden:
            print(f"Failed to assign role to {player.name}. User might have insufficient permissions.")
    
    # Wait before sending the message
    await asyncio.sleep(10)

    # Send the lobby information to the target channel
    await target_channel.send(f"{wl_lobby_role.mention}\n**Lobby Information:**\n{lobby_info}")
    
    # Construct the output message with rank emojis
    output = "**BLUE:**\n"
    output += '\n'.join([
        f"{rank_emoji([role.id for role in player.roles])} {player.name}" 
        for player in players if players.index(player) in group1
    ])
    
    output += f"\n\n**ORANGE:**\n"
    output += '\n'.join([
        f"{rank_emoji([role.id for role in player.roles])} {player.name}" 
        for player in players if players.index(player) in group2
    ])
    
    output += "\n==============================================="
    
    print("Constructed output 2s:", output)  # Debugging print
    
    # Send the output message to the target channel
    await target_channel.send(output)

    # Wait for 3 minutes before removing the role
    await asyncio.sleep(180)
    
    # Remove the wl_lobby_role from each player
    for player in players:
        try:
            await player.remove_roles(wl_lobby_role)
            print(f"Role removed from {player.name}.")
        except discord.Forbidden:
            print(f"Failed to remove role from {player.name}. User might have insufficient permissions.")



# Player class to represent a player in the queue
class Player:
    def __init__(self, name: str, rank: str, region: str):
        self.name = name
        self.rank = rank
        self.region = region

# MMR calculation function
def mmr(role_ids):
    # Dictionary mapping role IDs to MMR values for rank roles
    mmr_mapping = {
        S1_ROLE_ID: 300,
        S2_ROLE_ID: 350,
        S3_ROLE_ID: 415,
        G1_ROLE_ID: 475,
        G2_ROLE_ID: 530,
        G3_ROLE_ID: 600,
        P1_ROLE_ID: 650,
        P2_ROLE_ID: 715,
        P3_ROLE_ID: 775,
        D1_ROLE_ID: 840,
        D2_ROLE_ID: 915,
        D3_ROLE_ID: 1000,
        C1_ROLE_ID: 1100,
        C2_ROLE_ID: 1200,
        C3_ROLE_ID: 1300,
        GC1_ROLE_ID: 1400,
        GC2_ROLE_ID: 1500,
        GC3_ROLE_ID: 1600,
        SSL_ROLE_ID: 1680,
        SSL_2K_ROLE_ID: 1900

    }

    # If role_ids is an integer, convert it to a list
    if isinstance(role_ids, int):
        role_ids = [role_ids]

    # Initialize MMR value
    mmr_value = None

    # Iterate through the role IDs to find the highest-ranked rank role
    for role_id in role_ids:
        # Skip over the admin role
        if role_id == MOD_ROLE_ID or role_id == TWITCH_MOD_ROLE_ID or TIER3_ROLE_ID == role_id or TIER2_ROLE_ID == role_id or TIER2_ROLE_ID == role_id or TIER1_ROLE_ID == role_id or TWITCH_SUB_ROLE_ID == role_id or HAT_TRICK_ROLE_ID == role_id or EVENT_WINNER_ROLE_ID == role_id or ONES_WINNER_ROLE == role_id or TWOS_WINNER_ROLE == role_id or RISING_STAR_ROLE_ID == role_id:
            continue
        
        # Check if the role ID is a rank role
        if role_id in mmr_mapping:
            # Assign the MMR value for the rank role
            mmr_value = mmr_mapping[role_id]
            break  # Stop iterating once a rank role is found

    # If no rank role is found, return a default MMR value (e.g., 1)
    return mmr_value if mmr_value is not None else 1

def rank_emoji(role_ids):
    emoji_map = {
        SSL_2K_ROLE_ID: RANK_EMOJI["SSL2K"], 
        SSL_ROLE_ID: RANK_EMOJI["SSL"],
        GC3_ROLE_ID: RANK_EMOJI["GrandChamp3"],
        GC2_ROLE_ID: RANK_EMOJI["GrandChamp2"],
        GC1_ROLE_ID: RANK_EMOJI["GrandChamp1"],
        C3_ROLE_ID: RANK_EMOJI["Champ3"],
        C2_ROLE_ID: RANK_EMOJI["Champ2"],
        C1_ROLE_ID: RANK_EMOJI["Champ1"],
        D3_ROLE_ID: RANK_EMOJI["Diamond3"],
        D2_ROLE_ID: RANK_EMOJI["Diamond2"],
        D1_ROLE_ID: RANK_EMOJI["Diamond1"],
        P3_ROLE_ID: RANK_EMOJI["Platinum3"],
        P2_ROLE_ID: RANK_EMOJI["Platinum2"],
        P1_ROLE_ID: RANK_EMOJI["Platinum1"],
        G3_ROLE_ID: RANK_EMOJI["Gold3"],
        G2_ROLE_ID: RANK_EMOJI["Gold2"],
        G1_ROLE_ID: RANK_EMOJI["Gold1"],
        S3_ROLE_ID: RANK_EMOJI["Silver3"],
        S2_ROLE_ID: RANK_EMOJI["Silver2"],
        S1_ROLE_ID: RANK_EMOJI["Silver1"]
    }

    # Ensure role_ids is a list
    if isinstance(role_ids, int):
        role_ids = [role_ids]

    # Initialize rank_emoji to a default value
    rank_emoji = ":grey_question:"  # Default fallback emoji

    # Debug: Log the role IDs being passed to the function
    print(f"Checking roles for rank emoji: {role_ids}")

    # Iterate through the role IDs in descending order of rank
    for role_id in role_ids:
        # Debug: Log the current role being checked
        print(f"Checking role ID: {role_id}")

        # Skip non-rank-related roles
        if role_id in {MOD_ROLE_ID, TWITCH_MOD_ROLE_ID, TIER3_ROLE_ID, TIER2_ROLE_ID, TIER1_ROLE_ID, TWITCH_SUB_ROLE_ID, HAT_TRICK_ROLE_ID, EVENT_WINNER_ROLE_ID, ONES_WINNER_ROLE, TWOS_WINNER_ROLE, RISING_STAR_ROLE_ID}:
            continue

        # Check if the role ID corresponds to a rank role
        if role_id in emoji_map:
            # Assign the emoji for the rank role
            rank_emoji = emoji_map[role_id]
            print(f"Found rank role: {role_id} => {rank_emoji}")
            break  # Stop iterating once a rank role is found

    # Debug: Log the final emoji
    print(f"Final rank emoji: {rank_emoji}")

    return rank_emoji


# Function to find closest average MMR and create two teams
def find_closest_average(mmrs):
    if len(mmrs) != 6:
        raise ValueError("Input list must contain exactly 6 MMR values")
    
    closest_average = float('inf')
    closest_average_group1 = []
    closest_average_group2 = []
    
    for split in itertools.combinations(range(6), 3):
        group1 = list(split)
        group2 = [x for x in range(6) if x not in group1]
        
        average1 = sum(mmrs[i] for i in group1) / 3
        average2 = sum(mmrs[i] for i in group2) / 3
        
        diff = abs(average1 - average2)
        
        if diff < closest_average:
            closest_average = diff
            closest_average_group1 = group1
            closest_average_group2 = group2
    
    return closest_average_group1, closest_average_group2

def find_closest_average_2v2(mmrs):
    if len(mmrs) != 4:
        raise ValueError("Input list must contain exactly 4 MMR values")
    
    closest_average = float('inf')
    closest_average_group1 = []
    closest_average_group2 = []
    
    for split in itertools.combinations(range(4), 2):
        group1 = list(split)
        group2 = [x for x in range(4) if x not in group1]
        
        average1 = sum(mmrs[i] for i in group1) / 2
        average2 = sum(mmrs[i] for i in group2) / 2
        
        diff = abs(average1 - average2)
        
        if diff < closest_average:
            closest_average = diff
            closest_average_group1 = group1
            closest_average_group2 = group2
    
    return closest_average_group1, closest_average_group2

def generate_lobby_info():
    # Generate a random password between 1000 and 9999
    password = random.randint(1000, 9999)
    
    # Construct the lobby information with the provided name and random password
    lobby_info = f"Name: CplWL3v3\nPassword: {password}"
    
    return lobby_info

@bot.command(name='fetch_mmr')
async def fetch_mmr(ctx):
    # Get the user's roles
    user_roles = ctx.author.roles

    # Remove the @everyone role from the list
    user_roles = user_roles[1:]

    # Check if the user has any of the rank roles
    rank_roles = ["s1", "s2", "s3", "g1", "g2", "g3", "p1", "p2", "p3", "d1", "d2", "d3", "c1", "c2", "c3", "gc1", "gc2", "gc3", "ssl", "ssl_2k"]
    user_rank_roles = [role for role in user_roles if role.name.lower() in rank_roles]

    if not user_rank_roles:
        await ctx.send("You must have one of the rank roles to fetch your MMR.")
        return

    # Calculate MMR based on the user's roles
    mmr_value = mmr([role.id for role in user_rank_roles])

    await ctx.send(f"Your MMR based on your highest-ranked role is {mmr_value}.")

@bot.command(name='ci')
async def checkin_short(ctx):
    await checkin(ctx)

# Check in command
@bot.command(name='checkin')
async def checkin(ctx):
    if discord.utils.get(ctx.author.roles, id=CASTER_ROLE_ID) is None and discord.utils.get(ctx.author.roles, id=MOD_ROLE_ID) is None:
        await ctx.send("You don't have permission to use this command.")
        return

    if len(queue) < 6:
        await ctx.send("Not enough players in the queue to check in. You need at least 6 players.")
        return

    # Get the first six players in the queue (FIFO)
    top_6_players = queue[:6]

    # Mention the players in a message
    message_text = "It's your turn to check into Wholesome League. Please react with ✅ within 45 seconds to confirm your spot:\n"
    for member, _ in top_6_players:
        message_text += f"{member.mention}\n"

    message = await ctx.send(message_text)
    await message.add_reaction('✅')

    await asyncio.sleep(45)  # Wait for reactions

    # Double-check reactions after the timer ends
    message = await ctx.channel.fetch_message(message.id)
    
    confirmed_players = set()
    for reaction in message.reactions:
        if reaction.emoji == '✅':
            async for user in reaction.users():
                if user in [member for member, _ in top_6_players]:
                    confirmed_players.add(user)
    
    # Wait an extra 1 seconds and check again to ensure accuracy
    await asyncio.sleep(1)
    message = await ctx.channel.fetch_message(message.id)
    
    for reaction in message.reactions:
        if reaction.emoji == '✅':
            async for user in reaction.users():
                if user in [member for member, _ in top_6_players]:
                    confirmed_players.add(user)  # Ensure no one is missed
    
    # Remove unconfirmed players from the queue
    for member, _ in top_6_players:
        if member not in confirmed_players:
            queue.remove((member, _))
    
    # Notify the confirmed players
    response = "**All players confirmed their spot!**" if len(confirmed_players) == 6 else "**Not all players confirmed their spot. They have been removed from the queue.**"
    await ctx.send(response)

def regionRole(role_ids):
    # Dictionary mapping role IDs to region names
    region_mapping = {
        EU_ROLE_ID: "Europe",
        NAE_ROLE_ID: "NA East",
        NAW_ROLE_ID: "NA West",
        OCE_ROLE_ID: "Oceania",
        SAM_ROLE_ID: "South America",
        MENA_ROLE_ID: "Middle East",
        ASIA_EAST_ROLE_ID: "Asia East",
        SOUTH_AFRICA_ROLE_ID: "South Africa",
        ASIA_SE_ROLE_ID: "Asia SE"
    }

    print("Role IDs:", role_ids)

    # Ensure role_ids is a list
    if isinstance(role_ids, int):
        role_ids = [role_ids]

    # Iterate through the role IDs to find the region role
    for role_id in role_ids:
        # Skip over certain roles
        if role_id in [MOD_ROLE_ID, TWITCH_MOD_ROLE_ID, TIER3_ROLE_ID, TIER2_ROLE_ID, TIER1_ROLE_ID, TWITCH_SUB_ROLE_ID, HAT_TRICK_ROLE_ID, EVENT_WINNER_ROLE_ID, S1_ROLE_ID, S2_ROLE_ID, S3_ROLE_ID, G1_ROLE_ID, G2_ROLE_ID, G3_ROLE_ID, G3_ROLE_ID, P1_ROLE_ID, P2_ROLE_ID, P3_ROLE_ID, D2_ROLE_ID, D2_ROLE_ID, D3_ROLE_ID, C1_ROLE_ID, C2_ROLE_ID, C3_ROLE_ID, GC1_ROLE_ID, GC2_ROLE_ID, GC3_ROLE_ID, SSL_ROLE_ID, SSL_2K_ROLE_ID, ONES_WINNER_ROLE, TWOS_WINNER_ROLE, RISING_STAR_ROLE_ID]:
            continue
        # Check if the role ID corresponds to a region
        if role_id in region_mapping:
            return region_mapping[role_id]

    # If no region role is found, return "Unknown"
    return "Unknown"

def find_predominant_region(player_region_role):
    eu_count = 0
    nae_count = 0
    naw_count = 0
    sam_count = 0
    oce_count = 0
    mena_count = 0
    asia_count = 0
    south_africa_count = 0
    asia_se_count = 0

    if player_region_role == "Europe":
        eu_count += 1
    elif player_region_role == "NA East":
        nae_count += 1
    elif player_region_role == "NA West":
        naw_count += 1
    elif player_region_role == "Oceania":
        oce_count += 1
    elif player_region_role == "South America":
        sam_count += 1
    elif player_region_role == "Middle East":
        mena_count += 1
    elif player_region_role == "Asia East":
        asia_count += 1
    elif player_region_role == "South Africa":
        south_africa_count += 1
    elif player_region_role == "Asia SE":
        asia_se_count += 1
    else:
        return "ERROR INCREMENTING REGION COUNTER"

    if naw_count >= 1 and nae_count >= 2 or (nae_count > 3):
        return "NAE"
    elif eu_count >= 3:
        return "EU"
    elif naw_count >= 3 or (nae_count == 3 and naw_count == 3):
        return "NAW"
    else:
        print("EU:"+ eu_count)
        print("NAE:"+ nae_count)
        print("NAW:"+ naw_count)
        print("OCE:" + oce_count)
        print("SAM:"+ sam_count)
        print("MENA:" + mena_count)
        print("ASIA EAST:" + asia_count)
        print("SOUTH AFRICA:" + south_africa_count)
        print("ASIA SE:" + asia_se_count)
        return "Expected Error: Cannot Find Appropriate Region"
    
@bot.command(name='r')
async def region_short(ctx):
    await test_region(ctx)

@bot.command(name='region')
async def test_region(ctx):
    # Check if the user has permission to use the command
    if discord.utils.get(ctx.author.roles, id=CASTER_ROLE_ID) is None and discord.utils.get(ctx.author.roles, id=MOD_ROLE_ID) is None:
        await ctx.send("You don't have permission to use this command.")
        return
    
    # Check if there are enough players in the queue
    if len(queue) < 6:
        await ctx.send("Not enough players to find the region for 3s.")
        return
    
    # Get the IDs of all roles the user has
    user_roles = [role.id for role in ctx.author.roles]
    
    # List of region roles
    region_roles = ["eu", "nae", "naw", "oce", "sam", "mena", "asia_east", "south_africa", "asia_se"]
    
    # Initialize region count variables
    eu_count = 0
    nae_count = 0
    naw_count = 0
    oce_count = 0
    sam_count = 0
    mena_count = 0
    asia_count = 0
    south_africa_count = 0
    asia_se_count = 0
    
    # Iterate through each player in the queue
    for player in queue[:6]:
        # Extract player's name and roles
        player_name, player_roles = player[0].name, [role.id for role in player[1]]
        
        # Check if the player has any of the region roles and increment the corresponding count variable
        for region in region_roles:
            role_id = int(os.getenv(f"{region.upper()}_ROLE_ID"))
            if role_id in player_roles:
                if role_id in [MOD_ROLE_ID, TWITCH_MOD_ROLE_ID, TIER3_ROLE_ID, TIER2_ROLE_ID, TIER1_ROLE_ID, TWITCH_SUB_ROLE_ID, HAT_TRICK_ROLE_ID, EVENT_WINNER_ROLE_ID, ONES_WINNER_ROLE, TWOS_WINNER_ROLE, RISING_STAR_ROLE_ID]:
                    continue
                # Get the region name based on the region role
                region_name = regionRole(role_id)
                if region_name == "Europe":
                    eu_count += 1
                elif region_name == "NA East":
                    nae_count += 1
                elif region_name == "NA West":
                    naw_count += 1
                elif region_name == "Oceania":
                    oce_count += 1
                elif region_name == "South America":
                    sam_count += 1
                elif region_name == "Middle East":
                    mena_count += 1
                elif region_name == "Asia East":
                    asia_count += 1
                elif region_name == "South Africa":
                    south_africa_count += 1
                elif region_name == "Asia SE":
                    asia_se_count += 1
    
    # Print region counts for debugging
    print("EU Count:", eu_count)
    print("NAE Count:", nae_count)
    print("NAW Count:", naw_count)
    print("OCE Count:", oce_count)
    print("SAM Count:", sam_count)
    print("MENA Count:", mena_count)
    print("ASIA EAST Count:", asia_count)
    print("SOUTH AFRICA Count:", south_africa_count)
    print("ASIA SE Count:", asia_se_count)
    if naw_count >= 1 and nae_count >= 2 or (nae_count > 3) or (naw_count == 3 and eu_count == 3):
        predominant_region = "US EAST"
    elif eu_count >= 3 and nae_count <=2 or (asia_se_count >= 3) or (asia_count >= 3) or (mena_count >=3) or (asia_se_count >= 1 and eu_count >=2):
        predominant_region = "EUROPE"
    elif naw_count >= 3 and eu_count == 0 or (nae_count == 3 and naw_count == 3):
        predominant_region = "US WEST"
    elif nae_count == 3 and eu_count == 3:
        predominant_region = "TIE (Coin Flip)" # Tie between EU and NAE
    elif eu_count == 4 and nae_count == 1 and naw_count == 1:
        predominant_region =  "EUROPE"
    else:
        print("Expected Error: Cannot Find Appropriate Region")
        predominant_region =  "Cannot Find Appropriate Region (Coin Flip)"
    
    
    await ctx.send(f"The predominant region is: {predominant_region}")

@bot.command(name='sq')
async def shorthand_skip_queue(ctx, current_position: int, new_position: int):
    await skip_queue(ctx, current_position, new_position)

@bot.command(name='skipqueue')
async def skip_queue(ctx, current_position: int, new_position: int):
    # Check if the user has permission to use the command
    if discord.utils.get(ctx.author.roles, id=CASTER_ROLE_ID) is None and discord.utils.get(ctx.author.roles, id=MOD_ROLE_ID) is None:
        await ctx.send("You don't have permission to use this command.")
        return

    if ctx.guild is None:
        await ctx.send("This command can only be used in a server.")
        return

    # Ensure the positions are within the valid range
    if not (1 <= current_position <= len(queue)) or not (1 <= new_position <= len(queue)):
        await ctx.send("Invalid positions. Please make sure both positions are within the range of the queue.")
        return

    # Adjust for 0-based array index
    current_index = current_position - 1
    new_index = new_position - 1

    # Get the user and their roles from the current position
    user, user_roles = queue.pop(current_index)

    # Insert the user at the new position
    queue.insert(new_index, (user, user_roles))

    await ctx.send(f"{user.name} has been moved from position {current_position} to {new_position} in the queue.")

# Close queue command
@bot.command(name='closequeue')
async def close_queue(ctx):
    if discord.utils.get(ctx.author.roles, id=CASTER_ROLE_ID) is None and discord.utils.get(ctx.author.roles, id=MOD_ROLE_ID) is None:
        await ctx.send("You don't have permission to use this command.")
        return

    global queue_status
    if queue_status:
        queue_status = False
        await ctx.send("Queue is now closed.")
    else:
        await ctx.send("The queue is now open.")

# Open queue command
@bot.command(name='openqueue')
async def open_queue(ctx):
    if discord.utils.get(ctx.author.roles, id=CASTER_ROLE_ID) is None and discord.utils.get(ctx.author.roles, id=MOD_ROLE_ID) is None:
        await ctx.send("You don't have permission to use this command.")
        return

    global queue_status
    if queue_status == False:
        queue_status = True
        queue_max_size = None
        await ctx.send("Queue is now open.")
    else:
        await ctx.send("The queue is now closed.")
    
@bot.command(name='cq')
async def close_queue_short(ctx):
    await close_queue(ctx)

@bot.command(name='oq')
async def open_queue_short(ctx):
    await open_queue(ctx)

@bot.command(name='ranktest')
async def ranktest(ctx):
    # Get the player's roles (i.e., the command author's roles)
    player = ctx.author  # This ensures it always tests against the person running the command
    
    # Get the player's role IDs
    user_roles = [role.id for role in player.roles]
    
    # List of rank roles
    rank_roles = ["s1", "s2", "s3", "g1", "g2", "g3", "p1", "p2", "p3", "d1", "d2", "d3", "c1", "c2", "c3", "gc1", "gc2", "gc3", "ssl", "ssl_2k"]
    
    # Iterate through the role IDs to find the highest-ranked role
    for rank in rank_roles:
        role_id = int(os.getenv(f"{rank.upper()}_ROLE_ID"))
        if role_id in user_roles:
            # Get the rank emoji based on the role ID
            rank_emoji_result = rank_emoji([role_id])  # Call the original rank_emoji function with role_id
            
            # Send the result with the player's name and rank emoji
            await ctx.send(f"{player.name}'s rank emoji: {rank_emoji_result}")
            return  # Stop after finding the first rank role

@bot.command(name='ci2')
async def checkin2_short(ctx):
    await checkin2(ctx)

@bot.command(name='checkin2')
async def checkin2(ctx):
    if discord.utils.get(ctx.author.roles, id=CASTER_ROLE_ID) is None and discord.utils.get(ctx.author.roles, id=MOD_ROLE_ID) is None:
        await ctx.send("You don't have permission to use this command.")
        return

    if len(queue) < 4:
        await ctx.send("Not enough players in the queue to check in. You need at least 4 players.")
        return

    # Get the first four players in the queue (FIFO)
    top_4_players = queue[:4]

    # Mention the players in a message
    message_text = "It's your turn to check into Wholesome League. Please react with ✅ within 45 seconds to confirm your spot:\n"
    for member, _ in top_4_players:
        message_text += f"{member.mention}\n"

    message = await ctx.send(message_text)
    await message.add_reaction('✅')

    def check(reaction, user):
        return (
            reaction.emoji == '✅'
            and reaction.message.id == message.id
            and user in [member for member, _ in top_4_players]
        )

    try:
        # Wait for 45 seconds and capture all valid reactions
        await asyncio.sleep(45)

        # Refetch the message to get all reactions
        message = await ctx.channel.fetch_message(message.id)

        # Determine confirmed players based on the final reaction state
        confirmed_players = set()
        for reaction in message.reactions:
            if reaction.emoji == '✅':
                async for user in reaction.users():
                    if user in [member for member, _ in top_4_players]:
                        confirmed_players.add(user)

    except Exception as e:
        print(f"Error during check-in: {e}")
        confirmed_players = set()

    # Remove unconfirmed players from the queue
    for member, _ in top_4_players:
        if member not in confirmed_players:
            queue.remove((member, _))

    # Notify the confirmed players
    response = ""
    if len(confirmed_players) == 4:
        response = "**All players confirmed their spot!**"
    else:
        response = "**Not all players confirmed their spot. They have been removed from the queue.**"

    await ctx.send(response)

@bot.command(name='r2')
async def region2_short(ctx):
    await test_region2(ctx)

@bot.command(name='region2')
async def test_region2(ctx):
    # Check if the user has permission to use the command
    if discord.utils.get(ctx.author.roles, id=CASTER_ROLE_ID) is None and discord.utils.get(ctx.author.roles, id=MOD_ROLE_ID) is None:
        await ctx.send("You don't have permission to use this command.")
        return
    
    # Check if there are enough players in the queue
    if len(queue) < 6:
        await ctx.send("Not enough players to find the region for 3s.")
        return
    
    # Get the IDs of all roles the user has
    user_roles = [role.id for role in ctx.author.roles]
    
    # List of region roles
    region_roles = ["eu", "nae", "naw", "oce", "sam", "mena", "asia_east", "south_africa", "asia_se"]
    
    # Initialize region count variables
    eu_count = 0
    nae_count = 0
    naw_count = 0
    oce_count = 0
    sam_count = 0
    mena_count = 0
    asia_count = 0
    south_africa_count = 0
    asia_se_count = 0
    
    # Iterate through each player in the queue
    for player in queue[:4]:
        # Extract player's name and roles
        player_name, player_roles = player[0].name, [role.id for role in player[1]]
        
        # Check if the player has any of the region roles and increment the corresponding count variable
        for region in region_roles:
            role_id = int(os.getenv(f"{region.upper()}_ROLE_ID"))
            if role_id in player_roles:
                if role_id in [MOD_ROLE_ID, TWITCH_MOD_ROLE_ID, TIER3_ROLE_ID, TIER2_ROLE_ID, TIER1_ROLE_ID, TWITCH_SUB_ROLE_ID, HAT_TRICK_ROLE_ID, EVENT_WINNER_ROLE_ID, ONES_WINNER_ROLE, TWOS_WINNER_ROLE, RISING_STAR_ROLE_ID]:
                    continue
                # Get the region name based on the region role
                region_name = regionRole(role_id)
                if region_name == "Europe":
                    eu_count += 1
                elif region_name == "NA East":
                    nae_count += 1
                elif region_name == "NA West":
                    naw_count += 1
                elif region_name == "Oceania":
                    oce_count += 1
                elif region_name == "South America":
                    sam_count += 1
                elif region_name == "Middle East":
                    mena_count += 1
                elif region_name == "Asia East":
                    asia_count += 1
                elif region_name == "South Africa":
                    south_africa_count += 1
                elif region_name == "Asia SE":
                    asia_se_count += 1
    
    # Print region counts for debugging
    print("EU Count:", eu_count)
    print("NAE Count:", nae_count)
    print("NAW Count:", naw_count)
    print("OCE Count:", oce_count)
    print("SAM Count:", sam_count)
    print("MENA Count:", mena_count)
    print("ASIA EAST Count:", asia_count)
    print("SOUTH AFRICA Count:", south_africa_count)
    print("ASIA SE Count:", asia_se_count)
    if naw_count >= 1 and nae_count >= 1 or (nae_count > 3) or (naw_count == 2 and eu_count == 2):
        predominant_region = "US EAST"
    elif eu_count >= 2 or (asia_se_count >= 3) or (asia_count >= 3) or (mena_count >=3) or (asia_se_count >= 1 and eu_count >=2):
        predominant_region = "EUROPE"
    elif naw_count >= 2 and eu_count == 0 or (nae_count == 2 and naw_count == 2):
        predominant_region = "US WEST"
    elif nae_count == 2 and eu_count == 2:
        predominant_region = "TIE (Coin Flip)" # Tie between EU and NAE
    elif eu_count == 2 and nae_count == 1 and naw_count == 1:
        predominant_region =  "US EAST"
    else:
        print("Expected Error: Cannot Find Appropriate Region")
        predominant_region =  "Cannot Find Appropriate Region (Coin Flip)"

@bot.command(name='tregion')
async def tregion(ctx):
    # Check if the user has permission to use the command
    if discord.utils.get(ctx.author.roles, id=CASTER_ROLE_ID) is None and discord.utils.get(ctx.author.roles, id=MOD_ROLE_ID) is None:
        await ctx.send("You don't have permission to use this command.")
        return
    
    # Check if there are enough players in the queue
    if len(queue) < 2:
        await ctx.send("Not enough players to find the region for a tournament.")
        return
    
    # List of region roles
    region_roles = {
        "eu": "Europe",
        "nae": "NA East",
        "naw": "NA West",
        "oce": "Oceania",
        "sam": "South America",
        "mena": "Middle East",
        "asia_east": "Asia East",
        "south_africa": "South Africa",
        "asia_se": "Asia SE"
    }

    # Dictionary to store region counts
    region_counts = {region: 0 for region in region_roles.values()}
    
    # Iterate through each player in the queue
    for player in queue:
        player_roles = [role.id for role in player[1]]

        for region, region_name in region_roles.items():
            role_id = int(os.getenv(f"{region.upper()}_ROLE_ID"))
            
            if region == "naw":  # Count NAW as NAE
                region_name = "NA East"
            
            if role_id in player_roles:
                region_counts[region_name] += 1
                break  # Assign only the first matched region to prevent multiple counts
    
    # Print region counts for debugging
    for region, count in region_counts.items():
        print(f"{region} Count: {count}")

    # Find the most common region
    max_count = max(region_counts.values())
    predominant_regions = [region for region, count in region_counts.items() if count == max_count]

    # Determine the result
    if len(predominant_regions) == 1:
        predominant_region = predominant_regions[0]
    else:
        predominant_region = "TIE (Coin Flip)"  # Handle ties

    # Send the result
    await ctx.send(f"The most common region is: **{predominant_region}**")

# Limits the size of queue
@bot.command('limitqueue')
async def limit_queue(ctx, limit: int = None):
    if discord.utils.get(ctx.author.roles, id=CASTER_ROLE_ID) is None and discord.utils.get(ctx.author.roles, id=MOD_ROLE_ID) is None:
        await ctx.send("You don't have permission to use this command.")
        return

    global queue_status, queue_max_size, limit_queue_status
    if limit is None:
        await ctx.send("Please specify a queue limit!\nExample: `!limitqueue 12` (to set the max queue size to 12)") 
        return

    if limit < len(queue):
        await ctx.send(f"Cannot set limit lower than the current queue size ({len(queue)}).")
        return
    
    queue_max_size = limit
    queue_status = not queue_status
    limit_queue_status = not limit_queue_status

    if queue_status and limit_queue_status == True:
        await ctx.send(f"Queue is now limited to {queue_max_size} players. (**{queue_max_size - len(queue)} spots available!**)")
    else:
        await ctx.send("Queue limit removed. Do !join to rejoin into the queue!")

# Creates as many 2s teams as possible while keeping the closest average across all of them
@bot.command(name='tourny')
async def tourny(ctx):
    if discord.utils.get(ctx.author.roles, id=CASTER_ROLE_ID) is None and discord.utils.get(ctx.author.roles, id=MOD_ROLE_ID) is None:
        await ctx.send("You don't have permission to use this command.")
        return

    if len(queue) < 4:
        await ctx.send("Not enough players in the queue to form teams.")
        return

    teams = []
    remaining_players = queue[:]  # Copy the queue so we don't modify the original

    # List of rank roles
    rank_roles = ["s1", "s2", "s3", "g1", "g2", "g3", "p1", "p2", "p3", "d1", "d2", "d3", "c1", "c2", "c3", "gc1", "gc2", "gc3", "ssl", "ssl_2k"]

    # Extract MMRs dynamically
    player_mmr_list = []
    for player, user_roles in remaining_players:
        mmr_value = None
        for rank in rank_roles:
            role_id = int(os.getenv(f"{rank.upper()}_ROLE_ID"))
            if role_id in [role.id for role in user_roles]:  # Check player's roles
                mmr_value = mmr(role_id)
                break
        
        if mmr_value is None:
            await ctx.send(f"{player.name} does not have a valid rank role. Tournament creation failed.")
            return
        
        player_mmr_list.append((player, mmr_value))

    # Sort players by MMR (lowest to highest)
    sorted_players = sorted(player_mmr_list, key=lambda x: x[1])

    # Create teams by pairing the lowest-rated with the highest-rated player
    while len(sorted_players) >= 2:
        player1 = sorted_players.pop(0)  # Lowest MMR
        player2 = sorted_players.pop(-1)  # Highest MMR
        teams.append((player1[0], player2[0]))  # Store player objects

    # Handle unmatched players
    unmatched_players = [player[0].name for player in sorted_players]

    # Format the message
    message = "__**2v2 Teams Formed**__\n\n"
    for i, (team1, team2) in enumerate(teams, 1):
        message += f"__**Team {i}**__ \n"
        message += f"{rank_emoji([role.id for role in team1.roles])} {team1.name}\n"
        message += f"{rank_emoji([role.id for role in team2.roles])} {team2.name}\n\n"

    if unmatched_players:
        message += "**Unmatched Players:** " + ", ".join(unmatched_players)

    await ctx.send(message)

# Start the bot
bot.run(TOKEN)

