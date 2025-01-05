function show_main_page(){
    window.location.href="http://127.0.0.1:8000/restaurant/restaurant_main_page.html"
}

// Функция для отправки данных на сервер в формате JSON
async function add_new_menu(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение формы (перезагрузку страницы)

    // Получаем значения из формы
    const mealName = document.getElementById('meal_name').value;
    const mealDescription = document.getElementById('meal_description').value;
    const mealCost = document.getElementById('meal_cost').value;
    const mealType = document.getElementById('meal_type').value;
    const mealImage = document.getElementById('meal-image').files[0];
    // Проверяем, что все поля заполнены
    if (!mealName || !mealDescription || !mealCost || !mealType || !mealImage) {
        alert('Пожалуйста, заполните все поля и выберите изображение.');
        return;
    }

    // Преобразуем изображение в base64
    const reader = new FileReader();
    reader.onload = async function () {
        const base64Image = reader.result.split(',')[1]; // Убираем префикс "data:image/..."

        // Создаем объект JSON для отправки
        const data = {
            food_name: mealName,
            food_description: mealDescription,
            food_cost: mealCost,
            food_type: mealType,
            food_image: base64Image, // Изображение в формате base64
        };

        try {
            // Отправляем POST-запрос на сервер
            const response = await fetch('http://127.0.0.1:8000/restaurant/add_new_menu', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', // Указываем, что отправляем JSON
                },
                body: JSON.stringify(data), // Преобразуем объект в JSON
            });

            // Проверяем ответ сервера
            if (response.ok) {
                const result = await response.json();
                alert('Блюдо успешно добавлено!');
                console.log('Ответ сервера:', result);
            } else {
                const error = await response.json();
                alert('Ошибка при добавлении блюда: ' + error.message);
                console.error('Ошибка:', error);
            }
        } catch (error) {
            alert('Произошла ошибка при отправке запроса.');
            console.error('Ошибка:', error);
        }
    };

    // Читаем файл как Data URL (base64)
    reader.readAsDataURL(mealImage);
}

async function change_menu(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение формы (перезагрузку страницы)

    //получаем выбранное блюдо, которое будем изменять
    const updated_value = document.getElementById('updated_menu').value;
    const data = JSON.parse(updated_value);
    const food_photo_path = data.food_photo_path;
    const id = data.id;
    const food_name = data.food_name

    if (!id || !food_photo_path || !food_name) {
        alert('Пожалуйста выберете блюдо, которое хотите изменить');
        return;
    }

    // Получаем значения из формы, на которые нужно менять
    const mealName_to_update = document.getElementById('updated_meal_name').value;
    const mealDescription_to_update = document.getElementById('updated_meal_description').value;
    const mealCost_to_update = document.getElementById('updated_meal_cost').value;
    const mealType_to_update = document.getElementById('update_meal_type').value;
    const mealImage_to_update = document.getElementById('update_meal_image').files[0];
    // Проверяем, что все поля заполнены
    if (!mealName_to_update && !mealDescription_to_update && !mealCost_to_update && !mealType_to_update && !mealImage_to_update) {
        alert('Пожалуйста, заполните хотя бы одно поле или выберите изображение.');
        return;
    }

    // Преобразуем изображение в base64
    const reader = new FileReader();
    reader.onload = async function () {
        const base64Image = reader.result.split(',')[1]; // Убираем префикс "data:image/..."

        const menu_info = {
            id: id,
            food_photo_path: food_photo_path
        }
        // Создаем объект JSON для отправки
        const change_menu_info = {
            food_name: mealName_to_update,
            food_description: mealDescription_to_update,
            food_cost: mealCost_to_update,
            food_type: mealType_to_update,
            food_image: base64Image, // Изображение в формате base64
        };

        const data = {
            menu_info:menu_info,
            change_menu_info: change_menu_info
        }

        try {
            // Отправляем POST-запрос на сервер
            const response = await fetch('http://127.0.0.1:8000/restaurant/change_menu', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json', // Указываем, что отправляем JSON
                },
                body: JSON.stringify(data), // Преобразуем объект в JSON
            });

            // Проверяем ответ сервера
            if (response.ok) {
                const result = await response.json();
                alert('Блюдо успешно добавлено!');
                console.log('Ответ сервера:', result);
            } else {
                const error = await response.json();
                alert('Ошибка при добавлении блюда: ' + error.message);
                console.error('Ошибка:', error);
            }
        } catch (error) {
            alert('Произошла ошибка при отправке запроса.');
            console.error('Ошибка:', error);
        }
    };

    // Читаем файл как Data URL (base64)
    reader.readAsDataURL(mealImage_to_update);
}

