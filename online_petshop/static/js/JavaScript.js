//  INPUT SEARCH IN NAVBAR
document.getElementById('search-input').addEventListener('focus', function() {
  document.body.classList.add('focused');
  document.getElementById('overlay').style.display = 'block';
});
document.getElementById('search-input').addEventListener('blur', function() {
  document.body.classList.remove('focused');
  document.getElementById('overlay').style.display = 'none';
});

// PRODUCT SLIDER
$(document).ready(function() {
  $(".owl-carousel").owlCarousel({
    rtl: true, // فعال کردن حالت راست به چپ
    items: 7,
    loop: true,
    margin: 15,
    nav: false,
    autoplay: true,
    autoplayTimeout: 3000,
    autoplayHoverPause: true,
    responsive: {
      0: {
        items: 2
      },
      600: {
        items: 5
      },
      1000: {
        items: 7
      }
    }
  });
});
let items = document.querySelectorAll('.item');

// اضافه کردن event listeners برای هر item
items.forEach(item => {
    item.addEventListener('mouseover', function() {
        this.classList.add('shadow');
    });

    item.addEventListener('mouseout', function() {
        this.classList.remove('shadow');
    });
});

// Example of custom JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
  console.log("Custom JS loaded");
});
