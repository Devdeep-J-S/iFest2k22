responsiveness();
window.addEventListener('resize', () => {
    responsiveness();
})

function responsiveness() {
    let screenwidth = window.innerWidth;
    if (screenwidth < 780) {
        document.getElementById('large-screen').style.display = 'none';
        document.getElementById('mobile-screen').style.display = 'block';
    }
    else {
        document.getElementById('large-screen').style.display = 'block';
        document.getElementById('mobile-screen').style.display = 'none';
    }
}