async function delete_menu(event){
    event.preventDefault(); // Предотвращаем стандартное поведение формы (перезагрузку страницы)
    // Получаем значения из формы
    const deleted_value = document.getElementById('deleted_menu').value;
    const data = JSON.parse(deleted_value);
    const food_photo_path = data.food_photo_path;
    const id = data.id;
    // Проверяем, что все поля заполнены
    if (!id || !food_photo_path) {
        alert('Пожалуйста, заполните поле');
        return;
    }
    const json_data = {
        id: id,
        food_photo_path: food_photo_path
    };
    try {
        // Отправляем POST-запрос на сервер
        const response = await fetch('http://127.0.0.1:8000/restaurant/delete_menu', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json', // Указываем, что отправляем JSON
            },
            body: JSON.stringify(json_data), // Преобразуем объект в JSON
        });

        // Проверяем ответ сервера
        if (response.ok) {
            const result = await response.json();
            alert('Блюдо успешно удалено!');
        } else {
            const error = await response.json();
            alert('Ошибка при удалении блюда: ' + error.message);
        }
    }catch (error) {
        alert('Произошла ошибка при отправке запроса.');
        console.error('Ошибка:', error);
    }

}

async function add_user(event){
    event.preventDefault(); // Предотвращаем стандартное поведение формы (перезагрузку страницы)

    // Получаем значения из формы
    const user_name = document.getElementById('added_user_name').value;
    const email_addres = document.getElementById('added_email_addres').value;
    const user_password = document.getElementById('added_user_password').value;
    const user_role = document.getElementById('added_user_role').value;
    
    // Проверяем, что все поля заполнены
    if (!user_name || !email_addres || !user_password || !user_role){
        alert('Пожалуйста, заполните все поля.');
        return;
    }
    const json_data = {
        user_name:user_name,
        email_address:email_addres,
        user_role:user_role,
        password:user_password
    }
    try {
        // Отправляем POST-запрос на сервер
        const response = await fetch('http://127.0.0.1:8000/auth/register/', {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json', // Указываем, что отправляем JSON
            },
            body: JSON.stringify(json_data), // Преобразуем объект в JSON
        });

        // Проверяем ответ сервера
        if (response.ok) {
            const result = await response.json();
            alert('Новый пользователь добавлен');
        } else {
            const error = await response.json();
            alert('Ошибка при добавлении пользователя: ' + error.message);
        }
    }catch (error) {
        alert('Произошла ошибка при отправке запроса.');
        console.error('Ошибка:', error);
    }

}

async function change_user(event){
    event.preventDefault();
    const id = document.getElementById("updated_user").value
    if (!id){
        alert("Выберете пользователя, которого хотите изменить");
        return;
    }
    const user_info ={
        id:id
    }

    // Получаем значения из формы, на которые нужно менять
    const user_name_to_update = document.getElementById('update_user_name').value;
    const user_email_address_to_update = document.getElementById('update_user_email_address').value;
    const password_to_update = document.getElementById('update_new_password').value;
    const user_role_to_update = document.getElementById('new_user_role').value;

    // Проверяем, что все поля заполнены
    if (!user_name_to_update && !user_email_address_to_update && !password_to_update && !user_role_to_update) {
        alert('Пожалуйста, заполните хотя бы одно поле');
        return;
    }
    
    const new_data={
        user_name: user_name_to_update,
        password:password_to_update,
        email_address:user_email_address_to_update,
        user_role:user_role_to_update
    }    
    const json_data = {
        user_info:user_info,
        new_data:new_data
    }

    try {
        // Отправляем POST-запрос на сервер
        const response = await fetch('http://127.0.0.1:8000/auth/change_user/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json', // Указываем, что отправляем JSON
            },
            body: JSON.stringify(json_data), // Преобразуем объект в JSON
        });

        // Проверяем ответ сервера
        if (response.ok) {
            const result = await response.json();
            alert('пользователь успешно изменён!');
        } else {
            const error = await response.json();
            alert('Ошибка при изменении пользователя: ' + error.message);
        }
    }catch (error) {
        alert('Произошла ошибка при отправке запроса.');
        console.error('Ошибка:', error);
    }    

}

async function delete_user(event){
    event.preventDefault(); // Предотвращаем стандартное поведение формы (перезагрузку страницы)
    // Получаем значения из формы
    const id = document.getElementById('deleted_user').value;
    // Проверяем, что все поля заполнены
    if (!id) {
        alert('Пожалуйста, заполните поле');
        return;
    }
    const json_data = {
        id: id
    };
    try {
        // Отправляем POST-запрос на сервер
        const response = await fetch('http://127.0.0.1:8000/auth/delete_user/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json', // Указываем, что отправляем JSON
            },
            body: JSON.stringify(json_data), // Преобразуем объект в JSON
        });

        // Проверяем ответ сервера
        if (response.ok) {
            const result = await response.json();
            alert('Пользователь успешно удалён!');
        } else {
            const error = await response.json();
            alert('Ошибка при удалении пользователя: ' + error.message);
        }
    }catch (error) {
        alert('Произошла ошибка при отправке запроса.');
        console.error('Ошибка:', error);
    }
}

