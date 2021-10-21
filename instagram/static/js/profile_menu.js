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

// search function

const searchForm = document.getElementById("search-form");
const searchInput = document.getElementById("search-input");
const searchHref = document.getElementById("search-href");
searchForm.addEventListener("submit", (event) => {
  event.preventDefault();
  let value = searchInput.value;
  if (value[0] == "#") {
    value = "%23" + value.slice(1);
  } else if (value[0] == "!") {
    value = "%21" + value.slice(1);
  }
  searchHref.href = searchURL.replace("%E2%9D%A4", value);
  searchHref.click();
});
