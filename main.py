import asyncio
from sqlitedict import SqliteDict
import pandas as pd #SqLiteDict + Pandas why do i feel like it could be a lot less complicated and im just overcomplicating it
import discord
from discord.ext import commands
import os
import time
from dotenv import load_dotenv
load_dotenv()

#Made by @toasterclock
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents, activity= discord.Activity(type=discord.ActivityType.listening, name="$help"))
bot.remove_command('help')



#Databases
#db (todos database)
#timelog (not in use)
#points (points database)
db = SqliteDict('./todos.db', autocommit=True)
#timeLogDB = SqliteDict('./timeLog.db', autocommit=True)
pointsDB = SqliteDict('./points.db', autocommit=True)
#temporary timing storage
allTimer = {}
#Functions

def createTable(theID):
    df = pd.DataFrame({'todo': [], 'tag': []})
    db[theID] = df
    return df

def addToTable(theID,todo,tag):
    df = db[theID]
    df.loc[-1] = [todo,tag]
    df.index = df.index + 1
    df = df.sort_index()
    df = df.drop_duplicates(['todo', 'tag'])
    db[theID] = df
    try:
      addToTable(theID,todo,tag)
    except KeyError:
      createTable(theID)
      addToTable(theID,todo,tag)
    return db[theID] 

def removeFromTable(author,index):
    df = db[author]
    #if index is 1 then drop index 0 of the database cus python yeah
    index -= 1
    df = df.drop(index)
    db[author] = df
    return db[author]



#points system
#counts the number of seconds to 3 decimal places
#When displaying points, it will auto convert to points system
def timeToPoints(theID,endTime):
  points = 0
  points = endTime
  if theID in pointsDB.keys():
    pointsToInt = float(pointsDB[theID])
    pointsToInt += points
    pointsDB[theID] = str(round(pointsToInt,3))
  else:
    pointsDB[theID] = ''
    pointsDB[theID] = str(round(points,3))
  print(pointsDB[theID])

def pointsDisplayer(theID):
  pointsData = 0
  pointsData = float(pointsDB[theID]) / 60
  pointsData = round(pointsData,3)
  return pointsData



def newTimer(theID):
  allTimer[theID] = time.time()
  #json.dump(allTimer, open("timerdebugger.txt",'w'))
  return 'Starting Stopwatch: ' + str(theID)

def stopTimer(theID):
  ending = time.time()
  starting = allTimer[theID]
  endTime = ending - starting
  realEndTime = time_convert(endTime)
  allTimer.pop(theID, None)
  #json.dump(allTimer, open("timerdebugger.txt",'w'))
  #print(realEndTime) Debugging realendtime
  timeToPoints(theID,endTime)
  return realEndTime

def addAllTodo(theID):
  db[theID] = []
  return 'Added'

def editAllTodo(theID, addTodoItem):
  db[theID] += [addTodoItem]
  authorTodo(theID)
  return authorTodo(theID)

def authorTodo(theID):
  authorReturn = ''
  for stuff in range(len(db[theID])):
    authorReturn +=f"{(stuff+1)}. {db[theID][stuff]} \n"
  return authorReturn

#removeTodo FIXED
def removeTodo(theID, removeIndex):
  removeIndex -= 1
  temporarydb = db[theID]
  removeItem = temporarydb[removeIndex]
  temporarydb.remove(removeItem)
  db[theID] = temporarydb

def removeAllTodo(theID):
  db[theID] = []
  #json.dump(allTodo, open("todolist.txt",'w'))


#stopwatch conversion FIXED
def time_convert(seconds): 
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    seconds = round(seconds)
    minutes = round(minutes)
    hour = round(hour)
    if hour > 0:
      return str(hour) + "h " + str(minutes) + "min " + str(seconds) + "s"
    elif minutes > 0:
      return str(minutes) + "min " + str(seconds) + "s"
    else:
      return str(seconds) + "s"

#On Ready - prints that its ready
@bot.event
async def on_ready():
    print('Connection successful,  {0.user}'.format(bot))

#Under Development - On Bot Join: Send Messages
@bot.event
async def on_guild_join(ctx):
  await ctx.create_text_channel('study-timers')
  global studyVoiceChannel
  global studyChannel
  studyChannel = discord.utils.get(bot.get_all_channels(), name='study-timers')
  studyVoiceChannel = discord.utils.get(bot.get_all_channels(), name='ProductivityTimer')
  await ctx.create_voice_channel('ProductivityTimer')
  embedBotJoinServer = discord.Embed(
        title="Welcome to ProductivityBot", colour = discord.Colour.random())
  embedBotJoinServer.add_field(name="First-time setup", value="Text and voice channels have been added")
  embedBotJoinServer.set_footer(text='Use channels #study-timers and #ProductivityTimer to make use of the time logging!')
  await ctx.system_channel.send(content = None, embed = embedBotJoinServer)
  print("First-time setup sent")
