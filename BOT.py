import discord
import asyncio
from discord.embeds import Embed
from discord.ext import commands
import random
import os
import youtube_dl
import json
import requests
import datetime
import configparser
import aiohttp
import sqlite3

filtered_words=["Blessan sucks"]
joined=0

config = configparser.ConfigParser()
config.read('keys.ini')

client = commands.Bot(command_prefix = '=')

apikey = config['Tenor']['key']

client.remove_command('help')



#help command
@client.group(invoke_without_command=True)
async def help(ctx):
    em=discord.Embed(title="Help",description="Use =help <command> for extended info on that command",color=ctx.author.color)

    em.add_field(name="Moderation",value="kick,ban,mute,unmute,unban")
    em.add_field(name="Greetings",value="     Hi,Bye")
    em.add_field(name='Deleting messages',value="clear")

    await ctx.send(embed=em)

@help.command()
async def kick(ctx):
    em=discord.Embed(title="Kick",description="Kicks a member",color=ctx.author.color)
    em.add_field(name="**Example**",value="=kick <member> [reason]")
    await ctx.send(embed=em)
@help.command()
async def ban(ctx):
    em=discord.Embed(title="Ban",description="Bans a member",color=ctx.author.color)
    em.add_field(name="**Example**",value="=ban <member> [reason]")
    await ctx.send(embed=em)
@help.command()
async def unban(ctx):
    em=discord.Embed(title="Unban",description="Unbans a member",color=ctx.author.color)
    em.add_field(name="**Example**",value="=unban <member> [reason]")
    await ctx.send(embed=em)
@help.command()
async def mute(ctx):
    em=discord.Embed(title="mute",description="mutes a member from all channels",color=ctx.author.color)
    em.add_field(name="**Example**",value="=mute <member> ")
    await ctx.send(embed=em)
@help.command()
async def unmute(ctx):
    em=discord.Embed(title="Unmute",description="Unmutes a member, if he/she has being muted",color=ctx.author.color)
    em.add_field(name="**Example**",value="=unmute <member> ")
    await ctx.send(embed=em)
@help.command()
async def clear(ctx):
    em=discord.Embed(title="Clear",description="Clears number of messages",color=ctx.author.color)
    em.add_field(name="**Example**",value="=clear <amount>")
    await ctx.send(embed=em)
@help.command()
async def whois(ctx):
    em=discord.Embed(title="Whois",description="Gives Info about  a member",color=ctx.author.color)
    em.add_field(name="**Example**",value="=whois <member.mention>")
    await ctx.send(embed=em)
#help command end

@client.event
async def on_command_error(ctx,error):
    pass

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.do_not_disturb,activity=discord.Game('With Your Mind'))


    print('Bot is ready.')
    print(f'Logged in as: {client.user.name} ID: {565511660421382144}')
    print(f'Online in guilds:')
    for server in client.guilds:
        print(f'Guild name: {server.name}{server.name}')
        print(f'Guild ID: {759765256196063243}')

#welcome message
@client.event
async def on_member_join(member):
    global joined
    joined+=1
    for channel in member.server.channels:
        if str(channel)=="💬chat":
            await client.send_messages(f"Welcome to the server {member.mention}")


#delete bad words
@client.event
async def on_message(msg):
    for word in filtered_words:
        if word in msg.content:
            await msg.delete()
    await client.process_commands(msg)

#hi command
@client.command()
async def Hi(ctx):
    await ctx.send("How you dooin")


#bye command
@client.command()
async def Bye(ctx):
    await ctx.send("You are going?:(")

