"use strict";

const inputImage = document.getElementById("input-multiple-image");
inputImage.addEventListener("change", (event) => {
  const input = event.target;
  const multipleContainer = document.getElementById("multiple-container");

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
