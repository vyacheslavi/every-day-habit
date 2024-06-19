const button = document.getElementById("vrfct-btn");
const textDiv = document.getElementsByClassName("card-text")[0];
const text = document.getElementById("text");
const card = document.getElementsByClassName("card")[0];
const cardBody = document.getElementsByClassName("card-body")[0];

async function sendRequestVerification(token) {
  return await fetch(
    window.location.origin + `/api/v1/login/verificator/?token=${token}`,
    {
      method: "GET",
    }
  );
}

button.addEventListener("click", async () => {
  const params = new URL(document.location.toString()).searchParams;
  const token = params.get("token");
  var response = await sendRequestVerification(token);
  button.classList.add("d-none");
  if (response.ok) {
    card.classList.add("text-bg-success");
    text.textContent = "";
    const link = document.createElement("a");
    link.setAttribute("href", "/login");
    link.textContent = "Back to the login page";
    cardBody.appendChild(link);
  } else {
    card.classList.add("text-bg-danger");
    await response.json().then((err) => {
      textDiv.innerHTML = `<p>${err["detail"]}</p>`;
    });
  }
});
