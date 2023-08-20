from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
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
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id ORDER BY date_time;"
        results = connectToMySQL(db).query_db(query)
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
            all_posts.append(one_post)
        return all_posts
    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts (event_name, description, location, date_time, user_id) VALUES (%(name)s, %(description)s, %(location)s, %(date)s);"
        return connectToMySQL(db).query_db(query, data)