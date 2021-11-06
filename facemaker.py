import sys,os
import time
import tweepy
from PIL import Image, ImageEnhance
from wand.image import Image as wImage

if len(sys.argv) < 3:
    exit("You need more args fren\nFormat: python facemaker.py <twitter username> <input photo> [center x] [center y]")

uname = sys.argv[1]
inphoto = sys.argv[2]

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_key = os.environ['ACCESS_KEY']
access_secret = os.environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

im = Image.open(inphoto)
if len(sys.argv) < 5:
    center = (1515, 740)
else:
    center = (sys.argv[3], sys.argv[4])
scale = 350
cur_sentiment = ''

old_unhinged=-1
old_likes=-1

while True:
    res = api.user_timeline(screen_name = uname, count = 1)
    last_tweet = res[0]
    last_tweet_text = last_tweet.text
    last_tweet_likes = last_tweet.favorite_count
    unhinged_rating = len([c for c in last_tweet_text if c.isupper() or c == '!']) / len(last_tweet_text)
    if unhinged_rating != old_unhinged:
        print(f'Found tweet: {last_tweet_text}')
        print(f"New unhinged rating achieved: {unhinged_rating}")
        scale = int(300 - (unhinged_rating * 100))
        out = im.crop((center[0] - scale,
                       center[1] - scale,
                       center[0] + scale,
                       center[1] + scale))
        saturator = ImageEnhance.Color(out)
        finished = saturator.enhance(1 + (10 * unhinged_rating))
        finished.save('fried.jpg')
        old_unhinged = unhinged_rating
    if last_tweet_likes != old_likes:
        print(f'Found tweet: {last_tweet_text}')
        print(f"New like count achieved: {last_tweet_likes}")
        with wImage(filename='fried.jpg') as img:
            img.implode(amount= - (last_tweet_likes / 10))
            img.save(filename='explode.jpg')
        old_likes = last_tweet_likes
        api.update_profile_image('explode.jpg')
    time.sleep(5)
