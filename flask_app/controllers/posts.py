from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, post
from flask_app.controllers import users

@app.route('/posts/new')
def new_post():
    if 'user_id' not in session:
        flash("Must login or register")
        return redirect('/')
    return render_template('create_event.html')

@app.route('/create/post', methods = ['POST'])
def create_new_post():
    if not post.Post.validate_post(request.form):
        return redirect('/posts/new')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'location': request.form['location'],
        'date': request.form['date'],
        'user_id': session['user_id']
    }
    post.Post.save(data)
    return redirect('/dash')
@app.route('/post/<int:post_id>')
def show_post(post_id):
    if 'user_id' not in session:
        flash("Must login or register")
        return redirect('/')
    data = {'id': post_id}
    return render_template('view_event.html', post = post.Post.get_one(data))
    


@app.route('/posts/edit/<int:posts_id>')
def edit_post(posts_id):
    if 'user_id' not in session:
        return redirect('/clear')
    data={
        'posts_id':posts_id
    }
    one_post=post.Post.get_one(data)
    user_id={'id':session['user_id']}
    return render_template('edit_event.html',one_post=one_post,user=user.User.get_one(user_id))

@app.route('/update/<int:posts_id>',methods=['POST'])
def update(posts_id):
    if not post.Post.validations(request.form):
        return redirect(f"/events/edit/{posts_id}")
    data={
        'event_name': request.form['event_name'],
        'description': request.form['description'],
        'location': request.form['location'],
        'date': request.form['date'],
        'id':request.form['id']
        }
    post.Post.update(data)
    return redirect('/dash')
    



