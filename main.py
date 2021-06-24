from keep_alive import keep_alive
import discord
import os
import time
import json

client = discord.Client()

allTodo = {}
allTimer = {}
yourLastTimings = {}

def newTimer(theID):
  allTimer[theID] = time.time()
  return 'Starting Stopwatch: ' + str(theID)

def stopTimer(theID):
  ending = time.time()
  starting = allTimer[theID]
  endTime = ending - starting
  realEndTime = time_convert(endTime)
  allTimer[theID] = realEndTime
  return allTimer[theID]


def addPeopleToDo(theID):
  allTodo[theID] = ''
  return 'Added'

def editPeopleList(theID, addTodoItem):
  allTodo[theID] += addTodoItem + '\n'
  listPeopleList(theID)
  return listPeopleList(theID)

def listPeopleList(theID):
  return "Your To Do List: " + '\n' + allTodo[theID]

second = 0
#time lapse shi
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

    if message.content.startswith('$ping'):
        await message.channel.send('i am still alive')

    if message.content.startswith("$startwatch"):
      whoTimedThis = message.author.id
      await message.channel.send('Starting stopwatch')
      newTimer(whoTimedThis)
    if message.content.startswith("$stopwatch"):
      whoTimedThis = message.author.id
      stopTimer(whoTimedThis)
      await message.channel.send("Time spent: " + allTimer[whoTimedThis])
    
    if message.content.startswith("$todos"):
      whoSentThis = message.author.id
      if whoSentThis not in allTodo:
        addPeopleToDo(whoSentThis)
        await message.channel.send("(For first time users) Creating your todo list. ")
      else:
        whoSentThis = message.author.id
        await message.channel.send(listPeopleList(whoSentThis))

    if message.content.startswith("$todos add"):
      cmd = message.content[10:]
      print(cmd)
      whoSentThis = message.author.id
      if whoSentThis not in allTodo:
        addPeopleToDo(whoSentThis)
        editPeopleList(whoSentThis, cmd)
        json.dump(allTodo, open("todolist.txt",'w'))
        await message.channel.send("Added: " + cmd)
        await message.channel.send(listPeopleList(whoSentThis))
      else:
        editPeopleList(whoSentThis, cmd)
        await message.channel.send("Added: " + cmd)
        json.dump(allTodo, open("todolist.txt",'w'))
        await message.channel.send(listPeopleList(whoSentThis))
    
        

json.dump(allTodo, open("todolist.txt",'w'))

  
keep_alive()
client.run(os.getenv('TOKEN'))