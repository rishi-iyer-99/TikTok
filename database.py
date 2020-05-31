import sqlite3
import json

conn = sqlite3.connect('tiktok.db')
cursor = conn.cursor()

def load_json(input_file):
	with open(input_file) as f:
		data= json.load(f)
	return data

def update_table(cur,data,table_name):
	for v in data.values():
		columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in v.keys())
		values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in list(v.values()))
		sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % (table_name, columns, values)
		print(sql)
		for k,val in v.items():
			print(k,":",type(val))
		cur.execute(sql)

def create_table(cur,data,table_name):
	cur.execute("""CREATE TABLE test(
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
				-- top_hashtags VARCHAR(500),
				time_stamp VARCHAR(500)
			);""")
	# cur.execute(sql)


data = load_json("outputs/our_sounds_data.json")
# create_table(cursor,data,"test")
update_table(cursor,data,"test")
conn.commit()
conn.close()