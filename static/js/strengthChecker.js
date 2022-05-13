// Checks the strength of password and displays bars showing strength

// Constants to use in checking strength of password
const indicator = document.querySelector(".indicator");
const input = document.querySelector("#password");
const weak = document.querySelector(".weak");
const medium = document.querySelector(".medium");
const strong = document.querySelector(".strong");
const text = document.querySelector(".text");
const showBtn = document.querySelector(".showBtn");
let regExpWeak = /[a-z]/;
let regExpMedium = /\d+/;
let regExpStrong = /.[!,@,#,$,%,^,&,*,?,_,~,-,(,)]/;

// Runs every keyup on password
function trigger(){
  if(input.value != ""){
  medium.classList.add("hideColor");
  strong.classList.add("hideColor");
  indicator.style.display = "block"
  indicator.style.display = "flex"
  if(input.value.length <= 3 && (input.value.match(regExpWeak) || input.value.match(regExpMedium) || input.value.match(regExpStrong)))no=1;
  if(input.value.length >= 6 && ((input.value.match(regExpWeak) && input.value.match(regExpMedium)) || (input.value.match(regExpMedium) && input.value.match(regExpStrong)) || (input.value.match(regExpWeak) && input.value.match(regExpStrong))))no=2;
  if(input.value.length >= 6 && input.value.match(regExpWeak) && input.value.match(regExpMedium) && input.value.match(regExpStrong))no=3; 
  if(no==1){
  // weak.classList.add("active");
    text.style.display = "block";
    text.textContent = "Your password is too weak";
    text.classList.add("weak");
  }
  if(no==2){
    medium.classList.remove("hideColor");
    console.log(medium)
    text.textContent = "Your password is medium";
    text.classList.add("medium");
  }else{
    // medium.classList.add("hideColor");
    text.classList.remove("medium");
  }
  if(no==3){
    medium.classList.remove("hideColor");
    strong.classList.remove("hideColor");  
    text.textContent = "Your password is strong";
    text.classList.add("strong");
  }else{
      // strong.classList.remove("hideColor");
      text.classList.remove("strong");
  }

  showBtn.style.display = "block";
  showBtn.onclick = function(){
    if(input.type == "password"){
      input.type = "text";
      showBtn.textContent = "HIDE";
      showBtn.style.color = "#23ad5c";
    }else{
      input.type = "password";
      showBtn.textContent = "SHOW";
      showBtn.style.color = "#000";
    }
  }
  }else{
  indicator.style.display = "none";
  text.style.display = "none";
  showBtn.style.display = "none";
  }
}

// Makes sure passwords are valid
function validPassword()
{ 
    // Gets variables to check
    let strongPass = document.querySelector("span.strong")
    let pass = document.getElementById("password").value
    let confirmPass = document.getElementById("confirmPassword").value

    // Makes sure password is strong.
    if (strongPass.classList.contains("hideColor"))
    {
        swal({
            title: "Not Yet!",
            text: "You need a strong password",
            icon: "warning",
          });
        return false
    }
    // Makes sure password and confirm password are the same
    if (pass != confirmPass)
    {
        swal({
            title: "Look Closer!",
            text: "Passwords must be the same",
            icon: "warning",
          });
        return false
    }
    return true
}

// const togglePassword = document.querySelector('.togglePassword');
// function showPass()  {
//   // toggle the type attribute
//   const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
//   password.setAttribute('type', type);
//   // toggle the eye slash icon
//   this.classList.toggle('fa-eye-slash');
// }
