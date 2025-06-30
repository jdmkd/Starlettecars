const forms = document.querySelector(".forms"),
pwShowHide = document.querySelectorAll(".eye-icon"),
links = document.querySelectorAll(".link");

pwShowHide.forEach(eyeIcon => {
eyeIcon.addEventListener("click", () => {
  let pwFields = eyeIcon.parentElement.parentElement.querySelectorAll(".password");
  
  pwFields.forEach(password => {
      if(password.type === "password"){
          password.type = "text";
          eyeIcon.classList.replace("bx-hide", "bx-show");
          return;
      }
      password.type = "password";
      eyeIcon.classList.replace("bx-show", "bx-hide");
  })
  
})
})      

links.forEach(link => {
link.addEventListener("click", e => {
 e.preventDefault(); //preventing form submit
 forms.classList.toggle("show-signup");
})
})



// Popup Message
let popup_message =document.querySelector(".popup_message");
let modal_box = document.querySelector(".modal_box");
let closeBtnx = document.querySelector(".close_btn");
// setTimeout(()=>{ //remove shake class after 500ms
//     popup_message.classList.toggle("active")
    // pField.classList.remove("shake");
  setTimeout(() => {
    if (document.querySelector(".popup_message.active")){
      // popup_message.classList.toggle("active")
      return true
    }
    else{
      popup_message.classList.toggle("active")
    }
  },100000)

document.querySelector(".modal_box").addEventListener("click", () => {
  popup_message.classList.toggle("active")
})

// Sidebar collapse/expand logic

document.addEventListener('DOMContentLoaded', function () {
  const sidebar = document.getElementById('sidebar');
  const toggleBtn = document.getElementById('sidebar-toggle');
  const sidebarLinks = document.querySelectorAll('.sidebar-link');

  // Sidebar toggle for mobile
  function openSidebar() {
    sidebar.classList.remove('-translate-x-full');
    sidebar.classList.add('translate-x-0');
    document.body.classList.add('sidebar-open');
  }
  function closeSidebar() {
    sidebar.classList.add('-translate-x-full');
    sidebar.classList.remove('translate-x-0');
    document.body.classList.remove('sidebar-open');
  }

  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      if (sidebar.classList.contains('-translate-x-full')) {
        openSidebar();
      } else {
        closeSidebar();
      }
    });
  }

  // Hide sidebar when clicking outside (mobile only)
  document.addEventListener('click', function (e) {
    if (
      window.innerWidth < 1024 &&
      sidebar &&
      !sidebar.contains(e.target) &&
      !toggleBtn.contains(e.target)
    ) {
      closeSidebar();
    }
  });

  // Prevent sidebar click from closing it
  if (sidebar) {
    sidebar.addEventListener('click', function (e) {
      e.stopPropagation();
    });
  }

  // Ensure sidebar is always visible on desktop
  function handleResize() {
    if (window.innerWidth >= 1024) {
      sidebar.classList.remove('-translate-x-full');
      sidebar.classList.add('translate-x-0');
    } else {
      sidebar.classList.add('-translate-x-full');
      sidebar.classList.remove('translate-x-0');
    }
  }
  window.addEventListener('resize', handleResize);
  handleResize();

  // Active state for sidebar links
  sidebarLinks.forEach(link => {
    if (link.href === window.location.href) {
      link.classList.add('bg-neutral-200', 'dark:bg-neutral-800', 'text-emerald-600');
    }
  });
});



