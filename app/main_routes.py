import os
from flask import Blueprint, render_template, url_for, request, make_response, \
    send_from_directory, current_app, jsonify
from .models import Solution, PortfolioItem

main_bp = Blueprint('main', __name__)


# Обработка favicon
@main_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, 'static', 'images', 'logo'),
        'favicon.svg', mimetype='image/svg+xml')


# Главная страница
@main_bp.route('/')
def index():
    return render_template('index.html', active_page='index',
                           meta_title="Нанять Full-stack разработчика в СПб - Сайты под ключ",
                           meta_description="Full-stack разработка сайтов на Python/JS в СПб. "
                                            "Индивидуально, быстро, с поддержкой. "
                                            "Создам решение для вашего бизнеса!",
                           meta_keywords="нанять разработчика СПб, фрилансер веб, заказать сайт,"
                                         " создание сайта под ключ, Python JS, малый бизнес, "
                                         "стартап, быстро, качественно, поддержка, "
                                         "индивидуальный подход",
                           h1="Full-stack разработчик сайтов в Санкт-Петербурге")


# Магазин решений
@main_bp.route('/resheniya')
def solutions():
    packages = Solution.query.filter_by(category='package').all()
    modules = Solution.query.filter_by(category='module').all()

    return render_template('solutions.html', active_page='solutions',
                           meta_title="Магазин готовых решений для сайтов | СПб",
                           meta_description="Готовые пакетные решения для бизнеса в Санкт-Петербурге. "
                                            "Сайты под ключ за 14 дней с гарантией.",
                           h1="Магазин готовых решений для вашего бизнеса",
                           packages=packages, modules=modules)


@main_bp.route('/api/solutions')
def api_solutions():
    solutions = Solution.query.all()
    return jsonify([
        {'id': sol.id, 'name': sol.name, 'description': sol.description,
            'image': url_for('static',
                             filename=f'uploads/{sol.image_path}') if sol.image_path else None,
            'price': sol.price, 'delivery_days': sol.delivery_days,
            'tags': ['new'] if sol.is_new else [
                'popular'] if sol.is_popular else [], 'category': sol.category}
        for sol in solutions])


# Роуты для пакетных решений
@main_bp.route('/resheniya/<package_slug>')
def package_details(package_slug):
    solution = Solution.query.filter_by(slug=package_slug).first_or_404()
    return render_template(f'packages/{package_slug}.html',
                           active_page='solutions',
                           meta_title=f"{solution.name} | Готовое решение для бизнеса СПб",
                           h1=solution.name, solution=solution)


# Портфолио (кейсы)
@main_bp.route('/portfolio')
def portfolio():
    portfolio_items = PortfolioItem.query.all()
    return render_template('portfolio.html', active_page='portfolio',
                           meta_title="Портфолио Full-stack разработчика - Реальные проекты (СПб)",
                           meta_description="Примеры моих работ: сайты и веб-приложения на "
                                            "Python/JS, созданные для клиентов из Санкт-Петербурга."
                                            " Full-stack решения.",
                           meta_keywords="примеры работ, кейсы, реализованные сайты, отзывы "
                                         "клиентов, GitHub, технологии, Flask, JavaScript, "
                                         "бизнес-задачи",
                           h1="Мои проекты: Full-stack разработка в СПб",
                           portfolio_items=portfolio_items)


@main_bp.route('/portfolio/<slug>')
def portfolio_detail(slug):
    project = PortfolioItem.query.filter_by(slug=slug).first_or_404()
    return render_template('portfolio_detail.html', project=project,
                           active_page='portfolio',
                           meta_title=f"{project.title} | Пример работы",
                           meta_description=f"Проект {project.title} - {project.package}. "
                                            f"Особенности: {', '.join(project.features)}",
                           h1=project.title)


# Обо мне (включая отзывы)
@main_bp.route('/o-mne')
def about():
    biography = AboutContent.query.filter_by(section='biography').first()
    philosophy = AboutContent.query.filter_by(section='philosophy').first()
    tools = AboutContent.query.filter_by(section='tools').first()

    return render_template('about.html', active_page='about',
                           meta_title="Веб разработчик | Евгения Фесик - Фрилансер в СПб",
                           meta_description="full-stack web разработчик из Санкт-Петербурга. "
                                            "Создание сайтов и веб-приложений",
                           meta_keywords="full-stack разработчик, Python разработчик,"
                                         " Flask, JavaScript, создание сайтов,"
                                         " веб-приложения, Санкт-Петербург,"
                                         " фриланс",
                           h1="Отзывы о моей работе в СПб",
                           biography=biography, philosophy=philosophy,
                           tools=tools)


