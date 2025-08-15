from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', active_page='index')

@main_bp.route('/resheniya')
def solutions():
    return render_template('solutions.html', active_page='solutions')

@main_bp.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', active_page='portfolio')

@main_bp.route('/portfolio/<slug>')
def portfolio_detail(slug):
    return render_template('portfolio_detail.html', active_page='portfolio')

@main_bp.route('/o-mne')
def about():
    return render_template('about.html', active_page='about')

@main_bp.route('/kontakty')
def contacts():
    return render_template('contacts.html', active_page='contacts')

# Добавьте остальные ваши роуты