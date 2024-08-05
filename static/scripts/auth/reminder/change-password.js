const params = new URL(document.location.toString()).searchParams;
const token = params.get("token");

function serializeForm(form) {
  return new FormData(form);
}

async function sendData(data) {
  return await fetch(window.location.origin + "/api/v1/login/recover", {
    method: "PATCH",
    headers: {
      accept: "application/json",
    },
    body: data,
  });
}

async function handleFormSubmit(event) {
  event.preventDefault();

  const pwd = document.getElementById("pwd");
  const pwdConfirm = document.getElementById("pwd-confirm");
  const invalidFbk = document.getElementById("invalid-fbck");
  invalidFbk.innerHTML = "";

  if (pwd.value != pwdConfirm.value) {
    invalidFbk.innerHTML = "Password aren't equal";
  } else {
    const spinner = document.getElementById("spnr");
    spinner.classList.remove("visually-hidden");
    button = document.getElementById("btn").disabled = true;

    const data = serializeForm(applicantForm);
    data.append("token", token);
    const response = await sendData(data);

    if (response.ok) {
      validFbkDiv = document.getElementById("valid-fbck").innerHTML =
        "The password has been changed";
      document.getElementById("href-log-page").textContent =
        "Back to login page";
    } else {
      await response.json().then((err) => {
        invalidFbk.innerHTML = err["detail"];
      });
    }
    spinner.classList.add("visually-hidden");
    button = document.getElementById("btn").disabled = false;
  }
}

const applicantForm = document.getElementById("form");
applicantForm.addEventListener("submit", handleFormSubmit);
