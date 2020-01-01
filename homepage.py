from flask import Flask
from flask import render_template,url_for,request,redirect
from module.dbconnect import DBConnect as dbconnect
import time


app=Flask(__name__,template_folder='template',static_url_path='/static')


@app.route('/')
def homepage():
    return render_template("homepage.html")

@app.route('/forum',methods=['GET','POST'])
def forum():
    if request.method=='POST':
        if 'PostThread' in request.form:
            username = request.form.get("name")
            email = request.form.get("email_name")
            subject = request.form.get("subject_name")
            comment = request.form.get("comment_name")

            # check if user exsist
            with dbconnect() as session:
                uname = session.execute(f'SELECT uname FROM user WHERE  uname = "{username}"').fetchall()
                uname = [name[0] for name in uname] 
                if not uname:
                    session.execute(f'INSERT INTO user (uid, uname, email) VALUES ({len(uname)+1}, "{username}", "{email}")')
            # insert posts
            with dbconnect() as session:
                uid = session.execute(f'SELECT uid FROM user WHERE uname = "{username}"').fetchone()[0]
                pid = len(session.execute(f'SELECT pid FROM post').fetchall())

                session.execute(f'INSERT INTO post (p_uid, pid, title, context, date)\
                                  VALUES({uid}, {pid+1}, "{subject}", "{comment}", CURRENT_TIMESTAMP)')
            return redirect(url_for('forum'))
        elif 'HomepageButton' in request.form:
            return redirect(url_for('homepage'))

    if request.method=="GET":
        with dbconnect() as session:
            posts = session.execute(f'SELECT uname, email, title, context, date\
                                      FROM post, user\
                                      WHERE post.p_uid = user.uid'
            )
            bottle = []
            for post in posts:
                bottle.append({"username":post[0],
                               "email":post[1],
                               "subject":post[2],
                               "comment":post[3],
                               "date":post[4]
                })
        return render_template('forum.html',says=bottle)
    
    return render_template("forum.html")


if  __name__== '__main__':
        app.run(debug=True)
