from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='donor')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    donations = db.relationship('Donation', backref='donor', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username}>'


class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(255))  # Featured image filename
    target_amount = db.Column(db.Float, nullable=False)
    collected_amount = db.Column(db.Float, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    donations = db.relationship('Donation', backref='campaign', lazy='dynamic', cascade='all, delete-orphan')

    def progress_percentage(self):
        if self.target_amount == 0:
            return 0
        return min(100, (self.collected_amount / self.target_amount) * 100)

    def __repr__(self):
        return f'<Campaign {self.title}>'


class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Donation {self.amount} by User {self.user_id}>'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
