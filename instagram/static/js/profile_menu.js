"use strict";

const profileBtn = document.getElementById("nav-profile");
const profileMenu = document.getElementById("nav-profile-menu");
profileBtn.addEventListener("click", (event) => {
  event.preventDefault();
  profileMenu.style.display = "flex";
});

function handleMouseUp(event) {
  profileMenu.style.display = "none";
}

window.addEventListener("mouseup", handleMouseUp);
