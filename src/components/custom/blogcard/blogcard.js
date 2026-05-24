// Підключення функціоналу "Чортоги Фрілансера"
import {
  addTouchAttr,
  addLoadedAttr,
  isMobile,
  FLS,
} from "@js/common/functions.js";

import "./blogcard.scss";

// >===== render blogcsrd + click-> perhid na blog.html ===========
document.addEventListener("DOMContentLoaded", () => {
  const section = document.querySelector(".latest-news");
  if (!section) return;
  // const list = section.querySelector(".latest-news__list");
  const list =
    section.querySelector(".latest-news__list") ||
    section.querySelector(".blog__list");
  const template = section.querySelector("#blogcard-template");
  const LIMIT = 3;
  fetch("/data/blog.json")
    .then((res) => res.json())
    .then((data) => {
      const latestPosts = [...data]
        .sort((a, b) => new Date(b.date) - new Date(a.date))
        .slice(0, LIMIT);
      latestPosts.forEach((item) => {
        const clone = template.content.cloneNode(true);
        const url = `detail.html?post=${item.slug}`;
        const formattedDate = new Date(item.date).toLocaleDateString("en-US", {
          year: "numeric",
          month: "long",
          day: "numeric",
        });
        clone.querySelector(".blogcard__image img").src = item.image;
        clone.querySelector(".blogcard__image img").alt = item.title;
        clone.querySelector(".blogcard__label").textContent = formattedDate;
        clone.querySelector(".blogcard__title").textContent = item.title;
        clone.querySelector(".blogcard__descr").textContent = item.description;
        clone.querySelector(".blogcard__image-link").href = url;
        clone.querySelector(".blogcard__title-link").href = url;
        list.appendChild(clone);
      });
    });
});
