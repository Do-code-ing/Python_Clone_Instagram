"use strict";

const changeBtn = document.getElementById("change-profile-image-btn");
const imagePicker = document.getElementById("id_image");

if (imagePicker) {
  imagePicker.addEventListener("change", (event) => {
    changeBtn.click();
  });
}
