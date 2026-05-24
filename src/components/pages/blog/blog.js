import "./blog.scss";
// >=========== render blogcard ==========
document.addEventListener("DOMContentLoaded", () => {
  const section = document.querySelector(".blog");
  if (!section) return;
  const list = section.querySelector(".blog__list");
  const template = section.querySelector("#blogcard-template");
  const button = section.querySelector(".btn__blog");
  let data = [];
  let visible = 6;
  const STEP = 3;
  fetch("/data/blog.json")
    .then((res) => res.json())
    .then((json) => {
      data = json;
      render();
    });
  function render() {
    list.innerHTML = "";
    data.slice(0, visible).forEach((item) => {
      const clone = template.content.cloneNode(true);
      const url = `detail.html?post=${item.slug}`;
      clone.querySelector(".blogcard__image img").src = item.image;
      clone.querySelector(".blogcard__image img").alt = item.title;
      clone.querySelector(".blogcard__label").textContent = item.date;
      clone.querySelector(".blogcard__title").textContent = item.title;
      clone.querySelector(".blogcard__descr").textContent = item.description;
      clone.querySelector(".blogcard__image-link").href = url;
      clone.querySelector(".blogcard__title-link").href = url;
      list.appendChild(clone);
    });
    if (visible >= data.length) {
      button.style.display = "none";
    }
  }
  button.addEventListener("click", (e) => {
    e.preventDefault();
    visible += STEP;
    render();
  });
});
// ?================dlia newsdetail->perehid
document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const slug = params.get("post");

  if (!slug) return;

  fetch("/data/blog.json")
    .then((res) => res.json())
    .then((data) => {
      const article = data.find((item) => item.slug === slug);
      if (!article) return;

      const title = document.querySelector(".newsdetail__title");
      const date = document.querySelector(".newsdetail__date");
      const image = document.querySelector(".newsdetail__image img");
      const descr = document.querySelector(".newsdetail__descr");

      if (title) title.textContent = article.title;
      if (date) date.textContent = article.date;
      if (image) {
        image.src = article.image;
        image.alt = article.title;
      }
      if (descr) descr.textContent = article.description;
    });
});

// >========== form/subscribe ========
// const form = document.querySelector(".subscribe__form");
// form.addEventListener("submit", (e) => {
//   e.preventDefault();
//   const email = form.email.value.trim();
//   if (!email) return;
//   form.reset();
//   alert("You have successfully signed up!");
// });
