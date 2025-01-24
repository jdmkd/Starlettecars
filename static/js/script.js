let menu = document.querySelector('#menu-btn');
let navbar = document.querySelector('.navbar');

menu.onclick = () =>{
  menu.classList.toggle('fa-times');
  navbar.classList.toggle('active');
}

if(document.querySelector('#login-btn')){
  document.querySelector('#login-btn').onclick = () =>{
    document.querySelector('.login-form-container').classList.toggle('active');
  }
  
  if(document.querySelector('#close-login-form')){
    document.querySelector('#close-login-form').onclick = () =>{
      document.querySelector('.login-form-container').classList.remove('active');
    }
  }

  if(document.querySelector('#signup-btn')){
    document.querySelector('#signup-btn').onclick = () =>{
      document.querySelector('.signup-form-container').classList.toggle('active');
      document.querySelector('.login-form-container').classList.remove('active');
    }
    if(document.querySelector('#close-signup-form')){
      document.querySelector('#close-signup-form').onclick = () =>{
        document.querySelector('.signup-form-container').classList.remove('active'); 
        // document.querySelector('.login-form-container').classList.remove('active');
                     
      }
    }
    if(document.querySelector('#login-btnx')){
      document.querySelector('#login-btnx').onclick = () =>{
        document.querySelector('.login-form-container').classList.toggle('active');
        document.querySelector('.signup-form-container').classList.remove('active');
      } 
    }
  }
}




// sidebar-btn
// Toggle sidebar visibility and button icon
let sidebarBtn = document.querySelector('#sidebar-btn');
let sidebar = document.querySelector('.sidebar');

sidebarBtn.onclick = () =>{

  sidebar.classList.toggle('active');
  sidebar.classList.toggle('hidden');
  // sidebar.classList.toggle('-translate-x-full'); // Toggles the sidebar visibility
  // sidebar.classList.toggle('translate-x-0'); // Makes sidebar visible when active
  
  // Rotate the button icon
  sidebarBtn.classList.toggle('rotate');
  sidebarBtn.classList.toggle('rotate-180');

}








window.onscroll = () =>{

  menu.classList.remove('fa-times');
  navbar.classList.remove('active');

  if(window.scrollY > 0){
    document.querySelector('.header').classList.add('active');
  }else{
    document.querySelector('.header').classList.remove('active');
  }

}










// vehicle checkout page
let checkout_btn = document.querySelector('.checkout_btn')
let checkout_form_container = document.querySelector('.checkout-form-container')
let close_checkout_form= document.querySelector('.close-checkout-form')
// checkout_btn.onclick = () =>{
//   checkout_form_container.classList.toggle('active');
// }
// close_checkout_form.onclick = () =>{
//   checkout_form_container.classList.remove('active');
// }


document.querySelector('.home').onmousemove = (e) =>{
  document.querySelectorAll('.home-parallax').forEach(elm =>{
    let speed = elm.getAttribute('data-speed');

    let x = (window.innerWidth - e.pageX * speed) / 90;
    let y = (window.innerHeight - e.pageY * speed) / 90;

    elm.style.transform = `translateX(${y}px) translateY(${x}px)`;

  });

};


// document.querySelector('.home').onmouseleave = (e) =>{
//   document.querySelectorAll('.home-parallax').forEach(e =>{
//     e.style.transform = `translateX(0px) translateY(0px)`;
//   });
// };


// vehicle card swiper slider using swiperjs

// var swiper = new Swiper(".vehicles-slider", {
//   grabCursor: false,
//   // centeredSlides: true,
//   spaceBetween: 20,
//   // loop:true,
//   autoplay: {
//     delay: 10000,
//     disableOnInteraction: false,
//   },
//   pagination: {
//     el: ".swiper-pagination",
//     clickable:true,
//   },
//   navigation: {
//     nextEl: '.swiper-button-next',
//     prevEl: '.swiper-button-prev',
//   },
//   breakpoints: {
//     480: {
//       slidesPerView: 1,
//     },
//     640: {
//       slidesPerView: 2,
//     },
//     768: {
//       slidesPerView: 1,
//     },
//     1024: {
//       slidesPerView: 1,
//     },
//   },
// });

