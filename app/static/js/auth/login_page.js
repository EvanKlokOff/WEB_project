async function login(event){
    event.preventDefault()

    const email_address = document.getElementById('email').value;
    const password = document.getElementById('password').value.trim();
    const user_name = document.getElementById('user_name').value;
    const errorMessage = document.getElementById('errorMessage');

    errorMessage.textContent = '';
    if (user_name.length < 3) {
        errorMessage.textContent = 'Имя пользователя должно быть не короче 3 символов';
        return false;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email_address)) {
        errorMessage.textContent = 'Введите корректный адрес электронной почты';
        return false;
    }

    if (password.length < 6) {
        errorMessage.textContent = 'Пароль должен быть не короче 6 символов';
        return false;
    }

    const loginData = {
        user_name: user_name,
        email_address: email_address,
        password: password
    };

    // Здесь будет логика проверки авторизации
    //alert('Выполняется вход. Email: ' + email);
    try{
        const response = await fetch('http://127.0.0.1:8000/auth/login/', {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        });

        if (response.ok) {
            //Registration successful
            //alert('Вход прошёл успешно!');
            window.location.href = 'http://127.0.0.1:8000/restaurant/restaurant_main_page.html';
        } else {
            // Если ответ — HTML, открываем его в новом окне
            const html = await response.text();
            const newWindow = window.open("about:blank", "_blank");
            newWindow.document.write(html);
            newWindow.document.close();
        }
    }catch (error)
    {
        alert(error);
        errorMessage.textContent = 'Произошла ошибка. Пожалуйста, попробуйте снова.';
    }
};

async function go_to_main(){
    window.location.href = 'http://127.0.0.1:8000/restaurant/restaurant_main_page.html';
};

async function go_to_menu(){
    window.location.href = 'http://127.0.0.1:8000/restaurant/menu.html';
};

async function go_to_register(){
    window.location.href = 'http://127.0.0.1:8000/auth/register_page.html';
};

async function go_to_booking(){
    window.location.href = 'http://127.0.0.1:8000/restaurant/book_table.html';
};