// Navigation des fiches projets : sommaire collant, barre de progression,
// retour en haut et agrandissement des figures. Sans dépendance externe.
(function () {
  "use strict";
  var main = document.querySelector("main");
  var hero = document.querySelector(".project-hero");
  if (!main || !hero) return;

  function slug(text, used) {
    var base = text.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "")
      .replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "section";
    var id = base, n = 2;
    while (used[id] || document.getElementById(id)) id = base + "-" + n++;
    used[id] = true;
    return id;
  }

  // Sommaire construit à partir des titres de section visibles.
  var used = {};
  var headings = Array.prototype.filter.call(main.querySelectorAll("h2"), function (h) {
    return !h.closest("details, [hidden], .project-hero, .project-card");
  });
  if (headings.length > 2) {
    var bar = document.createElement("nav");
    bar.className = "project-toc";
    bar.setAttribute("aria-label", "Sommaire du projet");
    var list = document.createElement("ol");
    headings.forEach(function (h) {
      if (!h.id) h.id = slug(h.textContent, used);
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = "#" + h.id;
      a.textContent = h.textContent.replace(/^\d+\.\s*/, "");
      li.appendChild(a);
      list.appendChild(li);
    });
    bar.appendChild(list);
    var anchor = document.querySelector(".project-brief") || hero;
    anchor.insertAdjacentElement("afterend", bar);

    var links = list.querySelectorAll("a");
    if ("IntersectionObserver" in window) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          links.forEach(function (link) {
            var active = link.getAttribute("href") === "#" + entry.target.id;
            link.classList.toggle("active", active);
            if (active && link.scrollIntoView && bar.scrollWidth > bar.clientWidth) {
              list.scrollLeft = link.offsetLeft - 16;
            }
          });
        });
      }, { rootMargin: "-20% 0px -70% 0px" });
      headings.forEach(function (h) { observer.observe(h); });
    }
  }

  // Barre de progression de lecture et bouton de retour en haut.
  var progress = document.createElement("div");
  progress.className = "reading-progress";
  document.body.appendChild(progress);
  var top = document.createElement("button");
  top.type = "button";
  top.className = "back-to-top";
  top.setAttribute("aria-label", "Revenir en haut de la page");
  top.textContent = "↑";
  top.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
  document.body.appendChild(top);
  function onScroll() {
    var max = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.transform = "scaleX(" + (max > 0 ? Math.min(window.scrollY / max, 1) : 0) + ")";
    top.classList.toggle("visible", window.scrollY > 900);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Agrandissement des figures et photographies.
  var overlay = document.createElement("div");
  overlay.className = "lightbox";
  overlay.setAttribute("role", "dialog");
  overlay.setAttribute("aria-modal", "true");
  overlay.hidden = true;
  overlay.innerHTML = '<button type="button" class="lightbox-close" aria-label="Fermer">×</button><img alt=""><p></p>';
  document.body.appendChild(overlay);
  var bigImg = overlay.querySelector("img"), caption = overlay.querySelector("p");
  function close() { overlay.hidden = true; document.body.classList.remove("no-scroll"); }
  overlay.addEventListener("click", function (e) { if (e.target !== bigImg) close(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !overlay.hidden) close(); });
  main.querySelectorAll(".figure-card img, .gallery-card img").forEach(function (img) {
    img.classList.add("zoomable");
    img.setAttribute("tabindex", "0");
    function open() {
      bigImg.src = img.currentSrc || img.src;
      bigImg.alt = img.alt;
      var fig = img.closest("figure");
      var cap = fig && fig.querySelector("figcaption");
      caption.textContent = cap ? cap.innerText.replace(/\s*\n\s*/g, " · ") : img.alt;
      overlay.hidden = false;
      document.body.classList.add("no-scroll");
      overlay.querySelector(".lightbox-close").focus();
    }
    img.addEventListener("click", open);
    img.addEventListener("keydown", function (e) { if (e.key === "Enter") open(); });
  });
})();
