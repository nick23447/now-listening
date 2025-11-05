from __future__ import annotations
from datetime import datetime, timezone
from typing import List, Optional

from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from sqlalchemy import Integer, String, Text, DateTime, Float
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
    
class Album_Ratings(db.Model):  # type: ignore
    __tablename__ = 'album_ratings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    album_name: Mapped[str] = mapped_column(String(100), nullable=False)
    album_artist: Mapped[str] = mapped_column(String(100), nullable=False)
    album_image: Mapped[str] = mapped_column(String(100), nullable=False)
    avg_rating: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"User('{self.album_name}'), '{self.album_artist}')"
