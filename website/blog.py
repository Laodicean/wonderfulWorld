import datetime
import database
import auth_user
import tornado
import logging

@auth_user.check_authentication
def sub_post(response, user_id): 
    title = response.get_field("title")
    tags = response.get_field("tags")
    content = response.get_field("content")
    date = datetime.date.today().isoformat()
    post_id = response.get_field("post_id")
    database.write_post(title,tags,content,date,(-1 if post_id == "New" else post_id))
    response.redirect("/")
    tornado.autoreload._reload()
    logging.info("New post created, reloading webserver")

@auth_user.check_authentication    
def del_post(response, user_id):
    post_id = response.get_field("post_id")
    database.delete_post(post_id)
    response.redirect("/")
    tornado.autoreload._reload()
    logging.info("Post deleted, reloading webserver")

