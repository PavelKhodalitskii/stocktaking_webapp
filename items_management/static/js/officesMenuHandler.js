const menu_button = document.getElementById("menu_button")
const office_menu = document.getElementById("office_menu")
// office_menu.style.display = 'none';

const close_button = document.getElementById("close_button")

const showSideMenu = () => {
    if ( office_menu.style.display != 'none') {
        office_menu.style.display = 'none';
    } else {
        office_menu.style.display = 'block';
    }
};

menu_button.addEventListener("click", showSideMenu);
close_button.addEventListener("click", showSideMenu);