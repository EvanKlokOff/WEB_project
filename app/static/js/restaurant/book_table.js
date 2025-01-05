async function book_table(event){
    event.preventDefault()

    const order_time = document.getElementById('datetime').value;
    const guests_number = document.getElementById('guests').value;
    const extra_wishes = document.getElementById('comments').value.trim();
    const errorMessage = document.getElementById('errorMessage');

    alert("got data")
    if(!order_time || !guests_number || !extra_wishes){
        alert("выберете все поля");
        errorMessage.textContent="выберете все поля";
        return
    }
    
    errorMessage.textContent = '';
    const localDate = new Date(order_time)
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

    const booking_data = {
        order_time: order_time_iso,
        guest_amount: guests_number,
        extra_wishes: extra_wishes
    };

    // Здесь будет логика проверки авторизации
    //alert('Выполняется вход. Email: ' + email);
    try{
        alert("booking start")
        const response = await fetch('http://127.0.0.1:8000/restaurant/book_table/', {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(booking_data)
        });

        if (response.ok) {
            //Registration successful
            alert('Ваш столик забронирован!');
            window.location.href = 'http://127.0.0.1:8000/restaurant/restaurant_main_page.html';
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