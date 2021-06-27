
from keep_alive import keep_alive
import discord
import os
import time
import json
#Made by @toasterclock
client = discord.Client()

allTodo = json.load(open("todolist.txt"))
allTimer = {}
yourLastTimings = {}

#Functions

def newTimer(theID):
  allTimer[theID] = time.time()
  return 'Starting Stopwatch: ' + str(theID)

def stopTimer(theID):
  ending = time.time()
  starting = allTimer[theID]
  endTime = ending - starting
  realEndTime = time_convert(endTime)
  allTimer[theID] = realEndTime
  print(allTimer[theID])
  return allTimer[theID]


def addPeopleToDo(theID):
  allTodo[theID] = ''
  return 'Added'

def editPeopleList(theID, addTodoItem):
  allTodo[theID] += "● " + addTodoItem + '\n'
  listPeopleList(theID)
  return listPeopleList(theID)

def listPeopleList(theID):
  return allTodo[theID]


def removePeopleList(theID, removeIndex):
  todoSplit = allTodo[theID].replace(" ", "%").split()
  #Split into list items + replace spaces with percentage sign so that spaced words dont get split apart?
  global whatWasRemoved
  removeIndex -= 1
  removePeopleList.whatWasRemoved = todoSplit[removeIndex].replace("%", " ")
  todoSplit.pop(removeIndex)
  todoSplit = str(todoSplit)
  todoSplit = todoSplit.replace('[','')
  todoSplit = todoSplit.replace("'",'')
  todoSplit = todoSplit.replace(',','\n')
  todoSplit = todoSplit.replace(']','')
  todoSplit = todoSplit.replace(' ','')
  todoSplit = todoSplit.replace('%',' ')
  allTodo[theID] = todoSplit
  print(allTodo[theID])
 

second = 0
#stopwatch conversion
def time_convert(sec):
  mins = sec // 60
  second = sec % 60
  second = int(second)
  mins = mins % 60
  if second < 60:
    endedTime = str(int(second))+ "s"
  else:
    endedTime =str(int(mins)) + "min" + " " + str(int(second))+ "s"
  return endedTime


@client.event
async def on_ready():
    print('Connection successful,  {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
      print(message.author.id)

    if message.content == "$help":
        embedHelp = discord.Embed(
        title="Help", 
        description="Some useful commands",
        colour=discord.Colour.blue())
        embedHelp.add_field(name="$startwatch", value="Starts Stopwatch")
        embedHelp.add_field(name="$stopwatch", value="Ends Stopwatch")
        await message.channel.send(content=None, embed=embedHelp)

    if message.content.startswith("$startwatch"):

        whoTimedThis = message.author.id
        user = await client.fetch_user(whoTimedThis)

        newTimer(whoTimedThis)

        embedStartwatch = discord.Embed(
        title="<:datree:858669536885997588>"+ "Stopwatch started", 
        description="To end it, type $stopwatch",
        colour=discord.Colour.red())
        embedStartwatch.set_author(name=user, icon_url=user.avatar_url)

        await message.channel.send(content=None, embed=embedStartwatch)

    if message.content.startswith("$stopwatch"):

      whoTimedThis = message.author.id
      user = await client.fetch_user(whoTimedThis)


      stopTimer(whoTimedThis)

      embedStopwatch = discord.Embed(title="<a:pogoslide:858669948880551966> " + "Time Spent: "+ allTimer[whoTimedThis],
      colour=discord.Colour.green())
      embedStopwatch.set_author(name=user, icon_url=user.avatar_url)
      embedStopwatch.set_footer(text= "Good job!")
      await message.channel.send(content=None, embed=embedStopwatch)
      
    if message.content.lower() == '$todos':
      whoSentThis = str(message.author.id)
      if whoSentThis not in allTodo:
        addPeopleToDo(whoSentThis)
        embedTodos = discord.Embed(title="✅ "+ "Your Todo List has been created.")
        embedTodos.setFooter(text="This applies to first time users only")
        

        await message.channel.send(content=None, embed=embedTodos)
      else:
        embedTodos = discord.Embed(title="📝 "+ "Your Todo List", description=listPeopleList(whoSentThis))
        await message.channel.send(content=None, embed=embedTodos)
        

    if message.content.startswith("$todos add"):
      cmd = message.content[11:]
      print(cmd)
      #Who Sent This?
      whoSentThis = str(message.author.id)
      #ensure that a key is created for each user
      if whoSentThis not in allTodo:
        addPeopleToDo(whoSentThis)
        editPeopleList(whoSentThis, cmd)
        json.dump(allTodo, open("todolist.txt",'w'))
        await message.channel.send("Added: " + cmd)
        await message.channel.send(listPeopleList(whoSentThis))
      else:
        editPeopleList(whoSentThis, cmd)
        #return messages + save to todolist.txt
        await message.channel.send("Added: " + cmd)
        json.dump(allTodo, open("todolist.txt",'w'))
        await message.channel.send(listPeopleList(whoSentThis))

    #todos remove
    if message.content.startswith('$todos remove'):
      whoSentThis = str(message.author.id)
      #get rid of $todos remove in the string
      cmdremove = message.content[14:]
      print(cmdremove)
      global whatWasRemoved
      # Read what is about to be removed from the Todo list
      removePeopleList(whoSentThis, int(cmdremove))
      aboutToRemove = removePeopleList.whatWasRemoved
      #Save to todolist.txt
      json.dump(allTodo, open("todolist.txt",'w'))
      #return messages
      await message.channel.send("Removed: " + aboutToRemove)
      await message.channel.send(listPeopleList(whoSentThis))

        

json.dump(allTodo, open("todolist.txt",'w'))

  
keep_alive()
client.run(os.getenv('TOKEN'))