from flask import Flask
from flask import render_template, url_for, request, redirect, flash, session, make_response
from flask_session.__init__ import Session
from module.dbconnect import DBConnect as dbconnect
import time


app=Flask(__name__,template_folder='template',static_url_path='/static')
app.config['SESSION_TYPE']='memached'
app.config['SECRET_KEY']='super secret key'
sess=Session()


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
            print("form", request.form)
            input_ = {"username":username, "email":email, "title":subject, "comment":comment}
            is_empty = False
            for key in input_:
                if input_[key] == "":
                    flash(f'the {key} is empty')
                    is_empty = True
                
            if not is_empty:
            # check if user exsist
                with dbconnect('forum.db') as session:
                    uname = session.execute(f'SELECT uname FROM user WHERE uname = "{username}"').fetchone()
                    name_list = session.execute(f'SELECT * FROM user').fetchall()
                    
                    if not uname:
                        session.execute(f'INSERT INTO user (uid, uname, email)\
                                          VALUES ({len(name_list)+1}, "{username}", "{email}")')
            # insert posts
                with dbconnect('forum.db') as session:
                    uid = session.execute(f'SELECT uid FROM user WHERE uname = "{username}"').fetchone()[0]
                    pid = len(session.execute(f'SELECT pid FROM post').fetchall())

                    session.execute(f'INSERT INTO post (p_uid, pid, title, context, date)\
                                      VALUES({uid}, {pid+1}, "{subject}", "{comment}", CURRENT_TIMESTAMP)')
                return redirect(url_for('forum'))
            else:
                return redirect(url_for('forum'), code=201)
                
        elif 'HomepageButton' in request.form:
            return redirect(url_for('homepage'))

    if request.method=="GET":
        with dbconnect('forum.db') as session:
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
