import discord
from discord import client
from discord.ext import commands
from colorama import Fore, Style
import fade
import os
from inputimeout import inputimeout, TimeoutOccurred
import time
import requests


########config
prefix = ";"
fp = commands.Bot(command_prefix=prefix, self_bot=True)
keylist = ['nigger', 'nigga', 'faggot', 'kys', 'dox', 'doxx', 'ddos']
fp.remove_command("help")
token = ""
r = f'{Fore.RESET}'
status = True
########config 


def logo():
  startup = (f"""
      :::::::::: :::        ::::::::::: :::::::::  :::::::::: :::::::::       Logged into : {fp.user.name}#{fp.user.discriminator}
     :+:        :+:            :+:     :+:    :+: :+:        :+:    :+:       ID : {fp.user.id}
    +:+        +:+            +:+     +:+    +:+ +:+        +:+    +:+        Creation date : {fp.user.created_at}
   +#++:++#   +#+            +#+     +#+    +:+ +#++:++#   +#++:++#:    
  +#+        +#+            +#+     +#+    +#+ +#+        +#+    +#+          A project created by chineserice.
 #+#        #+#            #+#     #+#    #+# #+#        #+#    #+#           For more info, contact chinese rice#8270 on Discord.
########## ########## ########### #########  ########## ###    ###            Run ;help for command information.
""")
  faded_text = fade.fire(startup)
  print(faded_text)


@fp.event
async def on_connect():
  logo()
  if status == True:
    await fp.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Currently hosting Elider."))



@fp.command(aliases = ["help"])
async def info(ctx):
    await ctx.message.delete()
    await ctx.send('Check your console.', delete_after = 10)
    help = (f"""
Purge ; Purges your messages in the channel you typed the command in. Usage: ;purge amount. *
Keypurge ; Looks for certain words in a channel and deletes them. Usage: ;keypurge amount. *
Guildpurge ; Clears your messages in all guilds. Usage: ;guildpurge amount. *
Keyguildpurge ; Clears every message in all joined guilds that have a certain word/s in them. Usage: ;guildpurge amount. *
Accountpurge ; Wipes every message on your account. DMs, GCs & Guilds. You will be asked to verify this action in the console. Usage: ;accountpurge
*If amount is left blank, it will delete 100 messages.

》»»»◈«««《 Aliases 》»»»◈«««《
Purge ; chanpurge, clear
Keypurge ; keychanpurge, kcpurge
Guildpurge ; gpurge
Keyguildpurge ; keygpurge, kgpurge
Accountpurge ; accpurge, apurge
""")
    faded_text = fade.fire(help)
    print(faded_text)
    time.sleep(20)
    cc = lambda: os.system('cls')
    cc()
    logo()

###########################################singular channel purge    

@fp.command(aliases = ["chanpurge", "clear"])
async def purge(ctx, amount:int = None):
  if amount == None:
    amount = 100
  counter = 0
  messages = await ctx.channel.history(limit=amount).flatten()
  for message in messages:
    if message.author == fp.user:
      await message.delete()
      counter += 1
  print(f"{Fore.YELLOW}Deleted {counter} messages.{r}")

@fp.command(aliases = ["keychanpurge",'kcpurge'])
async def keypurge(ctx, amount:int = None):
  if amount == None:
    amount = 100
  counter = 0
  messages = await ctx.channel.history(limit=amount).flatten()
  for message in messages:
   if any(word in message.content for word in keylist):
      if message.author == fp.user:
         await message.delete()
         counter += 1
  print(f"{Fore.YELLOW}Deleted {counter} messages.{r}")

########################################################guild purge

@fp.command(aliases = ["guildpurge"])
async def gpurge(ctx, amount:int = None):
  if amount == None:
    amount = 100
  counter = 0
  guild = ctx.message.guild
  for channel in guild.channels:
    if str(channel.type) == 'text':
      messages = await channel.history(limit=amount).flatten()
      for message in messages:
        if message.author == fp.user:
          await message.delete()
          counter += 1
  print(f"{Fore.YELLOW}Deleted {counter} messages.{r}")

@fp.command(aliases = ["keyguildpurge", "kgpurge"])
async def keygpurge(ctx, amount:int = None):
  if amount == None:
    amount = 100
  counter = 0
  guild = ctx.message.guild
  for channel in guild.channels:
    if str(channel.type) == 'text':
      messages = await channel.history(limit=amount).flatten()
      for message in messages:
        if any(word in message.content for word in keylist):
          if message.author == fp.user:
            await message.delete()
            counter += 1
  print(f"{Fore.YELLOW}Deleted {counter} messages.{r}")

########################################################account purge

@fp.command(aliases = ["accpurge", 'apurge'])
async def accountpurge(ctx, amount:int = None):
  if amount == None:
    amount = 100
  counter = 0
  try:
    input = inputimeout(prompt=f'Are you sure you want to delete all messages sent from your account?\n{Fore.GREEN}{Style.BRIGHT}Y {r}\ {Fore.RED}{Style.BRIGHT}N{r}', timeout=15)
  except TimeoutOccurred:
    print(f"{Fore.RED}You took too long to input an answer, please try again.{r}")
  if input in ["N","n"]:
    print(f"{Fore.RED}Goodbye.")  
    time.sleep(5)
    exit()  
  if input in ["Y","y"]:
    for guild in fp.guilds: 
        for channel in guild.channels:
          if str(channel.type) == 'text':
            messages = await channel.history(limit=amount).flatten()
            for message in messages:
              if message.author == fp.user:
                await message.delete()
                counter += 1
                print(f"{Fore.YELLOW}Deleted {counter} messages. (Server)")
    dmchannels = [x["id"] for x in requests.get('https://discord.com/api/v9/users/@me/channels', headers={"authorization": fp.http.token}).json()]            
    for channel in dmchannels:
      channel = await fp.fetch_channel(channel)    
      async for message in channel.history(limit = None):
        if message.author == fp.user and message.type == discord.MessageType.default:
          await message.delete()
          counter += 1
    print(f"{Fore.YELLOW}Deleted {counter} messages.(DMs)")



try: 
  fp.run(token, bot = False)
except discord.LoginFailure:
  print(f"{Fore.RED} Token is invalid, please try again.")