// vehicle checkout page
let checkout_btn = document.querySelector('.checkout_btn')
let checkout_form_container = document.querySelector('.checkout-form-container')
let close_checkout_form= document.querySelector('.close-checkout-form')

checkout_btn.onclick = () =>{
  checkout_form_container.classList.toggle('active');
}
close_checkout_form.onclick = () =>{
  checkout_form_container.classList.remove('active');
}