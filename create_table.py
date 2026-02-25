from db_connect import db, cursor

sql = '''
  create table car(
    id integer primary key,
    brand text not null,
    model text not null,
    year integer not null,
    price integer not null
  );
'''

cursor.execute(sql)
db.commit()