# Контакты
@main_bp.route('/kontakty')
def contacts():
    contact_info = ContactInfo.query.first()
    return render_template('contacts.html', active_page='contacts',
                           meta_title="Python разработчик фрилансер в СПб - Нанять для вашего "
                                      "проекта",
                           meta_description="Ищете надежного Python-разработчика (Flask) "
                                            "фрилансера в Санкт-Петербурге? Индивидуальный "
                                            "подход, встречи, договор.",
                           meta_keywords="найти программиста Python, заказать backend, фриланс"
                                         " исполнитель, частный разработчик, консультация, "
                                         "встречи в СПб, стоимость услуг",
                           h1="Python фрилансер в Санкт-Петербурге",
                           contact_info=contact_info)


# Блог (пример)
@main_bp.route('/blog/kak-vybrat-frilansera-dlya-sajta-v-spb')
def choose_freelancer():
    return render_template('blog/choose_freelancer.html', active_page='blog',
                           meta_title="Как выбрать фрилансера для сайта в СПб: 7 ключевых критериев",
                           meta_description="Пошаговое руководство по выбору надежного "
                                            "фрилансера для создания сайта в Санкт-Петербурге. "
                                            "На что обратить внимание при подборе исполнителя.",
                           meta_keywords="выбор фрилансера, нанять разработчика СПб, критерии "
                                         "выбора, портфолио, отзывы, договор, этапы оплаты, "
                                         "техническое задание",
                           h1="Как выбрать фрилансера для создания сайта в СПб")


@main_bp.route('/order')
def order_form():
    return "Форма заказа в разработке", 200


@main_bp.route('/privacy')
def privacy():
    return render_template('privacy.html', active_page='privacy',
                           meta_title="Политика конфиденциальности | Full-stack разработчик",
                           meta_description="Как мы собираем, используем и защищаем вашу информацию",
                           hide_default_h1=True)


# XML Sitemap
@main_bp.route('/sitemap.xml')
def sitemap_xml():
    pages = []

    # Основные страницы
    main_pages = ['main.index', 'main.solutions', 'main.portfolio',
                  'main.about', 'main.contacts', 'main.privacy']

    for page in main_pages:
        pages.append(
            {'url': url_for(page, _external=True), 'lastmod': '2025-08-15',
                'changefreq': 'weekly', 'priority': '1.0'})

    # Решения
    solutions = Solution.query.all()
    for solution in solutions:
        pages.append({
            'url': url_for('main.package_details', package_slug=solution.slug,
                           _external=True), 'lastmod': '2025-08-15',
            'changefreq': 'monthly', 'priority': '0.8'})

    # Портфолио
    portfolio_items = PortfolioItem.query.all()
    for item in portfolio_items:
        pages.append({'url': url_for('main.portfolio_detail', slug=item.slug,
                                     _external=True), 'lastmod': '2025-08-15',
            'changefreq': 'monthly', 'priority': '0.8'})

    sitemap_xml = render_template('sitemap.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response


# HTML Sitemap
@main_bp.route('/sitemap')
def sitemap_html():
    # Словарь категорий
    categories = {"Основные страницы": [('main.index', 'Главная'),
        ('main.solutions', 'Магазин решений'), ('main.portfolio', 'Портфолио'),
        ('main.about', 'Обо мне'), ('main.contacts', 'Контакты')],
        "Пакетные решения": [], "Дополнительные модули": [], "Портфолио": [],
        "Правовая информация": [
            ('main.privacy', 'Политика конфиденциальности'),
            ('main.sitemap_html', 'Карта сайта')]}

    # Заполняем категории решениями
    solutions = Solution.query.all()
    for solution in solutions:
        if solution.category == 'package':
            categories["Пакетные решения"].append(
                (f'main.package_details({solution.slug})', solution.name))
        elif solution.category == 'module':
            categories["Дополнительные модули"].append(
                (f'main.package_details({solution.slug})', solution.name))

    # Заполняем портфолио
    portfolio_items = PortfolioItem.query.all()
    for item in portfolio_items:
        categories["Портфолио"].append(('main.portfolio_detail', item.title))

    return render_template('sitemap.html', active_page='sitemap',
                           meta_title="Карта сайта | Full-stack разработчик",
                           meta_description="Полный список страниц на сайте",
                           categories=categories, hide_default_h1=True)

