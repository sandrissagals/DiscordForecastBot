from bs4 import BeautifulSoup 
import requests 
import asyncio  
import discord  
import json 
from datetime import date

#Unique token for the bot
token = ""
client = discord.Client()   

#Code for scraping the webpage, returns a BS object
def scrape(URL): 
    page = requests.get(URL) 
    soup = BeautifulSoup(page.content, "html.parser") 
    return soup 

#get_forcast, returns Todays forcast as a dictionary 
def get_forecast(day): 
    soup = scrape("https://www.timeanddate.com/weather/latvia/riga/ext") 
    #Gets a certain days forcast
    table = soup.find('tbody').find_all('tr')[day] 
    #creates a list of data
    data = table.find_all('td') 
    #extracts data from the list and stores it in a dictionary  
    forcast = {"Temperature": data[1].text.replace(u'\xa0',''), "Weather": data[2].text, "Feels Like": data[3].text.replace(u'\xa0',''), "Wind Speed": data[4].text, "Wind Direction": data[5].span.get('title',''), "Humidity": data[6].text, "Chance": data[7].text, "Amount": data[8].text} 
    return forcast

#Why?
def writeToJson(forecast):
    #Reading Json data
    file = open("./weather.json","r",encoding='UTF-8') 
    data = json.load(file) 
    print(data)
    file.close() 
    
    #Appending and writing json data
    file = open("./weather.json","w",encoding='UTF-8') 
    today = str(date.today()) 
    print(today)
    data[today] = forecast
    json.dump(data,file,indent=4) 
    file.close()  
    

#When somone on discord posts a message that starts with $forecast it replies with the weather forcast for that day
@client.event
async def on_message(message): 
    #if the author is the bot don't check the message
    if message.author == client.user:
        return 
    elif message.content.startswith('$forecast'):
        forecast = get_forecast(0) 
        #Sends the message
        await message.channel.send(f'Temperature: {forecast["Temperature"]}, Weather:{forecast["Weather"]}, Feels Like:{forecast["Feels Like"]}, Wind Speed:{forecast["Wind Speed"]}, Wind Direction:{forecast["Wind Direction"]}, Humidity:{forecast["Humidity"]}, Chance:{forecast["Chance"]}, Amount:{forecast["Amount"]}')
        writeToJson(forecast)


client.run(token)