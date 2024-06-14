function serializeForm(form) {
  return new FormData(form);
}

async function sendData(data) {
  return await fetch(window.location.origin + "/api/v1/registration", {
    method: "POST",
    headers: {
      accept: "application/json",
    },
    body: data,
  });
}

async function handleFormSubmit(event) {
  event.preventDefault();
  const spinner = document.getElementById("spnr");
  spinner.classList.remove("visually-hidden");
  button = document.getElementById("reg-btn").disabled = true;
  const data = serializeForm(applicantForm);
  const response = await sendData(data);

  if (response.ok) {
    document.getElementById("valid-fbck").innerHTML =
      "Check email for verification message";
  } else {
    await response.json().then((err) => {
      document.getElementById("invalid-fbck").innerHTML = err["detail"];
    });
  }
  spinner.classList.add("visually-hidden");
  button = document.getElementById("reg-btn").disabled = false;
}

const applicantForm = document.getElementById("reg_form");
applicantForm.addEventListener("submit", handleFormSubmit);
