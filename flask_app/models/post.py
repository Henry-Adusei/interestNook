from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
import datetime
db = "interestnook"
class Post:
    def __init__(self, data):
        self.id = data['id']
        self.event_name = data['event_name']
        self.description = data['description']
        self.location = data['location']
        self.date_time = data['date_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.comments = []
        self.likes = None
    @classmethod
    def get_all(cls):
        query="SELECT * FROM posts ORDER BY date_time;"
        results = connectToMySQL(db).query_db(query)
        posts = []
        for post in results:
            posts.append(cls(post))
        return posts
    @classmethod
    def get_all_posts_with_creator(cls):
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id ORDER BY date_time DESC;"
        results = connectToMySQL(db).query_db(query)
        query2 = "SELECT COUNT(id) AS likes, post_id FROM likes GROUP by post_id;"
        results2 = connectToMySQL(db).query_db(query2)
        all_posts = []
        for row in results:
            one_post = cls(row)
            one_post_creator_info = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            new_creator = user.User(one_post_creator_info)
            one_post.creator = new_creator
            for row2 in results2:
                if(one_post.id == row2['post_id']):
                    one_post.likes = row2['likes']
            all_posts.append(one_post)
        return all_posts
    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts (event_name, description, location, date_time, user_id) VALUES (%(name)s, %(description)s, %(location)s, %(date)s, %(user_id)s);"
        return connectToMySQL(db).query_db(query, data)
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM posts WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        post = cls(results[0])
        print(results[0]['user_id'])
        data = {"id": results[0]['user_id']}
        post.creator = user.User.get_one(data)
        return post
    def update(cls, data):
        query = "UPDATE posts SET event_name=%(name)s, description=%(description)s, location=%(location)s,date_time=%(date)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)
    @staticmethod
    def add_like(data):
        query = "INSERT INTO likes (user_id, post_id) VALUES (%(user_id)s, %(post_id)s);"
        return connectToMySQL(db).query_db(query,data)
    @staticmethod
    def validate_post(data):
        is_valid = True
        if len(data['name']) < 2:
            flash("Event name must be at least 2 characters.")
            is_valid = False
        if len(data['description']) < 5:
            flash("Description for event must be at least 5 characters")
            is_valid = False
        if len(data['location']) < 2:
            flash("Location must be at least 2 characters")
            is_valid = False
        return is_valid
        