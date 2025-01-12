async function book_table(event){
    event.preventDefault()

    const order_time = document.getElementById('datetime').value;
    const guests_number = document.getElementById('guests').value;
    const extra_wishes = document.getElementById('comments').value.trim();
    const errorMessage = document.getElementById('errorMessage');

    alert("got data")
    if(!order_time || !guests_number){
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

        // Проверяем тип ответа
        const contentType = response.headers.get('content-type');

        if (response.ok) {
            // Успешное бронирование
            alert('Ваш столик забронирован!');
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
        errorMessage.textContent = error;
    }
}


async function loadPage(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const html = await response.text();
        return html;
    } catch (error) {
        console.error("Error loading page:", error);
        return null;
    }
}

function executeScripts(container) {
    const scripts = container.querySelectorAll("script");
    scripts.forEach((script) => {
        const newScript = document.createElement("script");
        if (script.src) {
            newScript.src = script.src;
        } else {
            newScript.textContent = script.textContent;
        }
        document.body.appendChild(newScript);
    });
}

async function renderPage(url, targetElementId) {
    const html = await loadPage(url);

    if (html) {
        const targetElement = document.getElementById(targetElementId);

        if (targetElement) {
            targetElement.innerHTML = html;
            executeScripts(targetElement);
        } else {
            console.error(`Target element with id "${targetElementId}" not found.`);
        }
    }
}