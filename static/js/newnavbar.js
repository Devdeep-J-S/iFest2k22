function sidebar_open() {
    document.getElementById('open_icon').style.display = 'none';
    document.querySelector('.navbar-container').style.transform =
        'translateX(0px)';
}

function sidebar_close() {
    document.querySelector('.navbar-container').style.transform =
        'translateX(-100%)';
    document.getElementById('open_icon').style.display = 'block';
}

window.addEventListener(
    'click',
    (e) => {
        if (!e.target.classList.contains('open_icon_button')) {
            if (!e.target.classList.contains('navbar-property')) {
                sidebar_close();
            }
        }
    },
    { capture: true }
);
