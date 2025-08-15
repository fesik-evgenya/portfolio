from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename

from app import db
from app.forms import LoginForm, AboutForm, ContactForm, SolutionForm, PortfolioForm
from app.models import Admin, AboutContent, ContactInfo, Solution, PortfolioItem
import os
import uuid

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            return redirect(url_for('admin.dashboard'))
        flash('Неверные учетные данные', 'danger')
    return render_template('admin/login.html', form=form)


@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@admin_bp.route('/')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')


@admin_bp.route('/about', methods=['GET', 'POST'])
@login_required
def manage_about():
    form = AboutForm()
    section = request.args.get('section', 'biography')
    content = AboutContent.query.filter_by(section=section).first()

    if form.validate_on_submit():
        if not content:
            content = AboutContent(section=section)

        content.content = form.content.data

        # Обработка загрузки изображения
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'],
                                    unique_filename)
            form.image.data.save(filepath)
            if content.image_path:  # Удаляем старое изображение
                old_path = os.path.join(current_app.config['UPLOAD_FOLDER'],
                                        content.image_path)
                if os.path.exists(old_path):
                    os.remove(old_path)
            content.image_path = unique_filename

        db.session.add(content)
        db.session.commit()
        flash('Изменения сохранены!', 'success')
        return redirect(url_for('admin.manage_about', section=section))

    if content:
        form.content.data = content.content
        form.section.data = section

    return render_template('admin/about.html', form=form, content=content,
                           section=section)


@admin_bp.route('/contacts', methods=['GET', 'POST'])
@login_required
def manage_contacts():
    contacts = ContactInfo.query.first()
    form = ContactForm(obj=contacts)

    if form.validate_on_submit():
        if not contacts:
            contacts = ContactInfo()

        form.populate_obj(contacts)
        db.session.add(contacts)
        db.session.commit()
        flash('Контактная информация обновлена!', 'success')
        return redirect(url_for('admin.manage_contacts'))

    return render_template('admin/contacts.html', form=form, contacts=contacts)


# Решения
@admin_bp.route('/solutions', methods=['GET', 'POST'])
@login_required
def manage_solutions():
    solutions = Solution.query.all()
    form = SolutionForm()

    if form.validate_on_submit():
        solution = Solution(name=form.name.data,
            description=form.description.data, price=form.price.data,
            delivery_days=form.delivery_days.data, is_new=form.is_new.data,
            is_popular=form.is_popular.data, category=form.category.data)

        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'],
                                    unique_filename)
            form.image.data.save(filepath)
            solution.image_path = unique_filename

        db.session.add(solution)
        db.session.commit()
        flash('Решение добавлено!', 'success')
        return redirect(url_for('admin.manage_solutions'))

    return render_template('admin/solutions.html', solutions=solutions,
                           form=form)


# Портфолио
@admin_bp.route('/portfolio', methods=['GET', 'POST'])
@login_required
def manage_portfolio():
    portfolio_items = PortfolioItem.query.all()
    form = PortfolioForm()

    if form.validate_on_submit():
        portfolio_item = PortfolioItem(title=form.title.data,
            category=form.category.data, package=form.package.data,
            duration=form.duration.data, geo=form.geo.data, images=[],
            # Будут обработаны ниже
            features=[f.strip() for f in form.features.data.split('\n') if
                      f.strip()], testimonial=form.testimonial.data,
            client=form.client.data, live_url=form.live_url.data,
            slug=form.slug.data)

        # Обработка загрузки изображений
        if form.images.data:
            for img in form.images.data:
                if img.filename:
                    filename = secure_filename(img.filename)
                    unique_filename = f"{uuid.uuid4().hex}_{filename}"
                    filepath = os.path.join(
                        current_app.config['UPLOAD_FOLDER'], unique_filename)
                    img.save(filepath)
                    portfolio_item.images.append(unique_filename)

        db.session.add(portfolio_item)
        db.session.commit()
        flash('Проект добавлен в портфолио!', 'success')
        return redirect(url_for('admin.manage_portfolio'))

    return render_template('admin/portfolio.html',
                           portfolio_items=portfolio_items, form=form)