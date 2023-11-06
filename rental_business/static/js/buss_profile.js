// document.querySelector('#home-tab').onclick = () =>{
//     document.querySelector('#home').classList.toggle('active');
// } 
document.querySelector('#profile').style.display = 'none';

document.querySelector('#profile-tab').onclick = () =>{
    document.querySelector('#profile-tab').classList.toggle('active');
    document.querySelector('#profile').classList.toggle('active');
    document.querySelector('#home-tab').classList.remove('active');
    document.querySelector('#home').classList.remove('active');

    document.querySelector('#home').style.display = 'none';
    document.querySelector('#profile').style.display = '';
    
}
  
document.querySelector('#home-tab').onclick = () =>{
    document.querySelector('#home-tab').classList.toggle('active');
    document.querySelector('#profile').classList.remove('active');
    document.querySelector('#profile-tab').classList.remove('active');
    document.querySelector('#home').classList.toggle('active');          

    document.querySelector('#profile').style.display = 'none';
    document.querySelector('#home').style.display = '';
}
