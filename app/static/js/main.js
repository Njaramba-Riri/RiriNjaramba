document.addEventListener('DOMContentLoaded', ()=>{
    var loader = document.getElementById("loader");
    var content = document.querySelector(".home");

    window.addEventListener('load', () => {
        if(content && loader){
            loader.classList.add('hidden');
            content.classList.add('visible');
        }else{
            loader.classList.remove('hidden');
        }
    });   
});

document.addEventListener('DOMContentLoaded', () => {
    const nav = document.querySelector("#nav");
    const sidebar = document.querySelector("html[sidebar-open] ")

    window.addEventListener('scroll', () => {
       if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20){
            if (sidebar){
                nav.classList.remove('scrolled');
            }else{
                nav.classList.add('scrolled');
            }
        }else{
            nav.classList.remove('scrolled');
        } 
    });

    const buttonMenu = document.querySelector("#menu-button");
    const rootElement = document.documentElement;
    const home = document.getElementById('home');

    buttonMenu.addEventListener('click', (e) => {
        rootElement.toggleAttribute('sidebar-open');
    });
    buttonMenu.addEventListener('mouseover', () =>{
        this.title = 'Close'
    });

    home.addEventListener('click', () => {
        window.location.href = "{{ url_for('mainapp.index') }}"
    });

    var service = document.getElementById("service");
    var project = document.getElementById("project");
    var quote = document.getElementById("quote");

    service.addEventListener('click', ()=> {
        let services = document.getElementById("services");
        if(services){
            services.scrollIntoView({behaviour: 'smooth'});
        }
    });
    project.addEventListener('click', () => {
        let projects = document.getElementById("projects");
        if(projects){
            projects.scrollIntoView({behavior: 'smooth'});
        }
    });
    quote.addEventListener('click', ()=>{
        const contact = document.getElementById('contacts');
        if(contact){
            contact.scrollIntoView({behaviour: 'smooth'});
        }
    });
});

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

document.addEventListener("DOMContentLoaded", () => {
    var search = document.getElementById("search-blog");
    let search_term = ''
    
    search.addEventListener('keyup', e => {
        search_term = e.target.value;
    })

})