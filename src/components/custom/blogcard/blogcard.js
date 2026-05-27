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
  const section = document.querySelector(".latest-news, .blog");
  if (!section) return;
  const list = section.querySelector(".latest-news__list, .blog__list");
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
        const imgLink = clone.querySelector(".blogcard__image-link");
        const titleLink = clone.querySelector(".blogcard__title-link");
        imgLink.href = url;
        titleLink.href = url;
        // Accessibility: provide descriptive labels for links
        imgLink.setAttribute("aria-label", `Open article: ${item.title}`);
        titleLink.setAttribute("aria-label", `Open article: ${item.title}`);
        list.appendChild(clone);
      });
    });
});
