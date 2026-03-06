let btn = document.querySelector("#close");
btn.addEventListener("click", () => {
  document.querySelector(".floter").style.display = "none";
});
try {
  let cat_close = document.querySelector("#category-close");
  cat_close.addEventListener("click", () => {
    document.querySelector(".category-list").classList.toggle("category-close");
  });

  let size_close = document.querySelector("#size-close");
  size_close.addEventListener("click", () => {
    console.log("hello");
    document.querySelector(".size-list").classList.toggle("size-close");
  });

  let price_close = document.querySelector("#price-close");
  price_close.addEventListener("click", () => {
    document.querySelector(".form-container").classList.toggle("form-close");
  });
} catch {
  console.log("error");
}

let cat_drop_btn = document.querySelector("#cat-drop-btn");
cat_drop_btn.addEventListener("click", () => {
  document.querySelector("#cat-drop").classList.toggle("cat-show");
});

function incrementQunatity (id){
  let ele=document.querySelector(`#${id}`).innerText;
  console.log(ele);
  console.log("hello");
  
}

try{
 let plus=document.querySelector("#plus")
 console.log(plus);
 plus.addEventListener("click",()=>{
  incrementQunatity(qunatity)
 })
}catch{
  console.log("error due to btn"); 
}