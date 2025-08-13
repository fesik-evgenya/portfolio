import os
from datetime import datetime

from flask import Flask, url_for, request, render_template, jsonify, \
    make_response, send_from_directory
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, current_user, login_user, logout_user, \
    login_required
from flask_wtf.csrf import CSRFProtect, validate_csrf, CSRFError
from werkzeug.utils import secure_filename

# регистрируем приложение
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'upload/'

# для безопасности секретный ключ
load_dotenv()
app.secret_key = os.environ.get("SECRET_KEY")

# разрешённые файлы для закачки
ALLOWED_EXTENSIONS = ['pdf', 'docx', 'txt', 'zip', 'jpg', 'png', 'py', 'js',
                      'json', 'xlsx']

debug = False


# проверка загруженного файла на нужное расширение
def allowed_file(filename):
    return ('.' in filename and filename.rsplit('.', 1)[
        1].lower() in ALLOWED_EXTENSIONS)


# Обработка favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'images', 'logo'), 'favicon.svg',
        mimetype='image/svg+xml')


# Ограничение: 120 запросов в минуту с одного IP
limiter = Limiter(
    app=app,
    key_func=get_remote_address,  # Автоматически определяет IP
    default_limits=["120 per minute"]
)


# обработка 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', active_page='404',
                           meta_title="404 - Страница не найдена | Full-stack разработчик",
                           meta_description="Запрашиваемая страница не найдена. Вернитесь на"
                                            " главную или ознакомьтесь с моими услугами по"
                                            " разработке сайтов под ключ.",
                           hide_default_h1=True), 404


@app.context_processor
def inject_global_data():
    return {'now': datetime.now(), 'domain': 'fesik-dev.ru'}


# Главная страница
@app.route('/')
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
@app.route('/resheniya')
def solutions():
    return render_template('solutions.html',
                           active_page='solutions',
                           meta_title="Магазин готовых решений для сайтов | СПб",
                           meta_description="Готовые пакетные решения для бизнеса в Санкт-Петербурге. "
                                            "Сайты под ключ за 14 дней с гарантией.",
                           h1="Магазин готовых решений для вашего бизнеса")


@app.route('/api/solutions')
def api_solutions():
    return jsonify([
        {
            'id': sol.id,
            'name': sol.name,
            'description': sol.short_description,
            'image': url_for('static', filename=sol.image_path),
            'price': sol.price,
            'delivery_days': sol.delivery_days,
            'tags': ['new'] if sol.is_new else ['popular'] if sol.is_popular else []
        }
        for sol in solutions
    ])

# Роуты для пакетных решений
@app.route('/resheniya/<package_id>')
def package_details(package_id):
    packages = {'startap': 'Стартап-Лаунч',
                'profi': 'Профи-Портфолио',
                'magazin': 'Магазин-Мини',
                'salon': 'Клиника-Салон',
                'kofeynya': 'Кофейня-Бистро',
                'uslugi': 'Услуги-Мастер',
                'agentstvo': 'Агентство-Студия'}

    title = packages.get(package_id, 'Пакетное решение')
    return render_template(f'packages/{package_id}.html',
                           active_page='solutions',
                           meta_title=f"{title} | Готовое решение для бизнеса СПб",
                           h1=title)


# Портфолио (кейсы)
@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', active_page='portfolio',
                           meta_title="Портфолио Full-stack разработчика - Реальные проекты (СПб)",
                           meta_description="Примеры моих работ: сайты и веб-приложения на "
                                            "Python/JS, созданные для клиентов из Санкт-Петербурга."
                                            " Full-stack решения.",
                           meta_keywords="примеры работ, кейсы, реализованные сайты, отзывы "
                                         "клиентов, GitHub, технологии, Flask, JavaScript, "
                                         "бизнес-задачи",
                           h1="Мои проекты: Full-stack разработка в СПб")


@app.route('/portfolio/<slug>')
def portfolio_detail(slug):
    # Здесь будет логика загрузки данных конкретного проекта
    # Пока просто возвращаем шаблон с тестовыми данными
    project_data = {
        'title': 'Кофейня "Булочная №1"',
        'category': 'cafe',
        'package': 'Кофейня-Бистро',
        'duration': '12 дней',
        'geo': 'Васильевский остров, СПб',
        'images': ['coffee-shop.jpg'],
        'features': ['Онлайн-меню', 'Бронирование столиков', 'Google Maps'],
        'testimonial': 'Сайт запустили за 10 дней! Клиенты сразу начали бронировать столики через сайт.',
        'client': 'Алексей, владелец кофейни',
        'live_url': 'https://bulkafe.ru'
    }
    return render_template('portfolio_detail.html', project=project_data, active_page='portfolio')


# Обо мне (включая отзывы)
@app.route('/o-mne')
def about():
    return render_template('about.html', active_page='about',
                           meta_title="Веб разработчик | Евгения Фесик - Фрилансер в СПб",
                           meta_description="full-stack web разработчик из Санкт-Петербурга. "
                                            "Создание сайтов и веб-приложений",
                           meta_keywords="full-stack разработчик, Python разработчик,"
                                         " Flask, JavaScript, создание сайтов,"
                                         " веб-приложения, Санкт-Петербург,"
                                         " фриланс",
                           h1="Отзывы о моей работе в СПб")


