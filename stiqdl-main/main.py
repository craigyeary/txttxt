from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
import requests, sys
import json, base64
import subprocess
from pyrogram import Client, client,  filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
from pyrogram.types import Message
import pyrogram
from pyrogram import Client, filters
import tgcrypto
from subprocess import getstatusoutput
import helper, format, StudyIQ
import logging
import time
import aiohttp
import asyncio
import aiofiles
from pyrogram.types import User, Message
import os
from requests.adapters import HTTPAdapter
#from requests.packages.urllib3.util.retry import Retry
#from urllib.parse import parse_qs, urlparse
import googleapiclient.discovery

auth_users = [ int(chat) for chat in os.environ.get("AUTH_USERS").split(",") if chat != '']
api_id=7520233
bot = Client(
    "stbotdll",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(str(api_id)), #int(os.environ.get("API_ID")),
    api_hash="8151cd1a69086a1d9b8760acd05fe27d", #os.environ.get("API_HASH")
)

logger = logging.getLogger()
r = requests.Session()
api_url = "https://philliptg.vercel.app"




   
async def linkdl(bot, m, url, caption, name, ytf, res):
    os.makedirs(f"./downloads/{m.chat.id}", exist_ok=True)
    try:
     if ".pdf" in url:
        #editable1 = await m.reply_text(f"**Downloading :- {name}.pdf\nUrl :-** ")
        #time.sleep(5)
        r = requests.get(url, allow_redirects=True, stream=True, verify=False)
        open(f"{name}.pdf",'wb').write(r.content)
        #await editable1.edit(f"**Uploading on Telegram**")
        #time.sleep(3)
        await m.reply_document(f"{name}.pdf", caption=caption)
        time.sleep(2)
        #await editable1.delete(True)
        os.remove(f"{name}.pdf")
     else:
       cmd = f'yt-dlp --no-check-certificate -f "{ytf}" -o "./downloads/{m.chat.id}/file.mp4" "{url}"'
       editable1 = await m.reply_text(f"**Downloading :- {name}.mkv\nUrl :-** ```{url}```")
       download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
       os.system(download_cmd)
       chat_id, path = m.chat.id, f"./downloads/{m.chat.id}/file.mp4"
       subprocess.run(f'ffmpeg -i "{path}" -ss 00:00:19 -vframes 1 "{path}.jpg"', shell=True)
       thumbnail = f"{path}.jpg"
       dur = int(helper.duration(path))
       await editable1.edit("**Uploading on Telegram**")
       await bot.send_video(chat_id = chat_id, video=path, caption=caption, thumb=thumbnail, duration=dur, supports_streaming=True, height=1080,width=1920)
       await editable1.delete(True)
       os.remove(path)
       os.remove(thumbnail)
    #except FloodWait as e:
       #  await asyncio.sleep(e.value)
    except Exception as e:
      try:
       await bot.send_video(chat_id=chat_id, video = path, caption=caption, thumb=thumbnail, duration=dur, supports_streaming=True, height=1080,width=1920)
       await editable1.delete(True)
       os.remove(path)
      except:
       await m.reply_text(f"Video Downloading Failed \n{caption}")
       await m.reply_text(e)
       os.remove(path)
