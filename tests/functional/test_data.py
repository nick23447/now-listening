from dataclasses import dataclass
from musicblog import bcrypt
from musicblog.models import User, Post
from datetime import datetime, timezone, timedelta
import random

post_data = [{'album_name': 'Grace', 'album_artist': 'Jeff Buckley', 'album_image': 'https://i.scdn.co/image/ab67616d0000b2736a760642a56847027428cb61'}, 
             {'album_name': 'Achtung Baby', 'album_artist': 'U2', 'album_image': 'https://i.scdn.co/image/ab67616d0000b273831c51426c89ade9bf275a77'},
             {'album_name': 'Vs.', 'album_artist': 'Pearl Jam', 'album_image': 'https://i.scdn.co/image/ab67616d0000b273777344aba9d5b5785b4593a5'}, 
             {'album_name': 'Ten', 'album_artist': 'Pearl Jam', 'album_image': 'https://i.scdn.co/image/ab67616d0000b273d400d27cba05bb0545533864'}, 
             {'album_name': 'Riot Act', 'album_artist': 'Pearl Jam', 'album_image': 'https://i.scdn.co/image/ab67616d0000b273a20dd7a979699da6dce878ae'}, 
             {'album_name': 'Californication', 'album_artist': 'Red Hot Chili Peppers', 'album_image': 'https://i.scdn.co/image/ab67616d0000b273a9249ebb15ca7a5b75f16a90'}, 
             {'album_name': "Ten Summoner's Tales", 'album_artist': 'Sting', 'album_image': 'https://i.scdn.co/image/ab67616d0000b273653b110d9560eb1656f4c583'}, 
             {'album_name': 'The Unforgettable Fire (Remastered)', 'album_artist': 'U2', 'album_image': 'https://i.scdn.co/image/ab67616d0000b273f3a97984c9fb5074f87e938d'}, 
             {'album_name': 'Born To Run', 'album_artist': 'Bruce Springsteen', 'album_image': 'https://i.scdn.co/image/ab67616d0000b273503143a281a3f30268dcd9f9'}, 
             {'album_name': 'Darkness On the Edge of Town', 'album_artist': 'Bruce Springsteen', 'album_image': 'https://i.scdn.co/image/ab67616d0000b273e2bb936c55fb54b0b9fdc666'}]


def get_post():
    one_post = random.choice(post_data)
    return one_post

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
    def create_batch(count):
        """Create multiple users"""
        users = []
        for i in range(1, count + 1):
            user = UserFactory.create(
                username=f'testuser{i}',
                email=f'test{i}@example.com',
                password=f'testpassword{i}'
            )
            users.append(user)
        return users
class PostFactory:
    """Factory for creating test posts"""
    
    @staticmethod
    def create(author, date_posted, title=None, content=None, **kwargs):
        """Create a single post"""
        if title is None:
            title = f'Test Post {id(object())}'
        if content is None:
            content = f'Test content for {title}'

        album_data = get_post()
        kwargs.update(album_data)
        post = Post(title=title, date_posted=date_posted, content=content, author=author, **kwargs)

        return post
    
    @staticmethod
    def create_batch(count, author):
        posts = []
        for i in range(1, count + 1): 
            
            date_posted = datetime.now(timezone.utc) - timedelta(days=i)
        
            post = PostFactory.create(
                author=author[i-1],
                title=f'Test Post {i}',
                date_posted=date_posted,
                content=f'Test Content {i}'
            )
                
            posts.append(post)
        return posts
        