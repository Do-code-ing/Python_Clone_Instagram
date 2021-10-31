"use strict";

const genderSelectView = document.getElementById("gender-select-view");
const genderSelectFieldset = document.getElementById("gender-select-fieldset");

const genderBtn = document.getElementById("gender-btn");
if (genderBtn) {
  genderBtn.addEventListener("click", handleToggleGenderBtnClick);
}

function handleToggleGenderBtnClick() {
  document.body.append(genderSelectView);
}

if (genderSelectFieldset) {
  const maleRadio = genderSelectFieldset.querySelector("#male-radio");
  const femaleRadio = genderSelectFieldset.querySelector("#female-radio");
  const customRadio = genderSelectFieldset.querySelector("#custom-radio");
  const customText = genderSelectFieldset.querySelector("#custom-text");
  const concealRadio = genderSelectFieldset.querySelector("#conceal-radio");
  const radioArray = [maleRadio, femaleRadio, customRadio, concealRadio];

  if (customGender) {
    customText.value = customGender;
  }
  customText.remove();
  customText.style.display = "inline-block";

  function radioInitialize() {
    switch (currentGender) {
      case "male":
        maleRadio.checked = true;
        break;
      case "female":
        femaleRadio.checked = true;
        break;
      case "custom":
        customRadio.checked = true;
        customRadio.parentNode.append(customText);
        genderBtn.value = "custom";
        break;
      case "conceal":
        concealRadio.checked = true;
    }
  }

  radioInitialize();

  radioArray.forEach((radio) => {
    radio.addEventListener("change", (event) => {
      const currentRadio = event.target;
      if (currentRadio == customRadio) {
        customRadio.parentNode.append(customText);
      } else {
        customText.remove();
      }
    });
  });

  const genderValue = document.getElementById("gender-value");
  const genderSelectSubmitBtn = document.getElementById(
    "gender-select-submit-btn"
  );
  const genderSelectExitBtn = document.getElementById("gender-select-exit-btn");
  const backgroundDiv = document.getElementsByClassName("background-div");

  if (genderSelectSubmitBtn) {
    genderSelectSubmitBtn.addEventListener("click", (event) => {
      event.preventDefault();
      document.body.style.overflow = "hidden";
      genderSelectView.remove();
      radioArray.forEach((radio) => {
        if (radio.checked == true && radio == customRadio) {
          genderValue.value = customText.value;
          genderBtn.value = "custom";
          return;
        } else if (radio.checked) {
          genderValue.value = radio.id.slice(0, -6);
          genderBtn.value = radio.id.slice(0, -6);
          return;
        }
      });
    });
  }

  if (genderSelectExitBtn) {
    genderSelectExitBtn.addEventListener("click", (event) => {
      document.body.style.overflow = "auto";
      genderSelectView.remove();
      radioInitialize();
      genderValue.value = currentGender;
      genderBtn.value = currentGender;
      if (customGender) {
        customText.value = customGender;
      }
    });
  }

  if (backgroundDiv) {
    Array.from(backgroundDiv).forEach((div) => {
      div.addEventListener("click", (event) => {
        genderSelectExitBtn.click();
      });
    });
  }
}

genderSelectView.remove();
genderSelectView.style.display = "block";
