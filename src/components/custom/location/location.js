// Підключення функціоналу "Чортоги Фрілансера"
import {
  addTouchAttr,
  addLoadedAttr,
  isMobile,
  FLS,
} from "@js/common/functions.js";

import "./location.scss";
// >===========maps / render card-info=========
window.addEventListener("load", () => {
  const mapEl = document.getElementById("map");
  if (!mapEl) return;
  const items = Array.from(document.querySelectorAll(".branches__item"));
  const card = document.querySelector(".map__card");
  const getCoords = (el) => ({
    lat: parseFloat(el.dataset.lat),
    lng: parseFloat(el.dataset.lng),
  });
  const updateCard = (el) => {
    if (!card) return;
    const title = card.querySelector(".map_title");
    const address = card.querySelector(".map__address");
    const phone = card.querySelector(".map__phone");
    const ratingValue = card.querySelector(".rating_value");
    const ratingCount = card.querySelector(".rating_count");
    const ratingWrapper = card.querySelector("[data-fls-rating]");
    const button = card.querySelector("[data-fls-button]");
    if (title) title.textContent = el.dataset.title;
    if (address) address.textContent = el.dataset.address;
    if (phone) phone.textContent = el.dataset.phone;
    if (ratingValue) ratingValue.textContent = el.dataset.rating;
    if (ratingCount) ratingCount.textContent = `(${el.dataset.reviews})`;
    if (ratingWrapper) {
      ratingWrapper.setAttribute("data-fls-rating-value", el.dataset.rating);
    }
    if (button) {
      button.setAttribute("href", el.dataset.route);
    }
  };
  let center;
  let defaultItem = null;
  if (items.length) {
    defaultItem =
      items.find((el) => el.dataset.default === "true") ||
      items[items.length - 1];
    center = getCoords(defaultItem);
  } else {
    center = {
      lat: parseFloat(mapEl.dataset.lat),
      lng: parseFloat(mapEl.dataset.lng),
    };
  }
  const map = new google.maps.Map(mapEl, {
    zoom: 16,
    center: center,
  });
  if (!items.length) {
    new google.maps.Marker({
      position: center,
      map: map,
    });
    return;
  }
  items.forEach((el) => {
    const coords = getCoords(el);
    const marker = new google.maps.Marker({
      position: coords,
      map: map,
    });
    el.addEventListener("click", () => {
      map.panTo(coords);
      map.setZoom(16);
      updateCard(el);
    });
  });
  if (defaultItem) {
    updateCard(defaultItem);
  }
});
