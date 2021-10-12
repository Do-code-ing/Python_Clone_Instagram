"use strict";

const mainImage = document.getElementById("id_main_image");

if (mainImage) {
  mainImage.addEventListener("change", (event) => {
    const input = event.target;
    const dummyImage = document.getElementById("dummy_image");

    if (input.files && input.files[0]) {
      const reader = new FileReader();

      reader.onload = (event) => {
        dummyImage.src = event.target.result;
      };
      reader.readAsDataURL(input.files[0]);
    } else {
      dummyImage.src = "/static/image/dummy_image.jpg";
    }
  });
}

const inputImage = document.getElementById("id_image");

if (inputImage) {
  inputImage.addEventListener("change", (event) => {
    const input = event.target;
    const multipleContainer = document.getElementById("multiple_container");

    while (multipleContainer.hasChildNodes()) {
      multipleContainer.removeChild(multipleContainer.firstChild);
    }

    if (input.files) {
      const fileArray = Array.from(input.files);

      fileArray.forEach((file) => {
        const reader = new FileReader();
        const div = document.createElement("div");
        const img = document.createElement("img");

        div.appendChild(img);

        reader.onload = (event) => {
          img.src = event.target.result;
          img.style.width = "200px";
          img.style.height = "auto";

          multipleContainer.appendChild(div);
        };
        reader.readAsDataURL(file);
      });
    }
  });
}
