/* ========== НАСТРОЙКА МОБИЛЬНОГО МЕНЮ ========== */
// Получаем элементы меню из DOM
const menuToggle = document.getElementById('menuToggle'); // Кнопка бургер-меню
const navLinks = document.getElementById('navLinks'); // Контейнер ссылок навигации

// Обработчик клика по бургер-меню
menuToggle.addEventListener('click', () => {
    // Переключаем класс 'active' для отображения/скрытия меню
    navLinks.classList.toggle('active');
    // Анимируем иконку бургер-меню
    menuToggle.classList.toggle('active');
});

// Закрытие меню при клике на любую ссылку
document.querySelectorAll('.nav__link').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        menuToggle.classList.remove('active');
    });
});

/* ========== НАСТРОЙКА CANVAS ДЛЯ АНИМАЦИИ ========== */
const canvas = document.getElementById('background-canvas'); // Получаем canvas элемент
const ctx = canvas.getContext('2d'); // Контекст для рисования

// Функция изменения размеров canvas при изменении размеров окна
function resizeCanvas() {
    canvas.width = window.innerWidth; // Ширина равна ширине окна
    canvas.height = window.innerHeight; // Высота равна высоте окна
}

// Слушатель изменения размеров окна
window.addEventListener('resize', resizeCanvas);
resizeCanvas(); // Инициализируем размеры при загрузке

/* ========== КЛАСС ЧАСТИЦ (ЗВЕЗД С ХВОСТАМИ) ========== */
class Particle {
    constructor() {
        this.reset(); // Инициализация частицы
        this.history = []; // Массив для хранения предыдущих позиций (хвост)
        this.maxHistory = 720; // Максимальная длина хвоста (количество точек)
        this.lifespan = 50000; // Полное время жизни частицы в миллисекундах (30 сек)
        this.fadeStartDelay = 45000; // Когда начинать затухание (за 5 сек до конца)
        this.isFadingOut = false; // Флаг состояния затухания
    }

    // Сброс параметров частицы (вызывается при создании и перерождении)
    reset() {
        // Случайная начальная позиция в пределах canvas
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;

        // Настройка скорости движения:
        const minSpeed = 0.7; // Минимальная скорость
        const maxSpeed = 2.7; // Максимальная скорость
        const speed = Math.random() * (maxSpeed - minSpeed) + minSpeed; // Случайная скорость
        this.vx = (Math.random() - 0.5) * speed; // Скорость по X (-speed/2 до speed/2)
        this.vy = (Math.random() - 0.5) * speed; // Скорость по Y (-speed/2 до speed/2)

        this.size = Math.random() * 1.7 + 0.8; // Размер частицы (0.8-2.5 пикселей)
        this.alpha = 0; // Начальная прозрачность (будет увеличиваться)
        this.targetAlpha = Math.random() * 0.3 + 0.2; // Целевая прозрачность (0.2-0.5)
        this.history = []; // Очищаем историю позиций
        this.isFadingOut = false; // Сбрасываем флаг затухания
        this.fadeStartTime = null; // Время начала затухания
        this.createdAt = Date.now(); // Время создания частицы
        this.fadeAlpha = 1; // Коэффициент затухания (1 = нет затухания)
    }

    // Начало процесса затухания частицы
    startFadeOut() {
        if (!this.isFadingOut) {
            this.isFadingOut = true;
            this.fadeStartTime = Date.now(); // Фиксируем время начала затухания
        }
    }

