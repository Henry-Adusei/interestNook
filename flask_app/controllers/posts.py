from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, post

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
@app.route('/like/<int:post_id>')
def add_like(post_id):
    if 'user_id' not in session:
        flash("Must login or register")
        return redirect('/')
    data = {'user_id': session['user_id'], 'post_id': post_id}
    post.Post.add_like(data)
    return redirect('/dash')

    


