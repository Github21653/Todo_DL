document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const logoutBtn = document.getElementById('logout-btn');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            try {
                const response = await axios.post('/api/login/', { username, password });
                localStorage.setItem('access_token', response.data.access);
                localStorage.setItem('refresh_token', response.data.refresh);
                window.location.href = '/tasks';
            } catch (error) {
                alert('Login failed: ' + error.response.data.detail);
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            try {
                await axios.post('/api/register/', { username, password });
                window.location.href = '/login';
            } catch (error) {
                alert('Registration failed: ' + error.response.data.detail);
            }
        });
    }

    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/login';
        });
    }
});