from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FloatField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Ingat Saya')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Konfirmasi Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Daftar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username sudah digunakan.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email sudah terdaftar.')


class CampaignForm(FlaskForm):
    title = StringField('Judul Campaign', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Deskripsi')
    target_amount = FloatField('Target Donasi (Rp)', validators=[DataRequired(), NumberRange(min=1)])
    is_active = BooleanField('Aktif')
    submit = SubmitField('Simpan')


class DonationForm(FlaskForm):
    amount = FloatField('Jumlah Donasi (Rp)', validators=[DataRequired(), NumberRange(min=1000)])
    message = TextAreaField('Pesan (Opsional)')
    submit = SubmitField('Donasi Sekarang')


class UserEditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[('donor', 'Donor'), ('admin', 'Admin')])
    submit = SubmitField('Simpan')
