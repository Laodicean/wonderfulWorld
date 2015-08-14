import tornado
import auth_user

def check_auth(response):
    session_id_cookie = response.get_secure_cookie('session_id')
    digest_cookie = response.get_secure_cookie('digest')
    if session_id_cookie != None and digest_cookie != None:
        ##send session_id for hashing AND send digest for comparison
        ##if authorised return 'error, already logged in'
        authorised_cookies = auth_user.validate_session(session_id_cookie, digest_cookie)
        if authorised_cookies is None:
            T = tornado.template.Loader("/home/brendan/Website/HTTP/templates", autoescape=None)
            response.write(T.load("admin.html").generate(**args))
        else:
            response.clear_cookie('session_id')
            response.clear_cookie('digest')
            login(response)
    else:
        login(response)
            
def login(response):
    T = tornado.template.Loader("/home/brendan/Website/HTTP/templates", autoescape=None)
    username = response.get_field('username')
    password = response.get_field('password')
    args = {"error": [], "user_id":-1, "title":"Login"}
    if username != None and password != None:
        username = username.lower()
        #send username and password via auth_user.authenticate(usr_name, passwd) returns boolean
        authorised_user = auth_user.authenticate(username, password)
        if authorised_user: #usr_name and pas_word compared to data base
            session_id, digest = auth_user.create_session(username)
            response.set_secure_cookie('session_id', session_id)
            response.set_secure_cookie('digest', digest)
            response.redirect('/admin')
        else: #The details are incorrect.
            args["error"].append("Your username or password is incorrect.")
            response.write(T.load("login.html").generate(**args))

    else: #The user hasn't logged in.
        args["error"].append("Please log in.")
        response.write(T.load("login.html").generate(**args))
        
def logout(response): # on logout, delete both session and hash
    session_id_cookie = response.get_secure_cookie('session_id')
    response.clear_cookie('session_id')
    response.clear_cookie('digest')
    #delete session row from database
    auth_user.remove_session(session_id_cookie)
    response.redirect('/')
