/* Hangarin custom scripts */
document.addEventListener("DOMContentLoaded", function() {
    // 1. Trigger the Page Fade-In
    document.body.classList.add('page-loaded');

    // 2. Smooth "Pre-loader" for Links
    // When clicking "Edit" or "Add Task", fade out slightly before moving
    const links = document.querySelectorAll('a:not([target="_blank"]):not([href^="#"])');
    links.forEach(link => {
        link.addEventListener('click', e => {
            // Ignore if it's a simple toggle or button-like link
            if (link.classList.contains('no-anim')) return;

            e.preventDefault();
            let targetUrl = link.href;
            document.body.style.opacity = '0';
            
            setTimeout(() => {
                window.location.href = targetUrl;
            }, 300); // Matches CSS transition time
        });
    });

    // 3. Initialize Tooltips (For the Edit/Delete icons)
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[title]'))
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
});
