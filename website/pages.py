import tornado
import auth_user
import database
import authenticate
import blog_io
import stats

args = {"title":"BrendanR"}

T = tornado.template.Loader("/home/brendan/Website/HTTP/templates", autoescape=None)

def index(response):
    T.reset()
    args["post"] = database.read_posts(1)[0]
    args["title"] = "BrendanR"
    response.write(T.load("index.html").generate(**args))

def allChess(response):
    T.reset()
    args["title"] = "allChess - BrendanR"
    response.write(T.load("allchess.html").generate(**args))

def projects(response):
    T.reset()
    args["title"] = "Projects - BrendanR"
    response.write(T.load("projects.html").generate(**args))

def random(response):
    T.reset()
    args["title"] = "Random - BrendanR"
    response.write(T.load("random.html").generate(**args))
    
def blog(response):
    T.reset()
    args["posts"] = database.read_posts(-1)
    args["title"] = "Blog - BrendanR"
    response.write(T.load("blog.html").generate(**args))

@auth_user.check_authentication
def admin(response, user_id):   
    args["title"] = "Admin - BrendanR"
    s = stats.StatsHandler()
    args["stats"] = s.stats
    post_id = response.get_field("post_id")
    if post_id is None:
        args["post"] = ["New","","","","Date"]
    else:
        args["post"] = database.read_post_from_id(post_id)
    T.reset()
    response.write(T.load("admin.html").generate(**args))