# Контакты
@app.route('/kontakty')
def contacts():
    return render_template('contacts.html', active_page='contacts',
                           meta_title="Python разработчик фрилансер в СПб - Нанять для вашего "
                                      "проекта",
                           meta_description="Ищете надежного Python-разработчика (Flask) "
                                            "фрилансера в Санкт-Петербурге? Индивидуальный "
                                            "подход, встречи, договор.",
                           meta_keywords="найти программиста Python, заказать backend, фриланс"
                                         " исполнитель, частный разработчик, консультация, "
                                         "встречи в СПб, стоимость услуг",
                           h1="Python фрилансер в Санкт-Петербурге")


# Блог (пример)
@app.route('/blog/kak-vybrat-frilansera-dlya-sajta-v-spb')
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


@app.route('/order')
def order_form():
    return "Форма заказа в разработке", 200


@app.route('/privacy')
def privacy():
    return render_template('privacy.html', active_page='privacy',
                           meta_title="Политика конфиденциальности | Full-stack разработчик",
                           meta_description="Как мы собираем, используем и защищаем вашу информацию",
                           hide_default_h1=True)


# XML Sitemap (для поисковых систем)
@app.route('/sitemap.xml')
def sitemap_xml():
    main_pages = ['index', 'solutions', 'portfolio', 'about', 'contacts', 'blog']
    base_url = request.url_root.rstrip('/')

    # Основные страницы
    main_pages = ['index', 'services', 'portfolio', 'about', 'contacts',
                  'pricing']
    for page in main_pages:
        pages.append(
            {'url': url_for(page, _external=True), 'lastmod': '2025-08-01',
             'changefreq': 'weekly', 'priority': '1.0'})

    # Услуги
    services_pages = ['ecommerce', 'mvp', 'landing', 'optimization']
    for page in services_pages:
        pages.append(
            {'url': url_for(page, _external=True), 'lastmod': '2025-08-01',
             'changefreq': 'monthly', 'priority': '0.8'})

    # Блог
    blog_pages = ['choose_freelancer']
    for page in blog_pages:
        pages.append(
            {'url': url_for(page, _external=True), 'lastmod': '2025-08-01',
             'changefreq': 'monthly', 'priority': '0.7'})

    # Системные страницы
    system_pages = ['privacy', 'sitemap_html']
    for page in system_pages:
        pages.append(
            {'url': url_for(page, _external=True), 'lastmod': '2025-08-01',
             'changefreq': 'yearly', 'priority': '0.5'})

    sitemap_xml = render_template('sitemap.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response


# HTML Sitemap (для пользователей)
@app.route('/sitemap')
def sitemap_html():
    # Словарь категорий с новыми группами страниц
    categories = {
        "Основные страницы": ['index', 'solutions', 'portfolio', 'about',
                              'contacts'], "Магазин решений": ['solutions'],
        # Основная категория для пакетов
        "Пакетные решения": ['package_startap', 'package_profi',
        'package_magazin', 'package_kofeynya', 'package_uslugi',
            'package_agentstvo'],
        "Дополнительные модули": ['module_chatbot', 'module_payment',
            'module_crm', 'module_sms', 'module_lk', 'module_qr',
            'module_delivery', 'module_calendar'],
        "Блог": ['choose_freelancer'],
        "Правовая информация": ['privacy', 'sitemap_html']}

    # Словарь заголовков страниц с новыми пунктами
    page_titles = {'index': 'Главная', 'solutions': 'Магазин решений',
        'portfolio': 'Портфолио', 'about': 'Обо мне', 'contacts': 'Контакты',

        # Пакетные решения
        'package_startap': 'Пакет "Стартап-Лаунч"',
        'package_profi': 'Пакет "Профи-Портфолио"',
        'package_magazin': 'Пакет "Магазин-Мини"',
        'package_kofeynya': 'Пакет "Кофейня-Бистро"',
        'package_salon': 'Пакет "Салон-Клиника"',
        'package_uslugi': 'Пакет "Услуги-Мастер"',
        'package_agentstvo': 'Пакет "Агентство-Студия"',

        # Дополнительные модули
        'module_chatbot': 'Модуль "Чат-бот для консультаций"',
        'module_payment': 'Модуль "Онлайн-оплата (ЮKassa)"',
        'module_crm': 'Модуль "Интеграция с CRM"',
        'module_sms': 'Модуль "SMS-напоминания"',
        'module_lk': 'Модуль "Личный кабинет клиента"',
        'module_qr': 'Модуль "QR-меню для кафе"',
        'module_delivery': 'Модуль "Интеграция с доставкой"',
        'module_calendar': 'Модуль "Запись по календарю"',

        # Остальные страницы
        'choose_freelancer': 'Как выбрать фрилансера',
        'privacy': 'Политика конфиденциальности',
        'sitemap_html': 'Карта сайта'}

    # Словарь иконок для категорий
    icons = {"Основные страницы": "sitemap", "Магазин решений": "store",
        "Пакетные решения": "box", "Дополнительные модули": "puzzle-piece",
        "Блог": "blog", "Правовая информация": "balance-scale"}

    return render_template('sitemap.html', active_page='sitemap',
                           meta_title="Карта сайта | Full-stack разработчик",
                           meta_description="Полный список страниц на сайте",
                           categories=categories, page_titles=page_titles,
                           icons=icons, hide_default_h1=True)


# Главная функция запуска приложения
if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=debug)
