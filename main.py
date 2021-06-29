from keep_alive import keep_alive
import discord
import os
import time
import json
#Made by @toasterclock
client = discord.Client()

allTodo = json.load(open("todolist.txt"))
allTimer = {}
#allTimer = json.load(open("timerdebugger.txt"))
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
  print(realEndTime) #Debugging realendtime
  return realEndTime


def addAllTodo(theID):
  allTodo[theID] = ''
  return 'Added'

def editAllTodo(theID, addTodoItem):
  allTodo[theID] += "● " + addTodoItem + '\n'
  authorTodo(theID)
  return authorTodo(theID)

def authorTodo(theID):
  return allTodo[theID]


def removeTodo(theID, removeIndex):
  rearrangeTodo = allTodo[theID].replace(" ", "%").split()
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
  allTodo[theID] = rearrangeTodo
 
def removeAllTodo(theID):
  allTodo[theID] = ''
  json.dump(allTodo, open("todolist.txt",'w'))

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


@client.event
async def on_ready():
    print('Connection successful,  {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return



    if message.content == "$help":
        embedHelp = discord.Embed(
        title="How to use the Productivity Bot", 
        description="Some useful commands",
        colour=discord.Colour.blue())
        embedHelp.add_field(name="$startwatch", value="Starts Stopwatch")
        embedHelp.add_field(name="$stopwatch", value="Ends Stopwatch")
        embedHelp.add_field(name="$todos", value="Your very own personal todo list. Use $todos add (name) and $todos remove (name)" ,inline=True)
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
      if authorSent not in allTodo:
        addAllTodo(authorSent)
        embedTodos = discord.Embed(title="✅ "+ "Your Todo List has been created.")
        embedTodos.set_footer(text="This applies to first time users only")
        json.dump(allTodo, open("todolist.txt",'w'))
        

        await message.channel.send(content=None, embed=embedTodos)
      else:
        json.dump(allTodo, open("todolist.txt",'w'))
        embedTodos = discord.Embed(title="📝 "+ "Your Todo List", description=authorTodo(authorSent))
        embedTodos.set_author(name=user, icon_url=user.avatar_url)
        await message.channel.send(content=None, embed=embedTodos)
        

    if message.content.startswith("$todos add"):
      cmd = message.content[11:]
      #Who Sent This?
      authorSent = str(message.author.id)
      user = await client.fetch_user(authorSent)
      #ensure that a key is created for each user
      if authorSent not in allTodo:
        addAllTodo(authorSent)
        editAllTodo(authorSent, cmd)
        json.dump(allTodo, open("todolist.txt",'w'))
        embedTodosAdd = discord.Embed(title = "✅ Added "+ '"'+cmd+'"')


        embedTodosAdd.set_author(name=user, icon_url=user.avatar_url)


        await message.channel.send(embed=embedTodosAdd, content = None)

        embedTodos = discord.Embed(title="📝 "+ "Your Todo List", description= authorTodo(authorSent))
        await message.channel.send(content=None, embed=embedTodos)

      else:

        editAllTodo(authorSent, cmd)
        json.dump(allTodo, open("todolist.txt",'w'))
        embedTodosAdd = discord.Embed(title = "✅ Added "+ '"'+cmd+'"')


        embedTodosAdd.set_author(name=user, icon_url=user.avatar_url)


        await message.channel.send(embed=embedTodosAdd, content = None)

        embedTodos = discord.Embed(title="📝 "+ "Your Todo List", description=authorTodo(authorSent))
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
      #Save to todolist.txt
      json.dump(allTodo, open("todolist.txt",'w'))
      embedTodosRemove = discord.Embed(title = "❌ Removed "+ '"'+aboutToRemove+'"')


      embedTodosRemove.set_author(name=user, icon_url=user.avatar_url)

      #async send back message
      await message.channel.send(embed=embedTodosRemove, content = None)

      embedTodos = discord.Embed(title="📝 "+ "Your Todo List", description=authorTodo(authorSent))
      await message.channel.send(content=None, embed=embedTodos)
    if message.content.lower() == "$todos clear":
      authorSent =  str(message.author.id) #Author ID
      user = await client.fetch_user(authorSent)
      removeAllTodo(authorSent)
      embedClearedTodo = discord.Embed(title="✅ Your Todo List has been cleared")
      await message.channel.send(content=None, embed=embedClearedTodo)


        

json.dump(allTodo, open("todolist.txt",'w'))

  
keep_alive()
client.run(os.getenv('TOKEN'))