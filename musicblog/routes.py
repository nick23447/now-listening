import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from musicblog import app, db, bcrypt
from musicblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from musicblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


