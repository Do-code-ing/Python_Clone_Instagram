"use strict";

if (user == undefined) {
  location.reload();
}

const toggleBtns = document.getElementsByClassName("post-btn");
if (toggleBtns) {
  Array.from(toggleBtns).forEach((toggleBtn) => {
    toggleBtn.addEventListener("click", handleToggleBtnClick);
  });
}

function handleToggleBtnClick(event) {
  document.body.style.overflow = "hidden";
  const postAuthor = event.target.dataset.idOne;

  const postManageView = document.createElement("article");
  const backgroundDiv = document.createElement("div");
  const postManageBtns = document.createElement("div");

  const unFollowBtn = document.createElement("button");
  const unFollowA = document.createElement("a");
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
    const newURL = `${window.location.protocol}${window.location.host}${postURL}`;
    navigator.clipboard.writeText(newURL).then(() => {
      cancleBtn.click();
    });
  });

  unFollowBtn.addEventListener("click", (event) => {
    unFollowA.click();
  });

  updateBtn.addEventListener("click", (event) => {
    updateA.click();
  });

  deleteBtn.addEventListener("click", (event) => {
    deleteA.click();
  });

  updateA.href = updateURL;
  deleteA.href = deleteURL;
  unFollowA.href = followURL;

  if (isFollowing === "True") {
    unFollowA.append("팔로우 취소");
  } else {
    unFollowA.append("팔로우");
    unFollowA.style.color = "green";
  }
  unFollowBtn.append(unFollowA);
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
  postManageBtns.appendChild(copyLinkBtn);
  postManageBtns.appendChild(cancleBtn);

  postManageView.appendChild(backgroundDiv);
  postManageView.appendChild(postManageBtns);

  document.body.appendChild(postManageView);
}

// comment btn

const toggleCommentBtns = document.getElementsByClassName("comment-btn");
if (toggleCommentBtns) {
  Array.from(toggleCommentBtns).forEach((toggleBtn) => {
    toggleBtn.addEventListener("click", handleToggleCommentBtnClick);
  });
}

function handleToggleCommentBtnClick(event) {
  const commentPk = event.target.dataset.idOne;

  const postManageView = document.createElement("article");
  const backgroundDiv = document.createElement("div");
  const postManageBtns = document.createElement("div");

  const deleteBtn = document.createElement("button");
  const deleteA = document.createElement("a");
  const cancleBtn = document.createElement("button");

  postManageView.className = "post-manage-view";
  backgroundDiv.className = "background-div";
  postManageBtns.className = "post-manage-btns";
  deleteBtn.className = "post-manage-delete";
  cancleBtn.className = "post-manage-cancle";

  cancleBtn.addEventListener("click", (event) => {
    postManageView.remove();
  });

  backgroundDiv.addEventListener("click", (event) => {
    cancleBtn.click();
  });

  deleteBtn.addEventListener("click", (event) => {
    deleteA.click();
  });

  const newCommentURL = commentURL.replace("%E2%9D%A4", commentPk);
  deleteA.href = newCommentURL;

  deleteA.append("삭제");
  deleteBtn.append(deleteA);
  cancleBtn.append("취소");

  postManageBtns.appendChild(deleteBtn);
  postManageBtns.appendChild(cancleBtn);

  postManageView.appendChild(backgroundDiv);
  postManageView.appendChild(postManageBtns);

  document.body.appendChild(postManageView);
}
