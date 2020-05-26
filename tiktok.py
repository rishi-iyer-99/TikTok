from TikTokApi import TikTokApi
from collections import Counter 
import json
from datetime import datetime
api = TikTokApi()

results = 5

# trending = api.trending(results)
# music = api.discoverMusic()
# guy = api.getUserObject("chrisbrownofficial")
# trendingChallenges = api.discoverHashtags()


test = 6818899548363032577

#Gets basic information about a music clip
def get_sound_info(sound_id):
	vals = {}
	sound = api.getMusicObject(sound_id).get("musicInfo")
	music = sound.get("music")
	stats = sound.get("stats")

	vals["title"] = music.get("title")
	vals["author"] = music.get("authorName")
	vals["play_url"] = music.get("playUrl")
	vals["posts"] = stats.get("videoCount")

	return vals

#Gets relevant statistics about videos song is featured in
def get_sound_stats(sound_id):
	vals = {}
	total_plays = 0
	most_plays = 0
	total_diggs = 0
	most_diggs = 0
	total_comments = 0
	most_comments = 0
	total_shares = 0
	most_shares = 0
	min_duration = 60
	max_duration = 0
	avg_duration = 0
	#most_plays_link
	most_followed_user = 0
	most_followed_username = ""
	verified_post = False
	top_hashtags = {}

	posts = api.bySound(sound_id,99)
	num_posts = len(posts)
	for p in posts:
		# for key, value in p.items():
		# 	print(key,":",value)
		# 	print("")
		stats = p.get("itemInfos")
		total_plays += stats.get("playCount")
		plays = stats.get("playCount")
		if plays>most_plays:
			most_plays = plays
			# most_plays_link = stats.get("video").get("urls")[0]
		# most_plays = max(most_plays,stats.get("playCount"))
		total_diggs += stats.get("diggCount")
		most_diggs = max(most_diggs,stats.get("diggCount"))
		total_comments += stats.get("commentCount")
		most_comments = max(most_comments,stats.get("commentCount"))
		total_shares += stats.get("shareCount")
		most_shares = max(most_shares,stats.get("shareCount"))

		duration = stats.get("video").get("videoMeta").get("duration")
		min_duration = min(min_duration, duration)
		max_duration = max(max_duration, duration)
		avg_duration += duration/num_posts

		follows = p.get("authorStats").get("followerCount")
		if follows>most_followed_user:
			most_followed_user = follows
			most_followed_username = p.get("authorInfos").get("uniqueId")

		verified = p.get("authorInfos").get("verified")
		if verified:
			verified_post = True

		hashtags = [c.get("challengeName") for c in p.get("challengeInfoList")]
		for h in hashtags:
			if h not in top_hashtags:
				top_hashtags[h]=1
			else:
				top_hashtags[h]+=1

	vals["total_plays"] = total_plays
	vals["most_plays"] = most_plays
	vals["total_diggs"] = total_diggs
	vals["most_diggs"] = most_diggs
	vals["total_comments"] = total_comments
	vals["most_comments"] = most_comments
	vals["total_shares"] = total_shares
	vals["most_shares"] = most_shares
	vals["min_duration"] = min_duration
	vals["max_duration"] = max_duration
	vals["avg_duration"] = avg_duration
	vals["most_followed_user"] = most_followed_user
	vals["most_followed_username"] = most_followed_username
	vals["verified_post"] = verified_post
	top_hashtags = Counter(top_hashtags)
	vals["top_hashtags"] = top_hashtags.most_common(10)

	return vals

#Returns a dictionary of all relevant sound_id information
def get_sound(sound_id):
	info = get_sound_info(sound_id)
	stats = get_sound_stats(sound_id)
	sound  = {**info, **stats} 
	for key, value in sound.items():
		print(key,":",value)
		print("")
	return sound

#Gets information for an array of sound_ids
def get_multiple_sounds(sound_ids):
	data = {}
	for s in sound_ids:
		data[s] = get_sound(s)
	return data

def save_json(data):
	# today = datetime.date(datetime.now())
	jason = json.dumps(data)
	f = open("sound_data.json","w")
	f.write(jason)
	f.close()


data = get_multiple_sounds([test])
save_json(data)



