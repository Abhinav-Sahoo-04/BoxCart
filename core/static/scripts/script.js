document.addEventListener("DOMContentLoaded", () => {

  let btn = document.querySelector("#close");

  if (btn) {
    btn.addEventListener("click", () => {
      document.querySelector(".floter").style.display = "none";
    });
  }

  let cat_close = document.querySelector("#category-close");

  if (cat_close) {
    cat_close.addEventListener("click", () => {
      document
        .querySelector(".category-list")
        .classList.toggle("category-close");
    });
  }

  let size_close = document.querySelector("#size-close");

  if (size_close) {
    size_close.addEventListener("click", () => {
      document
        .querySelector(".size-list")
        .classList.toggle("size-close");
    });
  }

  let price_close = document.querySelector("#price-close");

  if (price_close) {
    price_close.addEventListener("click", () => {
      document
        .querySelector(".form-container")
        .classList.toggle("form-close");
    });
  }

  let cat_drop_btn = document.querySelector("#cat-drop-btn");

  if (cat_drop_btn) {
    cat_drop_btn.addEventListener("click", () => {
      document
        .querySelector("#cat-drop")
        .classList.toggle("cat-show");
    });
  }

});