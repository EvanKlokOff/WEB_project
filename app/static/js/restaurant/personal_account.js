async function go_to_main_page(){
    window.location.href="http://127.0.0.1:8000/restaurant/restaurant_main_page.html"
}

async function cancel_booking(event){

}

async function change_password(){

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