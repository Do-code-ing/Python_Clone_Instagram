"use strict";

const submitBtn = document.getElementById("submit-btn");
const realSubmitBtn = document.getElementById("real-submit-btn");

if (submitBtn) {
  submitBtn.addEventListener("click", (event) => {
    realSubmitBtn.click();
  });
}

const slideImages = document.getElementsByClassName("slide-image");
Array.from(slideImages).forEach((slideImage) => {
  let fileCount = parseInt(slideImage.dataset.id) + 1;
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
  if (fileCount == 1) {
    nextBtn.style.display = "none";
  }
  prevBtn.addEventListener("click", prev);
  nextBtn.addEventListener("click", next);
});

// tag list

const mainCommentInput = document.getElementById("id_main_comment");
if (mainCommentInput) {
  tagList.forEach((tag) => {
    mainCommentInput.value += `${tag} `;
  });
}
