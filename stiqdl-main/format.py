import yt_dlp

ytdl_opts = {
    'external_downloader': 'aria2c',
    'allow_unplayable_formats': True,
    'listformats': True,
    'nocheckcertificate': True
}

ydl = yt_dlp.YoutubeDL(ytdl_opts)          
async def get_resolution(url):
     formats = ydl.extract_info(url, download=False)["formats"]     
     
     format_id = list()
     if len(formats) == 1:
        format_id.append({"best" : (formats[0]["format_id"])})
     else:
         for format in formats:  
            try:
                if ("vercel" in url) or ((format["acodec"]) != "none" and (format["vcodec"]) != "none"):
                   resol = (format["resolution"])
                   format_id.append({resol : (format["format_id"])})
            except:
                pass
         if not format_id:       
           for format in formats:
              if (format["vcodec"])!="none":
                        resol = (format["resolution"])
                        format_id.append({resol : (format["format_id"])+"+bestaudio"})
     return format_id
