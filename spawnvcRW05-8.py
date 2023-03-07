
#spawnvcRW05-8.py

import os
import threading
import asyncio
from datetime import datetime, timedelta
import time
import discord
from discord.ext import commands
from discord.ext import commands, tasks
import re
#import openai
#from reportlab.pdfgen import canvas


# uncomment the 2 lines below for PC deploy
# comment the 2 lines below for railway deploy
#from dotenv import load_dotenv
#load_dotenv('spammytest.env')

#uncomment for PC
#openai.api_key = os.getenv('TOKEN2')
#uncomment for railway
#openai.api_key = os.environ['TOKEN2']

#intents = discord.Intents().all()
#intents = discord.Intents().default()
intents = discord.Intents(members=True, voice_states=True, value=True, message_content = True)
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='?', intents=intents)







zuluDiff = -5
patternGetInt = r"^\D\D(\d{2})"
channelsData = {}
lockReporting = False
reportNumber = 0
doReport = False
#guildData = {}

















async def restart(ctx):

    message = client.guilds[0].name + ' server is restarting'
    print (message)
    await ctx.send(message)
    print (message)
    member = client.guilds[0].get_member(425437217612103684)
    await member.send(message)
    os.execv(sys.executable, ['python'] + sys.argv)
    #await client.close()
    #await client.logout()


@client.command()
async def ping(ctx):

    embed = discord.Embed(description=(f'Pong!'),  colour=discord.Colour.purple())
    print ('pong sent')
    await ctx.send(embed=embed)


@client.command()
async def latency(ctx):

    await ctx.send (f" {client.latency}")


##@client.command()
##async def lvc(ctx):
##    guild = ctx.guild
##    voice_channels = guild.voice_channels
##    channel_list = ""
##    for channel in voice_channels:
##        members = channel.members
##        member_list = [member.display_name for member in members]
##        member_string = ", ".join(member_list) if member_list else "None"
##        channel_list += f"{channel.name}: {member_string}\n"
##    await ctx.send(channel_list)





#@client.event
#async def on_message(message):
#    print ('receieved ' + message.content)
#    # Ignore messages sent by the bot itself
#    if message.author == client.user:
#        return

#    if message.content.startswith('chatGPT'):
#        words = message.content.split()
#        words.pop(0)
#        newMessage = " ".join(words)
#        response = openai.Completion.create(
#            engine="davinci",
#            prompt=newMessage,
#            max_tokens=100,
#            n=1,
#            stop=None,
#            temperature=0.5,
#            )
#        response_text = response.choices[0].text.strip()

#        # Send the response back to the member
#        await message.channel.send(response_text)








#########################           on ready            #########################





@client.event
async def on_ready():
    
    global lockRorting
    global doReport

    print ('\n\rLogged in as {0.user}'.format(client))
    print(f'Connected to {len(client.guilds)} guilds')
    print('executing version spawnvcPC05-8.py')

    for guild in client.guilds:
        print ('Connected to server: {}'.format(guild.name))

    for guild in client.guilds:
        print ('\n\r' f"Guild = [{guild.name}]")

        adjustmentsMade = False
        channels = guild.voice_channels
        
        # sort the voice channels
        target_channel = discord.utils.get(guild.voice_channels, name="MakeNewChannel")
        all_channels = guild.voice_channels
        target_index = all_channels.index(target_channel)
        vc_channels = sorted([c for c in all_channels if c.name.startswith("VC")], key=lambda c: c.name)
        for i, c in enumerate(vc_channels):
            await c.edit(position=target_index+i+1)

        # Remove empty VC channels
        for channel in channels:
            #print ('start channel name = ' + channel.name)
            if ((channel.name.startswith('VC')) and (len(channel.members) == 0)):
                await channel.delete()
                adjustmentsMade = True
                print (f"Guild [{guild.name}] deleted [{channel.name}]")

        # move members out of MakeNewChannel channel   
        for channel in channels:
            if ((f"{channel.name}"== 'MakeNewChannel') and (len(channel.members)) != 0):
                #print (channel.name)
                lenChannelMembers = len(channel.members)
                while len(channel.members) > 0:
                    mncMember =  channel.members[0]
                    existingChannels = [c for c in channel.guild.voice_channels if c.name.startswith("VC")]
                    newChannelNumber = getNewChannelNumber(existingChannels)
                    newChannelName = f"VC{newChannelNumber:02} {mncMember.display_name.split('#')[0]}"
                    movedToChannel = await channel.category.create_voice_channel(newChannelName)
                    await mncMember.move_to(movedToChannel)
                    adjustmentsMade = True
                    print (f"Guild [{guild.name}] channel [{newChannelName}] created moved [{mncMember.name}]")
                    # sort the voice channels
                    target_channel = discord.utils.get(guild.voice_channels, name="MakeNewChannel")
                    all_channels = guild.voice_channels
                    target_index = all_channels.index(target_channel)
                    vc_channels = sorted([c for c in all_channels if c.name.startswith("VC")], key=lambda c: c.name)
                    for i, c in enumerate(vc_channels):
                        await c.edit(position=target_index+i+1)

        message = ('adjustments made = 'f"{adjustmentsMade} on {guild.name} server")
        print ('finished cleaning up ' + message)
                    
        member = client.guilds[0].get_member(425437217612103684)
        print ('sending message')
        await member.send(message)

    


    botGuilds = client.guilds
    print ('guilds set')
    report.start()    # timer task for future use
    
    


    print ('exiting on_ready now')
    exit






    








