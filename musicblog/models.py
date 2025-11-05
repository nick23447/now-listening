from __future__ import annotations
from datetime import datetime, timezone
from typing import List, Optional

from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column # type: ignore[attr-defined]

from musicblog import db, login_manager


@login_manager.user_loader # type: ignore
def load_user(user_id: str) -> Optional['User']:
    user: Optional['User'] = db.session.get(User, int(user_id))
    return user

class User(db.Model, UserMixin): # type: ignore
    __table__name = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image_file: Mapped[str] = mapped_column(String(20), nullable=False, default='default.jpg')
    password: Mapped[str] = mapped_column(String(60), nullable=False)

    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self) -> str:
        s = Serializer(current_app.config['SECRET_KEY'])
        token: str = s.dumps({'user_id': self.id})
        return token
    
    @staticmethod
    def verify_reset_token(token: str, expires_sec: int = 900) -> Optional[User]:
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id: int = s.loads(token, max_age=expires_sec)['user_id']
        except:
            return None

        user: Optional['User'] = db.session.get(User, user_id)
        return user

    def __repr__(self) -> str:
        return f"{self.username}"
        #return f"User('{self.username}'), '{self.email}', '{self.image_file}')"
    

class Post(db.Model):  # type: ignore
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    date_posted: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    album_name: Mapped[str] = mapped_column(String(250), nullable=False)
    album_artist: Mapped[str] = mapped_column(String(250), nullable=False)
    album_image: Mapped[str] = mapped_column(String(250), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self) -> str:
        return f"User('{self.title}'), '{self.date_posted}')"

class Album(db.Model): #type: ignore
    __tablename__ = 'album'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    artist: Mapped[str] = mapped_column(String(250), nullable=False)
    image: Mapped[str] = mapped_column(String(250), nullable=False)

    ratings = db.relationship('AlbumRating', backref='album', lazy=True)

    @property
    def avg_rating(self) -> float:
        if not self.ratings:
            return 0.0
        return round(sum(r.rating for r in self.ratings) / len(self.ratings), 2)

    def __repr__(self) -> str:
        return f"<Album {self.name} by {self.artist}>"

class AlbumRating(db.Model): #type: ignore
    __tablename__ = 'album_rating'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    album_id: Mapped[int] = mapped_column(Integer, ForeignKey('album.id'), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
 
    __table_args__ = (db.UniqueConstraint('user_id', 'album_id', name='unique_user_album'),)

    def __repr__(self) -> str:
        return f"<AlbumRating user={self.user_id} album={self.album_id} rating={self.rating}>"


