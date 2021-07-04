from sqlitedict import SqliteDict
#Testing sqlitedict
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

#allTodo = json.load(open("todolist.txt"))
db = SqliteDict('./my_db.sqlite', autocommit=True)
allTimer = {}
#allTimer = json.load(open("timerdebugger.txt")) // Used to debug time.time() differences


#Functions

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
    print(authorReturn)
  return authorReturn

def removeTodo(theID, removeIndex):
  db[theID].pop((removeIndex-1))
  
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
  embedBotJoinServer = discord.Embed(
        title="Welcome to ProductivityBot", colour = discord.Colour.random())
  embedBotJoinServer.add_field(name="First-time setup", value="Created channel ProductivityTimer to the server")
  embedBotJoinServer.set_footer(text='Join the channel to use the time logger')
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
    embedStopwatch.set_footer(text= "Good job!")
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
      global whatWasRemoved
      # Read what is about to be removed from the Todo list
      aboutToRemove = db[authorSent][(cmdremove-1)]
      removeTodo(authorSent, cmdremove)
      #json.dump(allTodo, open("todolist.txt",'w')) // If you use a text file
      embedTodosRemove = discord.Embed(title = "❌ Removed "+ '"'+aboutToRemove+'"', colour=discord.Colour.red())


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
      author2 = await bot.fetch_user(authorSent)  #Author Username
      #get rid of $todos remove in the string
      global whatWasRemoved
      # Read what is about to be removed from the Todo list
      aboutToRemove = db[authorSent][(cmdremove-1)]
      removeTodo(authorSent, cmdremove)
      #json.dump(allTodo, open("todolist.txt",'w')) // If you use a text file
      embedTodosRemove = discord.Embed(title = "❌ Removed "+ '"'+aboutToRemove+'"', colour=discord.Colour.red())


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
    if before.channel is None and after.channel is not None:
        vcName = bot.get_channel(after.channel.id)
        await member.guild.system_channel.send(f"{member} Joined {vcName}")
        members = vcName.members #finds members connected to the channel

        usersInCall = [] #(list)
        for member in members:
          usersInCall.append(member.id)

          print(f"{member} joined {vcName}") #print info
    if before.channel is not None and after.channel is None:
        vcName = bot.get_channel(before.channel.id)
        await member.guild.system_channel.send(f"{member} left {vcName}")
        members = vcName.members #finds members connected to the channel
        usersRemaining = []
        for member in members:
          usersRemaining.append(member.id)
          print(f"{member} left {vcName}") #print info


keep_alive()
bot.run(os.getenv('TOKEN'))
#you can name the Secret/.env anything you want just replace TOKEN with (name)