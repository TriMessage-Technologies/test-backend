const API_BASE = 'http://localhost:8000'; // Измените на ваш порт FastAPI

// DOM элементы
const authSection = document.getElementById('auth-section');
const serversSection = document.getElementById('servers-section');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const serversList = document.getElementById('servers-list');
const logoutBtn = document.getElementById('logout-btn');
const messageDiv = document.getElementById('message');

// Проверка авторизации при загрузке
document.addEventListener('DOMContentLoaded', function() {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    if (isLoggedIn === 'true') {
        showServers();
    }
});

// Показать сообщение
function showMessage(text, type = 'success') {
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    messageDiv.style.display = 'block';
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 3000);
}

// Показать секцию серверов
function showServers() {
    authSection.style.display = 'none';
    serversSection.style.display = 'block';
    loadServers();
}

// Показать секцию авторизации
function showAuth() {
    serversSection.style.display = 'none';
    authSection.style.display = 'block';
    localStorage.removeItem('isLoggedIn');
}

// Загрузка серверов
async function loadServers() {
    try {
        const response = await fetch(`${API_BASE}/servers`);
        if (response.ok) {
            const servers = await response.json();
            displayServers(servers);
        } else {
            showMessage('Ошибка загрузки серверов', 'error');
        }
    } catch (error) {
        showMessage('Ошибка подключения к серверу', 'error');
    }
}

// Отображение серверов
function displayServers(servers) {
    serversList.innerHTML = '';
    servers.forEach(server => {
        const serverId = Object.keys(server)[0];
        const serverName = server[serverId];

        const serverDiv = document.createElement('div');
        serverDiv.className = 'server-item';
        serverDiv.innerHTML = `
            <strong>${serverName}</strong><br>
            <small>ID: ${serverId}</small>
        `;
        serversList.appendChild(serverDiv);
    });
}

// Авторизация
loginForm.addEventListener('submit', async function(e) {
    e.preventDefault();

    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                username: username,
                password: password
            })
        });

        if (response.ok) {
            localStorage.setItem('isLoggedIn', 'true');
            showServers();
            showMessage('Успешная авторизация!');
        } else {
            showMessage('Неверные данные для входа', 'error');
        }
    } catch (error) {
        showMessage('Ошибка подключения', 'error');
    }
});

// Регистрация
registerForm.addEventListener('submit', async function(e) {
    e.preventDefault();

    const username = document.getElementById('reg-username').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;

    try {
        const response = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                username: username,
                email: email,
                password: password
            })
        });

        if (response.ok) {
            showMessage('Регистрация успешна! Теперь войдите в систему.');
            registerForm.reset();
        } else {
            const error = await response.json();
            showMessage(error.detail || 'Ошибка регистрации', 'error');
        }
    } catch (error) {
        showMessage('Ошибка подключения', 'error');
    }
});

// Выход
logoutBtn.addEventListener('click', function() {
    showAuth();
    showMessage('Вы вышли из системы');
});
