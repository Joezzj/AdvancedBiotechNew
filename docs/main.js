/**
 * base device show/hide menu-toggle
 * @param elements - menu-toggle DOM elememt
 * @param userAgent - user agent object
 */

function checkDevice(userAgent, elements) {
  if (/mobile|android|iphone|ipad|phone/i.test(userAgent)) {
    elements
      ? (elements.style.display = "block")
      : console.log("Cant find toggle element");
  } else {
    elements
      ? (elements.style.display = "none")
      : console.log("Cant find toggle element");
  }
}

/**
 *  page init loading
 */

window.onload = function () {
  const userAgent = navigator.userAgent.toLowerCase();
  const elements = document.getElementById("menu-toggle");
  const dropDown = document.getElementById("dropDown");

  checkDevice(userAgent, elements); //menu-toggle show/hide
  //add click listner to menu-toggle
  elements.addEventListener("click", () => {
    dropDown.className == "nav-links"
      ? (dropDown.className = "nav-links active")
      : (dropDown.className = "nav-links");
  });

  document
    .getElementById("contactForm")
    .addEventListener("submit", async function (e) {
      document.getElementById("submit").disabled = true;
      e.preventDefault();
      const form = {
        name: this.name.value,
        email: this.email.value,
        message: this.message.value,
      };
      const result = await sendEmail(form);
      if (result.success) {
        alert("successful sent");
      } else {
        alert("fail sent:" + result.error);
      }
      document.getElementById("submit").disabled = false;
    });
};

/**
 * page drop
 */

window.addEventListener("beforeunload", (event) => {
  const dropDown = document.getElementById("dropDown");
  dropDown.className = "nav-links";
});

/**
 * api send request
 */

function sendEmail(form) {
  return new Promise((resolve, reject) => {
    fetch("http://localhost:5000/send_mail", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(form),
    })
      .then((response) => response.json())
      .then((data) => {
        resolve(data);
      });
  });
}