#All Commands reside below this comment


async def on_message(ctx):
    if ctx.author == bot.user:
        return

@bot.command()
async def help(ctx):
    embedHelp = discord.Embed(
    title="How to use the Productivity Bot", 
    description="Some useful commands",
    colour=discord.Colour.blue())
    embedHelp.add_field(name="$startwatch", value="Starts Stopwatch")
    embedHelp.add_field(name="$stopwatch", value="Ends Stopwatch")
    embedHelp.add_field(name="$todos", value="Personal Todo List \n $todos add (name) \n $todos remove (number)\n $todos clear" ,inline=True)
    embedHelp.add_field(name="$hw", value="Server Todo List \n $hw add (name) \n $hw remove (number) \n $hw clear")
    await ctx.channel.send(content=None, embed=embedHelp)

@bot.command()
async def startwatch(ctx):
    timerAuthor = str(ctx.author.id)
    user = await bot.fetch_user(timerAuthor)
    if timerAuthor in allTimer:
      embedStartwatch = discord.Embed(
      title="❌ "+ "You still have an active stopwatch running", description="Unable to start more than one stopwatch",
      colour=discord.Colour.red())
      embedStartwatch.set_author(name=user, icon_url=user.avatar_url)
      await ctx.channel.send(content=None, embed=embedStartwatch)
    else:
      newTimer(timerAuthor)
      embedStartwatch = discord.Embed(
      title="<:datree:858669536885997588>"+ "Stopwatch started", 
      description="To end it, type $stopwatch",
      colour=discord.Colour.red())
      embedStartwatch.set_author(name=user, icon_url=user.avatar_url)
      await ctx.channel.send(content=None, embed=embedStartwatch)

@bot.command()
async def stopwatch(ctx):
    timerAuthor = str(ctx.author.id)
    user = await bot.fetch_user(timerAuthor)
    embedStopwatch = discord.Embed(title="<a:pogoslide:858669948880551966> " + "Time Spent: "+ stopTimer(timerAuthor),
    colour=discord.Colour.green())
    embedStopwatch.set_author(name=user, icon_url=user.avatar_url)
    embedStopwatch.set_footer(text= f"Good job! You have {pointsDisplayer(timerAuthor)} points!")
    await ctx.channel.send(content=None, embed=embedStopwatch)
  
@bot.command()
async def todos(ctx, *args):
    args = list(args)
    if len(args) == 0:
      authorSent = str(ctx.author.id)
      user = await bot.fetch_user(authorSent)
      if authorSent not in db.keys():
        addAllTodo(authorSent)
        embedTodos = discord.Embed(title="✅ "+ "Your Todo List has been created.", colour=discord.Colour.green())
        embedTodos.set_footer(text="This applies to first time users only")
        #json.dump(allTodo, open("todolist.txt",'w'))

        await ctx.send(content=None, embed=embedTodos)
      else:
        #json.dump(allTodo, open("todolist.txt",'w'))
        embedTodos = discord.Embed(title="📝 "+ "Your Todo List", description=authorTodo(authorSent), colour = discord.Colour.random())
        embedTodos.set_author(name=user, icon_url=user.avatar_url)
        await ctx.send(content=None, embed=embedTodos)
      #Individual Todo Lists

    elif args[0] == "add":
      cmd = ''
      args.pop(0)
      for arg in args:
        cmd += ' ' + arg
      authorSent = str(ctx.author.id) #Who Sent It
      user = await bot.fetch_user(authorSent)
      #ensure that a key is created for each user
      if authorSent not in db.keys():
        addAllTodo(authorSent)
        editAllTodo(authorSent, cmd)
        #json.dump(allTodo, open("todolist.txt",'w')) // If you use a text file
        embedTodosAdd = discord.Embed(title = "✅ Added "+ '"'+cmd+'"', colour=discord.Colour.green())


        embedTodosAdd.set_author(name=user, icon_url=user.avatar_url)


        await ctx.send(embed=embedTodosAdd, content = None)

        embedTodos = discord.Embed(title="📝 "+ "Your Todo List", description=authorTodo(authorSent), colour=discord.Colour.random())
        await ctx.send(content=None, embed=embedTodos)

      else:

        editAllTodo(authorSent, cmd)
        #json.dump(allTodo, open("todolist.txt",'w')) // If you use a text file
        embedTodosAdd = discord.Embed(title = "✅ Added "+ '"'+cmd+'"', colour=discord.Colour.green())


        embedTodosAdd.set_author(name=user, icon_url=user.avatar_url)


        await ctx.send(embed=embedTodosAdd, content = None)

        embedTodos = discord.Embed(title="📝 "+ "Your Todo List", description=authorTodo(authorSent), colour = discord.Colour.random())
        await ctx.send(content=None, embed=embedTodos)

    #todos remove
    elif args[0] == "remove":
      cmdremove = int(args[1])
      authorSent =  str(ctx.author.id) #Author ID
      user = await bot.fetch_user(authorSent) #Author Username
      #get rid of $todos remove in the string
      # Read what is about to be removed from the Todo list
      aboutToRemove = db[authorSent][(cmdremove-1)]
      removeTodo(authorSent, cmdremove)
      #json.dump(allTodo, open("todolist.txt",'w')) // If you use a text file
      embedTodosRemove = discord.Embed(title =f"❌ Removed '{aboutToRemove}'", colour=discord.Colour.red())


      embedTodosRemove.set_author(name=user, icon_url=user.avatar_url)

      #async send back message
      await ctx.channel.send(embed=embedTodosRemove, content = None)

      embedTodos = discord.Embed(title="📝 "+ "Your Todo List", description=authorTodo(authorSent), colour=discord.Colour.random())
      await ctx.channel.send(content=None, embed=embedTodos)

      
    elif args[0] == 'clear':
      authorSent =  str(ctx.author.id) #Author ID
      user = await bot.fetch_user(authorSent)
      removeAllTodo(authorSent)
      embedClearedTodo = discord.Embed(title="✅ Your Todo List has been cleared", colour=discord.Colour.green())
      await ctx.channel.send(content=None, embed=embedClearedTodo)


