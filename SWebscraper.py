from bs4 import BeautifulSoup 
import requests 
import asyncio  
import discord  

#Unique token for the bot
token = ""
client = discord.Client()   

#Code for scraping the webpage, returns a BS object
def scrape(URL): 
    page = requests.get(URL) 
    soup = BeautifulSoup(page.content, "html.parser") 
    return soup 

#get_forcast, returns Todays forcast as a dictionary 
def get_forcast(day): 
    soup = scrape("https://www.timeanddate.com/weather/latvia/riga/ext") 
    #Gets a certain days forcast
    table = soup.find('tbody').find_all('tr')[day] 
    #creates a list of data
    data = table.find_all('td') 
    #extracts data from the list and stores it in a dictionary  
    forcast = {"Temperature": data[1].text.replace(u'\xa0',''), "Weather": data[2].text, "Feels Like": data[3].text.replace(u'\xa0',''), "Wind Speed": data[4].text, "Wind Direction": data[5].span.get('title',''), "Humidity": data[6].text, "Chance": data[7].text, "Amount": data[8].text} 
    return forcast

#When somone on discord posts a message that starts with $forecast it replies with the weather forcast for that day
@client.event
async def on_message(message): 
    #if the author is the bot don't check the message
    if message.author == client.user:
        return 
    elif message.content.startswith('$forecast'):
        forcast = get_forcast(0) 
        #Sends the message
        await message.channel.send(f'Temperature: {forcast["Temperature"]}, Weather:{forcast["Weather"]}, Feels Like:{forcast["Feels Like"]}, Wind Speed:{forcast["Wind Speed"]}, Wind Direction:{forcast["Wind Direction"]}, Humidity:{forcast["Humidity"]}, Chance:{forcast["Chance"]}, Amount:{forcast["Amount"]}') 

client.run(token)
