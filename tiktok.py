from TikTokApi import TikTokApi
from collections import Counter 
import json
import datetime
api = TikTokApi()


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
	top_hashtags = str(top_hashtags.most_common(5))
	top_hashtags = top_hashtags.replace("'","")
	vals["top_hashtags"] = top_hashtags

	return vals

#Returns a dictionary of all relevant sound_id information
def get_sound(sound_id):
	info = get_sound_info(sound_id)
	stats = get_sound_stats(sound_id)
	sound  = {**info, **stats} 
	sound["time_stamp"]=str(datetime.datetime.now().date())
	sound["sound_id"] = sound_id
	# for key, value in sound.items():
	# 	print(key,":",value)
	# 	print("")
	return sound

#Gets information for an array of sound_ids
def get_multiple_sounds(sound_ids):
	data = {}
	for s in sound_ids:
		data[s] = get_sound(s)
	return data

#Return a list of Ids of the trending songs
def get_trending_sounds():
	music = api.discoverMusic()
	sound_ids = []
	for m in music:
		sound_id = m.get("cardItem").get("id")
		sound_ids.append(sound_id)
	return sound_ids

def save_json(data,output_file):
	jason = json.dumps(data,indent=4)
	path = output_file
	f = open(path,"w")
	f.write(jason)
	f.close()

#Returns an array of sound ids from txt file
def read_file(filename):
	with open(filename) as f:
		sound_ids = f.read().splitlines() 
	sound_ids = [int(s) for s in sound_ids]
	return sound_ids

#Get daily info of all sound ids in file
def process_update(input_file,output_file):
	today = datetime.datetime.now().date()
	print("Updating Data For {date}:{file}...".format(date = today,file = input_file))
	sound_ids = read_file(input_file)
	data = get_multiple_sounds(sound_ids)
	save_json(data,output_file)
	print("Success, Data Written To:",output_file)
	print("")

if __name__ == '__main__':
	process_update("inputs/our_sounds.txt","outputs/our_sounds_data.json")



