import sqlite3
import json

conn = sqlite3.connect('tiktok.db')
cursor = conn.cursor()

def load_json(input_file):
	with open(input_file) as f:
		data= json.load(f)
	return data

def update_table(data, table_name):
	for v in data.values():
		columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in v.keys())
		values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in list(v.values()))
		sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('mytable', columns, values)
		print(sql)

data = load_json("outputs/our_sounds_data.json")
update_table(data,"test")