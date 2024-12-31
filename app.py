from flask import Flask
import os
from flask import render_template,request ,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager ,login_user ,UserMixin, logout_user

# Install required packages
# pip install flask flask-sqlalchemy flask-login

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SECRET_KEY"] = "secret+key"    

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader  
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id  = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(120), nullable = False)
    last_name = db.Column(db.String(120), nullable = False)
    email = db.Column(db.String(120), nullable = False)
    password = db.Column(db.String(120), nullable = False)
    def __repr__(self):
        return '<User %r>' % self.first_name

class Blog(db.Model):
    __tabename__ = 'blog'
    id  = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), nullable = False)
    writer_name = db.Column(db.String(120), nullable = False)
    contact_number = db.Column(db.Integer, nullable = False)
    blog_details = db.Column(db.Text(), nullable = False)
    def __repr__(self):
        return '<Blog %r>' % self.title



@app.route('/')
def main():
    user_data = Blog.query.all()
    return render_template('home.html',user_data=user_data)

@app.route('/register',methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        users = User(first_name=first_name,last_name=last_name,email=email,password=password)
        db.session.add(users)   
        db.session.commit()
        flash('User created successfully','success') 
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        email =request.form.get('email')
        password = request.form.get('password')
        print(email,password)
        current_user = User.query.filter_by(email=email).first()
        if current_user and current_user.password == password:
            login_user(current_user)
            flash('Login successful','success')
            return redirect('/')
        else:
            flash('Invalid email or password','danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/postblog', methods = ['POST','GET']) 
def postblog():
    if request.method == 'POST':
        
        title= request.form.get('title')
        writer_name = request.form.get('writer_name')
        contact_number = request.form.get('contact_number')
        blog_details = request.form.get('blog_details')
        user_blog = Blog(title = title,writer_name= writer_name,contact_number = contact_number,blog_details = blog_details) 
        flash("user blog is create sucessfully",'success')  
        # print(user_blog.contact_number)   
        db.session.add(user_blog)
        db.session.commit()
       
        return redirect("/")
        
    return render_template('postblog.html')



@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")

@app.route('/details/<int:id>')
def details(id):
    blog_data = Blog.query.get(id)
    return render_template('details.html',blog_data = blog_data)

@app.route('/delete/<int:id>')
def delete(id):
    blog_data = Blog.query.get(id)
    print(blog_data)
    db.session.delete(blog_data)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>',methods = ["POST","GET"])
def edit(id):
    blog_data = Blog.query.get(id)
    if request.method == "POST" :
        blog_data.title = request.form.get("title")
        blog_data.writer_name = request.form.get('writer_name')
        blog_data.contact_number = request.form.get('contact_number')
        blog_data.blog_details = request.form.get('blog_details')
        db.session.commit()
        flash("user blog is create sucessfully",'success')  
        return redirect("/")
    return render_template('edit.html',blog_data = blog_data)
if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug = True)