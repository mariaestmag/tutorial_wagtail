//Script para navbar semitransparente con scrolling

$(document).ready(function () {
    // Transition effect for navbar 
    $(window).scroll(function () {
      // checks if window is scrolled more than 100px, adds/removes navbar-opacity class
      if ($(this).scrollTop() > 100) {
        $('.navbar').addClass('navbar-opacity');
      } else {
        $('.navbar').removeClass('navbar-opacity');
      }
    });
  });