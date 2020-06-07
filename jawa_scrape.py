from TikTokApi import TikTokApi
api = TikTokApi()

#returns a set of sound ids
def read_file(filename):
	print("Reading File..")
	sound_set = set()
	try:
		with open(filename) as f:
			sound_ids = f.read().splitlines() 
		for s in sound_ids:
			sound_set.add(int(s))
	except:
		print("No File Found, Initializing Empty")
	return sound_set


def get_user_sounds(user_id, sound_set):
	print("Getting Sounds..")
	data = api.byUsername(user_id, count=99)
	for d in data:
		sound_id = d.get("music").get("id")
		sound_id = int(sound_id)
		sound_set.add(sound_id)
	return sound_set

def write_file(sound_set, output_file):
	print("Writing File..")
	list_ids = list(sound_set)
	with open(output_file, 'w') as filehandle:
		filehandle.truncate(0)
		filehandle.writelines("%s\n" % sound for sound in list_ids)

def process_user_sounds(filename,username):
	initial_sounds = read_file(filename)
	current_sounds = get_user_sounds(username, initial_sounds)
	write_file(current_sounds, filename)
	print("Complete")

if __name__ == '__main__':
	process_user_sounds('inputs/jawa_sounds.txt','ad_hok')





