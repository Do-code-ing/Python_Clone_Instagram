"use strict";

const toggleBtns = document.getElementsByClassName("post-btn");
if (toggleBtns) {
  Array.from(toggleBtns).forEach((toggleBtn) => {
    toggleBtn.addEventListener("click", handleToggleBtnClick);
  });
}

function handleToggleBtnClick(event) {
  document.body.style.overflow = "hidden";
  const postAuthor = event.target.dataset.idOne;
  const postPk = event.target.dataset.idTwo;

  const postManageView = document.createElement("article");
  const backgroundDiv = document.createElement("div");
  const postManageBtns = document.createElement("div");

  const unFollowBtn = document.createElement("button");
  const unFollowA = document.createElement("a");
  const goToPostBtn = document.createElement("button");
  const goToPostA = document.createElement("a");
  const updateBtn = document.createElement("button");
  const updateA = document.createElement("a");
  const deleteBtn = document.createElement("button");
  const deleteA = document.createElement("a");
  const copyLinkBtn = document.createElement("button");
  const cancleBtn = document.createElement("button");

  postManageView.className = "post-manage-view";
  backgroundDiv.className = "background-div";
  postManageBtns.className = "post-manage-btns";
  unFollowBtn.className = "post-manage-unfollow";
  goToPostBtn.className = "post-manage-gotopost";
  updateBtn.className = "post-manage-update";
  deleteBtn.className = "post-manage-delete";
  copyLinkBtn.className = "post-manage-copylink";
  cancleBtn.className = "post-manage-cancle";

  cancleBtn.addEventListener("click", (event) => {
    postManageView.remove();
  });

  backgroundDiv.addEventListener("click", (event) => {
    cancleBtn.click();
  });

  copyLinkBtn.addEventListener("click", (event) => {
    const newURL = `${window.location.protocol}${window.location.host}${newPostURL}`;
    navigator.clipboard.writeText(newURL).then(() => {
      cancleBtn.click();
    });
  });

  unFollowBtn.addEventListener("click", (event) => {
    unFollowA.click();
  });

  goToPostBtn.addEventListener("click", (event) => {
    goToPostA.click();
  });

  updateBtn.addEventListener("click", (event) => {
    updateA.click();
  });

  deleteBtn.addEventListener("click", (event) => {
    deleteA.click();
  });

  const newPostURL = postURL.replace("%E2%9D%A4", postPk);
  const newUpdateURL = updateURL.replace("%E2%9D%A4", postPk);
  const newDeleteURL = deleteURL.replace("%E2%9D%A4", postPk);
  const newFollowURL = followURL.replace("%E2%9D%A4", postAuthor);

  goToPostA.href = newPostURL;
  updateA.href = newUpdateURL;
  deleteA.href = newDeleteURL;
  unFollowA.href = newFollowURL;

  unFollowA.append("팔로우 취소");
  unFollowBtn.append(unFollowA);
  goToPostA.append("게시물로 이동");
  goToPostBtn.append(goToPostA);
  updateA.append("수정");
  updateBtn.append(updateA);
  deleteA.append("삭제");
  deleteBtn.append(deleteA);
  copyLinkBtn.append("링크 복사");
  cancleBtn.append("취소");

  if (postAuthor === user) {
    postManageBtns.appendChild(updateBtn);
    postManageBtns.appendChild(deleteBtn);
  } else {
    postManageBtns.appendChild(unFollowBtn);
  }
  postManageBtns.appendChild(goToPostBtn);
  postManageBtns.appendChild(copyLinkBtn);
  postManageBtns.appendChild(cancleBtn);

  postManageView.appendChild(backgroundDiv);
  postManageView.appendChild(postManageBtns);

  document.body.appendChild(postManageView);
}
