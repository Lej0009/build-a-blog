from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:1234@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y37kGcys&zP3B'


def title_error(blog_title):
    if len(blog_title) > 0:
        return False
    else:
        return True

def body_error(blog_body):
    if len(blog_body) > 0:
        return False
    else:
        return True


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(800))



    def __init__(self, blog, blogbody):
        self.name=blog
        self.body=blogbody

@app.route('/', methods=['POST', 'GET'])
def index():

    blog_id = str(request.args.get('id'))
    blogs = Blog.query.all()
    myblog = Blog.query.get(blog_id)

    return render_template('blogs.html', blogs=blogs, myblog=myblog)
  

@app.route('/newblog', methods=['POST', 'GET'])
def new_blog():
        
    if request.method == 'POST' :
        blog_title = request.form['blog']   
        blog_body = request.form['blogbody']
        title_error_msg = ''
        body_error_msg = ''
        

        if title_error(blog_title):
            title_error_msg = "Please input a title."
            return render_template('newblog.html', title_error=title_error_msg, body_error=body_error_msg, blog_body=blog_body)
        if body_error(blog_body):
            body_error_msg = "Please input blog content."
            return render_template('newblog.html', title_error=title_error_msg, body_error=body_error_msg, blog_title=blog_title)
                   
        else:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()  
            return redirect('/?id=' + str(new_blog.id)) 
    else:
            return render_template('newblog.html')  
    


if __name__ == '__main__':
    app.run()