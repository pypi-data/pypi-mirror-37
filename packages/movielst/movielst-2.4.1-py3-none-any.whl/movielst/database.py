import sqlite3
import csv
import xlsxwriter
import logging
from passlib.context import CryptContext
from .config import *

pwd_context = CryptContext(schemes=['pbkdf2_sha256'], default='pbkdf2_sha256', pbkdf2_sha256__default_rounds=30000)
LATEST_VERSION = 1


def connect_db():
    con = sqlite3.connect(get_setting('Index', 'location') + 'movies.db')
    return con


def upgrade():
    con = connect_db()
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS version (db_version INTEGER UNIQUE)')
    con.commit()
    version = cur.execute('SELECT db_version FROM version')
    try:
        current_version = version.fetchone()[0]
    except TypeError:
        cur.execute('INSERT INTO version (db_version) VALUES(?)', (LATEST_VERSION,))
        con.commit()
        current_version = LATEST_VERSION
    if current_version == LATEST_VERSION:
        logging.info('Database already latest version, doing nothing.')
    elif current_version < LATEST_VERSION:
        logging.info('Upgrading database to latest version')
        db_upgrade_file = open('db_upgrade', 'r')
        s = db_upgrade_file.read()
        upgrade_sql = s[s.find('[UPGRADE_START_'+str(LATEST_VERSION)+']')+len('[UPGRADE_START_'+str(LATEST_VERSION)+']'):s.rfind('[UPGRADE_END_'+str(LATEST_VERSION)+']')]
        cur.execute(upgrade_sql)
        cur.execute('UPDATE version SET db_version=?', (LATEST_VERSION,))
        con.commit()
    cur.close()


def create_user_table():
    sql = '''
        CREATE TABLE IF NOT EXISTS users
        (user TEXT PRIMARY KEY, password TEXT)
    '''
    con = connect_db()
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()


def add_user(username, password):
    sql = '''
        INSERT OR IGNORE INTO users
        (user, password) VALUES(?, ?)    
    '''
    con = connect_db()
    cur = con.cursor()
    cur.execute(sql, (username, pwd_context.encrypt(password)))
    con.commit()
    cur.close()


def verify_user(username, password):
    con = connect_db()
    cur = con.cursor()
    cur.execute('SELECT password FROM users WHERE user=?', (username,))
    try:
        result = pwd_context.verify(password, cur.fetchone()[0])
    except TypeError:
        return False
    return result


def get_users():
    con = connect_db()
    cur = con.cursor()
    return cur.execute('SELECT user FROM users')


def delete_user(username):
    con = connect_db()
    cur = con.cursor()
    cur.execute('DELETE FROM users WHERE user=?', (username,))
    con.commit()
    con.close()


def create_movie_table():
    sql = '''
        CREATE TABLE IF NOT EXISTS movies
            (title TEXT, genre TEXT, imdb FLOAT, runtime TEXT, tomato TEXT, year INT,
             awards TEXT, cast TEXT, director TEXT, poster TEXT, description TEXT, response BOOLEAN, 
             file_info_name TEXT UNIQUE, file_info_location TEXT, file_info_ext TEXT)
    '''
    con = connect_db()
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()


def add_movie(data, force_index):
    if force_index is True:
        sql = '''
            INSERT INTO movies
            (title, genre, imdb, runtime, tomato, year, awards, cast, director, poster, 
            description, response, file_info_name, file_info_location, file_info_ext)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
    elif force_index is False:
        sql = '''
            INSERT OR IGNORE INTO movies
            (title, genre, imdb, runtime, tomato, year, awards, cast, director, poster, 
            description, response, file_info_name, file_info_location, file_info_ext)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
    con = connect_db()
    cur = con.cursor()
    cur.execute(sql, (data['title'], data['genre'], data['imdb'],
                      data['runtime'], data['tomato'], data['year'],
                      data['awards'], data['cast'], data['director'],
                      data['poster'], data['description'], data['response'], data['file_info']['name'],
                      data['file_info']['location'], data['file_info']['extension']))
    con.commit()


def export_to_csv(output):
    con = connect_db()
    cur = con.cursor()
    with open(output, 'w') as output_file:
        writer = csv.writer(output_file, delimiter=',')
        for row in cur.execute('SELECT * FROM movies'):
            writer.writerow(row)


def export_to_xlsx(output):
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    con = connect_db()
    cur = con.cursor()

    for i, row in enumerate(cur.execute('SELECT * FROM movies')):
        for j, value in enumerate(row):
            worksheet.write(i, j, value)
    workbook.close()


def db_to_json():
    con = connect_db()
    cur = con.cursor()
    result = cur.execute('SELECT * FROM movies')
    items = []
    for row in result:
        items.append({'title': row[0], 'genre': row[1], 'imdb': row[2], 'runtime': row[3], 'tomato': row[4],
                      'year': row[5], 'awards': row[6], 'cast': row[7], 'director': row[8], 'poster': row[9],
                      'description': row[10], 'response': row[11], 'file_info': {'name': row[12], 'location': row[13], 'extension': row[14]}})
    return items


def edit(type, file_name, new_info):
    con = connect_db()
    cur = con.cursor()
    if type == "name":
        cur.execute('UPDATE movies SET title=? WHERE file_info_name=?', (new_info, file_name))
    elif type == "genre":
        cur.execute('UPDATE movies SET genre=? WHERE file_info_name=?', (new_info, file_name))
    elif type == "imdb_rating":
        cur.execute('UPDATE movies SET imdb=? WHERE file_info_name=?', (new_info, file_name))
    elif type == "runtime":
        cur.execute('UPDATE movies SET runtime=? WHERE file_info_name=?', (new_info, file_name))
    elif type == "tomato_rating":
        cur.execute('UPDATE movies SET tomato=? WHERE file_info_name=?', (new_info, file_name))
    elif type == "year":
        cur.execute('UPDATE movies SET year=? WHERE file_info_name=?', (new_info, file_name))
    elif type == "awards":
        cur.execute('UPDATE movies SET awards=? WHERE file_info_name=?', (new_info, file_name))
    elif type == "cast":
        cur.execute('UPDATE movies SET cast=? WHERE file_info_name=?', (new_info, file_name))
    elif type == "director":
        cur.execute('UPDATE movies SET director=? WHERE file_info_name=?', (new_info, file_name))
    else:
        logging.error("Unsupported edit type : " + type)
    con.commit()
    con.close()
