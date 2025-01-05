function show_main_page(){
    window.location.href="http://127.0.0.1:8000/restaurant/restaurant_main_page.html"
}
async function book_table(){
        const response = await fetch("http://127.0.0.1:8000/restaurant/book_table.html", {
            method: 'GET',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });
        if (response.ok){
            window.location.href="http://127.0.0.1:8000/restaurant/book_table.html"
        }else{
            window.location.href="http://127.0.0.1:8000/auth/enter_page.html"
        }
}