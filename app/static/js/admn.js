function sidebarClick(event){
    const element  = event.target;
    if (element.tagName === 'LI' || element.className === 'drop-item'){
        document.querySelectorAll('.savigation li', '.savigation #dropdown .drop-item').forEach(item =>{
            item.classList.remove('active', 'hovered');
        });

        element.classList.add('active', 'hovered');

        sessionStorage.setItem('activeSideItem', element.id || 'default');
    }
}

document.querySelector('.savigation',  '.savigation #dropdown .drop-item').addEventListener('click', sidebarClick);

function loadContent(){
    const activeItemId = sessionStorage.getItem("activeSideItem");
    const sectionId = activeItemId || 'default';

    document.querySelectorAll('section').forEach(section =>{
        section.style.display = 'none';
    });
    
    const section = document.getElementById(sectionId);
    if (section){
        section.style.display = 'block';
    }     
}

window.addEventListener('DOMContentLoaded', loadContent);
