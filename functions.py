#For development purposes
#Not in use 



def newTimer(theID):
  allTimer[theID] = time.time()
  return 'Starting Stopwatch: ' + str(theID)

def stopTimer(theID):
  ending = time.time()
  starting = float(allTimer[theID])
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
  global exportSeconds
  mins = sec // 60
  second = sec % 60
  second = int(second)
  mins = mins % 60
  if second < 60:
    endedTime = str(int(second))+ "s"

    exportSeconds = second

  else:
    endedTime =str(int(mins)) + "min" + " " + str(int(second))+ "s"

    exportSeconds = second

  return endedTime