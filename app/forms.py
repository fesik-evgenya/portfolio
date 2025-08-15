from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FileField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), Length(min=4, max=80)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])

class AboutForm(FlaskForm):
    section = SelectField('Раздел', choices=[
        ('biography', 'Биография'),
        ('philosophy', 'Философия работы'),
        ('tools', 'Инструменты и технологии')
    ], validators=[DataRequired()])
    content = TextAreaField('Содержание', validators=[DataRequired()])
    image = FileField('Изображение')

class ContactForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Телефон', validators=[DataRequired()])
    address = TextAreaField('Адрес', validators=[DataRequired()])
    telegram = StringField('Telegram', validators=[DataRequired()])
    github = StringField('GitHub', validators=[DataRequired()])

class SolutionForm(FlaskForm):
    name = StringField('Название решения', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    image = FileField('Изображение')
    price = IntegerField('Цена', validators=[DataRequired()])
    delivery_days = IntegerField('Срок разработки (дни)', validators=[DataRequired()])
    is_new = BooleanField('Новинка')
    is_popular = BooleanField('Популярное')
    category = SelectField('Категория', choices=[
        ('package', 'Пакетное решение'),
        ('module', 'Дополнительный модуль')
    ])

class PortfolioForm(FlaskForm):
    title = StringField('Название проекта', validators=[DataRequired()])
    category = StringField('Категория', validators=[DataRequired()])
    package = StringField('Пакет', validators=[DataRequired()])
    duration = StringField('Срок разработки', validators=[DataRequired()])
    geo = StringField('Локация', validators=[DataRequired()])
    images = FileField('Изображения', render_kw={'multiple': True})
    features = TextAreaField('Особенности (каждая с новой строки)')
    testimonial = TextAreaField('Отзыв клиента')
    client = StringField('Имя клиента')
    live_url = StringField('Ссылка на сайт')
    slug = StringField('URL-идентификатор', validators=[DataRequired()])