async function book_table(event){
    event.preventDefault();
    const booking_user_id = document.getElementById("booking_user_id").value
    const booking_guests_quantity = document.getElementById("booking_guests_quantity").value
    const booking_date = document.getElementById("booking_date").value
    const booking_guest_comments = document.getElementById("booking_guest_comments").value
    
    if (!booking_user_id || !booking_guests_quantity || !booking_date){
        alert("Выберете все поля");
        return;
    };

    const localDate = new Date(booking_date)
    const utcDate = new Date(
        Date.UTC(
            localDate.getFullYear(),
            localDate.getMonth(),
            localDate.getDate(),
            localDate.getHours(),
            localDate.getMinutes(),
            localDate.getSeconds()
        )
    );

    const order_time_iso = utcDate.toISOString().slice(0,-5)

    const json_data = {
        order_time: order_time_iso,
        guest_amount: booking_guests_quantity,
        extra_wishes: booking_guest_comments,
        user_id: booking_user_id
    };

    try{
        alert("booking start")
        const response = await fetch('http://127.0.0.1:8000/restaurant/book_table/', {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(json_data)
        });

        if (response.ok) {
            //Registration successful
            alert('Ваш столик забронирован!');
        } else {
            // Handle registration errors
            const errorData = await response.json();
            errorMessage.textContent = errorData.message || 'Ошибка регистрации';
        }
    }catch (error)
    {
        errorMessage.textContent = error;
    }

}

async function free_table(event){
    event.preventDefault();
    const freed_table_info = document.getElementById("freed_table_info").value;
    const data = JSON.parse(freed_table_info);
    const order_time = data.order_time;
    const table_id = data.table_id;
    const user_id = data.user_id;

    if(!order_time || !table_id || !user_id){
        alert("Заполните все поля");
        return;
    }

    const json_data={
        order_time: order_time,
        table_id: table_id,
        user_id: user_id
    }
    
    try {
        // Отправляем POST-запрос на сервер
        const response = await fetch('http://127.0.0.1:8000/restaurant/free_table/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json', // Указываем, что отправляем JSON
            },
            body: JSON.stringify(json_data), // Преобразуем объект в JSON
        });

        // Проверяем ответ сервера
        if (response.ok) {
            const result = await response.json();
            alert('Столик освобожден!');
        } else {
            const error = await response.json();
            alert('Ошибка при освобождении столика' + error.message);
        }
    }catch (error) {
        alert('Произошла ошибка при отправке запроса.');
        console.error('Ошибка:', error);
    }   

}

async function change_booking_table(event){
    event.preventDefault();
    const freed_table_info = document.getElementById("update_booking_table").value;
    const data = JSON.parse(freed_table_info);
    
    const order_time = data.order_time;
    const table_id = data.table_id;
    const user_id = data.user_id;

    if(!order_time || !table_id || !user_id){
        alert("Заполните все поля");
        return;
    }
    const order_info={
        order_time: order_time,
        table_id: table_id,
        user_id: user_id
    }

    const update_guests_quantity = document.getElementById("update_guest_amount").value
    const update_order_date = document.getElementById("update_order_date").value
    const update_guest_comments = document.getElementById("update_guest_comments").value
    
    if(!update_guests_quantity && !update_order_date && !update_guest_comments){
        alert("Заполните хотя бы одно поле");
        return;
    }

    const booking_info={
        order_time: update_order_date,
        guest_amount: update_guests_quantity,
        user_id: user_id,
        extra_wishes:update_guest_comments
    }

    const json_data={
        order_info: order_info,
        booking_info: booking_info
    }
    try {
        // Отправляем POST-запрос на сервер
        const response = await fetch('http://127.0.0.1:8000/restaurant/change_table/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json', // Указываем, что отправляем JSON
            },
            body: JSON.stringify(json_data), // Преобразуем объект в JSON
        });

        // Проверяем ответ сервера
        if (response.ok) {
            const result = await response.json();
            alert('Бронирование изменено!');
        } else {
            const error = await response.json();
            alert('Ошибка при изменении бронирования: ' + error.message);
        }
    } catch (error) {
        alert('Произошла ошибка при отправке запроса.');
        console.error('Ошибка:', error);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    function previewImage(event, previewId) {
        //alert('Функция previewImage вызвана');
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                //alert('Изображение загружено, отрисовываем превью');
                const preview = document.getElementById(previewId);
                preview.innerHTML = `<img src="${e.target.result}" alt="Превью изображения">`;
            };
            reader.readAsDataURL(file);
        }
    }

    document.getElementById('meal_image').addEventListener('change', function (event) {
        //alert('Изменение в meal-image');
        previewImage(event, 'image_preview');
    });

    document.getElementById('update_meal_image').addEventListener('change', function (event) {
        //alert('Изменение в update-meal-image');
        previewImage(event, 'update_image_preview');
    });
});