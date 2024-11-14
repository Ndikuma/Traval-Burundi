function toggleNavbar() {
    const navbarMobile = document.getElementById('navbar-mobile');
    navbarMobile.classList.toggle('hidden');
}
  const carouselWrapper = document.getElementById('carouselWrapper');
    const slides = document.querySelectorAll('.carousel-slide');
    let currentIndex = 0;
    const slideInterval = 3000; // Slide interval in milliseconds (3 seconds)

    function moveCarousel(direction) {
        currentIndex += direction;

        // Loop to first/last slide if at the end/start
        if (currentIndex < 0) {
            currentIndex = slides.length - 1;
        } else if (currentIndex >= slides.length) {
            currentIndex = 0;
        }

        // Move the wrapper to show the current slide
        carouselWrapper.style.transform = `translateX(-${currentIndex * 100}%)`;
    }

    // Set up the automatic carousel sliding
    setInterval(() => {
        moveCarousel(1);
    }, slideInterval);