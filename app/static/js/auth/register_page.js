async function go_to_main(){
    window.location.href = 'http://127.0.0.1:8000/restaurant/restaurant_main_page.html';
};

async function go_to_menu(){
    window.location.href = 'http://127.0.0.1:8000/restaurant/menu.html';
};
function go_to_login() {
    window.location.href = "'http://127.0.0.1:8000/auth/login_page.html";
}

async function go_to_booking(){
    window.location.href = 'http://127.0.0.1:8000/restaurant/book_table.html';
};

async function regFunction(event){
    event.preventDefault()
    alert('скрипт запущен');

    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = '';

    // Validate username
    if (username.length < 3) {
        errorMessage.textContent = 'Имя пользователя должно быть не короче 3 символов';
        return false;
    }

    // Validate email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        errorMessage.textContent = 'Введите корректный адрес электронной почты';
        return false;
    }

    // Validate password
    if (password.length < 6) {
        errorMessage.textContent = 'Пароль должен быть не короче 6 символов';
        return false;
    }

    const registrationData = {
        user_name: username,
        email_address: email,
        password: password
    };

    try{
        const response = await fetch('http://127.0.0.1:8000/auth/register/', {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(registrationData)
        });
        
        if (response.ok) {
            // Registration successful
            alert('Регистрация успешна!');
            // Optional: Redirect to login page or dashboard
            window.location.href = 'http://127.0.0.1:8000/auth/login_page.html';
        } else {
            // Handle registration errors
            const errorData = await response.json();
            errorMessage.textContent = errorData.message || 'Ошибка регистрации';
        }
    }catch (error)
    {
        alert(error);
        errorMessage.textContent = 'Произошла ошибка. Пожалуйста, попробуйте снова.';
    }
};
