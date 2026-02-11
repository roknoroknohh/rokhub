from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    accepted_terms = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    
    sent_messages = db.relationship('ContactMessage', 
        foreign_keys='ContactMessage.user_id', 
        backref='sender', 
        lazy=True)
    
    resolved_messages = db.relationship('ContactMessage', 
        foreign_keys='ContactMessage.resolved_by', 
        backref='resolver', 
        lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50), default='gamepad')
    color = db.Column(db.String(20), default='#3b82f6')
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    games = db.relationship('Game', backref='category', lazy=True, cascade='all, delete-orphan')

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(500))
    version = db.Column(db.String(50))
    size = db.Column(db.String(50))
    platform = db.Column(db.String(20), default='both')
    download_url = db.Column(db.String(1000))
    external_url = db.Column(db.String(1000))
    download_count = db.Column(db.Integer, default=0)
    view_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    health_status = db.Column(db.String(20), default='unknown')
    last_check = db.Column(db.DateTime)

class SiteSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), default='ROKhub')
    site_description = db.Column(db.String(500), default='أفضل منصة ألعاب رقمية')
    maintenance_mode = db.Column(db.Boolean, default=False)
    allow_registration = db.Column(db.Boolean, default=True)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    msg_type = db.Column(db.String(20), default='support')
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    is_resolved = db.Column(db.Boolean, default=False)
    admin_reply = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'))

class GameSite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(500))
    description = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    health_status = db.Column(db.String(20), default='unknown')
    last_check = db.Column(db.DateTime)

class ErrorLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    error_type = db.Column(db.String(100))
    error_message = db.Column(db.Text)
    route = db.Column(db.String(200))
    user_agent = db.Column(db.String(500))
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_resolved = db.Column(db.Boolean, default=False)

class AutoFixLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    action_taken = db.Column(db.Text)
    success = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
