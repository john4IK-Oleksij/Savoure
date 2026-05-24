import "./our-menu.scss";
console.log("START OUR-MENU");
const template = document.querySelector("#dishcard-template-menu");
function createCard(item) {
  const clone = template.content.cloneNode(true);
  const img = clone.querySelector("img");
  img.src = item.image;
  img.alt = item.title;
  clone.querySelector(".dishcard__label").textContent = item.label;
  clone.querySelector(".dishcard__title").textContent = item.title;
  clone.querySelector(".dishcard__price").textContent = `$${item.price}`;
  clone.querySelector(".dishcard__description").textContent = item.description;
  return clone;
}
function renderMenu(data) {
  const containers = document.querySelectorAll(".today-tab__body");
  const tabs = ["all", "appetizer", "main", "dessert", "beverage"];
  containers.forEach((container, index) => {
    const category = tabs[index];
    container.innerHTML = "";
    const filtered =
      category === "all"
        ? data
        : data.filter((item) => item.category === category);
    filtered.forEach((item) => {
      container.appendChild(createCard(item));
    });
  });
}
// fetch JSON
fetch("/data/menu.json")
  .then((res) => res.json())
  .then((data) => {
    console.log("FULL DATA:", data.length);
    renderMenu(data);
    tabs();
  });

console.log("TEMPLATE:", template);
