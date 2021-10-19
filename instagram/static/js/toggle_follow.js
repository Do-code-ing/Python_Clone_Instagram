"use strict";

const toggleFollowBtn = document.getElementsByClassName("unfollow-btn");
if (toggleFollowBtn) {
  Array.from(toggleFollowBtn).forEach((toggleBtn) => {
    toggleBtn.addEventListener("click", handleToggleFollowBtnClick);
  });
}

function handleToggleFollowBtnClick(event) {
  const followName = event.target.dataset.idOne;

  const postManageView = document.createElement("article");
  const backgroundDiv = document.createElement("div");
  const postManageBtns = document.createElement("div");

  const unFollowBtn = document.createElement("button");
  const unFollowA = document.createElement("a");
  const cancleBtn = document.createElement("button");

  postManageView.className = "post-manage-view";
  backgroundDiv.className = "background-div";
  postManageBtns.className = "post-manage-btns";
  unFollowBtn.className = "post-manage-unfollow";
  cancleBtn.className = "post-manage-cancle";

  cancleBtn.addEventListener("click", (event) => {
    postManageView.remove();
  });

  backgroundDiv.addEventListener("click", (event) => {
    cancleBtn.click();
  });

  unFollowBtn.addEventListener("click", (event) => {
    unFollowA.click();
  });

  const newFollowURL = followURL.replace("%E2%9D%A4", followName);

  unFollowA.href = newFollowURL;

  unFollowA.append("팔로우 취소");
  unFollowBtn.append(unFollowA);
  cancleBtn.append("취소");

  postManageBtns.appendChild(unFollowBtn);
  postManageBtns.appendChild(cancleBtn);

  postManageView.appendChild(backgroundDiv);
  postManageView.appendChild(postManageBtns);

  document.body.appendChild(postManageView);
}