#In this case, variable user refers to ther server name instead of user name
#userAdded stands for who added to the server's todo list
#authorAdded stands for ID of person that added to the server's todo list
#authorSent remains as server ID
@bot.command()
async def hw(ctx, *args):
    args = list(args)
    if len(args) == 0:
      authorSent = str(ctx.guild.id)
      user = ctx.guild.name
      if authorSent not in db.keys():
        addAllTodo(authorSent)
        embedTodos = discord.Embed(title=f"✅ {user}'s Todo List has been created", colour=discord.Colour.green())
        embedTodos.set_footer(text="This applies to first time users only")
        #json.dump(allTodo, open("todolist.txt",'w'))

        await ctx.send(content=None, embed=embedTodos)
      else:
        #json.dump(allTodo, open("todolist.txt",'w'))
        embedTodos = discord.Embed(title=f"📝 {user}'s Todo List", description=authorTodo(authorSent), colour = discord.Colour.random())
        await ctx.send(content=None, embed=embedTodos)
      #Individual Todo Lists

    elif args[0] == "add":
      cmd = ''
      args.pop(0)
      for arg in args:
        cmd += ' ' + arg
      authorSent = str(ctx.guild.id) #Guild 
      authorAdded = str(ctx.author.id) #Who used the command
      user = ctx.guild.name #Server Name
      userAdded = await bot.fetch_user(authorAdded) #Who Added to Server List
      #ensure that a key is created for each user
      if authorSent not in db.keys():
        addAllTodo(authorSent)
        editAllTodo(authorSent, cmd)
        #json.dump(allTodo, open("todolist.txt",'w')) // If you use a text file
        embedTodosAdd = discord.Embed(title = "✅ Added "+ '"'+cmd+'"', colour=discord.Colour.green())

        embedTodosAdd.set_author(name=userAdded, icon_url=userAdded.avatar_url)
        await ctx.send(embed=embedTodosAdd, content = None)

        embedTodos = discord.Embed(title=f"📝 {user}'s Todo List", description=authorTodo(authorSent), colour=discord.Colour.random())
        await ctx.send(content=None, embed=embedTodos)

      else:

        editAllTodo(authorSent, cmd)
        #json.dump(allTodo, open("todolist.txt",'w')) // If you use a text file
        embedTodosAdd = discord.Embed(title = "✅ Added "+ '"'+cmd+'"', colour=discord.Colour.green())

        embedTodosAdd.set_author(name=userAdded, icon_url=userAdded.avatar_url)
        await ctx.send(embed=embedTodosAdd, content = None)

        embedTodos = discord.Embed(title=f"📝 {user}'s Todo List", description=authorTodo(authorSent), colour=discord.Colour.random())
        await ctx.send(content=None, embed=embedTodos)

    #todos remove
    elif args[0] == "remove":
      cmdremove = int(args[1])
      userSent = str(ctx.author.id)
      authorSent = str(ctx.guild.id)  #Author ID
      user = ctx.guild.name
      author2 = await bot.fetch_user(userSent)  #Author Username
      #get rid of $todos remove in the string
      global whatWasRemoved
      # Read what is about to be removed from the Todo list
      aboutToRemove = db[authorSent][(cmdremove-1)]
      removeTodo(authorSent, cmdremove)
      #json.dump(allTodo, open("todolist.txt",'w')) // If you use a text file
      embedTodosRemove = discord.Embed(title = f"❌ Removed '{aboutToRemove}'", colour=discord.Colour.red())


      embedTodosRemove.set_author(name=author2, icon_url=author2.avatar_url)

      #async send back message
      await ctx.channel.send(embed=embedTodosRemove, content = None)

      embedTodos = discord.Embed(title=f"📝 {user}'s Todo List", description=authorTodo(authorSent), colour=discord.Colour.random())
      await ctx.channel.send(content=None, embed=embedTodos)

      
    elif args[0] == 'clear':
      authorSent = str(ctx.guild.id) #Server ID
      authorCleared = str(ctx.author.id) #User ID
      user = ctx.guild.name #username
      userCleared = await bot.fetch_user(authorCleared) #Server name
      removeAllTodo(authorSent)
      embedClearedTodo = discord.Embed(title=f"✅ {user}'s Todo List has been cleared", colour=discord.Colour.green())
      embedClearedTodo.set_author(name=userCleared, icon_url=userCleared.avatar_url)
      await ctx.channel.send(content=None, embed=embedClearedTodo)
    
