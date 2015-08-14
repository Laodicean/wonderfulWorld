import hashlib
import sqlite3
import random

def check_authentication(fn):
    """
    This function is a decorator, which will check a user's 
    authentication before directing them to a page. If they
    have not got correct authentication, they will be sent to
    the login page. Setting redirect to false means that the
    user will not be redirected, but will simply get the user ID
    """
    def wrapper(response, *args):
        #print('Checking auth.',args)
        user_id = None
        if response.get_secure_cookie('session_id') is not None and response.get_secure_cookie('digest') is not None:
            session_id = bytes.decode(response.get_secure_cookie('session_id'))
            session_digest = bytes.decode(response.get_secure_cookie('digest'))
            user_id = validate_session(session_id,session_digest)
        if not user_id:
            print('Failed.')
            response.redirect('/login')
        else:
            #print('Succeded-',user_id )
            #for arg in args:print(arg)
            fn(response, *args, user_id = user_id)
    return wrapper

def check_login(fn):
    """
    This function is a decorator, which will check a user's
    authentication before directing them to a page. If they
    have not got correct authentication, it will return None.
   	"""
    #print('rapping')
    def wrapper(response, *args):
    	#print('Checking auth.',args)
        user_id = None
        if response.get_secure_cookie('session_id') is not None and response.get_secure_cookie('digest') is not None:
            session_id = bytes.decode(response.get_secure_cookie('session_id'))
            session_digest = bytes.decode(response.get_secure_cookie('digest'))
            user_id = validate_session(session_id,session_digest)
        fn(response, *args, user_id = user_id)
    return wrapper

#authenticate(usr_name, passwd): Checks authentication details,
#returns bool True if authentication details match database details.
def authenticate(usr_name, passwd):
    """
    Checks authentication details, and returrns boolean True if 
    authentication details match database details. If there is no
    match, returns false.
    
    Usage:
    authenticate(username,password) -> True/False
    """
    
    connection = sqlite3.connect('database/main.db')
    cursor = connection.cursor()
    hashed_passwd = hashlib.sha512(passwd.encode()).hexdigest()
    cursor.execute("""
                   SELECT u.usr_name, u.passwd 
                   FROM users u 
                   WHERE u.usr_name = ? AND u.passwd = ?""",
                   ([usr_name, hashed_passwd])
                   )               
    row = cursor.fetchone()
    if row:
        connection.close()
        return True
    connection.close()
    return False

#create_session(usr_name): Returns session_id and session_digest 
#for the username specified.
def create_session(usr_name):
    """
    Returns a tuple containing a new session_id and session_digest 
    for the username specified.
    
    Usage:
    create_session(username) -> (session_id, session_digest)
    """
    connection = sqlite3.connect('database/main.db')
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT u.user_id 
                   FROM users u
                   WHERE u.usr_name = ?""",
                   ([usr_name])
                   )
    x = cursor.fetchone()
    if not x:
        #return None
        raise Exception('Username does not exist :(')
    user_id = x[0]
    session_id = ''.join([random.choice('1234567890qwertyuiopasdfghjklzxcvbnm') for x in range(20)])
    cursor.execute("""
                   INSERT INTO sessions VALUES (
                   ?,
                   ?)""",
                   ([session_id,user_id])
                   )
    digest = hashlib.sha512((str(session_id) + '0x7a6g1d1i0f5b6d1c5a4g').encode()).hexdigest()
    #the secondary item passed into the digest is 100% random, 
    #however is intended to stay the same.
    #it might not even be legal hex (I haven't checked lol)    
    connection.commit()
    connection.close()
    #print('from create_session: ',session_id, digest)
    return (session_id, digest)

#def validate_digest(session_id, digest): Checks that the digest generated
#matches the one supplied, and returns usr_name if true, else returns 
#False

def validate_session(session_id, digest):
    """
    Returns checks that the digest supplied matches the one 
    generated, and then returns the corresponding username.
    
    If there is no match, returns False.
    
    
    Usage:
    validate_digest(session_id, digest) -> username
    """
    connection = sqlite3.connect('database/main.db')
    cursor = connection.cursor()
    if digest != hashlib.sha512((str(session_id) + '0x7a6g1d1i0f5b6d1c5a4g').encode()).hexdigest():
        return None
    cursor.execute("""
                   SELECT u.user_id
                   FROM users u
                   WHERE u.user_id = (SELECT s.user_id
                                        FROM sessions s
                                        WHERE s.session_id = ?)""",
                                        ([session_id])
                   )
    x = cursor.fetchone()
    if not x:
        #return None
        raise Exception('Username does not exist for session... Something\'s gone pretty damn wrong DX')
    user_id = x[0]
    return (user_id)

def remove_session(session_id):
    connection = sqlite3.connect('database/main.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM sessions WHERE session_id = ?',
                  ([session_id]))
    connection.commit()
    connection.close()
