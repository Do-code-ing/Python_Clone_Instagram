"use strict";

const toggleBtns = document.getElementsByClassName("post-btn");
if (toggleBtns) {
  Array.from(toggleBtns).forEach((toggleBtn) => {
    toggleBtn.addEventListener("click", handleToggleBtnClick);
  });
}

function handleToggleBtnClick(event) {
  const postManageView = document.createElement("article");
  const backgroundDiv = document.createElement("div");
  const postManageBtns = document.createElement("div");
  const unFollowBtn = document.createElement("button");
  const goToPostBtn = document.createElement("button");
  const updateBtn = document.createElement("button");
  const deleteBtn = document.createElement("button");
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

  unFollowBtn.append("팔로우 취소");
  goToPostBtn.append("게시물로 이동");
  updateBtn.append("수정");
  deleteBtn.append("삭제");
  copyLinkBtn.append("링크 복사");
  cancleBtn.append("취소");

  postManageBtns.appendChild(unFollowBtn);
  postManageBtns.appendChild(goToPostBtn);
  postManageBtns.appendChild(updateBtn);
  postManageBtns.appendChild(deleteBtn);
  postManageBtns.appendChild(copyLinkBtn);
  postManageBtns.appendChild(cancleBtn);

  postManageView.appendChild(backgroundDiv);
  postManageView.appendChild(postManageBtns);

  document.body.appendChild(postManageView);
}
