from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.comment import Comments
from flask_app.models.post import Post

@app.route("/comment/<int:post_id>")
def comment_form(post_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('comment.html', post = Post.get_one({'id':post_id}))

@app.route("/comment/<int:post_id>/submit")
def submit_comment(post_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    data = {
        'post_id': post_id,
        'user_id': session['user_id'],
        'content' : request.form['content'],
    }
    Comments.add_comment(data)
    return redirect('/dash', post = Post.get_one({'id':post_id}))