#Authored by TheArcticKitten/Noah O.
import praw
import time
import json
import re
reddit = praw.Reddit('bot1', user_agent='bot1 user agent')
subreddit = reddit.subreddit("Kitten_bots")
replies = 0
 
print(reddit.user.me())

with open("info.json") as f:
	info = json.load(f)

def gen_reply(name, desc, links):
	return """**{}**\n
{}\n
{}\n
------
[^SSBMBot](https://github.com/thearctickitten/SSBMBot) ^by ^[TheArcticKitten](/u/thearctickitten)""".format(name, desc, links)

while True:
	for submission in subreddit.hot(limit=300):
		submission.comments.replace_more(limit=0)
		for comment in submission.comments.list():
			#continue on if we've commented already
			if comment.id in open('commented.txt').read():
				continue

			#find the keyword in the comment body
			for item in info:
				if re.search("!{}".format(item), comment.body, flags=re.IGNORECASE):
					comment.reply(gen_reply(
						info[item]['Name'],
						"\n\n".join(info[item]['Description']),
						"\n\n".join("[{}]({})".format(link, info[item]['Links'][link]) for link in info[item]['Links'])
					))
					open("commented.txt", "a+").write(comment.id + "\n")
					replies += 1
					print("Replied to comment ID: {} Count: {}".format(comment.id, replies))

