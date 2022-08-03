from tqdm import tqdm
import json
from pathlib import Path
import httpx

def convertDateToFileName(date):
    return date.replace(" ", "_").replace(":", "-") 

def createFileName(date, ext):
    ext = ext.lower()
    if ext == "video":
        ext = ".mp4"
    else:
        ext = ".jpg"

    convertedDate = convertDateToFileName(date)
    counter = 1

    file = Path("output") / (convertedDate + ext)

    while file.exists():
        # print("file exists")
        filename = convertedDate + f" ({counter})" + ext
        file = Path("output") / filename
        counter += 1
    # print(file)
    return file

links = []
with open("memories_history.json", "r") as file:
    memories = json.load(file)
    for obj in memories["Saved Media"]:
        # print(obj)
        links.append((obj["Date"],obj["Media Type"],obj["Download Link"]))


for date, ext_type, url in tqdm(links):
    try:
        aws_link = httpx.post(url)
        aws_link = aws_link.content.decode("utf-8")
        data = httpx.get(aws_link)

        with createFileName(date, ext_type).open(mode="wb") as output_image:
            output_image.write(data.content)

    except Exception as e:
        print("COULD NOT SAVE IMAGE/VIDEO")
        print(url)
        print(e)
    

    # exit()