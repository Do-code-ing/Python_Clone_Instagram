"use strict";

const mainImage = document.getElementById("id_image");

if (mainImage) {
  mainImage.addEventListener("change", (event) => {
    const input = event.target;
    const dummyImage = document.getElementById("profile-image");

    if (input.files && input.files[0]) {
      const reader = new FileReader();

      reader.onload = (event) => {
        dummyImage.src = event.target.result;
      };
      reader.readAsDataURL(input.files[0]);
    } else {
      dummyImage.src = "{{ user.user_image.image.url }}";
    }
  });
}