##################        functions           ###########################



def truncateDatetime (dt):

    dt_str = str(dt)
    period_index = dt_str.rfind(".")
    if period_index != -1:
        dt_str = dt_str[:period_index]
    return dt_str


def getNewChannelNumber (existingChannels):

    takenNumbers = []
    for channel in existingChannels:
        match = re.match(patternGetInt, channel.name)
        if match:
            number = int(match.group(1))
            takenNumbers.append(number)
    
    newChannelNumber = 0
    while newChannelNumber in takenNumbers:
        newChannelNumber += 1
        
    return newChannelNumber


















@tasks.loop(seconds = 60) # repeat in 1 minute
async def report():
    
    global reportNumber
    global doReport

    if not lockReporting:
        if doReport:
            print ('\n\rchannel report ' + str(reportNumber) + '\n\r')
            reportNumber += 1

            for guild_name, guild_channels in channelsData.items():
                print(f"\n\rGuild: [{guild_name}]")
                for channel_name, channel_members in guild_channels.items():
                    if channel_members:
                        member_list = "\r\r ".join(channel_members)
                        channel_name += ' ->'
                        print(f"  {channel_name:<25}{member_list:>25})
                        
            channelsData.clear()
            doReport = False
        else:
            print ('No activity')
    else:
        print ('reporting locked')










    



@client.event
async def on_voice_state_update(member, before, after):
    
    global doReport
    global lockReporting
    showMoves = False

    guild = member.guild
    nlcr = '\n\r'

    memberDisplayName = member.display_name.split('#')[0]
    memberName = member.name
    #if after.channel is not None and before.channel is None:
    
    if (before.channel is None):
        beforeChannel = 'None'
    else: beforeChannel=(f"{before.channel}")
    if (after.channel is None):
        afterChannel = 'None'
    else: afterChannel=(f"{after.channel}")

    if (beforeChannel != afterChannel):
        if beforeChannel == "MakeNewChannel": nlcr = ''
        if showMoves:
            print (f"{nlcr}01 --> {truncateDatetime(datetime.now() + timedelta(hours=zuluDiff))} Guild [{guild.name}] [{memberDisplayName}] - [{memberName}] left channel [{beforeChannel}] joined channel [{afterChannel}]")

        # join MakeNewChannel
        if (after.channel is not None) and (after.channel.name == "MakeNewChannel"):
            category = after.channel.category
            existingChannels = [c for c in after.channel.guild.voice_channels if c.name.startswith("VC")]
            newChannelNumber = getNewChannelNumber(existingChannels)
            newChannelName = f"VC{newChannelNumber:02} {member.display_name.split('#')[0]}"

            channel = await category.create_voice_channel(newChannelName)
            await member.move_to(channel)
            # sort the voice channels
            target_channel = discord.utils.get(guild.voice_channels, name="MakeNewChannel")
            all_channels = guild.voice_channels
            target_index = all_channels.index(target_channel)
            vc_channels = sorted([c for c in all_channels if c.name.startswith("VC")], key=lambda c: c.name)
            for i, c in enumerate(vc_channels):
                await c.edit(position=target_index+i+1)
    
        # channel vacated
        if (before.channel is not None) and ('VC' in str({before.channel})):
            if len(before.channel.members) == 0:
                await before.channel.delete()
                if showMoves:
                    print (f"02 --> {truncateDatetime(datetime.now() + timedelta(hours=zuluDiff))} Guild [{guild.name}] [{memberDisplayName}] - [{memberName}] vacated channel [{before.channel}] deleted") #moved to {after.channel}")
            else:
                beforeChannel = f"{before.channel}"
                if((beforeChannel) != (f"{after.channel}")):
                    newName = f"VC{(re.match(patternGetInt, str(beforeChannel)).group(1))} {before.channel.members[0].display_name.split('#')[0]}"
                    if (f"{before.channel}") != newName:
                        await before.channel.edit(name=newName)
                        if showMoves:
                            print (f"03 --> {truncateDatetime(datetime.now() + timedelta(hours=zuluDiff))} Guild [{guild.name}] [{memberDisplayName}] - [{memberName}] before channel [{beforeChannel}] renamed to [{newName}]")
                    elif showMoves:
                        (f"04 --> {truncateDatetime(datetime.now() + timedelta(hours=zuluDiff))} Guild [{guild.name}] [{memberDisplayName}] - [{memberName}] before channel [{beforeChannel}] moved to [{after.channel}]")
 


        lockReporting = True
    
        #for guild in client.guilds:
        #    channelsData[guild.name] = {}
        #    for channel in guild.voice_channels:
        #        channelsData[guild.name][channel.name] = [member.name for member in channel.members]


        for guild in client.guilds:
            channelsData[guild.name] = {}
            for channel in guild.voice_channels:
                members = []
                for member in channel.members:
                    members.append(f"{member.name} ({member.display_name})")
                channelsData[guild.name][channel.name] = members







        lockReporting = False
        doReport = True

    




# PC deploy
client.run(os.getenv('TOKEN'))  

#railway deploy 
#client.run(os.environ['TOKEN'])

# https://discord.com/api/oauth2/authorize?client_id=1079357107771551814&permissions=16787472&scope=bot%20applications.commands







