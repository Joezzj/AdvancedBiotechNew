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
    console.log(dropDown);
    dropDown.className == "nav-links"
      ? (dropDown.className = "nav-links active")
      : (dropDown.className = "nav-links");
  });
};

/**
 * page drop
 */

window.addEventListener("beforeunload", (event) => {
  const dropDown = document.getElementById("dropDown");
  dropDown.className = "nav-links";
});
