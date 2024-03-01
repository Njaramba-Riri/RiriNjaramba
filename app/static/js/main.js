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

document.addEventListener('DOMContentLoaded', (event) => {
    var message = document.getElementById("messages");
    var timer;

    function startTimer(){
        timer = setTimeout(function(){
            if(message){
                message.classList.add('clear');
            }
        }, 5000)
    }

    function stopTimer(){
        clearTimeout(timer)
    }

    if(message){
        message.addEventListener('mouseover', startTimer);
        message.addEventListener('mouseout', startTimer)
        message.addEventListener('click', function(){
            stopTimer();
            message.classList.add('clear');
        });

        startTimer();
    }
});
// document.addEventListener("DOMContentLoaded", ()=>{
//     const sidebar = document.getElementById("sidebar");

//     if (sidebar){
//         if(sidebar.classList.contains('active'))
//     }
// })
document.addEventListener("DOMContentLoaded", (event) => {
    var passwordField = document.querySelectorAll(".password-field");
    var togglePassword = document.querySelectorAll(".toggle-password");
    var error = document.querySelectorAll(".errors");
    var fields = document.querySelectorAll(".input");
    var form  = document.getElementById('auth');

    passwordField.forEach((field, index) => {
        var toggle = togglePassword[index];

        if(toggle){
            toggle.addEventListener('click', function(){
                if (field.type === 'password'){
                    field.type = 'text';
                    toggle.className = 'far fa-eye';
                }else{
                    field.type = 'password';
                    toggle.className = 'far fa-eye-slash';
                }
            });
        }
    });

    form.addEventListener('submit', function(e){
        e.prevebtDefault();
        if(error){
            fields.forEach((field) => {
                field.style.border = '2px solid red';
            })
        }else{
            fields.classList.remove('errors');
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const nav = document.querySelector("#nav");
    const sidebar = document.querySelector("html[sidebar-open] ")
    const close = document.querySelector(".close-button");
    const about = document.getElementById("about-me");
    const theme = document.getElementById("theme");

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
    about.addEventListener('click', function(){
        var targetAbout = document.getElementById("blogs");
        if (!targetAbout){
            targetAbout = document.createElement('div');
            targetAbout.id = 'whome';
            document.body.append(targetAbout);
        }

        targetAbout.scrollIntoView({behaviour: 'smooth'});

        setTimeout(function(){
            var url = document.getElementById('about-me').dataset.url;
            window.location.href = url;
        }, 500);
    });
    
    // if (theme){
    //     theme.addEventListener('click', function(){
    //         document.body.classList.toggle('dark-theme');
    //     });
    // }
    // function toggleTheme(){
    //     document.body.classList.toggle('dark-theme');

    //     var isDarkTheme = document.body.classList.contains('dark-theme');
    //     localStorage.setItem('theme', isDarkTheme ? 'dark': 'light');
    // }

    // var savedTheme = localStorage.getItem('theme');
    // if (savedTheme === 'dark'){
    //     document.body.classList.add('dark-theme');
    // }

    
    if(close){
        // close.style.background = 'red';
        close.addEventListener('click', ()=>{
            sidebar.style.display = 'none';
        })
    }

    const buttonMenu = document.querySelector("#menu-buttton");
    const closeSidebar = document.querySelector("#menu-button");
    const rootElement = document.documentElement;
    const home = document.getElementById('home');

    buttonMenu.addEventListener('click', (e) => {
        rootElement.toggleAttribute('sidebar-open');
    });
    closeSidebar.addEventListener('click', ()=>{
        rootElement.toggleAttribute('sidebar-open');
    });
    buttonMenu.addEventListener('mouseover', () =>{
        this.title = 'Close'
    });

    window.addEventListener('click', ()=>{
        if(! closeSidebar){
            rootElement.toggleAttribute('sidebar-open');
        }
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

});

document.addEventListener("DOMContentLoaded", (event) => {
    const openReplyButtons = document.querySelectorAll(".open-reply");
    const replyComments = document.querySelectorAll(".reply-comment");

    openReplyButtons.forEach((button, index) => {
        button.addEventListener("click", () => {
            // Toggle the "active" class on the corresponding reply comment
            replyComments[index].classList.toggle("active");
            // replyComments.forEach((otherComments) => {
            //     otherComments.classList.remove('active');
            // })
            
            // Update the button text
            if (replyComments[index].classList.contains("active")) {
                button.textContent = "Close discussion.";
                button.style.color = 'brown';
            } else {
                button.textContent = "Open discussion.";
                button.style.color = '';
            }
        });
    });
});
