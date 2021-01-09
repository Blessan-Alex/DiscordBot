import discord
import random
import asyncio
from discord.embeds import Embed
from discord.ext import commands
import random
import os
import youtube_dl



hugimage=['https://www.clipartkey.com/view/Jbwxib_milkandmocha-hug-cute-bears-happy-kawaii-freetoedit-milk/']
filtered_words=["Blessan sucks"]
joined=0


client = commands.Bot(command_prefix = '=')
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


#sending images command
@client.command()
async def meme(ctx):
    embed=discord.Embed(color=discord.Colour.red())
    random_link=random.choice(hugimage)
    embed.set_image(url=random_link)
    await ctx.send(embed=embed)


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




client.run('Your token')
