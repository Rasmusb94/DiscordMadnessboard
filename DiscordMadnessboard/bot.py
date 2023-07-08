import asyncio
import os
import random
import discord
import json

from mutagen.mp3 import MP3
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import CommandNotFound

with open('botdata.json', 'r') as jsonbotdata:
    botdata = json.load(jsonbotdata)
TOKEN = botdata['discord_token']
PREFIX = botdata['command_prefix']
EXTENSION = botdata['file_extension']
SERVERID = botdata['discord_server_id']
SPAM_LIMIT = botdata['max_spam_count']
rudebotcheck = botdata['rude_bot']
RUDE_BOT = True if rudebotcheck == 'True' else False
intents = discord.Intents.all()
intents.members = True
help_command = commands.DefaultHelpCommand(no_category = 'Commands')
helpdescription = "These are the commands for the soundboard, therefore clips named the same way will not play if typed in. You can also play any sound file in the directory by typing '" + PREFIX + "nameofthefile'."

soundfilesPath = botdata['soundfiles_path']
soundfiles = os.listdir(soundfilesPath)
sounds = []
allSounds = []
for x in soundfiles:
    allSounds.append(os.path.splitext(x)[0])

for x in allSounds:
    sounds.append(x.lower())

keywords = [
    PREFIX + "random",
    PREFIX + "join",
    PREFIX + "stop",
    PREFIX + "spam",
    PREFIX + "help",
    PREFIX + "chaos",
    PREFIX + "fullchaos",
    PREFIX + "dr",
    PREFIX + "combo",
    PREFIX + "list",
    PREFIX + "leave",
]

bot = commands.Bot(command_prefix=PREFIX,
                   intents=intents,
                   case_insensitive=True,
                   help_command=help_command,
                   description=helpdescription)


@bot.event
async def on_ready():
    '''Connects the bot to Discord'''
    print(f"{bot.user.name} has connected to Discord!")
    print(sounds)
    statusmessage = "Type " + PREFIX + "help"
    activity = discord.Game(statusmessage)
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.command(pass_context=True, name="join", help="Joins the voice channel")
async def _join(ctx):
    await getvoice(ctx)

@bot.command(pass_context=True, name="leave", help="Leaves the voice channel")
async def _leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        botresponse = "leaving"
        errormessage = await getbotresponse(botresponse)
        botmessage = await ctx.send(errormessage)
        await asyncio.sleep(5)
        await botmessage.delete()
        print("Leaving the channel")
    else:
        botresponse = "notconnected"
        errormessage = await getbotresponse(botresponse)
        botmessage = await ctx.send(errormessage)
        await asyncio.sleep(5)
        await botmessage.delete()

@bot.command(pass_context=True, name="list", help="Sends a list of all available sound files")
async def _list(ctx):
    username = ctx.message.author.id
    userid = bot.get_user(username)
    print('Sending list to', ctx.message.author)
    if len(sounds) > 150:
        with open("soundfiles.txt", "w") as file:
            file.write('\n'.join(sounds))
        with open("soundfiles.txt", "rb") as file:
            await userid.send("Here's your list!", file=discord.File(file, "soundfiles.txt"))
    else:
        await userid.send('\n'.join(sounds))
        

@bot.command(pass_context=True, name="random", help="Plays a random sound file")
async def _random(ctx):
    voice = await getvoice(ctx)
    randomsound = random.choice(sounds)
    filepath = soundfilesPath + randomsound + EXTENSION
    sound = FFmpegPCMAudio(filepath)
    voice.stop()
    await stopalltasks()
    voice.play(sound)
    print("Playing", randomsound, "Requested by", ctx.message.author.name)

@bot.command(pass_context=True, name="dr", help="Plays 2 random sounds with a set delay, default 0.5s. Example '?dr 0.5'")
async def _doublerandom(ctx, arg="0.501"):
    voice = await getvoice(ctx)
    try:
        sounddelay = float(arg)
        randomsound = random.choice(sounds)
        filepath = soundfilesPath + randomsound + EXTENSION
        sound = FFmpegPCMAudio(filepath)
        if sounddelay == 0.501:
            sounddelay = random.uniform(0.2, 0.8)
        voice.stop()
        voice.play(sound)
        print("Playing", randomsound, "Requested by", ctx.message.author.name)
        await asyncio.sleep(sounddelay)
        randomsound = random.choice(sounds)
        filepath = soundfilesPath + randomsound + EXTENSION
        sound = FFmpegPCMAudio(filepath)
        voice.stop()
        await stopalltasks()
        voice.play(sound)
        print("Playing ", randomsound)
    except ValueError as valerror:
        botresponse = "valerror"
        errormessage = await getbotresponse(botresponse)
        botmessage = await ctx.send(errormessage)
        print(valerror)
        await asyncio.sleep(5)
        await botmessage.delete()
        await stopalltasks()

