import json
import urllib.request
import time
import csv
import os.path

def RequestSource():
    url = 'https://giphy.com'  #site URL
    search='@username'  #page userName
    #page = '1'  courser for pagination
    iso='1'
    channel = 'channelname'  #channel name
    js = 'ture'
    offset='0'    #Endpoint for limitations
    headers = {}             #request header
    headers['authority'] = ' giphy.com'
    headers['accept'] = 'application/json'
    headers['x-requested-with'] = 'XMLHttpRequest'
    headers['user-agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
    full_url = url +'/'+'search'+'/'+search+ '/'+ '?' + 'channel=' + channel + '&'+'is='+iso+'&'+'json='+ js+ 'offset='+offset # +'&'+'offset='+offset   #https://giphy.com/search/@worldrugby?2/channel=worldrugby&is=1&json=true
    print( full_url )
    fullurl( full_url, headers )
def fullurl(full_url, headers):
    req=urllib.request.Request(full_url,headers=headers)
    res=urllib.request.urlopen(req).read()
    data=json.loads(res)
    #rs=json.dumps(re)
    print(data)
    data_first=[]
    table=[]
    for i in data['data']['gifs']:
         data_first.append({"username":i["username"],"id": i["id"],"type": i["type"],"title": i["title"], "rating": i["rating"], "images-original-mp4": i["images"]["original"]["mp4"],"tags": i["tags"], "create_datetime": i["create_datetime"]})
         table.append(i['id'])
    print(data_first)
    next=(data['data']['pagination']['next_url'])
    print(next)
    viewCount(table)
    nextRequest(next)
def nextRequest(next):
    url = 'https://giphy.com'
    iso = '1'
    js = 'ture'
    nexturl=url+next+'&'+'is='+iso+'&'+'json='+js
    print(nexturl)
    headers = {}
    headers['authority'] = ' giphy.com'
    headers['accept'] = 'application/json'
    headers['x-requested-with'] = 'XMLHttpRequest'
    headers['user-agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
    req=urllib.request.Request(nexturl,headers=headers)
    res=urllib.request.urlopen(req).read()
    print(res)
    re=json.loads(res)
    data_sec=[]
    data=[]
    for i in re['data']['gifs']:
        data_sec.append( {"username":i["username"],"id": i["id"],"type": i["type"],"title": i["title"], "rating": i["rating"], "images-original-mp4": i["images"]["original"]["mp4"],"tags": i["tags"], "create_datetime": i["create_datetime"]} )
        data.append(i['id'])
    print(data_sec)
    nexttwo = (re['data']['pagination']['next_url'])
    print(nexttwo)
   # writetocsv(data_sec)
    viewCount(data)
    if nexttwo !='null':
       return nextRequest(nexttwo)
    else:
        print("finished")
def viewCount(data):
    # time.sleep(1)
    View_count_URL = 'https://giphy.com/api/v1/proxy-gif/'
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'
    headers['Accept'] = 'application/json'
    headers['Accept-Language'] = 'en-US,en;q=0.5'
    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['Connection'] = 'keep-alive'
    count = 0
    while data:
        id = data[count]
        count = count + 1
        # time.sleep(1)
        view_full_url = View_count_URL + id + '/' + 'view-count' + '/'
        print( view_full_url )
        reqs( view_full_url, headers)
        print( count )
        if count == len( data ):
            break
def reqs(view_full_url, headers):
    req = urllib.request.Request( view_full_url, headers=headers )
    res = urllib.request.urlopen( req ).read()
    data = json.loads( res )
    d_data = []
    d_data.append( {'userId': data['userId'], 'Gif_Id': data['gifId'], 'ViewCount': data['viewCount'],'UploadDate': data['uploadDate']} )
    print(d_data)
    file_varible = ('yourfilepath')
    file_Empty = os.path.isfile( file_varible )
    with open( 'file.csv', 'a' ) as file:
         f = ("userId", "Gif_Id", "ViewCount", "UploadDate")
         w = csv.DictWriter( file, fieldnames=f )
         if not file_Empty:
             w.writeheader()
         w.writerows( d_data )
def writetocsv(data):
    file_name = 'yourfilepath'
    file_Empty = os.path.isfile( file_name )
    with open( '_your_File_Path', 'a' ) as file:
        f = ["username","id","type","title","rating", "images-original-mp4", "tags", "create_datetime"]
        w = csv.DictWriter( file, fieldnames=f )
        if not file_Empty:
            w.writeheader()
        w.writerows( data )
RequestSource()