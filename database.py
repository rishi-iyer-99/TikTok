import sqlite3
import json
import datetime

def load_json(input_file):
	with open(input_file) as f:
		data= json.load(f)
	return data

def update_table(cur,data,table_name):
	print("INSERTING VALUES...")
	for v in data.values():
		columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in v.keys())
		values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in list(v.values()))
		sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % (table_name, columns, values)
		try:
			cur.execute(sql)
		except:
			print("VALUE ALREADY EXISTS")
	print(len(data.values()),"VALUE(S) INSERTED")

def create_table(cur,data,table_name):
	print("CREATING TABLE...")
	cur.execute("""CREATE TABLE IF NOT EXISTS {}(
				sound_id INT,
				title VARCHAR(500),
				author VARCHAR(500),
				play_url VARCHAR(500),
				posts INT,
				total_plays INT,
				most_plays INT,
				total_diggs INT,
				most_diggs INT,
				total_comments INT,
				most_comments INT,
				total_shares INT,
				most_shares INT,
				min_duration INT,
				max_duration INT,
				avg_duration REAL,
				most_followed_user INT,
				most_followed_username VARCHAR(500),
				verified_post BOOLEAN,
				top_hashtags VARCHAR(500),
				time_stamp VARCHAR(500),
				PRIMARY KEY(sound_id,time_stamp)
			);""".format(table_name))
	print("TABLE CREATED")



if __name__ == '__main__':
	today = datetime.datetime.now().date()
	print("UPDATING DATABASE:",today)
	data = load_json("outputs/our_sounds_data.json")

	conn = sqlite3.connect('tiktok.db')
	cursor = conn.cursor()
	try:
		update_table(cursor,data,"SoundStats")
	except:
		create_table(cursor,data,"SoundStats")
		update_table(cursor,data,"SoundStats")
	conn.commit()
	conn.close()
	print("DATABASE UPDATED")