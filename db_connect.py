from sqlite3 import connect

db = connect('car_db.sqlite')
cursor = db.cursor()