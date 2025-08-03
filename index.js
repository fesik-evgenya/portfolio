// Меню для мобильных устройств
const menuToggle = document.getElementById('menuToggle');
const navLinks = document.getElementById('navLinks');

menuToggle.addEventListener('click', () => {
    navLinks.classList.toggle('active');
    menuToggle.classList.toggle('active');
});

// Закрытие меню при клике на ссылку
document.querySelectorAll('.nav__link').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        menuToggle.classList.remove('active');
    });
});

// Анимированный фон с технологичными линиями
const canvas = document.getElementById('background-canvas');
const ctx = canvas.getContext('2d');

// Размеры canvas
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// Класс для частиц (технологичных линий)
class Particle {
    constructor() {
        this.reset();
        this.history = [];
        this.maxHistory = 40;
        this.createdAt = Date.now();
        this.fadeStartTime = null; // Время начала затухания
        this.isFadingOut = false;  // Флаг затухания
    }

    reset() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.vx = (Math.random() - 0.5) * 0.8;
        this.vy = (Math.random() - 0.5) * 0.8;
        this.size = Math.random() * 0.8 + 0.2;
        this.alpha = 0;
        this.targetAlpha = Math.random() * 0.15 + 0.05;
        this.history = [];
        this.fadeStartTime = null;
        this.isFadingOut = false;
    }

    startFadeOut() {
        if (!this.isFadingOut) {
            this.isFadingOut = true;
            this.fadeStartTime = Date.now();
        }
    }

    update() {
        const currentTime = Date.now();
        const age = currentTime - this.createdAt;

        // Запускаем затухание за 2 секунду до окончания времени жизни
        if (age > 8000 && !this.isFadingOut) {
            this.startFadeOut();
        }

        // Полное удаление частицы через 10 секунд
        if (age > 10000) {
            this.reset();
            this.createdAt = currentTime;
            return;
        }

        // Плавное затухание
        if (this.isFadingOut) {
            const fadeProgress = (currentTime - this.fadeStartTime) / 1000;
            this.fadeAlpha = Math.max(0, 1 - fadeProgress);
        } else {
            this.fadeAlpha = 1;
        }

        // Сохраняем текущую позицию в историю
        this.history.push({
            x: this.x,
            y: this.y,
            alpha: this.targetAlpha,
            fadeAlpha: this.fadeAlpha
        });

        if (this.history.length > this.maxHistory) {
            this.history.shift();
        }

        // Движение
        this.x += this.vx;
        this.y += this.vy;

        // Плавное появление
        if (this.alpha < this.targetAlpha) {
            this.alpha += 0.002;
        }

        // Если частица выходит за пределы экрана
        if (this.x < 0 || this.x > canvas.width || this.y < 0 || this.y > canvas.height) {
            this.reset();
        }

        // Постепенное исчезновение хвоста
        this.history.forEach((point, index) => {
            const ageInHistory = index / this.history.length;
            point.alpha = this.targetAlpha * ageInHistory * 0.6 * point.fadeAlpha;
        });
    }

    draw() {
        // Рисуем хвост
        for (let i = 1; i < this.history.length; i++) {
            const prev = this.history[i - 1];
            const current = this.history[i];

            ctx.beginPath();
            ctx.moveTo(prev.x, prev.y);
            ctx.lineTo(current.x, current.y);
            ctx.strokeStyle = `rgba(210, 168, 225, ${current.alpha})`;
            ctx.lineWidth = this.size * 0.3;
            ctx.lineCap = 'round';
            ctx.stroke();
        }

        // Рисуем основную частицу
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(210, 168, 225, ${this.alpha * this.fadeAlpha})`;
        ctx.fill();
    }
}

// Создаем частицы
const particles = [];
const particleCount = 35;

for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
}

// Рисуем статичную технологическую сетку
function drawGrid() {
    const gridSize = 50;
    const lineWidth = 0.2;

    ctx.strokeStyle = 'rgba(210, 168, 225, 0.08)';
    ctx.lineWidth = lineWidth;

    // Вертикальные линии
    for (let x = 0; x < canvas.width; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }

    // Горизонтальные линии
    for (let y = 0; y < canvas.height; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }
}

// Функция анимации
function animate() {
    // Затемняем фон для эффекта шлейфа
    ctx.fillStyle = 'rgba(26, 26, 46, 0.04)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Обновляем и рисуем частицы
    particles.forEach(particle => {
        particle.update();
        particle.draw();
    });

    requestAnimationFrame(animate);
}

// Первоначальная отрисовка сетки
drawGrid();

// Запускаем анимацию
animate();