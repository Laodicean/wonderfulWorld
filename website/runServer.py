#!/usr/bin/python3

from tornado import Server, template

import pages
import authenticate
import database
import blog
import os

server = Server(port=8080)
server.register('/', pages.index)
server.register('/allChess', pages.allChess)
server.register('/blog', pages.blog)
server.register('/random', pages.random)
server.register('/projects', pages.projects)
server.register('/login', authenticate.check_auth)
server.register('/logout', authenticate.logout)
server.register('/admin', pages.admin)
server.register('/sub_post', blog.sub_post)
server.register('/del_post', blog.del_post)

T = template.Loader("/home/brendan/Website/HTTP/templates", autoescape=None)

#Registers all blog posts in their own page
blog_pages = []
for i in database.read_posts()[::-1]:
	blog_pages.append(i)
	server.register("/"+str(i[0]), lambda response: response.write(
		T.load("post_page.html").generate(**{"title":"{} - BrendanR".format(i[1]), "post":blog_pages[int(response.request.uri[1:])-1]}))
		)
	#I wonder if there is a better way of doing this? ^ It is pretty neat though <3

#Registers all static (no templating) pages in their own page
#Was loading the pong page for both fireworks and pong, weird.
#for i in os.listdir("/home/brendan/Website/HTTP/templates/static"):
#    server.register("/"+i[:-5], lambda response: response.write(
#		T.load("static/{}".format(i)).generate(**{}))
#	)
#    print("Registering {} to {}".format(i,i[:-5]))

server.register("/pong", lambda response: response.write(T.load("static/pong.html").generate(**{})))
server.register("/fireworks", lambda response: response.write(T.load("static/fireworks.html").generate(**{})))
server.run()



