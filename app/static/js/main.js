/* =============================================================
   DYNAMIC ACADEMY — MAIN JS
   Vanilla JS only. No frameworks, no build step.
   ============================================================= */
(function () {
  "use strict";

  /* ---- Mobile navigation toggle ---- */
  var navToggle = document.querySelector("[data-nav-toggle]");
  var mobileNav = document.querySelector("[data-mobile-nav]");
  if (navToggle && mobileNav) {
    navToggle.addEventListener("click", function () {
      var isOpen = mobileNav.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
      document.body.style.overflow = isOpen ? "hidden" : "";
    });
    // Close mobile nav whenever a link inside it is clicked
    mobileNav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        mobileNav.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
        document.body.style.overflow = "";
      });
    });
  }

  /* ---- Scroll reveal (respects prefers-reduced-motion via CSS) ---- */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    revealEls.forEach(function (el) { observer.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* ---- Animated stat counters ---- */
  var counters = document.querySelectorAll("[data-counter]");
  if ("IntersectionObserver" in window && counters.length) {
    var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var counterObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var el = entry.target;
          var target = parseInt(el.getAttribute("data-counter"), 10) || 0;
          var suffix = el.getAttribute("data-suffix") || "";
          counterObserver.unobserve(el);

          if (prefersReducedMotion) {
            el.textContent = target.toLocaleString() + suffix;
            return;
          }
          var duration = 1400;
          var start = null;
          function step(timestamp) {
            if (!start) start = timestamp;
            var progress = Math.min((timestamp - start) / duration, 1);
            var eased = 1 - Math.pow(1 - progress, 3);
            el.textContent = Math.round(eased * target).toLocaleString() + suffix;
            if (progress < 1) window.requestAnimationFrame(step);
          }
          window.requestAnimationFrame(step);
        });
      },
      { threshold: 0.4 }
    );
    counters.forEach(function (el) { counterObserver.observe(el); });
  }

  /* ---- Newsletter AJAX form (footer) ---- */
  var newsletterForm = document.querySelector("[data-newsletter-form]");
  if (newsletterForm) {
    newsletterForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var statusEl = newsletterForm.querySelector("[data-newsletter-status]");
      var button = newsletterForm.querySelector("button[type='submit']");
      var formData = new FormData(newsletterForm);

      button.disabled = true;
      fetch(newsletterForm.action, { method: "POST", body: formData })
        .then(function (res) { return res.json().then(function (data) { return { ok: res.ok, data: data }; }); })
        .then(function (result) {
          if (statusEl) {
            statusEl.textContent = result.data.message || "";
            statusEl.style.color = result.ok ? "#8ee9ff" : "#f2b8b5";
          }
          if (result.ok) { newsletterForm.reset(); }
        })
        .catch(function () {
          if (statusEl) {
            statusEl.textContent = "Something went wrong. Please try again.";
            statusEl.style.color = "#f2b8b5";
          }
        })
        .finally(function () { button.disabled = false; });
    });
  }

  /* ---- Confirm dialogs for destructive admin actions ---- */
  document.querySelectorAll("[data-confirm]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      var message = form.getAttribute("data-confirm") || "Are you sure?";
      if (!window.confirm(message)) {
        e.preventDefault();
      }
    });
  });

  /* ---- Simple client-side "required agreement" nicety: enable submit
     only visually - server-side validation is still authoritative. ---- */
  document.querySelectorAll("form[data-enhance]").forEach(function (form) {
    var submitBtn = form.querySelector("button[type='submit']");
    if (!submitBtn) return;
    form.addEventListener("submit", function () {
      submitBtn.disabled = true;
      submitBtn.dataset.originalText = submitBtn.textContent;
      submitBtn.textContent = "Please wait...";
      setTimeout(function () {
        submitBtn.disabled = false;
        if (submitBtn.dataset.originalText) {
          submitBtn.textContent = submitBtn.dataset.originalText;
        }
      }, 4000);
    });
  });

  var prefersReducedMotionGlobal = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- Fun effect #1: button click ripple ---- */
  if (!prefersReducedMotionGlobal) {
    document.querySelectorAll(".btn").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        var rect = btn.getBoundingClientRect();
        var ripple = document.createElement("span");
        var size = Math.max(rect.width, rect.height) * 2;
        ripple.className = "btn-ripple";
        ripple.style.width = ripple.style.height = size + "px";
        ripple.style.left = (e.clientX - rect.left - size / 2) + "px";
        ripple.style.top = (e.clientY - rect.top - size / 2) + "px";
        btn.appendChild(ripple);
        window.setTimeout(function () { ripple.remove(); }, 650);
      });
    });
  }

  /* ---- Fun effect #2: gentle tilt-on-hover for cards ---- */
  if (!prefersReducedMotionGlobal && window.matchMedia("(hover: hover)").matches) {
    document.querySelectorAll(".value-card, .course-card, .testimonial-card").forEach(function (card) {
      card.classList.add("tilt-card");
      card.addEventListener("mousemove", function (e) {
        var rect = card.getBoundingClientRect();
        var px = (e.clientX - rect.left) / rect.width - 0.5;
        var py = (e.clientY - rect.top) / rect.height - 0.5;
        card.style.transform = "perspective(700px) rotateY(" + (px * 6) + "deg) rotateX(" + (py * -6) + "deg) translateY(-6px)";
      });
      card.addEventListener("mouseleave", function () {
        card.style.transform = "";
      });
    });
  }

  /* ---- Fun effect #3: cursor spotlight glow inside the hero ---- */
  if (!prefersReducedMotionGlobal) {
    var heroSection = document.querySelector(".hero");
    if (heroSection) {
      heroSection.addEventListener("mousemove", function (e) {
        var rect = heroSection.getBoundingClientRect();
        var x = ((e.clientX - rect.left) / rect.width) * 100;
        var y = ((e.clientY - rect.top) / rect.height) * 100;
        heroSection.style.setProperty("--spot-x", x + "%");
        heroSection.style.setProperty("--spot-y", y + "%");
        heroSection.classList.add("spotlight-active");
      });
      heroSection.addEventListener("mouseleave", function () {
        heroSection.classList.remove("spotlight-active");
      });
    }
  }

  /* ---- Fun effect #4: auto-staggered reveal delays within each grid ---- */
  document.querySelectorAll(".grid").forEach(function (grid) {
    var items = grid.querySelectorAll(":scope > .reveal, :scope > div.reveal");
    items.forEach(function (item, index) {
      item.style.transitionDelay = Math.min(index * 90, 450) + "ms";
    });
  });

  /* ---- Fun effect #5: confetti burst (e.g. registration success pages) ---- */
  var confettiTarget = document.querySelector("[data-confetti]");
  if (confettiTarget && !prefersReducedMotionGlobal) {
    var colors = ["#c8952c", "#2547a8", "#4a72e0", "#dcae4c", "#ffffff"];
    for (var i = 0; i < 36; i++) {
      var piece = document.createElement("span");
      piece.className = "confetti-piece";
      piece.style.left = (45 + Math.random() * 10) + "%";
      piece.style.top = "0%";
      piece.style.background = colors[Math.floor(Math.random() * colors.length)];
      piece.style.setProperty("--dx", (Math.random() * 240 - 120) + "px");
      piece.style.setProperty("--dr", (Math.random() * 540 - 270) + "deg");
      piece.style.animationDelay = (Math.random() * 0.3) + "s";
      confettiTarget.appendChild(piece);
      (function (p) { window.setTimeout(function () { p.remove(); }, 2200); })(piece);
    }
  }
})();
