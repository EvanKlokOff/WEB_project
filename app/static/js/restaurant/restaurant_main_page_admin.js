async function show_menu(){
    window.location.href="http://127.0.0.1:8000/restaurant/menu.html"
}
async function login(){
    window.location.href="http://127.0.0.1:8000/auth/login_page.html"
}
async function register(){
    window.location.href="http://127.0.0.1:8000/auth/register_page.html"
}
async function show_admin_panel(){
    window.location.href="http://127.0.0.1:8000/restaurant/admin_panel.html"
}
async function show_personal_account(){
    window.location.href="http://127.0.0.1:8000/restaurant/personal_account.html"
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
            window.location.href="http://127.0.0.1:8000/auth/login_page.html"
        }
}