document.addEventListener('DOMContentLoaded', () => {
    const controls = document.querySelectorAll('.slider');
    
    function activeLi() {
        controls.forEach((item) => {
            item.classList.remove('active');
        });
        this.classList.add('active');
    }

    controls.forEach((control) => {
        control.addEventListener('click', activeLi);
    });
});


window.addEventListener('scroll', function(){
    var contacts = document.querySelector(".icons a");
    var position = contacts.getBoundingClientRect();

    if(position.top >= 0 && position.bottom <= window.innerHeight){
        contacts.style.animation = '1s ease-in-out forwards sliders';
    }
});