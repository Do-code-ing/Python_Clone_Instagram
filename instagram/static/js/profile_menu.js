"use strict";

const profileBtn = document.getElementById("nav-profile");
const profileMenu = document.getElementById("nav-profile-menu");

if (profileBtn) {
  profileBtn.addEventListener("click", (event) => {
    event.preventDefault();
    profileMenu.style.display = "flex";
  });
  window.addEventListener("mouseup", handleMouseUp);
}

function handleMouseUp(event) {
  profileMenu.style.display = "none";
}
