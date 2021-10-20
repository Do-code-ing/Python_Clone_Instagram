"use strict";

const submitBtn = document.getElementById("submit-btn");
const realSubmitBtn = document.getElementById("real-submit-btn");

if (submitBtn) {
  submitBtn.addEventListener("click", (event) => {
    realSubmitBtn.click();
  });
}

const mainImage = document.getElementById("id_main_image");
const mainImageBtn = document.getElementById("main-image-btn");
const dummyImage = document.getElementById("dummy-image");

mainImageBtn.addEventListener("click", (event) => {
  mainImage.click();
});

if (mainImage) {
  mainImage.addEventListener("change", (event) => {
    const input = event.target;

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
const multipleContainer = document.getElementById("multiple-container");
const subImageBtn = document.getElementById("sub-image-btn");

subImageBtn.addEventListener("click", (event) => {
  inputImage.click();
});

if (inputImage) {
  inputImage.addEventListener("change", (event) => {
    const input = event.target;
    const filesLength = input.files.length;

    while (multipleContainer.hasChildNodes()) {
      multipleContainer.removeChild(multipleContainer.firstChild);
    }

    if (filesLength > 0) {
      const fileArray = Array.from(input.files);

      fileArray.forEach((file) => {
        const reader = new FileReader();
        const div = document.createElement("div");
        const img = document.createElement("img");
        div.appendChild(img);

        reader.onload = (event) => {
          img.src = event.target.result;
          img.className = "post-image";

          multipleContainer.appendChild(div);
        };
        reader.readAsDataURL(file);
      });
    } else {
      const img = document.createElement("img");
      img.className = "post-image";
      img.src = "/static/image/dummy_image.jpg";
      multipleContainer.appendChild(img);
    }
  });
}

const slideImages = document.getElementsByClassName("slide-image");
Array.from(slideImages).forEach((slideImage) => {
  inputImage.addEventListener("change", (event) => {
    const input = event.target;
    const filesLength = input.files.length;
    fileCount = filesLength;

    if (fileCount > 1) {
      nextBtn.style.display = "flex";
    } else {
      prevBtn.style.display = "none";
      nextBtn.style.display = "none";
      curPos = 0;
      position = 0;
    }
  });

  let fileCount;
  let curPos = 0;
  let position = 0;
  const IMAGE_WIDTH = 544;
  const prevBtn = slideImage.childNodes[1];
  const nextBtn = slideImage.childNodes[3];
  const image = slideImage.childNodes[5];

  function prev() {
    if (curPos > 0) {
      nextBtn.style.display = "flex";
      position -= IMAGE_WIDTH;
      image.scrollLeft = position;
      curPos--;
    }
    if (curPos == 0) {
      prevBtn.style.display = "none";
    }
  }

  function next() {
    if (curPos < fileCount) {
      prevBtn.style.display = "flex";
      position += IMAGE_WIDTH;
      image.scrollLeft = position;
      curPos++;
    }
    if (curPos == fileCount - 1) {
      nextBtn.style.display = "none";
    }
  }

  prevBtn.style.display = "none";
  nextBtn.style.display = "none";
  prevBtn.addEventListener("click", prev);
  nextBtn.addEventListener("click", next);
});
