/*
jQuery for homepage carousel controls
*/
// Controls carousel auto-scroll time.
$('#homepageCarousel').carousel({
  interval: 1000 * 6  // 1000 ms * # sec
});


/*
JS controls for scroll animations, via https://github.com/jlmakes/scrollreveal
*/
// Making delay, transition distance, and viewFactor mass-changeable.
var standard_delay      = 2000;
var standard_distance   = '500px';
var standard_viewFactor = 0.5;

// Initializing ScrollReveal object.
window.sr               = new ScrollReveal();
// Navbar reveal.
sr.reveal('.navbar', {
    duration: standard_delay
});

/* HOMEPAGE TRANSITIONS */
// Slideshow reveal.
sr.reveal('#Homepage', {
    duration: standard_delay
});
// Subjects section left side reveal.
sr.reveal('#Subjects, #subjects-left', {
    duration: standard_delay * 0.75,
    origin: 'left',
    distance: standard_distance,
    viewFactor: standard_viewFactor
});
// Subjects section right side reveal.
sr.reveal('#subjects-right', {
    duration: standard_delay * 1.5,
    origin: 'left',
    distance: standard_distance * .5,
    viewFactor: standard_viewFactor
});
// About section reveal.
sr.reveal('#About', {
    duration: standard_delay * 0.75,
    origin: 'right',
    distance: standard_distance,
    viewFactor: standard_viewFactor
});

/* REGISTER PAGE TRANSITIONS */
sr.reveal('#Register', {
    duration: standard_delay * .75,
    origin: 'bottom',
    distance: standard_distance
});

/* Login PAGE TRANSITIONS */
sr.reveal('#Login', {
    duration: standard_delay * .75,
    origin: 'bottom',
    distance: standard_distance
});
