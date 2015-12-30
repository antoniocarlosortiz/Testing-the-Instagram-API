POPULAR = 1
LIKE_TAG = 2
LIKE_POP = 3
LIKE_GEO = 4
LIKE_USER_POS = 5
LIKE_USER_TAG = 6
LIKE_USER_GEO = 7
UNFOLLOW = 8

#Choose tags for search.
#Keep the tags in double quotes.
#Do not forget to put a hashtag at the start of the tag.
TAGS = ["beach", "bikini", "love", "dog"]

#ACTION CHOICES
#ACTION = POPULAR #follows people that have liked a photo at the popular page.
#ACTION = UNFOLLOW
#ACTION = LIKE_FOLLOW
ACTION = LIKE_TAG

#CHANGE THE NUMBER OF LIKES UNTIL THE PROGRAM ENDS
MAX_COUNT = 100

#MAX_SECS FOR THE WAIT BETWEEN ACTIONS
MAX_SECS = 37

#MAX PICTURES TO LIKE ON A USER
MAX_USER_LIKE = 4

#Generate the url below from your instagram account to create your own auth token.
#https://api.instagram.com/oauth/authorize/?client_id=658e42989bce4dca972d1c9adc5779ac&redirect_uri=http://stangggtestsite.net/&response_type=token&display=touch&scope=likes+relationships

client_id = "<your client id>"
my_url = "<url of your website>"
auth_token = "<your auth token>"
client_secret = "<your client secret>"

print "FOLLOW PY BEGINS - GRAB A SLICE AND SIT BACK\n"
print "The script will now proceed\n"

import time, random
import urllib, json, urllib2
from pprint import pprint
import requests
import hmac

import visible_clock
import ipgetter

likedDict = {}

def header_generate():
    '''
    This function is needed by instagram for security.
    Encrypt the secret key with your IP address so it can only be decrypted if you have both.
    '''
    ips = ipgetter.myip()
    print "my ip %r".format(ips)
    secret = client_secret

    signature = hmac.new(secret, ips, sha256).hexdigest()
    headers_sha256 = "|".join([ips, signature])

    return headers_sha256

headers_sha256 = header_generate()
user_agent = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7',
headers = { "User-Agent" : user_agent,
            "Content-type": "application/x-www-form-urlencoded",
            "X-Insta-Forwarded-For": headers_sha256}


def likePicture(pictureId):
    liked = 0
    try:
        urlLike = "https://api.instagram.com/v1/media/%s/likes"
        values = {'access_token': auth_token,
                  'client_id': client_id}
        newLike = urlLike % (pictureId)

        r = requests.post(newLike, params=values, headers=headers)
        dataObj = r.text

        print "dataObj: %r, pictureId: %r" % (dataObj, pictureId)

        liked = 1
    except Exception, e:
        print "An error occurred:", repr(e)

    return liked


if (ACTION == LIKE_TAG or ACTION == LIKE_USER_TAG):
    def likeUser(max_results, tag, c, follow, url):
        if c > 0:
            urlFindLike = url

        urlFindLike = "https://api.instagram.com/v1/tags/%s/media/recent?access_token=%s" % (tag, auth_token)

        r = requests.get(urlFindLike)
        dataObj = r.json()

        numResults = len(dataObj['data'])
        pictureId = 0

        for likeObj in dataObj['data']:
            pictureId = likeObj['id']
            next_url = dataObj["pagination"]["next_url"]
            user = likeObj['user']
            userId = user['id']

            #no. of likes that we've done for a photo.
            #(to track if we're only repeatedly liking the same pictures or not.)
            try:
                numLikes = likedDict[picturedId]
                numLikes = numLikes + 1
                likedDict[pictureId] = numLikes
            except:
                numLikes = 1
                likedDict[pictureId] = numLikes

            try:
                result = likePicture(pictureId)
                c = c + result
                if c % 10 == 0:
                    print "Liked %s photos and of users that posted with the tag: %s" % (c, tag)

            #needed so we won't get blocked for spamming (HTTP 429)
            seconds = random.randint(MAX_SECS - 1, MAX_SECS)
            visible_clock.visibleclock(seconds)

            if c % 20 == 0:
                seconds = random.randint(120, 126)
                print "sleeping for %s" % seconds
                visible_clock.visibleclock(seconds)

            except Exception, e:
                print repr(e)

            if ACTION == LIKE_USER_TAG:

                print "liking photos of user: %s with user_id: %s" % (user, userId)
                urlUser = "https://api.instagram.com/v1/users/%s/media/recent/?access_token=%s" % (userId, auth_token)
                r = requests.get(urlUser)
                user_dataObj = r.json()

                user_count = 0

                for user_obj in user_dataObj['data']:

                    pictureId = user_obj['id']

                    try:
                        result = likePicture(pictureId)
                        c = c + result
                        if c % 10 == 0:
                            print "Liked %s pictures and of users that posted that tag: %s" % (tag, c)4
                        if c == max_results:
                            break


                    #needed so we won't get blocked for spamming (HTTP 429)
                    seconds = random.randint(MAX_SECS - 1, MAX_SECS)
                    visible_clock.visibleclock(seconds)

                    if c % 20 == 0:
                        seconds = random.randint(120, 126)
                        print "sleeping for %s" % seconds
                        visible_clock.visibleclock(seconds)

                    user_count = user_count + 1

                    if user_count >= MAX_USER_LIKE:
                        print "finished liking %s or more pictures of %s" % (MAX_USER_LIKE % userId)
                        break

                    except Exception, e:
                        print repr(e) 
        
        if c != max_results:
            # symbolically replace pagination_Id with next_url
            likeUsers(max_results, tag, c, follow, next_url)

        return c, follow

    for tag in TAGS:
        c = 0
        follow = 0
        c, follow = likeUsers(MAX_COUNT, tag, c, follow, 0)
        print "Liked %s for tag %s" % (c, tag)                    