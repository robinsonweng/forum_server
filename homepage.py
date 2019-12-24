from flask import Flask
from flask import render_template,url_for,request,redirect

app=Flask(__name__,template_folder='template')

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
           

            username = request.form["name"]
            email = request.form["email_name"]
            subject = request.form["subject_name"]
            comment = request.form["comment_name"]
           

            return redirect(url_for('forum'))          
        elif 'HomepageButton' in request.form:
            return redirect(url_for('homepage'))
    return render_template("forum.html")



if  __name__== '__main__':
        app.run(debug=True)