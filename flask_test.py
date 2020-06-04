  
from flask import Flask, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

def query_sound(sound_id):
	conn = sqlite3.connect('tiktok.db')
	cursor = conn.cursor()
	column = "most_plays"
	sql = "SELECT {col}, time_stamp FROM SoundStats WHERE sound_id =={sound}".format(col=column,sound = sound_id)
	cursor.execute(sql)
	data = cursor.fetchall()
	values = []
	dates = []
	for row in data:
		values.append(row[0])
		d = datetime.strptime(row[1], '%Y-%m-%d').date()
		dates.append(row[1])
	print (type(values[0]))
	templateData = {
		'dates': dates,
		'values': values
	}
	return templateData


@app.route('/data/<sound_id>')
def data(sound_id):
	return query_sound(sound_id)

@app.route("/")
def hello():
    return render_template('test.html')


@app.route('/sounds/<sound_id>')
def sound_page(sound_id):
	print(sound_id)
	print(type(sound_id))
	return render_template('chart.html',id= sound_id)


if __name__ == '__main__':
	app.run(debug=True)