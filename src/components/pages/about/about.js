import "./about.scss";
// >============= render teamcard ======
document.addEventListener("DOMContentLoaded", () => {
  const section = document.querySelector(".team");

  if (!section) return;

  const list = section.querySelector(".team__list");
  const template = document.querySelector("#teamcard-template");

  fetch("/data/team.json")
    .then((res) => res.json())
    .then((data) => {
      data.forEach((member) => {
        const clone = template.content.cloneNode(true);

        clone.querySelector(".teamcard__image img").src = member.image;
        clone.querySelector(".teamcard__image img").alt = member.name;

        clone.querySelector(".teamcard__title").textContent = member.name;

        clone.querySelector(".teamcard__position").textContent =
          member.position;

        clone.querySelector(".teamcard__descr p").textContent =
          member.description;

        list.appendChild(clone);
      });
    })
    .catch((error) => {
      console.error("Team data loading error:", error);
    });
});
