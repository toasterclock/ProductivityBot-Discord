from replit import db
#Testing Replit DB but any obviously you can use any DB of your choice or just simply use a .txt file like i did
from keep_alive import keep_alive
import discord
import os
import time
#import json
#Made by @toasterclock
client = discord.Client()

#allTodo = json.load(open("todolist.txt"))
allTimer = {}
#allTimer = json.load(open("timerdebugger.txt")) // Used to debug time.time() differences
#yourLastTimings = {} (NOT IN USE)

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
  db[theID] = ''
  return 'Added'

def editAllTodo(theID, addTodoItem):
  db[theID] += "● " + addTodoItem + '\n'
  authorTodo(theID)
  return authorTodo(theID)

def authorTodo(theID):
  return db[theID]


def removeTodo(theID, removeIndex):
  rearrangeTodo = db[theID].replace(" ", "%").split()
  #Split into list items + replace spaces with percentage sign so that spaced words dont get split apart?
  global whatWasRemoved
  removeIndex -= 1
  removeTodo.whatWasRemoved = rearrangeTodo[removeIndex].replace("%", " ")
  rearrangeTodo.pop(removeIndex)
  rearrangeTodo = str(rearrangeTodo)
  rearrangeTodo = rearrangeTodo.replace('[','')
  rearrangeTodo = rearrangeTodo.replace("'",'')
  rearrangeTodo = rearrangeTodo.replace(',','\n')
  rearrangeTodo = rearrangeTodo.replace(']','')
  rearrangeTodo = rearrangeTodo.replace(' ','')
  rearrangeTodo = rearrangeTodo.replace('%',' ')
  db[theID] = rearrangeTodo
 
def removeAllTodo(theID):
  db[theID] = ''
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
@client.event
async def on_ready():
    print('Connection successful,  {0.user}'.format(client))