@client.event
async def on_message(ctx):
    if ctx.content.startswith("tenor.search"):
            message_content = ctx.content
            split_message = message_content.split()
            len_message = int(len(split_message)) - 1
            datetime_now = datetime.datetime.now()
            time = datetime_now.strftime("%d/%m/%Y %H:%M:%S")
            try:
                int(split_message[len_message])
                check = True
            except:
                check = False
            if check == False:
                search = "https://api.tenor.com/v1/search?q{}&key={}&limit=1&media_filter=basic".format(split_message[1:], apikey)
                get = requests.get(search)
                if get.status_code == 200:
                    json_search = get.json()
                    json_check = json_search['next']
                    if json_check == "0":
                        await ctx.channel.send("{} I didn't found any gifs".format(ctx.author.mention))
                    else:
                        json_s = json_search['results']
                        table = json_s[0]
                        title = table["title"]
                        ID = table['id']
                        url = json_search['results']
                        url = url[0]
                        url = url['url']
                        shares = json_search['results']
                        shares = shares[0]
                        shares = shares['shares']
                        table = table.get("media")
                        table = table[0]
                        table = table.get("gif")
                        table = table.get("url")
                        if title == "":
                            title = "None"
                        search_embed = discord.Embed(title="Search Results", colour=discord.Color.blue(), image="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
                        search_embed.add_field(name="Title: ", value=title, inline=False)
                        search_embed.add_field(name="ID: ", value=ID, inline=False)
                        search_embed.add_field(name="Link: ", value=url, inline=True)
                        search_embed.set_image(url=table)
                        search_embed.set_footer(text="You sent requests at {}".format(time), icon_url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
                        search_embed.set_thumbnail(url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
                        await ctx.channel.send(embed=search_embed)
                elif get.status_code == 404:
                    await ctx.channel.send("{} Tenor is working at the moments now!".format(ctx.author.mention))	
            elif check == True:
                search_limit = split_message[len_message]
                split_message.pop()
                search = "https://api.tenor.com/v1/search?q={}&key={}&limit={}&media_filter=basic".format(split_message[1:], apikey, search_limit)
                get = requests.get(search)
                if get.status_code == 200:
                    json_s = get.json()
                    json_check = json_s["next"]
                    if json_check == "0":
                        await ctx.channel.send("{} I didn't found any gifs".format(ctx.author.mention))
                    elif json_check < search_limit:
                        await ctx.channel.send("{} The maximum of this search is {}!".format(ctx.author.mention, json_check))
                    else:
                        json_s = json_s["results"]	
                        i = 0
                        while i <= int(search_limit):
                            table = json_s[i]
                            title = table['title']
                            ID = table['id']
                            url = json_s[i]
                            url = url['url']
                            table = table.get("media")
                            table = table[0]
                            table = table.get("gif")
                            table = table.get("url")
                            #await message.channel.send("{}".format(table))
                            if title == "":
                                title = "None"
                            i += 1
                            search_embed = discord.Embed(title="Search Results", colour=discord.Color.blue(), image="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
                            search_embed.add_field(name="Title: ", value=title, inline=False)
                            search_embed.add_field(name="ID: ", value=ID, inline=False)
                            search_embed.add_field(name="Link: ", value=url, inline=True)
                            search_embed.set_image(url=table)
                            search_embed.set_footer(text="You sent requests at {}".format(time), icon_url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
                            search_embed.set_thumbnail(url="https://i.ibb.co/dKtMKmG/tenor-logo.jpg")
                            await ctx.channel.send(embed=search_embed)
                            if i == int(search_limit):
                                break
                            else:
                                continue			
                elif get.status_code == 404:
                    await ctx.channel.send("{} Tenor is working at the problems now!".format(ctx.author.mention))
            elif split_message[len_message] == 50:
                await ctx.channel.send("{} It's to much gifs in 1 time!".format(ctx.author.mention))



#kick command

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx,member: discord.Member,*,reason=None):
    await member.kick(reason=reason)


#ban command
@client.command()
@commands.has_permissions(kick_members=True)
async def ban(ctx,member: discord.Member,*,reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned{member.mention}')



#unban members command
@client.command()
@commands.has_permissions(kick_members=True)
async def unban(ctx,*,member):
    banned_users=await ctx.guild.bans()
    member_name, member_discriminator=member.split('#')
    for ban_entry in banned_users:
        user= ban_entry.user
        if (user.name,user.member_discriminator)==(member_name,member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {member.mention}')
            return
    await ctx.send(member+' was not found')


#deleting messages command
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx,amount=2):
    await ctx.channel.purge(limit=amount)


#mute command
@client.command(aliases=['m'])
@commands.has_permissions(kick_members=True)
async def mute(ctx,member:discord.Member):
    Mute_role=ctx.guild.get_role(785551595366121483)
    await member.add_roles(Mute_role)
    await ctx.send(member.mention+' has being muted')


#umute command
@client.command(aliases=['un'])
@commands.has_permissions(kick_members=True)
async def unmute(ctx,member:discord.Member):
    muted_role=ctx.guild.get_role(785551595366121483)
    await member.remove_roles(muted_role)
    await ctx.send(member.mention+' has being unmuted')

#whois command
@client.command(aliases=['user','info'])
@commands.has_permissions(kick_members=True)
async def whois(ctx,member:discord.Member):
    embed=discord.Embed(title=member.name,description=member.mention,color=discord.Colour.red())
    embed.add_field(name='ID',value=member.id,inline=True)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(icon_url=ctx.author.avatar_url,text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)


#music commandss
@client.command()
async def play(ctx,url : str,channel):
    song_there=os.path.isfile('song.mp3')
    try:
        if song_there:
            os.remove('song.mp3')
    except PermissionError:
        await ctx.send('Wait for the current music to end or us the <stop> command')
        return

    voiceChannel= discord.utils.get(ctx.guild.voice_channels, name=channel)
    await voiceChannel.connect()
    voice =discord.utils.get(client.voice_clients,guild=ctx.guild)


    ydl_opts={
        'format': 'bestaudio/best',
        'postprocessors' : [{
            'key':'FFmpegExtractAudio',
            'prefferedcodec':'mp3',
            'prefferedquality':'192'
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            os.rename(file,'song.mp3')
    voice.play(discord.FFmpegPCMAudio('song.mp3'))
    

@client.command()
async def leave(ctx):
    voice =discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send('```The bot is not connected to a voice channel```')

@client.command()
async def pause(ctx):
    voice =discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send('```Currently no audio is playing.```')

@client.command()
async def resume(ctx):
    voice =discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send('```The audio is not paused```')

@client.command()
async def stop(ctx):
    voice =discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()
#music commands end
  


#error messages
@kick.error
async def kick(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send('`You dont have the permission to kick members.`')
@ban.error
async def ban(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send('`You dont have the permission to ban members.`')
@unban.error
async def unban(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send('`You dont have the permission to unban members.`')
@mute.error
async def ban(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send('`You dont have the permission to mute members.`')
@unmute.error
async def unban(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send('`You dont have the permission to unmute members.`')
@clear.error
async def clear(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send('`You dont have the permission to clear messages`')
    
#error messages end

client.run(config['Discord']['key'])