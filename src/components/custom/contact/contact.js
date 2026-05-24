// Підключення функціоналу "Чортоги Фрілансера"
import {
  addTouchAttr,
  addLoadedAttr,
  isMobile,
  FLS,
} from "@js/common/functions.js";

import "./contact.scss";
// >============= dropdawn contact country select  ================
document.addEventListener("DOMContentLoaded", () => {
  const select = document.getElementById("countrySelect");
  const head = select.querySelector(".contact__select-head");
  const dropdown = select.querySelector(".contact__select-dropdown");
  const input = select.querySelector("input");
  const headImg = head.querySelector("img");
  const headCode = head.querySelector("span");
  const countries = [
    { code: "+1", flag: "us" },
    { code: "+44", flag: "gb" },
    { code: "+33", flag: "fr" },
  ];
  countries.forEach((c) => {
    const item = document.createElement("div");
    item.className = "contact__select-item";
    item.innerHTML = `
      <img src="https://flagcdn.com/w20/${c.flag}.png">
      <span>${c.code}</span>
    `;
    item.addEventListener("click", (e) => {
      e.stopPropagation();
      headImg.src = `https://flagcdn.com/w20/${c.flag}.png`;
      headCode.textContent = c.code;
      input.value = c.code;
      select.classList.remove("open");
    });
    dropdown.appendChild(item);
  });
  head.addEventListener("click", (e) => {
    e.stopPropagation();
    select.classList.toggle("open");
  });
  document.addEventListener("click", () => {
    select.classList.remove("open");
  });
});
// >============== form-(contact; subscribe; reservation) ==========
document.addEventListener("DOMContentLoaded", () => {
  const sections = document.querySelectorAll("[data-fls-contact]");
  if (!sections.length) return;
  sections.forEach((section) => {
    const form = section.querySelector("form");
    if (!form) return;
    const dateInput = form.querySelector('input[type="date"]');
    if (dateInput) {
      const today = new Date().toISOString().split("T")[0];
      dateInput.min = today;
    }
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const inputs = form.querySelectorAll(
        "input:not([type='checkbox']), textarea",
      );
      inputs.forEach((input) => {
        if (typeof input.value === "string") {
          input.value = input.value.trim();
        }

        if (input.type === "email") {
          input.value = input.value.toLowerCase();
        }
      });
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      const terms = form.querySelector('[name="terms"]');

      if (terms && !terms.checked) {
        terms.reportValidity();
        return;
      }
      const submitButton = form.querySelector('button[type="submit"]');
      if (submitButton) {
        submitButton.disabled = true;
      }
      const formType = form.dataset.formType;
      if (formType === "reservation") {
        const formData = new FormData(form);
        const name = formData.get("name");
        const email = formData.get("email");
        const countryCode = formData.get("country_code");
        const phone = formData.get("phone");
        const date = formData.get("date");
        const time = formData.get("time");
        const guests = Number(formData.get("guests"));
        const transactionId = Math.floor(
          100000000000 + Math.random() * 900000000000,
        );
        const formattedDate = new Date(date).toLocaleDateString("en-US", {
          day: "numeric",
          month: "short",
          year: "numeric",
        });
        const total = guests * 22;
        document.querySelector("[data-reservation-id]").textContent =
          transactionId;
        document.querySelector("[data-reservation-name]").textContent = name;
        document.querySelector("[data-reservation-email]").textContent = email;
        document.querySelector("[data-reservation-phone]").textContent =
          `${countryCode} ${phone}`;
        document.querySelector("[data-reservation-date]").textContent =
          `${time} • ${formattedDate}`;
        document.querySelector("[data-reservation-type]").textContent =
          "Dine-In";
        document.querySelector("[data-reservation-guests]").textContent =
          guests;
        document.querySelector("[data-reservation-total]").textContent =
          `$${total}`;
        await new Promise((resolve) => setTimeout(resolve, 800));
        window.flsPopup.open("reservation-link");
      }
      switch (formType) {
        case "subscribe":
          alert("You are successfully subscribed.");
          break;
        case "contact":
          alert("Your message has been sent.");
          break;
        case "reservation":
          break;
        default:
          alert("Form submitted.");
      }
      form.reset();
      if (submitButton) {
        submitButton.disabled = false;
      }
    });
  });
});
