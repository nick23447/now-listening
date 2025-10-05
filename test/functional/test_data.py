# tests/factories.py
from musicblog import bcrypt
from musicblog.models import User, Post

class UserFactory:
    """Factory for creating test users"""
    
    @staticmethod
    def create(username=None, email=None, password='testpassword123'):
        """Create a single user"""
        if username is None:
            username = f'user_{id(object())}'  # Generate unique username
        if email is None:
            email = f'{username}@example.com'
        
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_pw)
        
        return user
    
    @staticmethod
    def create_batch(count=10, **kwargs):
        """Create multiple users"""
        users = []
        for i in range(count):
            user = UserFactory.create(
                username=f'testuser{i}',
                email=f'test{i}@example.com',
                **kwargs
            )
            users.append(user)
        return users

class PostFactory:
    """Factory for creating test posts"""
    
    @staticmethod
    def create(author, title=None, content=None, commit=True):
        """Create a single post"""
        if title is None:
            title = f'Test Post {id(object())}'
        if content is None:
            content = f'Test content for {title}'
        
        post = Post(title=title, content=content, author=author)
        
        if commit:
            db.session.add(post)
            db.session.commit()
        
        return post
    
    @staticmethod
    def create_batch(count, author, **kwargs):
        """Create multiple posts for an author"""
        posts = []
        for i in range(count):
            post = PostFactory.create(
                author=author,
                title=f'Post {i}',
                content=f'Content {i}',
                **kwargs
            )
            posts.append(post)
        return posts