    // Обновление состояния частицы (вызывается каждый кадр анимации)
    update() {
        const currentTime = Date.now();
        const age = currentTime - this.createdAt; // Возраст частицы в мс

        // Активируем затухание, если пришло время
        if (age > this.fadeStartDelay && !this.isFadingOut) {
            this.startFadeOut();
        }

        // Если время жизни истекло - пересоздаем частицу
        if (age > this.lifespan) {
            this.reset();
            return;
        }

        // Расчет коэффициента затухания (если оно активно)
        if (this.isFadingOut) {
            const fadeProgress = (currentTime - this.fadeStartTime) / 5000; // Затухание за 5 сек
            this.fadeAlpha = Math.max(0, 1 - fadeProgress); // Плавное уменьшение от 1 до 0
        }

        // Добавляем текущую позицию в историю для хвоста
        this.history.push({
            x: this.x,
            y: this.y,
            baseAlpha: this.targetAlpha // Сохраняем базовую прозрачность
        });

        // Ограничиваем длину истории
        if (this.history.length > this.maxHistory) {
            this.history.shift(); // Удаляем самые старые точки
        }

        // Обновляем позицию частицы
        this.x += this.vx;
        this.y += this.vy;

        // Плавное появление (увеличение прозрачности)
        if (this.alpha < this.targetAlpha) {
            this.alpha += 0.002; // Скорость появления
        }

        // Если частица вышла за границы - пересоздаем ее
        if (this.x < 0 || this.x > canvas.width || this.y < 0 || this.y > canvas.height) {
            this.reset();
        }

        // Обновляем прозрачность точек хвоста
        this.history.forEach((point, index) => {
            // Чем старше точка в истории - тем она прозрачнее
            const ageInHistory = index / this.history.length;
            point.alpha = point.baseAlpha * ageInHistory * 0.8 * this.fadeAlpha;
        });
    }

