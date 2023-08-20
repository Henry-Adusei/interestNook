from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user

@app.route('/create/post', methods = ['POST'])
def create_new_post():
    if not 