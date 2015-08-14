
import csv

#CSV fields:
#ID, DATE, TITLE, AUTHOR, CONTENT

BLOG_FILE = "blog.csv"
DEFAULT_HTML = """
<div class="blog_post">
<span class="blog_title">{}</span> <span class="blog_date">{}</span>
<div class="blog_content">{}</div>
</div>"""

def read_posts(n=-1):
    """Reads n blog posts, use n = -1 for all"""
    posts = []
    reader = csv.reader(open(BLOG_FILE))
    if n == -1:
	    for post in reader:
	    	posts.append(DEFAULT_HTML.format(post[2],post[1],post[4]))
    else: 
    	for i in range(n):
    		try:
    			post = next(reader)
    			posts.append(DEFAULT_HTML.format(post[2],post[1],post[4]))
    		except:
    			break
    return posts

def write_post(date, title, author, content):
    writer = csv.writer(open(BLOG_FILE))
    writer.writerow((date,title,author,content))
    
