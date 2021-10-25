"use strict";

const changeBtn = document.getElementById("change-profile-image-btn");
const imagePicker = document.getElementById("id_user_image");

if (imagePicker) {
  imagePicker.addEventListener("change", (event) => {
    changeBtn.click();
  });
}

// gender btn

const genderSelectView = document.getElementById("gender-select-view");
const genderSelectFieldset = document.getElementById("gender-select-fieldset");

if (genderSelectFieldset) {
  const maleRadio = genderSelectFieldset.querySelector("#male-radio");
  const femaleRadio = genderSelectFieldset.querySelector("#female-radio");
  const customRadio = genderSelectFieldset.querySelector("#custom-radio");
  const customText = genderSelectFieldset.querySelector("#custom-text");
  const concealRadio = genderSelectFieldset.querySelector("#conceal-radio");
  const radioArray = [maleRadio, femaleRadio, customRadio, concealRadio];

  customText.remove();
  customText.style.display = "inline-block";

  switch (currentGender) {
    case "male":
      maleRadio.checked = true;
      break;
    case "female":
      femaleRadio.checked = true;
      break;
    case "custom":
      customRadio.checked = true;
      break;
    case "conceal":
      concealRadio.checked = true;
  }

  radioArray.forEach((radio) => {
    radio.addEventListener("change", (event) => {
      const currentRadio = event.target;
      if (currentRadio == customRadio) {
        currentRadio.parentNode.append(customText);
      } else {
        customText.remove();
      }
    });
  });

  const genderValue = document.getElementById("gender-value");
  const genderSelectSubmitBtn = document.getElementById(
    "gender-select-submit-btn"
  );

  if (genderSelectSubmitBtn) {
    genderSelectSubmitBtn.addEventListener("click", (event) => {
      event.preventDefault();
      genderSelectView.remove();
      radioArray.forEach((radio) => {
        if (radio.checked == true && radio == customRadio) {
          genderValue.value = customText.value;
          return;
        } else if (radio.checked) {
          genderValue.value = radio.id.slice(0, -6);
          return;
        }
      });
    });
  }
}

const genderBtn = document.getElementById("gender-btn");
if (genderBtn) {
  genderBtn.addEventListener("click", handleToggleGenderBtnClick);
}

function handleToggleGenderBtnClick() {
  document.body.append(genderSelectView);
}

genderSelectView.remove();
genderSelectView.style.display = "block";
