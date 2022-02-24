from googleapiclient.discovery import build
import re
import config

mylist = []  # the list of data after it is retrieved from the api and processed.

uploadsId = "" # playlist is Id is needed.  "uploadsId" is the playlist for all uploads to a channel.
playlistId = "PLi01XoE8jYohWFPpC17Z-wWhPOSuh8Er-"
apikey = config.apy_key  #api key youtube/google for permission to access api
pageTokenList=[]  # I haven't coded how to populate this automatically, so just manually by copypasta for now.
youtube = build('youtube', 'v3', developerKey=apikey)


def myData(response, mylist): # function to reformat response data into a list of date title and video id

    items = response["items"]
    
    for count, item in enumerate(items):
        date = item["snippet"]["publishedAt"] # gets published date
        mylist.append({"date": date})
        title = item["snippet"]["title"]
        fTitle = re.sub(r'[^a-zA-Z0-9 ]', '', title) # regular expression to remove non-alpha-numeric characters from the Video Title
        mylist[count].update({"title": fTitle})
        videoid = item["snippet"]["resourceId"]["videoId"]
        mylist[count].update({"id": videoid})
        thumbnail = item["snippet"]["thumbnails"]["high"]["url"]
        mylist[count].update({"thumbnail": thumbnail})
    return mylist

def createFile(myNewList):  # this function creates pelican  post with data from the list of dictionaries
    myDate = myNewList["date"]
    fDate = myDate.split('T')[0] # splits the string fron  "T" and returns the only preceding date
    
    postTitle = myNewList["title"]
    slug = myNewList["title"].replace(' ','-')

    # print(postTitle)
    vidID = myNewList["id"]
    postThumb = myNewList["thumbnail"]
    postUrl = slug
    mystring = f"""Title: {postTitle}
Date: {fDate}
Category: Youtube
Slug: {slug}
Summary: <a href="/{postUrl}.html"><img src="{postThumb}" alt="Video Image - click to go to article></a>

<iframe width="560" height="315" src="https://www.youtube.com/embed/{vidID}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

"""

    f = open("posts/" + slug + ".md", "w")
    f.write(mystring)
    f.close

# def makeFileForEach(createFile):  #make pelican post for each in the list
#     for item in myNewList:
#         createFile(myNewList)
filecount=0
# for item in pageTokenList:
request = youtube.playlistItems().list( 
    part="snippet",
    maxResults=50,
    pageToken=pageTokenList[0],  #if playlist is longer then 50 itmes, the api will return a pageteken to get the next <=50 items
    playlistId=playlistId
)

response = request.execute()
myNewList = myData(response, mylist)
# makeFileForEach(createFile)
for index, item in enumerate(myNewList):
    createFile(myNewList[index])  #calld the createFile function for each video which creates the formatted html in and md file for pelican site generator.
    filecount += 1
    print(str(filecount))  # just prints to screen for verification incrementing number for each file created