#All Commands reside below this comment
@client.event
async def on_message(message):
    if message.author == client.user:
        return



    if message.content.lower() == "$help":
        embedHelp = discord.Embed(
        title="How to use the Productivity Bot", 
        description="Some useful commands",
        colour=discord.Colour.blue())
        embedHelp.add_field(name="$startwatch", value="Starts Stopwatch")
        embedHelp.add_field(name="$stopwatch", value="Ends Stopwatch")
        embedHelp.add_field(name="$todos", value="$todos add (name) \n $todos remove (number)\n $todos clear" ,inline=True)
        embedHelp.add_field(name="$hw", value="$hw add (name) \n $hw remove (number) \n $hw clear")
        embedHelp.set_footer(text='Enjoy your stay!')
        await message.channel.send(content=None, embed=embedHelp)

    if message.content.startswith("$startwatch"):
        timerAuthor = str(message.author.id)
        user = await client.fetch_user(timerAuthor)
        if timerAuthor in allTimer:
          embedStartwatch = discord.Embed(
          title="❌ "+ "You still have an active stopwatch running", description="Unable to start more than one stopwatch",
          colour=discord.Colour.red())
          embedStartwatch.set_author(name=user, icon_url=user.avatar_url)
          await message.channel.send(content=None, embed=embedStartwatch)
        else:
          newTimer(timerAuthor)

          embedStartwatch = discord.Embed(
          title="<:datree:858669536885997588>"+ "Stopwatch started", 
          description="To end it, type $stopwatch",
          colour=discord.Colour.red())
          embedStartwatch.set_author(name=user, icon_url=user.avatar_url)

          await message.channel.send(content=None, embed=embedStartwatch)

    if message.content.startswith("$stopwatch"):

      timerAuthor = str(message.author.id)
      user = await client.fetch_user(timerAuthor)
      embedStopwatch = discord.Embed(title="<a:pogoslide:858669948880551966> " + "Time Spent: "+ stopTimer(timerAuthor),
      colour=discord.Colour.green())
      embedStopwatch.set_author(name=user, icon_url=user.avatar_url)
      embedStopwatch.set_footer(text= "Good job!")
      await message.channel.send(content=None, embed=embedStopwatch)
      
    if message.content.lower() == '$todos':
      authorSent = str(message.author.id)
      user = await client.fetch_user(authorSent)
      if authorSent not in db.keys():
        addAllTodo(authorSent)
        embedTodos = discord.Embed(title="✅ "+ "Your Todo List has been created.", colour=discord.Colour.green())
        embedTodos.set_footer(text="This applies to first time users only")
        #json.dump(allTodo, open("todolist.txt",'w'))
        

        await message.channel.send(content=None, embed=embedTodos)
      else:
        #json.dump(allTodo, open("todolist.txt",'w'))
        embedTodos = discord.Embed(title="📝 "+ "Your Todo List", description=authorTodo(authorSent), colour = discord.Colour.random())
        embedTodos.set_author(name=user, icon_url=user.avatar_url)
        await message.channel.send(content=None, embed=embedTodos)
        
    #Individual Todo Lists
    if message.content.startswith("$todos add"):
      cmd = message.content[11:]
      #Who Sent This?
      authorSent = str(message.author.id)
      user = await client.fetch_user(authorSent)
      #ensure that a key is created for each user
      if authorSent not in db.keys():
        addAllTodo(authorSent)
        editAllTodo(authorSent, cmd)
        #json.dump(allTodo, open("todolist.txt",'w')) // If you use a text file
        embedTodosAdd = discord.Embed(title = "✅ Added "+ '"'+cmd+'"', colour=discord.Colour.green())


        embedTodosAdd.set_author(name=user, icon_url=user.avatar_url)


        await message.channel.send(embed=embedTodosAdd, content = None)

        embedTodos = discord.Embed(title="📝 "+ "Your Todo List", description=authorTodo(authorSent), colour=discord.Colour.random())
        await message.channel.send(content=None, embed=embedTodos)

      else:

        editAllTodo(authorSent, cmd)
        #json.dump(allTodo, open("todolist.txt",'w')) // If you use a text file
        embedTodosAdd = discord.Embed(title = "✅ Added "+ '"'+cmd+'"', colour=discord.Colour.green())


        embedTodosAdd.set_author(name=user, icon_url=user.avatar_url)


        await message.channel.send(embed=embedTodosAdd, content = None)

        embedTodos = discord.Embed(title="📝 "+ "Your Todo List", description=authorTodo(authorSent), colour = discord.Colour.random())
        await message.channel.send(content=None, embed=embedTodos)

    #todos remove
    if message.content.startswith('$todos remove'):
      authorSent =  str(message.author.id) #Author ID
      user = await client.fetch_user(authorSent) #Author Username
      #get rid of $todos remove in the string
      cmdremove = message.content[14:]
      global whatWasRemoved
      # Read what is about to be removed from the Todo list
      removeTodo(authorSent, int(cmdremove))
      aboutToRemove = removeTodo.whatWasRemoved
      #json.dump(allTodo, open("todolist.txt",'w')) // If you use a text file
      embedTodosRemove = discord.Embed(title = "❌ Removed "+ '"'+aboutToRemove+'"', colour=discord.Colour.red())


      embedTodosRemove.set_author(name=user, icon_url=user.avatar_url)

      #async send back message
      await message.channel.send(embed=embedTodosRemove, content = None)

      embedTodos = discord.Embed(title="📝 "+ "Your Todo List", description=authorTodo(authorSent), colour=discord.Colour.random())
      await message.channel.send(content=None, embed=embedTodos)
    if message.content.lower() == "$todos clear":
      authorSent =  str(message.author.id) #Author ID
      user = await client.fetch_user(authorSent)
      removeAllTodo(authorSent)
      embedClearedTodo = discord.Embed(title="✅ Your Todo List has been cleared", colour=discord.Colour.green())
      await message.channel.send(content=None, embed=embedClearedTodo)


    # Server List
    if message.content.lower() == "$hw":
      authorSent = str(message.guild.id)
      if authorSent not in db.keys():
        addAllTodo(authorSent)
        embedTodos = discord.Embed(title="✅ "+ "Server Todo List has been created", colour=discord.Colour.green())
        embedTodos.set_footer(text="This applies to first time users only")
        #json.dump(allTodo, open("todolist.txt",'w'))
        

        await message.channel.send(content=None, embed=embedTodos)
      else:
        #json.dump(allTodo, open("todolist.txt",'w'))
        embedTodos = discord.Embed(title="📝 "+ "Server Todo List", description=authorTodo(authorSent), colour = discord.Colour.random())
        embedTodos.set_author(name=message.guild.name, icon_url=message.guild.icon_url)
        await message.channel.send(content=None, embed=embedTodos)
    
    if message.content.startswith("$hw add"):
      cmd = message.content[8:]
      #Who Sent This?
      authorSent = str(message.guild.id)
      #ensure that a key is created for each user
      if authorSent not in db.keys():
        addAllTodo(authorSent)
        editAllTodo(authorSent, cmd)
        #json.dump(allTodo, open("todolist.txt",'w')) // If you use a text file
        embedTodosAdd = discord.Embed(title = "✅ Added "+ '"'+cmd+'"', colour=discord.Colour.green())


        embedTodosAdd.set_author(name=message.guild.name, icon_url=message.guild.icon_url)


        await message.channel.send(embed=embedTodosAdd, content = None)

        embedTodos = discord.Embed(title="📝 "+ "Server Todo List", description=authorTodo(authorSent), colour=discord.Colour.random())
        await message.channel.send(content=None, embed=embedTodos)

      else:

        editAllTodo(authorSent, cmd)
        #json.dump(allTodo, open("todolist.txt",'w')) // If you use a text file
        embedTodosAdd = discord.Embed(title = "✅ Added "+ '"'+cmd+'"', colour=discord.Colour.green())


        embedTodosAdd.set_author(name=message.guild.name, icon_url=message.guild.icon_url)


        await message.channel.send(embed=embedTodosAdd, content = None)

        embedTodos = discord.Embed(title="📝 "+ "Server Todo List", description=authorTodo(authorSent), colour = discord.Colour.random())
        await message.channel.send(content=None, embed=embedTodos)

    if message.content.startswith('$hw remove'):
      authorSent = str(message.guild.id) #Server ID
      #get rid of $todos remove in the string
      cmdremove = message.content[11:]
      global whatWasRemoved
      # Read what is about to be removed from the Todo list
      removeTodo(authorSent, int(cmdremove))
      aboutToRemove = removeTodo.whatWasRemoved
      #json.dump(allTodo, open("todolist.txt",'w')) // If you use a text file
      embedTodosRemove = discord.Embed(title = "❌ Removed "+ '"'+aboutToRemove+'"', colour=discord.Colour.red())


      embedTodosRemove.set_author(name=message.guild.name, icon_url=message.guild.icon_url)

      #async send back message
      await message.channel.send(embed=embedTodosRemove, content = None)

      embedTodos = discord.Embed(title="📝 "+ "Server Todo List", description=authorTodo(authorSent), colour=discord.Colour.random())
      await message.channel.send(content=None, embed=embedTodos)

    if message.content.lower() == "$hw clear":
      authorSent =  str(message.guild.id) #Author ID
      removeAllTodo(authorSent)
      embedClearedTodo = discord.Embed(title="✅ Your Server's Todo List has been cleared", colour=discord.Colour.green())
      await message.channel.send(content=None, embed=embedClearedTodo)
#json.dump(allTodo, open("todolist.txt",'w')) // If you use a text file


# Under Development
@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        if after.channel.id == 857610586577436682:
          vcName = client.get_channel(857610586577436682)
          await member.guild.system_channel.send(f"User Joined {vcName}")
          members = vcName.members #finds members connected to the channel

          memids = [] #(list)
          for member in members:
            memids.append(member.id)

            print(memids) #print info
            await member.guild.system_channel.send(memids)
    if before.channel is not None and after.channel is None:
        if after.channel.id == 857610586577436682:
          vcName = client.get_channel(857610586577436682)
          await member.guild.system_channel.send(f"User Left {vcName}")
          members = vcName.members #finds members connected to the channel

          memids = [] #(list)
          for member in members:
            memids.append(member.id)

            print(memids) #print info
            await member.guild.system_channel.send(memids)
  
keep_alive()
client.run(os.getenv('TOKEN'))