import requests, json, concurrent.futures
crux_url="https://www.studyiq.net/api/v4/my_course_video_crux"
ppt_url="https://www.studyiq.net/api/v4/my_course_video_ppt"
url = "https://www.studyiq.net/api/v4/course_detail"
headers={"Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "108",
    "Host": "www.studyiq.net",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/4.9.1"}
s, dict = requests.Session(), []
def videos(i, user_id, lang_id, api_token, course_id):
          
          link = f"https://www.studyiq.net/api/v4/video_course_notification?user_id={user_id}&api_token={api_token}&course_id={course_id}&language_id={lang_id}&page={i}"
          resp = s.get(link).json()["results"][ : :-1]
          for data in resp:
               dict.append(data)
              
def pdfs(i, user_id, lang_id, api_token, course_id):
          link = f"https://www.studyiq.net/api/v4/text_course_notification?user_id={user_id}&api_token={api_token}&course_id={course_id}&language_id={lang_id}&page={i}"
          resp = s.get(link).json()["results"][ : :-1]
          for data in resp:
               dict.append(data)
def exturl(data, course_title):
    try: 
       class_name = (data["name"])       
       if "text_upload_url" in data:
           url = (data["text_upload_url"])    
           open(f"{course_title}.txt","a+",encoding="utf8").write(f"{class_name} : {url}\n") 
         
       videotype, s3type = (data["video_type_id"]), (data["s3_enabled"])
       if s3type == 1:
           #print((data["s3_url"]))
           if (data["s3_url"]) is not None and (data["s3_url"]).startswith("http"):
              url = (data["s3_url"])
           else:                   
             if videotype == 2:
              url1 = (data["embed_code"])
              url = "https://player.vimeo.com/video/"+str(url1).split("/")[-1]
             elif videotype == 1:
              url = (data["video_id"])
       else:                   
           if videotype == 2:
              url1 = (data["embed_code"])
              url = "https://player.vimeo.com/video/"+str(url1).split("/")[-1]
           elif videotype == 1:
              url = (data["video_id"])         
       open(f"{course_title}.txt","a+",encoding="utf8").write(f"{class_name} : {url}\n")
    except Exception as e:
          print(e)
async def extdata(inpurl):
       dt=inpurl.split("?")[1]
       user_id = inpurl.split("user_id=")[1].split("&")[0] if dt.startswith("user_id") else inpurl.split("user_id=")[1]
       api_token, course_id=str(inpurl).split("&api_token=")[1].split("&")[0], inpurl.split("course_id=")[1].split("&")[0]
       lang_id = inpurl.split("language_id=")[1].split("&")[0]
       link = f"https://www.studyiq.net/api/v4/video_course_notification?user_id={user_id}&api_token={api_token}&course_id={course_id}&language_id={lang_id}&page=1"
       inpurl = inpurl+"&page=" if "&page=" not in inpurl else inpurl
       
       dt = link.split("?")[1].split("&page=")[0] + "&course_slug="
       
       course_title = s.post(url, headers=headers, data=dt).json()
      
       course_title = course_title["data"]["course_title"]
       
       token=f"{api_token}&user_id={user_id}"
       print(token)
       resp1 = s.get(link).json()
       total_page = resp1["total_page"]
       
       with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
               results = [executor.submit(videos, i, user_id, lang_id, api_token, course_id) for i in range(total_page, 0, -1)]
          
       with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
               results = [executor.submit(pdfs, i, user_id, lang_id, api_token, course_id) for i in range(total_page, 0, -1)]
       for data in dict:
            exturl(data, course_title)
     
                        
       return course_title
