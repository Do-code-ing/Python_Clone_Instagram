"use strict";

const posts = document.getElementsByClassName("profile-post");

if (posts) {
  Array.from(posts).forEach((post) => {
    const background = post.querySelector(".profile-post-background");
    const info = post.querySelector(".profile-post-info");
    post.addEventListener("mouseover", (event) => {
      background.style.display = "block";
      info.style.display = "flex";
    });

    post.addEventListener("mouseleave", (event) => {
      background.style.display = "none";
      info.style.display = "none";
    });
  });
}