#json.dump(allTodo, open("todolist.txt",'w')) // If you use a text file
    #@bot.command()
    #FIRST TIME SETUP: Setting Study Voice channel
    #async def set(ctx,*args):
    #if len(args) == 0:
    #await 
    #
# Under Development - Voice Channel Logging
@bot.event
async def on_voice_state_update(member, before, after):
    studyChannel = discord.utils.get(member.guild.channels, name='study-timers')
    studyVoiceChannel = discord.utils.get(member.guild.channels, name='ProductivityTimer')
    if before.channel is None and after.channel is not None:
      if after.channel == studyVoiceChannel:
        memberVoiceID = str(member.id)
        user = await bot.fetch_user(memberVoiceID)
        newTimer(memberVoiceID)
        embedStartwatch = discord.Embed(
        title="<:datree:858669536885997588>"+ "Timer started", 
        description="To end it, leave the ProductivityTimer call",
        colour=discord.Colour.red())
        embedStartwatch.set_author(name=user, icon_url=user.avatar_url)
        await studyChannel.send(content=None, embed=embedStartwatch)
    if before.channel is not None and after.channel is None:
      if before.channel == studyVoiceChannel:
        memberVoiceID = str(member.id)
        user = await bot.fetch_user(memberVoiceID)
        embedStopwatch = discord.Embed(title="<a:pogoslide:858669948880551966> " + "Time Spent: "+ stopTimer(memberVoiceID),
        colour=discord.Colour.green())
        embedStopwatch.set_author(name=user, icon_url=user.avatar_url)
        embedStopwatch.set_footer(text= f"Good job! You have {pointsDisplayer(memberVoiceID)} points")
        await studyChannel.send(content=None, embed=embedStopwatch)

@bot.command()
async def remindme(ctx,*args):
  remindUser = bot.get_user(int(ctx.author.id))
  cmd = ''
  for arg in args:
    cmd += ' ' + arg
  cmdList = cmd.split()
  timeSet = cmdList.pop(-1)
  if 's' in timeSet:
    remindTime = timeSet.replace('s','')
  elif 'm' in timeSet:
    remindTime = timeSet.replace('m','')
    remindTime = remindTime * 60
  elif 'h' in timeSet:
    remindTime = timeSet.replace('s','')
    remindTime = remindTime * 60 * 60
  elif 'd' in timeSet:
    remindTime = timeSet.replace('d','')
    remindTime = remindTime * 60 * 24
  cmd = cmd[:(len(cmd)-len(timeSet))]
  remindTime = int(remindTime)
  await ctx.send('Reminder set')
  await asyncio.sleep(remindTime)
  await remindUser.send(f'Reminder: {cmd}')



@bot.command()
async def alertmsg(ctx,*args):
  cmd = ''
  for arg in args:
    cmd += ' ' + arg
  if ctx.author.id != 662496683451613204: #This is to allow me (or anyone using running this bot locally) to send alert messages! 
    pass
  else:
    for guild in bot.guilds:
        for channel in guild.channels:
            if(channel.name == guild.system_channel):
                await channel.send(cmd)
            elif (channel.name == 'study-timers'):
              await channel.send(cmd)
            elif channel.name == 'general':
              await channel.send(cmd)

bot.run(os.getenv('TOKEN'))
#you can name the Secret/.env anything you want just replace TOKEN with (name)