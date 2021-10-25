const slideImages = document.getElementsByClassName("slide-image");
Array.from(slideImages).forEach((slideImage) => {
  let fileCount = parseInt(slideImage.dataset.id) + 1;
  console.log(fileCount);
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
