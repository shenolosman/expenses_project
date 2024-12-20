const passwordField = document.querySelector("#passwordField");
const emailField = document.querySelector("#emailField");
const usernameField = document.querySelector("#usernameField");
const usernameFeedbackField = document.querySelector(".username-error");
const emailFeedbackField = document.querySelector(".email-error");
const passwordFeedbackField = document.querySelector(".password-error");
const showPasswordToggle = document.querySelector("#showPasswordToggle");
const submitBtn = document.querySelector(".submit-btn");

showPasswordToggle.addEventListener("click", handleToggleInput);

function handleToggleInput() {
  if (passwordField.type === "password") {
    passwordField.type = "text";
    showPasswordToggle.innerHTML = "Hide";
  } else {
    passwordField.type = "password";
    showPasswordToggle.innerHTML = "Show";
  }
}

usernameField.addEventListener("keyup", (e) => {
  const usernameVal = e.target.value;

  if (usernameVal.length > 0) {
    fetch("/authentication/validate-username", {
      method: "POST",
      body: JSON.stringify({ username: usernameVal }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.username_error) {
          submitBtn.setAttribute("disabled", true);
          usernameField.classList.add("is-invalid");
          usernameFeedbackField.style.display = "block";
          usernameFeedbackField.innerHTML = `<p>${data.username_error}</p>`;
        } else {
          submitBtn.removeAttribute("disabled");
          usernameField.classList.remove("is-invalid");
          usernameFeedbackField.style.display = "none";
        }
      });
  }
});

emailField.addEventListener("keyup", (e) => {
  const emailVal = e.target.value;

  if (emailVal.length > 0) {
    fetch("/authentication/validate-email", {
      method: "POST",
      body: JSON.stringify({ email: emailVal }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.email_error) {
          submitBtn.setAttribute("disabled", true);
          emailField.classList.add("is-invalid");
          emailFeedbackField.style.display = "block";
          emailFeedbackField.innerHTML = `<p>${data.email_error}</p>`;
        } else {
          submitBtn.removeAttribute("disabled");
          emailField.classList.remove("is-invalid");
          emailFeedbackField.style.display = "none";
        }
      });
  }
});
