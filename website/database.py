import sqlite3
import hashlib

DB_FILE = "database/main.db"

def get_username(user_id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT usr_name FROM users WHERE user_id=?;',[user_id])
        value = cursor.fetchone()
    return value[0] if value else None

def get_userid(usr_name):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM users WHERE usr_name=?;',[usr_name])
        value = cursor.fetchone()
    return value[0] if value else None
    
def change_password(user_id, values):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        values.append(0)
        cursor.execute('''UPDATE users
                          SET passwd = ?,
                          passwd_status = ?                         
                          WHERE user_id = ?''', (values))
        conn.commit()

def read_posts(n=-1):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM posts')
        posts = cursor.fetchall()[::-1]
        if n != -1:
        	posts = posts[:n]
        return posts

def read_post_from_id(id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM posts WHERE post_id = ?', id)
        return cursor.fetchone()

def write_post(title, tags, content, date, update_id = -1):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        if update_id == -1:
            cursor.execute('INSERT INTO posts VALUES (NULL, ?, ?, ?, ?); ',(title,tags,content,date))
        else:
            cursor.execute('''UPDATE posts 
                          SET title = ?,
                          tags = ?,
                          content = ?
                          WHERE post_id =
                          ?''',(title,tags,content,update_id))
            
        conn.commit()

def delete_post(id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM posts WHERE post_id = ?', id)
        conn.commit()
