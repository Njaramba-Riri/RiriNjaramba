var share = document.querySelectorAll(".fa-share");
var shareable = document.querySelectorAll(".shareables");
var gear = document.querySelectorAll(".opts");
var options = [".edit"];
var opts = ['.del', '.ficha'];
var actuals = ['#del-blog', '#hide-blog'];
// var actuals = [".action-modal"];
var tag = document.querySelectorAll(".tag");

// Function to toggle visibility of shareable items
function toggleShareables(container) {
    // Find shareable items within the same container
    var shareables = container.querySelectorAll('.shareables');

    // Toggle the "active" class for shareable items within the same container
    shareables.forEach(function(shareable) {
        shareable.classList.toggle("active");
    });
}

// Event listener for share elements
document.querySelectorAll('.posted').forEach(function(container) {
    container.addEventListener('click', function(event) {
        // Find the closest .share element
        var shareElement = event.target.closest('.fa-share');
        
        // If .share element is found within the container
        if (shareElement && shareElement.closest('.posted') === container) {
            // Toggle visibility of shareable items within the same container
            toggleShareables(container);
        }
    });
});

// Close shareable items when mouse leaves the blog container
document.querySelectorAll('.posted').forEach(function(container) {
    container.addEventListener('mouseleave', function() {
        // Hide all shareable items within the container
        container.querySelectorAll('.shareables.active').forEach(function(shareable) {
            shareable.classList.remove("active");
        });
    });
});


// Function to toggle visibility of options
function toggleOptions(container) {
    // Find options within the same container
    var options = container.querySelectorAll('.options');

    // Toggle the "active" class for options within the same container
    options.forEach(function(option) {
        option.classList.toggle("active");

        // if(option.classList.contains("active")){
        //     window.addEventListener('click', function(event){
        //         option.classList.remove("active");
        //     });
        // }
    });

    // Close options when mouse leaves the blog container
    document.querySelectorAll('.blog').forEach(function(blg){
        blg.addEventListener("mouseleave", function(){
            setTimeout(function() {
                options.forEach(function(option) {
                    option.classList.remove("active");
                });
            }, 20);            
        });
    });
}

// Event listener for gear elements
document.querySelectorAll('.posted .opts').forEach(function(gear) {
    gear.addEventListener('click', function() {
        // Find the parent container of the clicked gear element
        var container = this.closest('.posted');

        // If container is found
        if (container) {
            // Toggle visibility of options within the same container
            toggleOptions(container);
        }
    });
});

// Check sessionStorage on page load and show previously visible options
document.addEventListener('DOMContentLoaded', function() {
    var containerId = sessionStorage.getItem('Options');
    if (containerId) {
        var container = document.getElementById(containerId);
        if (container) {
            toggleOptions(container);
        }
    }
});


var opts = ['.ficha', '.del'];
var actuals = ['#hide-blog', '#del-blog'];

// Add event listeners to elements within each "blog" container
document.querySelectorAll('.blog').forEach(function(container) {
    opts.forEach(function(opt, index) {
        var actions = container.querySelectorAll(opt);
        var actual = actuals[index];

        console.log("Actals ", index , actuals[index])
        actions.forEach(function(action) {
            action.addEventListener('click', function() {
                var modal = document.querySelector(actual);
                if (modal) {
                    modal.classList.add("active");
                }
            });
        });
    });

    // Add event listener to close button within each modal
    document.querySelectorAll('#close').forEach(function(closeBtn) {
        closeBtn.addEventListener('click', function() {
            document.querySelectorAll('.action-modal.active').forEach(function(modal) {
                modal.classList.remove("active");
            });
        });
    });

    // Add event listeners to proceed buttons within each modal
    document.querySelectorAll('.delete').forEach(function(proceedBtn) {
        proceedBtn.addEventListener('click', function() {
            // Add logic to handle proceed actions here
            opts.forEach((opt)=> {
                var actions = container.querySelectorAll(opt);

                actions.forEach((action)=>{
                    url = action.getAttribute("data-url");
                    window.location.href = url;
                });                
            });
        });
    });            
});



// Close modals when clicking outside of them
// window.addEventListener('click', function(event) {
//     if (!event.target.matches('.action-modal.active')) {
//         document.querySelectorAll('.action-modal.active').forEach(function(modal) {
//             modal.classList.remove("active");
//         });
//     }
// });


options.forEach(function(option){
    var actions = document.querySelectorAll(option);

    actions.forEach(function(action){
        action.addEventListener('click', ()=>{
            url = action.getAttribute("data-url");
            window.location.href = url;
        });                
    });
});

tag.forEach(function(toTag){
    toTag.addEventListener('click', ()=>{
        var url = toTag.getAttribute("data-url");
        setTimeout(function(){
            window.location.href = url;
        }, 100);
    });
});
