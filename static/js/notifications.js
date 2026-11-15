/**
 * Savoure Restaurant — Luxury Toast & Popup Notification Handler
 */
(function () {
  "use strict";

  const AUTO_DISMISS_MS = 7000;

  function initToast(toast) {
    if (!toast || toast.dataset.toastInit === "true") return;
    toast.dataset.toastInit = "true";

    // Reveal with slide-in animation
    requestAnimationFrame(() => {
      toast.classList.add("toast--visible");
    });

    const progressBar = toast.querySelector(".toast__progress");
    const closeBtn = toast.querySelector(".toast__close");

    let remainingMs = AUTO_DISMISS_MS;
    let startTime = Date.now();
    let timerId = null;

    if (progressBar) {
      progressBar.style.transition = `transform ${AUTO_DISMISS_MS}ms linear`;
      requestAnimationFrame(() => {
        progressBar.style.transform = "scaleX(0)";
      });
    }

    function dismiss() {
      if (timerId) clearTimeout(timerId);
      toast.classList.remove("toast--visible");
      toast.classList.add("toast--leaving");
      setTimeout(() => {
        toast.remove();
      }, 400);
    }

    function startTimer() {
      startTime = Date.now();
      timerId = setTimeout(dismiss, remainingMs);
    }

    function pauseTimer() {
      if (timerId) {
        clearTimeout(timerId);
        timerId = null;
        remainingMs -= Date.now() - startTime;
        if (remainingMs < 0) remainingMs = 0;
      }
      if (progressBar) {
        const computedStyle = window.getComputedStyle(progressBar);
        progressBar.style.transition = "none";
        progressBar.style.transform = computedStyle.transform;
      }
    }

    function resumeTimer() {
      if (remainingMs > 0) {
        if (progressBar) {
          progressBar.style.transition = `transform ${remainingMs}ms linear`;
          progressBar.style.transform = "scaleX(0)";
        }
        startTimer();
      } else {
        dismiss();
      }
    }

    if (closeBtn) {
      closeBtn.addEventListener("click", (e) => {
        e.preventDefault();
        dismiss();
      });
    }

    toast.addEventListener("mouseenter", pauseTimer);
    toast.addEventListener("mouseleave", resumeTimer);

    startTimer();
  }

  function getOrCreateContainer() {
    let container = document.querySelector(".toast-container");
    if (!container) {
      container = document.createElement("div");
      container.className = "toast-container";
      container.setAttribute("aria-live", "polite");
      document.body.appendChild(container);
    }
    return container;
  }

  function showToast(message, type = "info", title = "") {
    const container = getOrCreateContainer();
    const toast = document.createElement("div");
    toast.className = `toast toast--${type}`;
    toast.setAttribute("role", "alert");

    const defaultTitles = {
      success: "Успішно",
      error: "Помилка",
      warning: "Увага",
      info: "Повідомлення",
    };

    const displayTitle = title || defaultTitles[type] || "Повідомлення";

    toast.innerHTML = `
      <div class="toast__icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          ${
            type === "success"
              ? '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>'
              : type === "error"
              ? '<circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line>'
              : '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line>'
          }
        </svg>
      </div>
      <div class="toast__content">
        <h4 class="toast__title">${displayTitle}</h4>
        <p class="toast__text">${message}</p>
      </div>
      <button type="button" class="toast__close" aria-label="Закрити">&times;</button>
      <div class="toast__progress" aria-hidden="true"></div>
    `;

    container.appendChild(toast);
    initToast(toast);
  }

  // Initialize on page load for SSR Django messages
  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".toast").forEach(initToast);
  });

  // Expose global helper
  window.showToast = showToast;
})();
