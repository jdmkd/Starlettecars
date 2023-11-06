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

