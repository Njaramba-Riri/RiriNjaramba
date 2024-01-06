document.addEventListener("DOMContentLoaded", (event) => {
    let sliders = document.querySelectorAll('.carousel-indicators li')

    function activeLink(){
        sliders.forEach((item) => {
            item.classList.remove('active');
        });
        this.classList.add('active');
    }

    sliders.forEach((item) => {
        item.addEventListener('click', activeLink);
    });
});