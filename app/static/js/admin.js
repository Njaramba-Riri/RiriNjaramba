const clickables = [".savigation ul .item", ".savigation ul #dropdown #drop",
                    ".savigation ul #dropdown .drop-item", ".paginaation li"];
const content = document.getElementById("page-content");

// Function to load content into page-content element
function loadContent(url, clickedElementId) {
    fetch(url)
        .then(response => response.text())
        .then(data => {
            content.innerHTML = data;

            history.pushState({ page: url}, "", url);
            // Save loaded page URL and clicked element ID to sessionStorage
            sessionStorage.setItem('loadedPage', url);
            sessionStorage.setItem('clickedElementId', clickedElementId);

            // Remove 'hovered' class from all clickable elements
            document.querySelectorAll(clickables.join(', ')).forEach(item => {
                item.classList.remove('hovered');
            });

            // Add 'hovered' class to clicked element
            const clickedElement = document.getElementById(clickedElementId);
            if (clickedElement) {
                clickedElement.classList.add('hovered');
            }
        })
        .catch(error => console.error("Error:", error));
}

// Event delegation for click events on common ancestor
document.addEventListener('click', function(event) {
    const target = event.target;

    if (clickables.some(selector => target.matches(selector))) {
        event.preventDefault();

        // Remove active and hovered classes from all items
        document.querySelectorAll(clickables.join(', ')).forEach(item => {
            item.classList.remove('active', 'hovered');
        });

        // Add active and hovered classes to clicked item
        target.classList.add('active', 'hovered');

        // Load content from data-url attribute
        const url = target.getAttribute("data-url");
        if (url) {
            const clickedElementId = target.id;
            loadContent(url, clickedElementId);
        }

        return false;
    }
});

// Retrieve and load previously loaded page from sessionStorage on page load
const loadedPage = sessionStorage.getItem('loadedPage');
const clickedElementId = sessionStorage.getItem('clickedElementId');
if (loadedPage) {
    // Load the previously loaded page content
    loadContent(loadedPage, clickedElementId);
}

window.addEventListener('popstate', function(event){
    const state = event.state;
    if (state && state.page){
        loadContent(state.page);
    }
});

var actions = [".enable", ".disable", ".delete"]
var blogs = document.querySelectorAll(".toBlog");

actions.forEach((click)=>{
    var cElements = document.querySelectorAll(click);
    cElements.forEach(function(clickee){
        clickee.addEventListener('click', function(){
            window.location.href = this.getAttribute('data-url');
        });
    });
});

blogs.forEach(function(clickMe){
    clickMe.addEventListener('click', function(){
        url = clickMe.getAttribute("data-url");
        window.location.href = url;                
    });
});