async def formatSL(format_id, resolution):
     try:
       print(format_id)
       if resolution == "low":          
             ytf = format_id[0] 
       elif resolution == "medium":
            ytf = format_id[len(format_id)//2]
       elif resolution == "high":
          if len(format_id) >= 3:
             ytf = format_id[len(format_id)-1]
               
       
       for data in ytf:
          ytf, res = (ytf[data]), data
          return ytf, res
     except Exception as e:
        print(e)
        ytf, res = "best", "best"
        return ytf, res
     
async def drmdl(bot, m, url, caption, name, ytf, res):
   try:
    path = "./DOWNLOADS"
    os.makedirs(path, exist_ok=True)
    mpd = r.get(url).text.split("*")[0]

    keys_status = r.get(f"{api_url}/drmkeys/url={url}")
    if keys_status.status_code != 200:  
          rm = r.get(f"{api_url}/rm")
          keys_status = r.get(f"{api_url}/drmkeys/url={url}")
    keys = keys_status.text            
    cmd1 = f'yt-dlp -o "{path}/fileName.%(ext)s" --allow-unplayable-format --external-downloader aria2c -f "{ytf}" "{mpd}"'
    os.system(cmd1)
    avDir = os.listdir(path)
    editable1 = await m.reply_text("Decrypting")
    time.sleep(2)
    for data in avDir:
        if data.endswith("mp4"):
           cmd2 = f'mp4decrypt --show-progress {keys} {path}/{data} "video.mp4"'
           await editable1.edit("**Downloading Video**")
           time.sleep(2)
           os.system(cmd2)
           os.remove(f'{path}/{data}')
        elif data.endswith("m4a"):
           cmd3 = f'mp4decrypt --show-progress {keys} {path}/{data} "audio.m4a"'
           await editable1.edit("**Downloading Audio**")
           time.sleep(2)
           os.system(cmd3)
           os.remove(f'{path}/{data}')
    await editable1.edit("**merging audio & video formats**")
    
    cmd4 = f'ffmpeg -i "video.mp4" -i "audio.m4a" -c copy "{name}.mp4"'
    os.system(cmd4)
    filename = f"{name}.mp4"
    subprocess.run(f'ffmpeg -i "{filename}" -ss 00:01:00 -vframes 1 "{filename}.jpg"', shell=True)
    thumbnail = f"{filename}.jpg"
    try:
      dur = int(helper.duration(filename))
    except:
      dur = int(helper.get_duration(filename)) 
    await editable1.edit("**Uploading on Telegram**")
    
      
    await m.reply_video(filename, caption=caption, thumb=thumbnail, duration=dur, supports_streaming=True, height=1080,width=1920)
    time.sleep(2)
    await editable1.delete(True)
    os.remove(f"video.mp4")
    os.remove(f"audio.m4a")
    os.remove(filename)
    os.remove(thumbnail)   
   except Exception as e:           
      await m.reply_text(f"**Video Downloading Failed**\n\n{caption}")   
      await m.reply_text(e)
      try:
           os.remove(f"video.mp4")
           os.remove(f"audio.m4a")
           os.remove(filename)
           os.remove(thumbnail)
      except:
           pass
@bot.on_message(filters.command(["download_txt"]))   
async def drm(bot: Client, m: Message):
   edit = await m.reply_text("Send .txt file.")
   @bot.on_message(filters.document)
   async def processdoc(bot:Client, m:Message):
    x = await m.download()
    resolution, raw_text, arg = "medium", "", 0
    
    if m.caption is not None:
       cap = m.caption.strip().replace(" :",":").replace(": ", ":").split("\n")
       for data in cap:
            
            if "resolution:" in data:
                 reso= data.split(":")[-1]
                 resolution = reso
            elif "sn:" in data:
                 arg1 = data.split(":")[-1]                             
                 arg = int(arg1)-1 if arg1!=0 else 0          
            else:
                 raw_text+=data+"\n"
               
            
       
    else: 
        arg = 0
    if resolution not in ["low", "medium", "high"]:
           resolution = "medium"
    print("arg:", arg) 
    print("raw_text2:", raw_text)
    try:
       with open(x) as f:
           content = f.read()
       content = content.replace(": http", ":http").split("\n")
       links = []
       for i in content:
                 links.append(i.split(":http", 1))
       os.remove(x)
    except:
         await m.reply_text("fcuk! wrong input")
         os.remove(x)
         return
    total_links = len(content) + 1 - arg if arg!=0 else len(content)
    await m.reply_text(f"total links found are {total_links}")
    try:
        sn = arg+1
        for i in range(arg, len(links)-1):          
          url = links[i][1]
          rawName =  links[i][0]
          url = "http"+str(url)
          
          name = (
            rawName.replace("/", "")
            .replace("|", "_")
            .replace("*", "")
            .replace("?", "")
            .replace("#", "")
            .replace("\t", "")
            .replace(":", "-")
            .replace(";", "")
            .replace("+", "")
            .replace("@", "")
            .replace("'", "")
            .replace('"', '')
            .replace("{", "(")
            .replace("}", ")")
            .replace("`", "")
            .replace("__", "_")
            .strip()
          )
          if  "classplusapp" in url:
                    url = f"{api_url}/classplus/url={url}"
          elif "cpvod" in url:
                   url = f"{api_url}/cpvod/url={url}"
          elif "//studyiq.com" in url:
                  url = f"{api_url}/curl/{url.split('/')[-1]}"
         
          if url.startswith("http"):
             try:
              if not url.endswith(".pdf"):
               
                url1=r.get(url).text.split("*")[0] if "curl" in url or "cpvod" in url else url
                
                format_id = await format.get_resolution(url1)
                ytf, res = await formatSL(format_id, resolution)
                caption = f"**{sn}. {name} {res}.mkv**\n\n**Description-\n**{raw_text}"
              else:
                ytf, res = "", ""
                caption = f"**{sn}. {name}.pdf\n\nDescription-\n**{raw_text}"
              await drmdl(bot, m, url, caption, name, ytf, res) if "curl" in url or "cpvod" in url else await linkdl(bot, m, url, caption, name, ytf, res)
              sn+=1
             except FloodWait as e:
                 await asyncio.sleep(e.value+1)
                 await drmdl(bot, m, url, caption, name, ytf, res) if "curl" in url or "cpvod" in url else await linkdl(bot, m, url, caption, name, ytf, res)
                 sn+=1
             except Exception as e:
                await m.reply_text(f"{e}\n\n**{sn}. {name}\n\nDescription-\n**{raw_text}")
                sn+=1
    except Exception as exception:
          await m.reply_text(exception)
    await m.reply_text(f"**completed!**")
@bot.on_message(filters.command(["stiq"]) & filters.chat(auth_users))  
async def stiq(bot: Client, m: Message):
     r = requests.Session()
     editable = m.text
     inpurl = editable.replace("/stiq ","")
     boturl = inpurl.split("?")[1].replace(".","\.").replace("=",":")
     
     #x=await m.reply_text(inpurl)
     try:
        course_title = await StudyIQ.extdata(inpurl)
        
        await m.reply_document(f"{course_title}.txt", caption=f"**{course_title}\n#BHAUKAL**")
        os.remove(f"{course_title}.txt") 
     except Exception as e:
        await m.reply_text(e)
        os.remove(f"{course_title}.txt")
       
    

@bot.on_message(filters.command("restart"))
async def restart_handler(_, m):
    await m.reply_text("Restarted!", True)
    os.execl(sys.executable, sys.executable, *sys.argv)      

         
                    
                    
@bot.on_message(filters.command("download_link") & filters.chat(auth_users))
async def linkk(bot: Client, m: Message):     
     msg = m.text.strip().replace("/download_link ","")
     if msg.startswith("http"):
       try:
         if "|" in msg:
              msg = msg.replace("| ","|").split("|")     
              resolution, url = msg[1] , msg[0]
         else:
              resolution, url = "medium", msg
         name, caption = "file", ""
         if resolution not in ["low", "medium", "high"]:
                 resolution = "medium"
         format_id = await format.get_resolution(url)
         ytf, res = await formatSL(format_id, resolution)
         json3 = await linkdl(bot, m, url, caption, name, ytf, res)
    
       except Exception as e:
                await m.reply_text(f"{e}")
       
                  
bot.run()                      

