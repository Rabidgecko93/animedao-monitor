from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
from colorama import Fore, init
from discord.ext import commands
import datetime
import discord
import asyncio
import requests
import pyimgur
import sys
import os

bot = commands.Bot(command_prefix='!')

options = webdriver.ChromeOptions()
#options.headless = True
options.add_argument("--log-level=3")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36")
driver = webdriver.Chrome(options=options)
os.system('cls')

CLIENT_ID = "" # <-- imgur client ID

async def background_task():
        await bot.wait_until_ready()
        lastanime = "haha"
        while True:
                try:
                        epnum = "N/A"
                        animetitle = "N/A"
                        animeepisodename = "N/A"
                        animelink = "N/A"
                        animeimage = "N/A"
                        driver.execute_script("window.open('https://animedao.to/')")
                        driver.switch_to.window(driver.window_handles[1])
                        await asyncio.sleep(10)
                        wellhtml = driver.find_elements_by_xpath("//div[@class='well']") 
                        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                        await asyncio.sleep(2)
                        while True:
                            try:
                                #print("hi")
                                current = wellhtml[0].get_attribute('innerHTML')
                                #print("current: " + current)
                                try:
                                    epnum = current.split('Episode ')[1].split('"')[0]
                                except:
                                    pass
                                try:
                                    animetitle = current.split('class="latest-parent" title="')[1].split('"')[0]
                                except:
                                    pass
                                try:
                                    animeepisodename = current.split('class="latestanime-subtitle" title="')[1].split('"')[0]
                                except:
                                    pass
                                try:
                                    animeimage = "https://animedao.to" + current.split('img src="')[1].split('"')[0]
                                except:
                                    pass
                                try:
                                    animelink = "https://animedao.to" + current.split('href="')[1].split('"')[0]
                                except:
                                    pass
                                channel = bot.get_channel() # <-- channel ID
                                if lastanime != animetitle:
                                        #print("anime#: " + epnum)
                                        #print("animetitle: " + animetitle)
                                        #print("animeepisodename: " + animeepisodename)
                                        #print("animelink: " + animelink)
                                        #print("animeimage: " + animeimage)
                                        print("\n" + animetitle + " - Episode " + epnum + "\n" + animeepisodename + " - " + animelink)
                                        #await channel.send("<@140720684417417217>")
                                        #print("Saving image ...")
                                        driver.get(animeimage)
                                        await asyncio.sleep(3)
                                        with open('anime.png', 'wb') as file:
                                            file.write(driver.find_element_by_xpath('/html/body/img').screenshot_as_png)
                                        #print("Saved!")
                                        im = pyimgur.Imgur(CLIENT_ID)
                                        uploaded_image = im.upload_image('C:/Users/Administrator/Desktop/anime.png', title="shdwbot - " + animetitle)
                                        #print(uploaded_image.link)
                                        embed=discord.Embed(title="New episode of " + animetitle + "!", timestamp=datetime.datetime.utcnow(), url=animelink, description="*" + animetitle + "*\nEpisode " + epnum + " - " + animeepisodename + "\n" + animelink, color=discord.Color.green()).set_thumbnail(url=uploaded_image.link)
                                        embed.set_footer(text="shdw's animedao monitor", icon_url="https://i.imgur.com/m8Fg9HI.png")
                                        await channel.send(embed=embed)
                                        print("Discord embed sent!")
                                        lastanime = animetitle
                                driver.close()
                                driver.switch_to.window(driver.window_handles[-1])
                                await asyncio.sleep(300)
                                break
                            except:
                                driver.close()
                                driver.switch_to.window(driver.window_handles[-1])
                                break
                            
                        
                except Exception as e:
                        print(e)

@bot.event
async def on_ready():
        print("now watching animedao.to")
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="animedao.to"))

bot.loop.create_task(background_task())

bot.run('') #<-- bot token