    // Отрисовка частицы (вызывается каждый кадр анимации)
    draw() {
        // 1. Рисуем хвост (линии между предыдущими позициями)
        for (let i = 1; i < this.history.length; i++) {
            const prev = this.history[i-1]; // Предыдущая точка
            const current = this.history[i]; // Текущая точка

            ctx.beginPath();
            ctx.moveTo(prev.x, prev.y);
            ctx.lineTo(current.x, current.y);
            // Цвет хвоста с учетом прозрачности
            ctx.strokeStyle = `rgba(255, 220, 255, ${current.alpha * 1.2})`;
            ctx.lineWidth = this.size * 0.5; // Толщина линии зависит от размера частицы
            ctx.lineCap = 'round'; // Закругленные концы линий
            ctx.stroke();
        }

        // 2. Рисуем саму звезду с радиальным градиентом
        const gradient = ctx.createRadialGradient(
            this.x, this.y, 0, // Центр градиента
            this.x, this.y, this.size // Внешний круг градиента
        );
        // Яркое бело-фиолетовое ядро
        gradient.addColorStop(0, `rgba(255, 230, 255, ${this.alpha * this.fadeAlpha * 1.5})`);
        // Средняя часть - фиолетовая
        gradient.addColorStop(0.7, `rgba(230, 180, 255, ${this.alpha * this.fadeAlpha * 0.7})`);
        // Края - темно-фиолетовые
        gradient.addColorStop(1, `rgba(210, 150, 225, ${this.alpha * this.fadeAlpha * 0.2})`);

        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = gradient;
        ctx.fill();

        // 3. Добавляем свечение вокруг звезды
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size * 1.5, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 230, 255, ${this.alpha * this.fadeAlpha * 0.25})`;
        ctx.fill();
    }
}

/* ========== СОЗДАНИЕ ЧАСТИЦ ========== */
const particles = []; // Массив для хранения всех частиц
const particleCount = 65; // Общее количество частиц

// Создаем частицы и добавляем их в массив
for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
}

/* ========== ФУНКЦИЯ ОТРИСОВКИ СЕТКИ ========== */
function drawGrid() {
    const gridSize = 50; // Расстояние между линиями сетки

    // Настройки стиля линий сетки
    ctx.strokeStyle = 'rgba(230, 190, 255, 0.12)'; // Полупрозрачный фиолетовый
    ctx.lineWidth = 0.3; // Тонкие линии

    // Вертикальные линии сетки
    for (let x = 0; x < canvas.width; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0); // Начало линии (верх)
        ctx.lineTo(x, canvas.height); // Конец линии (низ)
        ctx.stroke();
    }

    // Горизонтальные линии сетки
    for (let y = 0; y < canvas.height; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y); // Начало линии (левый край)
        ctx.lineTo(canvas.width, y); // Конец линии (правый край)
        ctx.stroke();
    }
}

/* ========== ОСНОВНАЯ ФУНКЦИЯ АНИМАЦИИ ========== */
function animate() {
    // 1. Очищаем canvas (убираем предыдущий кадр)
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 2. Рисуем сетку (она будет под частицами)
    drawGrid();

    // 3. Обновляем и рисуем все частицы
    for (const particle of particles) {
        particle.update(); // Обновляем состояние
        particle.draw(); // Рисуем частицу
    }

    // 4. Запрашиваем следующий кадр анимации
    requestAnimationFrame(animate);
}

// Запускаем анимацию
animate();

// Взаимодействие с видео-отзывами
document.addEventListener('DOMContentLoaded', () => {
    // Отложенная загрузка видео
    const videoObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const iframe = entry.target.querySelector('iframe');
                if (iframe && !iframe.src) {
                    iframe.src = iframe.dataset.src;
                }
                videoObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    const videoContainer = document.querySelector('.video-review');
    if (videoContainer) {
        videoObserver.observe(videoContainer);
    }

    // Tooltips for skills
    const toolItems = document.querySelectorAll('.tool-item');
    toolItems.forEach(item => {
        item.addEventListener('click', () => {
            const toolName = item.querySelector('span').textContent;
            alert(`Подробнее о работе с ${toolName} в моих проектах`);
        });
    });
});

/* ========== КАРТА НА СТРАНИЦЕ КОНТАКТЫ ========== */
document.addEventListener('DOMContentLoaded', function() {
    ymaps.ready(initMap);

    function initMap() {
        const map = new ymaps.Map('map', {
            center: [59.9386, 30.3141],
            zoom: 11,
            controls: ['zoomControl']
        }, {
            suppressMapOpenBlock: true // Отключаем стандартные элементы управления
        });

        // Правильный формат координат (двумерный массив)
        const coverageAreaCoords = [[59.815936, 30.378236], [59.816428, 30.382851], [59.818053, 30.398876],
            [59.818410, 30.401977], [59.818866, 30.404879], [59.819486, 30.407937], [59.820541, 30.412807],
            [59.821703, 30.417818], [59.824469, 30.429950], [59.824469, 30.429950], [59.825325, 30.433192],
            [59.825681, 30.434282], [59.826087, 30.435217], [59.826515, 30.436151], [59.827263, 30.437524],
            [59.830257, 30.441630], [59.837347, 30.451157], [59.838993, 30.452913], [59.841130, 30.454937],
            [59.844132, 30.456911], [59.845814, 30.458052], [59.846892, 30.459290], [59.846431, 30.461337],
            [59.822652, 30.525012], [59.804402, 30.576847], [59.809853, 30.594042], [59.813664, 30.590212],
            [59.817331, 30.582267], [59.820665, 30.572668], [59.823070, 30.562737], [59.824805, 30.559651],
            [59.826900, 30.557571], [59.832994, 30.558469], [59.833959, 30.558456], [59.834805, 30.557173],
            [59.835132, 30.555860], [59.834753, 30.552069], [59.834456, 30.551951], [59.831879, 30.540355],
            [59.831820, 30.537272], [59.832206, 30.532094], [59.835013, 30.521005], [59.841005, 30.509889],
            [59.842824, 30.499429], [59.842601, 30.498190], [59.842987, 30.495417], [59.844977, 30.489353],
            [59.847901, 30.488027], [59.847901, 30.488027], [59.853986, 30.489937], [59.854230, 30.496352],
            [59.854807, 30.504449], [59.855946, 30.508429], [59.864411, 30.525866], [59.873230, 30.522762],
            [59.870023, 30.513976], [59.872398, 30.511995], [59.886431, 30.500933], [59.892482, 30.523998],
            [59.892482, 30.523998], [59.916168, 30.525361], [59.916168, 30.525361], [59.922988, 30.528223],
            [59.924729, 30.518925], [59.945589, 30.521437], [59.945869, 30.511642], [59.970675, 30.513577],
            [59.975327, 30.537782], [59.980999, 30.518067], [59.983158, 30.500223], [59.986274, 30.490732],
            [59.991011, 30.482374], [59.998861, 30.476596], [60.007508, 30.475990], [60.013852, 30.470177],
            [60.021010, 30.454993], [60.034853, 30.441099], [60.040520, 30.438411], [60.044787, 30.447213],
            [60.033890, 30.485078], [60.034399, 30.496001], [60.078820, 30.496683], [60.080493, 30.462229],
            [60.071431, 30.456139], [60.069998, 30.424137], [60.049633, 30.417643], [60.056107, 30.395061],
            [60.060752, 30.389026], [60.084645, 30.377657], [60.090387, 30.370770], [60.093590, 30.360892],
            [60.097119, 30.306013], [60.099589, 30.281401], [60.091356, 30.243099], [60.083864, 30.209716],
            [60.081580, 30.197369], [60.077129, 30.184349], [60.066121, 30.167696], [60.060621, 30.153285],
            [60.059055, 30.143981], [60.044459, 30.152345], [60.039181, 30.164179], [60.037357, 30.178828],
            [60.021489, 30.219129], [60.013272, 30.202690], [60.008077, 30.199761], [59.994044, 30.192356],
            [59.989726, 30.184574], [59.989726, 30.184574], [59.981685, 30.193021], [59.979252, 30.203889],
            [59.973221, 30.209947], [59.969314, 30.213546], [59.964717, 30.214765], [59.960287, 30.187933],
            [59.952465, 30.183243], [59.944348, 30.178250], [59.931515, 30.192932], [59.928420, 30.202382],
            [59.928075, 30.210569], [59.905632, 30.206860], [59.885417, 30.175740], [59.864510, 30.146522],
            [59.862612, 30.124619], [59.848814, 30.125000], [59.853041, 30.090670], [59.833789, 30.091763],
            [59.830257, 30.104304], [59.827118, 30.122540], [59.825195, 30.142576], [59.823628, 30.183802],
            [59.799208, 30.156075], [59.799574, 30.160783], [59.801462, 30.170590], [59.807954, 30.179984],
            [59.810713, 30.189238], [59.812701, 30.199674], [59.812701, 30.199674], [59.824109, 30.226441],
            [59.834571, 30.269707], [59.834649, 30.274251], [59.833929, 30.280342], [59.830287, 30.287251],
            [59.813931, 30.260692], [59.815983, 30.286687], [59.803929, 30.323207], [59.803929, 30.323207],
            [59.793628, 30.351937], [59.798415, 30.404622], [59.815314, 30.371611], [59.815936, 30.378236],
        ];

// Создаем полигон с явным указанием стиля
        const coveragePolygon = new ymaps.Polygon([coverageAreaCoords], {
            // Описание геометрии
        }, {
            // Стиль обводки
            strokeColor: "#d2a8e1",
            strokeWidth: 3,
            // Стиль заливки (RGBA формат)
            fillColor: "rgba(210, 168, 225, 0.8)",
            fillOpacity: 0.8,
            // Явно указываем тип геометрии
            geometry: 'polygon'
        });

        // Принудительно устанавливаем стиль после создания
        coveragePolygon.options.set({
            fillColor: "rgba(210, 168, 225, 0.8)",
            strokeColor: "#d2a8e1"
        });

        map.geoObjects.add(coveragePolygon);

        // Добавляем метку с кастомной иконкой
        const placemark = new ymaps.Placemark([59.9386, 30.3141], {
            hintContent: 'Возможны встречи в любых районах Санкт-Петербурга',
            balloonContent: 'Санкт-Петербург'
        }, {
            iconLayout: 'default#image',
            iconImageHref: '/static/images/map-marker.svg', // Путь к кастомной иконке
            iconImageSize: [25, 25],             // Размер иконки
            iconImageOffset: [-10, -5],         // Смещение иконки
            iconColor: '#d2a8e1'                 // Цвет иконки
        });

        map.geoObjects.add(placemark);

        // Автомасштабирование под все объекты
        map.setBounds(map.geoObjects.getBounds(), {
            checkZoomRange: true,  // Проверять допустимый уровень масштабирования
            zoomMargin: 50         // Отступы от краев (в пикселях)
        });

        // Принудительное обновление карты
        setTimeout(() => {
            map.container.fitToViewport();
        }, 500);
    }

    // Обработка формы контактов
    const form = document.getElementById('contact-form');
    const modal = document.getElementById('successModal');
    const closeModal = document.querySelector('.modal-close');
    const confirmBtn = document.querySelector('.modal-confirm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            // Показываем кастомное модальное окно
            modal.style.display = 'block';

            // Сбрасываем форму
            form.reset();
        });
    }

    // Закрытие модального окна
    function closeSuccessModal() {
        modal.style.display = 'none';
    }

    if (closeModal) {
        closeModal.addEventListener('click', closeSuccessModal);
    }

    if (confirmBtn) {
        confirmBtn.addEventListener('click', closeSuccessModal);
    }

    // Закрытие при клике вне модального окна
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeSuccessModal();
        }
    });
});


/* ========== ПОРТФОЛИО ========== */
document.addEventListener('DOMContentLoaded', () => {
    // Фильтрация проектов - добавлена проверка на существование элементов
    const portfolioFilterButtons = document.querySelectorAll('.portfolio-filters button');
    if (portfolioFilterButtons.length > 0) {
        portfolioFilterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                // Удаляем активный класс у всех кнопок
                portfolioFilterButtons.forEach(b => b.classList.remove('active'));

                // Добавляем активный класс текущей кнопке
                btn.classList.add('active');

                const filter = btn.dataset.filter;
                const portfolioCards = document.querySelectorAll('.portfolio-card');

                portfolioCards.forEach(card => {
                    if (filter === 'all' || card.dataset.category === filter) {
                        card.style.display = 'block';
                        card.style.opacity = '0';
                        // Анимация появления
                        setTimeout(() => card.style.opacity = '1', 50);
                    } else {
                        card.style.opacity = '0';
                        // Анимация исчезновения перед скрытием
                        setTimeout(() => card.style.display = 'none', 300);
                    }
                });
            });
        });
    }

    // Улучшенная функция загрузки модального окна проекта
    function loadProjectModal(id) {
        const modal = document.getElementById('projectModal');
        if (!modal) return;

        // Показываем loader перед загрузкой данных
        const modalBody = modal.querySelector('.portfolio-modal__body');
        if (modalBody) {
            modalBody.innerHTML = '<div class="loader">Загрузка проекта...</div>';
        }

        // Показываем модальное окно сразу с лоадером
        modal.style.display = 'block';

        // Загружаем данные проекта
        fetch(`/api/projects/${id}`)
            .then(response => {
                if (!response.ok) throw new Error('Ошибка загрузки');
                return response.json();
            })
            .then(data => {
                if (!modalBody) return;

                // Формируем содержимое модального окна
                modalBody.innerHTML = `
                    <div class="project-gallery">
                        ${data.images.map(img => `
                            <img src="/static/projects/${img}" alt="${data.title}" loading="lazy">
                        `).join('')}
                    </div>
                    <h2>${data.title}</h2>
                    <p class="project-geo">${data.geo}</p>
                    <div class="project-features">
                        <h3>Функционал:</h3>
                        <ul>
                            ${data.features.map(feature => `
                                <li>${feature}</li>
                            `).join('')}
                        </ul>
                    </div>
                    <div class="project-meta">
                        <p><strong>Пакет:</strong> ${data.package}</p>
                        <p><strong>Срок разработки:</strong> ${data.duration}</p>
                    </div>
                    ${data.testimonial ? `
                    <blockquote class="project-testimonial">
                        <p>"${data.testimonial}"</p>
                        <cite>${data.client}</cite>
                    </blockquote>
                    ` : ''}
                    <div class="project-actions">
                        <a href="${data.live_url}" target="_blank" class="btn btn--primary">
                            Посмотреть сайт
                        </a>
                        <button class="btn btn--secondary modal-close">Закрыть</button>
                    </div>
                `;

                // Добавляем обработчик закрытия на новую кнопку
                const closeBtn = modalBody.querySelector('.modal-close');
                if (closeBtn) {
                    closeBtn.addEventListener('click', () => {
                        modal.style.display = 'none';
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (modalBody) {
                    modalBody.innerHTML = `
                        <div class="error-message">
                            <p>Произошла ошибка при загрузке проекта</p>
                            <button class="btn modal-close">Попробовать снова</button>
                        </div>
                    `;

                    const retryBtn = modalBody.querySelector('.modal-close');
                    if (retryBtn) {
                        retryBtn.addEventListener('click', () => loadProjectModal(id));
                    }
                }
            });
    }

    // Обработка кликов по карточкам проектов
    document.querySelectorAll('.portfolio-card').forEach(card => {
        card.addEventListener('click', (e) => {
            // Проверяем, не был ли клик по ссылке внутри карточки
            if (!e.target.closest('a') && card.dataset.id) {
                loadProjectModal(card.dataset.id);
            }
        });
    });

    // Закрытие модального окна проекта
    const modalCloseBtn = document.querySelector('.portfolio-modal__close');
    if (modalCloseBtn) {
        modalCloseBtn.addEventListener('click', () => {
            const modal = document.getElementById('projectModal');
            if (modal) modal.style.display = 'none';
        });
    }

    // Закрытие при клике вне контента
    document.addEventListener('click', (e) => {
        const modal = document.getElementById('projectModal');
        if (modal && e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Кнопка "Показать ещё" - базовая реализация
    const loadMoreBtn = document.querySelector('.portfolio-pagination button');
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', () => {
            loadMoreBtn.textContent = 'Загрузка...';
            loadMoreBtn.disabled = true;

            // Здесь должен быть реальный запрос на сервер
            setTimeout(() => {
                // Это пример - нужно заменить на реальную загрузку
                console.log('Загружаем дополнительные проекты...');
                loadMoreBtn.textContent = 'Показать ещё';
                loadMoreBtn.disabled = false;
            }, 1000);
        });
    }
});

/* ========== КЕЙС ПОРТФОЛИО ========== */
document.addEventListener('DOMContentLoaded', function() {
    const gallery = document.querySelector('.project-gallery');
    if (!gallery) return;

    const slides = gallery.querySelectorAll('.gallery-slide');
    const thumbnails = gallery.querySelectorAll('.thumbnail');
    const prevBtn = gallery.querySelector('.gallery-prev');
    const nextBtn = gallery.querySelector('.gallery-next');
    const counter = gallery.querySelector('.current-slide');

    let currentIndex = 0;
    const totalSlides = slides.length;

    // Переключение слайдов
    function showSlide(index) {
        // Корректируем индекс для циклической навигации
        if (index >= totalSlides) index = 0;
        if (index < 0) index = totalSlides - 1;

        // Скрываем все слайды
        slides.forEach(slide => slide.classList.remove('active'));
        thumbnails.forEach(thumb => thumb.classList.remove('active'));

        // Показываем текущий слайд
        slides[index].classList.add('active');
        if (thumbnails[index]) thumbnails[index].classList.add('active');

        // Обновляем счетчик
        if (counter) counter.textContent = index + 1;

        currentIndex = index;
    }

    // Обработчики событий
    if (prevBtn) {
        prevBtn.addEventListener('click', () => showSlide(currentIndex - 1));
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => showSlide(currentIndex + 1));
    }

    // Клики по миниатюрам
    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', () => {
            const index = parseInt(thumb.dataset.index);
            showSlide(index);
        });
    });

    // Автопрокрутка (опционально)
    let autoSlideInterval;
    function startAutoSlide() {
        autoSlideInterval = setInterval(() => {
            showSlide(currentIndex + 1);
        }, 5000);
    }

    function stopAutoSlide() {
        clearInterval(autoSlideInterval);
    }

    // Запускаем автопрокрутку, если больше 1 слайда
    if (totalSlides > 1) {
        startAutoSlide();

        // Останавливаем при наведении
        gallery.addEventListener('mouseenter', stopAutoSlide);
        gallery.addEventListener('mouseleave', startAutoSlide);
    }
});