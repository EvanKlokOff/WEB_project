async function go_to_main_page(){
    window.location.href="http://127.0.0.1:8000/restaurant/restaurant_main_page.html"
}

async function cancel_booking(event) {
    event.preventDefault()
    // Получаем кнопку, на которую нажали
    const button = event.target;
    // Получаем id кнопки (btn_id: {{order.user.id}})
    const user_id = button.getAttribute('id').split(": ")[1];
    // Получаем элемент заказа, который содержит данные о бронировании
    const orderItem = button.closest('.order-item');
    const orderDate = orderItem.querySelector('.date').textContent.split(': ')[1];
    // Создаем объект с данными для отправки
    alert(orderDate)

    const json_data = {
        user_id: user_id,
        order_time: orderDate
    };
    try
    {
        const response = await fetch("http://127.0.0.1:8000/restaurant/free_table_for_authorized_user/", {
                method: 'DELETE',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(json_data)
            });

        if (response.ok) {
            // Если запрос успешен, удаляем элемент заказа из DOM
            orderItem.remove();
            alert('Бронирование успешно отменено!');
        } else {
            // Если произошла ошибка, выводим сообщение
            alert('Ошибка при отмене бронирования. Попробуйте снова.');
        }
    }catch{
        alert('Произошла ошибка при отправке запроса.');
    };
}

async function logout(event){
    event.preventDefault()

    try{
        const response = await fetch('http://127.0.0.1:8000/auth/logout/', {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            //Registration successful
            //alert('Вход прошёл успешно!');
            window.location.href = 'http://127.0.0.1:8000/restaurant/restaurant_main_page.html';
        } else {
            // Handle registration errors
            const errorData = await response.json();
        }
    }catch (error)
    {
        alert(error);
        errorMessage.textContent = 'Произошла ошибка. Пожалуйста, попробуйте снова.';
    }
    window.location.href="http://127.0.0.1:8000/restaurant/restaurant_main_page.html"
}

//эти действия требуют повторной авторизации

function change_user(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение кнопки

    // кнопка на которую нажали
    const button = event.target;
    const user_id = button.getAttribute('id').split(": ")[1];
    
    // Создаем форму для изменения данных
    const form = document.createElement('form');
    form.id = 'change-user-form';

    form.innerHTML = `
        <label for="new-username">Новое имя:</label>
        <input type="text" id="new-username" name="new-username">

        <label for="new-email">Новый Email:</label>
        <input type="email" id="new-email" name="new-email">

        <label for="new-password">Новый пароль:</label>
        <input type="password" id="new-password" name="new-password">

        <label for="current-password">Текущий пароль (для подтверждения):</label>
        <input type="password" id="current-password" name="current-password" required>

        <button type="submit">Сохранить изменения</button>
        <button type="button" onclick="cancelChange()">Отмена</button>
    `;

    // Добавляем форму в секцию профиля
    const profileSection = document.getElementById('profile');
    profileSection.appendChild(form);

    // Обработчик отправки формы
    form.addEventListener('submit', async function (e) {
        e.preventDefault(); // Предотвращаем стандартную отправку формы

        // Собираем данные из формы
        const newUsername = document.getElementById('new-username').value;
        const newEmail = document.getElementById('new-email').value;
        const newPassword = document.getElementById("new-password").value;
        const currentPassword = document.getElementById('current-password').value;

        if(!newUsername && !newEmail && !newPassword){
            alert("Пожалуйста заполните хотябы одно поле");
            return;
        }

        if(!currentPassword){
            alert("Пожалуйста введите текущий пароль, чтобы подтвердить изменения");
            return;
        }

        const user_change_info={}

        const user_credential={
            id: user_id,
            password: currentPassword
        }

        if(newUsername)user_change_info.user_name = newUsername;
        if(newEmail)user_change_info.email_address=newEmail;
        if(newPassword)user_change_info.password=newPassword;

        const json_data={
            user_credential: user_credential,
            user_change_info: user_change_info
        }
        // Проверяем авторизацию (отправляем текущий пароль на сервер для подтверждения)
        try {
            const response = await fetch('http://127.0.0.1:8000/auth/change_user_by_user/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(json_data)
            });

            if (response.ok) {
                alert('Данные успешно изменены.');
                window.location.reload(); // Перезагружаем страницу для обновления данных
            } else {
                alert('Ошибка при изменении данных: ');
            }
        } catch (error) {
            alert('Произошла ошибка при отправке данных.');
            alert(error);
        }
    });
}

function cancelChange() {
    // Удаляем форму изменения данных
    const form = document.getElementById('change-user-form');
    if (form) {
        form.remove();
    }
}