@bot.command(pass_context=True, name="spam", help="Rapid Fire! Example: '?spam' or '?spam 5 0.5' for specific num of clips and delay")
async def _spam(ctx, arg1="15", arg2="0.501"):
    spam_task.start(ctx, arg1, arg2)

@tasks.loop()
async def spam_task(ctx, arg1, arg2):
    '''Spam x number of clips with a x second delay'''
    voice = await getvoice(ctx)
    try:
        numberofclips = int(arg1)
        sounddelay = float(arg2)
        if numberofclips == 15:
            numberofclips = random.randint(3, 9)
            if numberofclips > SPAM_LIMIT:
                numberofclips = SPAM_LIMIT
        if sounddelay == 0.501:
            sounddelay = random.uniform(0.2, 1.0)
        print(
            "Playing ", numberofclips, " clips with a ", sounddelay, " second delay"
        )
        for y in range(numberofclips):
            randomsound = random.choice(sounds)
            filepath = soundfilesPath + randomsound + EXTENSION
            sound = FFmpegPCMAudio(filepath)
            voice.stop()
            voice.play(sound)
            print(sound)
            await asyncio.sleep(sounddelay)
        await stopalltasks()
    except ValueError as valerror:
        botresponse = "valerror"
        errormessage = await getbotresponse(botresponse)
        botmessage = await ctx.send(errormessage)
        print(valerror)
        await asyncio.sleep(5)
        await botmessage.delete()
        await stopalltasks()

@bot.command(pass_context=True, name="chaos", help="What the FK is going on")
async def _chaos(ctx):
    chaos_task.start(ctx)

@tasks.loop()
async def chaos_task(ctx):
    '''Plays a random number of clips with a random delay'''
    voice = await getvoice(ctx)
    numberofclips = random.randint(4, 20)
    sounddelay = random.uniform(0.1, 2.0)
    print("Playing ", numberofclips, " clips with a random 0.1 - 2 second delay")
    for y in range(numberofclips):
        randomsound = random.choice(sounds)
        filepath = soundfilesPath + randomsound + EXTENSION
        sound = FFmpegPCMAudio(filepath)
        voice.stop()
        voice.play(sound)
        await asyncio.sleep(sounddelay)
        sounddelay = random.uniform(0.1, 2.0)
        print("Playing", randomsound)
    await stopalltasks()

@bot.command(pass_context=True, name="fullchaos", help="Chaos but clips never get cut off")
async def _fullchaos(ctx):
    fullchaos_task.start(ctx)

@tasks.loop()
async def fullchaos_task(ctx):
    '''Plays a random number of full clips'''
    voice = await getvoice(ctx)
    numberofclips = random.randint(4, 20)
    print("Playing ", numberofclips, " clips")
    for y in range(numberofclips):
        randomsound = random.choice(sounds)
        filepath = soundfilesPath + randomsound + EXTENSION
        sound = FFmpegPCMAudio(filepath)
        audiolength = MP3(os.path.abspath(filepath))
        sounddelay = audiolength.info.length
        voice.stop()
        voice.play(sound)
        await asyncio.sleep(sounddelay - 0.1)
        print("Playing", randomsound)
    await stopalltasks()

@bot.command(pass_context=True, name="combo", help="Plays clips containing the given word. Example '?combo ramsey' or '?combo ramsey 5 0.5' for number of clips and sound delay")
async def _combo(ctx, comboword = "", *args):
    combo_task.start(ctx, comboword, *args)

