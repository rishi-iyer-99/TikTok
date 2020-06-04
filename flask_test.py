  
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


@app.route('/data')
def data():
	return query_sound(6789771236114171906)

@app.route("/")
def hello():
    return render_template('test.html')


@app.route('/sounds/<sound_id>')
def sound_page(sound_id=0):
	return render_template('chart.html')


if __name__ == '__main__':
	app.run(debug=True)