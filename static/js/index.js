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