@tasks.loop()
async def combo_task(ctx, comboword, *args):
    '''Plays multiple clips containing the same string'''
    numberofclips = 0
    sounddelay = 0.0
    try:
        if args[0] is not None:
            try:
                numberofclips = (int)(args[0])
            except ValueError as valerror:
                throwvalueerror(ctx, valerror)
        if args[1] is not None:
            try:
                sounddelay = (float)(args[1])
            except ValueError as valerror:
                throwvalueerror(ctx, valerror)
    except IndexError as indexerror:
        print(indexerror, 'One or more arguments not given, randomizing!')
    if numberofclips == 0:
        numberofclips = random.randint(4, SPAM_LIMIT)
    elif numberofclips > SPAM_LIMIT:
        numberofclips = SPAM_LIMIT
    if sounddelay == 0.0:
        sounddelay = random.uniform(0.2, 0.8)
    try:
        voice = await getvoice(ctx)
        print(
            "Playing", numberofclips, "clips containing the word", 
            comboword, "with a", sounddelay, "second delay."
        )
        soundstoplay = [s for s in sounds if comboword in s]
        random.shuffle(soundstoplay)
        print(soundstoplay)
        playedclips = 0
        for y in range(numberofclips):
            randomsound = soundstoplay[y]
            print('Playing', randomsound)
            filepath = soundfilesPath + randomsound + EXTENSION
            sound = FFmpegPCMAudio(filepath)
            voice.stop()
            voice.play(sound)
            print(y, numberofclips)
            await asyncio.sleep(sounddelay)
            if y == numberofclips - 1:
                await stopalltasks()
            playedclips += 1
    except ValueError as valerror:
        throwvalueerror(ctx, valerror)
        await stopalltasks()
    except IndexError as inderror:
        if playedclips > 0:
            botresponse = "inderror"
            errormessage = await getbotresponse(botresponse, playedclips, comboword)
            print(errormessage)
        else:
            botresponse = "noclips"
            errormessage = await getbotresponse(botresponse, comboword)
        print(inderror)
        botmessage = await ctx.send(errormessage)
        await asyncio.sleep(5)
        await botmessage.delete()
        await stopalltasks()

@bot.event
async def on_message(message):
    '''Finds soundfiles using the input string'''
    await bot.process_commands(message)
    if message.content.startswith(PREFIX):
        await message.delete()
        guildcheck = int(message.guild.id)
        if guildcheck != SERVERID:
            print("I do not have access to this guild, please check your .env file and update your guild ID.")
        else:
            keywordcheck = message.content.split()[0]
            keywordused = 0
            for y in keywords:
                if y == keywordcheck:
                    keywordused += 1
            if keywordused > 0:
                print("Keyword used")
            else:
                foundfiles = 0
                for i in sounds:
                    command = message.content.replace("?", "")
                    if i == command:
                        if message.author.voice:
                            voice = discord.utils.get(
                                bot.voice_clients, guild=message.guild
                            )
                            channel = message.author.voice.channel
                            if voice is None:
                                voice = await channel.connect()
                            filepath = soundfilesPath + i + EXTENSION
                            print(filepath)
                            sound = FFmpegPCMAudio(filepath)
                            await stopalltasks()
                            voice.stop()
                            voice.play(sound)
                        foundfiles = foundfiles + 1
                if foundfiles == 0:
                    if message.author.voice:
                        voice = discord.utils.get(bot.voice_clients, guild=message.guild)
                        channel = message.author.voice.channel
                        if voice is None:
                            voice = await channel.connect()
                        randomsound = random.choice(sounds)
                        filepath = soundfilesPath + randomsound + EXTENSION
                        sound = FFmpegPCMAudio(filepath)
                        await stopalltasks()
                        voice.stop()
                        voice.play(sound)
                        print("Playing random soundfile:", randomsound)
                        botresponse = "randomclip"
                        errormessage = await getbotresponse(botresponse, randomsound)
                        botmessage = await message.channel.send(errormessage)
                        await asyncio.sleep(5)
                        await botmessage.delete()
                    else:
                        botresponse = "usernotconnected"
                        errormessage = await getbotresponse(botresponse)
                        botmessage = await message.channel.send(errormessage)
                        await asyncio.sleep(5)
                        await botmessage.delete()

