from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user,post
from flask import flash
db = "interestnook"

class Comment:
    def __init__(self,data):
        self.comments_id=data['comments_id']
        self.content=data['content']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user_id=data['user_id']
        self.post_id=data['post_id']
        self.user=None
        self.post=None
        
    @classmethod
    def add_comment(cls,data):
        query="""
        INSERT INTO comments(
            content,
            created_at,
            updated_at,
            user_id,
            post_id)
            VALUES(
            %(content)s,
            NOW(),
            NOW(),
            %(user_id)s,
            %(post_id)s;
            )"""
        return connectToMySQL('interestNook').query_db(query,data)
    
    @classmethod
    def get_comment_by_id(cls,data):
        query="""
        SELECT 
        content FROM
        comments WHERE
        comments_id=%(comments_id)s;
        """
        return connectToMySQL('interestNook').query_db(query,data)
    
    @classmethod
    def get_all_comments_by_user(cls):
        query="""
        SELECT content
        FROM comments
        JOIN user
        on comments.user_id=user.id;
        """
        results=connectToMySQL('interestNook').query_db(query)
        comments_made=[]
        for one_user in results:
            one_comment=cls(one_user)
            user_data={
                'id':one_user['user.id'],
                'first_name':one_user['first_name'],
                'last_name':one_user['last_name'],
                'email':one_user['email'],
                'password':one_user['password'],
                'created_at':one_user['created_at'],
                'updated_at': one_user['updated_at']
            }
            one_comment.user=user.User(user_data)
            comments_made.append(one_comment)
            return comments_made
        
    @classmethod
    def get_all_comments_under_post(cls):
        query="""
        SELECT content
        FROM comments
        JOIN user
        on comments.post_id=post.id;
        """
        results=connectToMySQL('interestNook').query_db(query)
        comments_made=[]
        for one_post in results:
            one_comment=cls(one_post)
            post_data={
                'id':one_post['post.id'],
                'event_name':one_post['event_name'],
                'description':one_post['description'],
                'location':one_post['location'],
                'date_time':one_post['date_time'],
                'created_at':one_post['created_at'],
                'updated_at': one_post['updated_at'],
                'user_id':one_post['post.user_id']
            }
            one_comment.post=post.Post(post_data)
            comments_made.append(one_comment)
            return comments_made
    
    @classmethod
    def update_comment(cls,data):
        query="""
        UPDATE comments
        SET
        content=%(content)s,
        updated_at=NOW()
        WHERE
        comments_id=%(comments_id)s;
        """
        return connectToMySQL('interestNook').query_db(query,data)
    
    @classmethod
    def delete_comment(cls,data):
        query="""
        DELETE
        FROM comments
        WHERE comments_id=%(comments_id)s;
        """
        return connectToMySQL('interestNook').query_db(query,data) 
    
    @staticmethod
    def validations(data):
        is_valid=True
        if len(data['content'])<3:
            flash("Comment must be more than 3 characters!!")
            is_valid=False
        return is_valid

