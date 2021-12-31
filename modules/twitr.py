import tweepy
import os, re, time

scrub_regex = r'(https?://[^\s]*)|(@[^\s]*)|\s'

def get_api_context():
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    access_key = os.environ['ACCESS_KEY']
    access_secret = os.environ['ACCESS_SECRET']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return(tweepy.API(auth))

def get_last_tweet(api_context, uname):
    res = api_context.user_timeline(screen_name = uname, count = 1)
    last_tweet = res[0]
    last_tweet.text = re.sub(scrub_regex, '', last_tweet.text)
    return(last_tweet)
    
def search_tweet_comments(api_context, tweet_target, keyword):
    try:
        replies = [
            k for k in
            api_context.search_tweets(f'@{tweet_target.user.screen_name}',
                                      since_id=tweet_target.id) if
            k.in_reply_to_status_id == tweet_target.id # and
            #keyword in re.sub(scrub_regex, '', k.text).lower()
        ]
        return(replies)
    except Exception as e:
        print(e)
        print("Rate limit hit searching comments waiting 10 seconds")
        time.sleep(10)

def update_pfp(api_context, img):
    try:
        img.save(filename='pfp.png')
        print("Uploading profile picture...")
        api_context.update_profile_image('pfp.png')
    except:
        print("Rate limit hit updating pfp, waiting 10 seconds")
        time.sleep(10)