async def getvoice(ctx):
    '''Checks if the bot is connected to a channel and connects to the user'''
    if await doguildcheck(ctx) is True:
        if ctx.voice_client is None:
            if ctx.author.voice:
                channel = ctx.message.author.voice.channel
                voice = await channel.connect()
                print("joining voice channel of", ctx.author.name)
                return voice
            joinmessage(ctx)
        else:
            if ctx.author.voice:
                if ctx.voice_client.channel != ctx.message.author.voice.channel:
                    await ctx.guild.voice_client.disconnect()
                    channel = ctx.message.author.voice.channel
                    voice = await channel.connect()
                    print("moving to channel of", ctx.author.name)
                    return voice
                voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
                channel = ctx.message.author.voice.channel
                return voice
            joinmessage(ctx)

async def doguildcheck(ctx):
    '''Checks if the bot is connected to a channel and connects to the user'''
    guildcheck = int(ctx.guild.id)
    if guildcheck != SERVERID:
        print("I do not have access to this guild, please check your .env file and update your guild ID.")
    return True if guildcheck == SERVERID else False

@bot.command(pass_context=True, name="stop", help="Stops the current sound clip or loop")
async def _stop(ctx):
    if ctx.author.voice:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        voice.stop()
        await stopalltasks()
        botresponse = "stop"
        errormessage = await getbotresponse(botresponse)
        botmessage = await ctx.send(errormessage)
        await asyncio.sleep(5)
        await botmessage.delete()
    else:
        botresponse = "usernotconnected"
        errormessage = await getbotresponse(botresponse)
        botmessage = await ctx.send(errormessage)
        await asyncio.sleep(5)
        await botmessage.delete()

async def stopalltasks():
    '''Stops all currently running tasks'''
    fullchaos_task.cancel()
    combo_task.cancel()
    chaos_task.cancel()
    spam_task.cancel()

async def getbotresponse(botresponse, *args):
    match RUDE_BOT:
        case True:
            match botresponse:
                case 'valerror':
                    return("Wrong input dickhead")
                case 'leaving':
                    return("Peace out losers")
                case 'alreadyjoined':
                    return("Hey, I'm right here bitch")
                case 'inderror':
                    returnmessage = "There are only "+ str(args[0])+ " clips matching '" + args[1] + "' :dragon_face::sweat_drops:"
                    return(returnmessage)
                case 'notconnected':
                    return("I can't leave if I'm not connected.. Jeez Louise..")
                case 'noclips':
                    returnmessage = "There aren't any clips matching " +args[0] + " :face_with_raised_eyebrow:"
                    return(returnmessage)
                case 'randomclip':
                    returnmessage = "Seems like you completely missed, here's '" +args[0] + "' instead :woozy_face:"
                    return(returnmessage)
                case 'usernotconnected':
                    return("How 'bout you join first, and then I'll consider it.")
                case 'stop':
                    return("Alright, alright, jeez...")
                case _:
                    return("It doesn't work I guess, beats me.")
        case False:
            match botresponse:
                case 'valerror':
                    returnmessage = "Wrong input, check "+ PREFIX +"help for command guides"
                    return(returnmessage)
                case 'leaving':
                    return("Leaving the voice channel")
                case 'alreadyjoined':
                    return("I'm already in your voice channel")
                case 'inderror':
                    returnmessage = "There are only "+ str(args[0])+ " clips with the word " + args[1]
                    return(returnmessage)
                case 'notconnected':
                    return("I'm already not here mate")
                case 'noclips':
                    returnmessage = "There are no clips matching " +args[0]
                    return(returnmessage)
                case 'randomclip':
                    returnmessage = "There are no matching sound clips, so here's a random one!"
                    return(returnmessage)
                case 'usernotconnected':
                    return("You need to join the channel before using a bot command")
                case 'stop':
                    return("Stopping the madness")
                case _:
                    return("It doesn't work I guess, beats me.")

async def joinmessage(ctx):
    '''Error message, user not in a voice channel'''
    botresponse = "usernotconnected"
    errormessage = await getbotresponse(botresponse)
    botmessage = await ctx.send(errormessage)
    print("user is not in a channel or bot does not have access")
    await asyncio.sleep(5)
    await botmessage.delete()

async def throwvalueerror(ctx, valerror):
    '''Faulty argument inputs, check help for argument info'''
    botresponse = "valerror"
    errormessage = await getbotresponse(botresponse)
    botmessage = await ctx.send(errormessage)
    print(valerror)
    await asyncio.sleep(5)
    await botmessage.delete()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

bot.run(TOKEN)