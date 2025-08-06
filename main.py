from datetime import datetime
import os
from flask import Flask, url_for, request, render_template, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, current_user, login_user, logout_user, \
    login_required
from flask_wtf.csrf import CSRFProtect, validate_csrf, CSRFError
from werkzeug.utils import secure_filename

# регистрируем приложение
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'upload/'
app.config['SECRET_KEY'] = 'Tdutif_85'
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
        os.path.join(app.root_path, 'static', 'images', 'logo'),
        'favicon.svg',
        mimetype='image/svg+xml'
    )

# обработка 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',
        active_page='404',
        meta_title="404 - Страница не найдена | Full-stack разработчик",
        meta_description="Запрашиваемая страница не найдена. Вернитесь на"
                         " главную или ознакомьтесь с моими услугами по"
                         " разработке сайтов под ключ.",
        hide_default_h1=True
    ), 404


@app.context_processor
def inject_global_data():
    return {'now': datetime.now(), 'domain': 'fesik-dev.ru'}


# Главная страница
@app.route('/')
def index():
    return render_template('index.html',
        active_page='index',
        meta_title="Нанять Full-stack разработчика в СПб - Сайты под ключ",
        meta_description="Full-stack разработка сайтов на Python/JS в СПб. "
                         "Индивидуально, быстро, с поддержкой. "
                         "Создам решение для вашего бизнеса!",
        meta_keywords="нанять разработчика СПб, фрилансер веб, заказать сайт,"
                      " создание сайта под ключ, Python JS, малый бизнес, "
                      "стартап, быстро, качественно, поддержка, "
                      "индивидуальный подход",
        h1="Full-stack разработчик сайтов в Санкт-Петербурге"
    )


# Услуги
@app.route('/uslugi')
def services():
    return render_template('services.html', active_page='services',
        meta_title="Создание сайтов на Python и JS в СПб - Full-stack под ключ",
        meta_description="Профессиональная разработка сайтов на Python и "
                         "JavaScript в Санкт-Петербурге. От идеи до запуска."
                         " Индивидуальный подход, гарантия.",
        meta_keywords="веб-студия альтернатива, заказать сайт недорого, сайт"
                      " для бизнеса СПб, лендинг, интернет-магазин, визитка,"
                      " запуск сайта, Django/Flask, фронтенд, бэкенд",
        h1="Создание сайтов на Python и JS в СПб")


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


# Обо мне (включая отзывы)
@app.route('/o-mne')
def about():
    return render_template('about.html', active_page='about',
        meta_title="Отзывы клиентов - Веб-разработчик фрилансер в СПб",
        meta_description="Реальные отзывы заказчиков о моей работе как "
                         "Full-stack разработчика сайтов в Санкт-Петербурге."
                         " Гарантия качества.",
        meta_keywords="рекомендации, кейсы, примеры сотрудничества, репутация,"
                      " доверие, выполненные проекты, фриланс отзывы",
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


# Стоимость услуг (страница с расчетом)
@app.route('/stoimost')
def pricing():
    return render_template('pricing.html', active_page='pricing',
        meta_title="Стоимость сайта под ключ в СПб - Прозрачное ценообразование",
        meta_description="Узнайте примерную стоимость разработки сайта "
                         "под ключ в Санкт-Петербурге. От чего зависит цена?"
                         " Индивидуальный расчет.",
        meta_keywords="цена сайта, бюджет разработки, расчет стоимости, "
                      "этапы оплаты, экономия, типы сайтов (лендинг, магазин),"
                      " гарантии, ТЗ",
        h1="Сколько стоит создать сайт в СПб?")


# Создание интернет-магазина (услуга)
@app.route('/uslugi/internet-magazin')
def ecommerce():
    return render_template('ecommerce.html', active_page='services',
        meta_title="Интернет-магазин на Python в СПб - Full-stack разработка "
                   "под ключ",
        meta_description="Разработка интернет-магазинов на Python (Flask) и JS"
                         " в Санкт-Петербурге. Каталог, корзина, оплата, "
                         "админка. Под ключ.",
        meta_keywords="онлайн магазин, e-commerce, продажи через сайт, товары,"
                      " платежные системы, CMS, интеграция 1С, SEO база",
        h1="Создание интернет-магазина на Python в СПб")


# Создание MVP (услуга)
@app.route('/uslugi/mvp-dlya-startapa')
def mvp():
    return render_template('mvp.html', active_page='services',
        meta_title="Создание MVP для стартапа в СПб - Быстро и экономно на "
                   "Python",
        meta_description="Запустите MVP вашего стартапа быстро и в рамках "
                         "бюджета! Full-stack разработка на Python/JS в "
                         "Санкт-Петербурге. Фокус на вашу бизнес-идею.",
        meta_keywords="минимальный продукт, прототип сайта, запуск стартапа,"
                      " привлечь инвесторов, быстрая реализация, низкий бюджет,"
                      " Python Flask, бизнес-модель",
        h1="Разработка MVP для стартапа в СПб")


# Создание лендинга (услуга)
@app.route('/uslugi/sozdanie-lendinga')
def landing():
    return render_template('landing.html', active_page='services',
        meta_title="Создание лендинга у фрилансера в СПб - Быстро и эффективно",
        meta_description="Нужен продающий лендинг? Фрилансер в СПб создаст "
                         "адаптивный одностраничник на HTML/CSS/JS для вашего "
                         "продукта или услуги.",
        meta_keywords="посадочная страница, landing page, продающий сайт, "
                      "заказать лендинг недорого, конверсия, целевое действие,"
                      " мобильная верстка, сроки",
        h1="Лендинг Пейдж от фрилансера в СПб")


# Оптимизация скорости сайта (услуга)
@app.route('/uslugi/uskorenie-sajta')
def optimization():
    return render_template('optimization.html', active_page='services',
        meta_title="Ускорение сайта в СПб - Оптимизация скорости загрузки",
        meta_description="Ваш сайт медленно грузится? Профессиональная "
                         "оптимизация скорости в Санкт-Петербурге. Улучшение"
                         " Core Web Vitals, SEO.",
        meta_keywords="ускорить сайт, PageSpeed Insights, Lighthouse, время"
                      " загрузки, кэширование, сжатие, CDN, мобильная скорость,"
                      " SEO продвижение",
        h1="Оптимизация скорости сайта в СПб")


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


# Sitemap
@app.route('/sitemap')
def sitemap():
    pages = [
        {'url': url_for('index'), 'title': 'Главная', 'lastmod': '2025-08-06'},
        {'url': url_for('services'), 'title': 'Услуги', 'lastmod': '2025-08-06'},
        {'url': url_for('about'), 'title': 'Услуги', 'lastmod': '2025-08-06'},
        {'url': url_for('services'), 'title': 'Услуги', 'lastmod': '2025-08-06'},
        {'url': url_for('services'), 'title': 'Услуги', 'lastmod': '2025-08-06'},
        {'url': url_for('services'), 'title': 'Услуги', 'lastmod': '2025-08-06'},
    ]

    return render_template('sitemap.html', active_page='sitemap',
                           meta_title="Карта сайта | Full-stack разработчик",
                           meta_description="Полный список страниц на сайте",
                           pages=pages, hide_default_h1=True)


@app.route('/privacy')
def privacy():
    return render_template('privacy.html',
        active_page='privacy',
        meta_title="Политика конфиденциальности | Full-stack разработчик",
        meta_description="Как мы собираем, используем и защищаем вашу информацию",
        hide_default_h1=True
    )


# Главная функция запуска приложения
if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=debug)
