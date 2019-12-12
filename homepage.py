from flask import Flask
from flask import render_template,url_for,request,redirect

app=Flask(__name__,template_folder='template')

@app.route('/')
def homepage():
    return render_template("homepage.html")

@app.route('/forum',methods=['GET','POST'])
def forum():
    if request.method=='POST':
        return redirect(url_for('homepage'))
    return render_template("forum.html")


if  __name__== '__main__':
        app.run(debug=True)