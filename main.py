from keep_alive import keep_alive
import discord
import os
import time
client = discord.Client()

todolist = []

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

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith("$startwatch"):
      global start_time
      global end_time
      await message.channel.send('Starting stopwatch')
      start_time = time.time()
    if message.content.startswith("$stopwatch"):

      end_time = time.time()
      time_lapsed = end_time - start_time
      time_convert(time_lapsed)
      await message.channel.send("Time spent: " + time_convert(time_lapsed))

  

keep_alive()
client.run(os.getenv('TOKEN'))