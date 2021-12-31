import sys, time
from modules import twitr, imgs

if len(sys.argv) < 5:
    exit("Usage: python3 facemaker.py <username> <picture> <x> <y>")

uname = sys.argv[1]

api = twitr.get_api_context()

im = imgs.open_image(sys.argv[2])
center = (int(sys.argv[3]),int(sys.argv[4]))

overlaid = False
old_unhinged=-1
old_likes=-1
reply_ids = set()

def calc_unhinged(tweet):
    return(len(
        [c for c in last_tweet.text if
         c.isupper() or c == '!']) /
           len(last_tweet.text) if len(last_tweet.text) > 0 else 0)

def process_img(img, replies, unhinged, likes):
    im = imgs.crop_img(img, unhinged, center)
    im.implode(amount= - (likes / 15))
    for rep in replies:
        if rep.id not in reply_ids:
            print(f"DAN NO DETECTED FROM {rep.user.screen_name}")
            im = imgs.overlay_pfp(api, rep.user.screen_name, im)
            reply_ids.add(rep.id)
    return(im)

def update_check(replies, unhinged, likes):
    return(unhinged != old_unhinged or
           likes != old_likes or
           {k.id for k in replies} != reply_ids)

while True:
    last_tweet = twitr.get_last_tweet(api, uname)
    unhinged_rating = calc_unhinged(last_tweet)
    kword_comments = twitr.search_tweet_comments(api, last_tweet, r'dan.*((no)|(yes))')
    
    if update_check(kword_comments, unhinged_rating, last_tweet.favorite_count):
        if {k.id for k in kword_comments} != reply_ids:
            print("resetting overlays...")
            reply_ids = set()
            
        im = imgs.open_image(sys.argv[2])
        im = process_img(im,
                    kword_comments,
                    unhinged_rating,
                    last_tweet.favorite_count)
        
        print(f'Found tweet: {last_tweet.text}')
        if unhinged_rating != old_unhinged:
            print(f"New unhinged rating achieved: {unhinged_rating}")
        if last_tweet.favorite_count != old_likes:
            print(f"New like count achieved: {last_tweet.favorite_count}")
            
        old_likes = last_tweet.favorite_count
        old_unhinged = unhinged_rating

        twitr.update_pfp(api, im)
        
    time.sleep(5)
