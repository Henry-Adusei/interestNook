from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.comment import Comments
from flask_app.models.post import Post

@app.route("/comment/<int:post_id>/submit", methods = ['POST'])
def submit_comment(post_id):
    if 'user_id' not in session:
        return redirect('/clear')
    if not Comments.validate_comment(request.form):
        return redirect(f'/comment/{post_id}')
    data = {
        'user_id': session['user_id'],
        'post_id': post_id,
        'content' : request.form['content'],
    }
    Comments.add_comment(data)
    print('MADE IT HERE####################################')
    return redirect('/dash')

@app.route("/comment/delete/<int:comment_id>")
def delete_comment(comment_id):
    if 'user_id' not in session:
        return redirect('/clear')
    data = {
        'id' : comment_id
    }
    Comments.delete_comment(data)
    return redirect('/dash', comment = Comments.get_comment({'id':comment_id}))

