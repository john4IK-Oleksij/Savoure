import "./chefsdishes.scss";
document.addEventListener("DOMContentLoaded", () => {
  const section = document.querySelector("[data-fls-chefsdishes]");
  if (!section) return;
  const list = section.querySelector(".chefsdishes__list");
  const template = section.querySelector("#dishcard-template-featured");
  fetch("/data/menu.json")
    .then((res) => res.json())
    .then((data) => {
      const featured = data.filter((item) => item.featured);
      featured.forEach((item) => {
        const clone = template.content.cloneNode(true);
        clone.querySelector(".dishcard__image img").src = item.image;
        clone.querySelector(".dishcard__label").textContent = item.label;
        clone.querySelector(".dishcard__title").textContent = item.title;
        clone.querySelector(".dishcard__price").textContent = `$${item.price}`;
        clone.querySelector(".dishcard__description").textContent =
          item.description;
        list.appendChild(clone);
      });
    });
});
