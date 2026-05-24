/*
Документація по роботі у шаблоні: 
Документація слайдера: https://swiperjs.com/
Сніппет(HTML): swiper
*/

// Підключаємо слайдер Swiper з node_modules
// При необхідності підключаємо додаткові модулі слайдера, вказуючи їх у {} через кому
// Приклад: { Navigation, Autoplay }
import Swiper from "swiper";
import { Navigation, Autoplay, Scrollbar } from "swiper/modules";
/*
Основні модулі слайдера:
Navigation, Pagination, Autoplay, 
EffectFade, Lazy, Manipulation
Детальніше дивись https://swiperjs.com/
*/

// Стилі Swiper
// Підключення базових стилів
import "./slider.scss";
// Повний набір стилів з node_modules
// import 'swiper/css/bundle';

// Ініціалізація слайдерів

function initSliders() {
  if (document.querySelector(".feedback__slider")) {
    new Swiper(".feedback__slider", {
      modules: [Navigation, Autoplay, Scrollbar],
      observer: true,
      observeParents: true,
      slidesPerView: 3,
      spaceBetween: 30,
      speed: 2500,
      loop: true,
      grabCursor: true,
      autoplay: {
        delay: 4000,
        disableOnInteraction: false,
      },
      navigation: {
        prevEl: ".feedback-button-prev",
        nextEl: ".feedback-button-next",
      },
      scrollbar: {
        el: ".feedback-scrollbar",
        draggable: true,
      },
      breakpoints: {
        320: {
          slidesPerView: 1.3,
        },
        480: {
          slidesPerView: 1.7,
        },
        640: {
          slidesPerView: 2.3,
        },
        992: {
          slidesPerView: 2.7,
        },
        1200: {
          slidesPerView: 3,
        },
      },
    });
  }
}
document.querySelector("[data-fls-slider]")
  ? window.addEventListener("load", initSliders)
  : null;
