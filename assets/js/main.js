// probalbose.com: small progressive enhancements. The pages read fine without it.
(function () {
  "use strict";
  var L = window.LETTERS || [];
  var FIELDS = [["maths", "Maths"], ["physics", "Physics"], ["stats", "Stats"], ["finance", "Finance"]];

  // Header rule once the page scrolls
  var head = document.querySelector(".site-head");
  if (head) {
    var onScroll = function () { head.classList.toggle("scrolled", window.scrollY > 4); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // Decorative tile wall: all 24 small letters in their book colours
  document.querySelectorAll("[data-tiles]").forEach(function (box) {
    L.forEach(function (r) {
      var s = document.createElement("span");
      s.textContent = r.small;
      s.style.background = r.tint;
      s.style.color = r.deep;
      s.setAttribute("aria-hidden", "true");
      box.appendChild(s);
    });
  });

  // Letter explorer on the book page
  var grid = document.querySelector("[data-letter-grid]");
  var card = document.querySelector("[data-letter-card]");
  if (!grid || !card || !L.length) return;

  function esc(t) {
    return String(t).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function show(i, focus) {
    var r = L[i];
    grid.querySelectorAll("button").forEach(function (b, j) {
      b.setAttribute("aria-pressed", j === i ? "true" : "false");
    });
    var rows = FIELDS.map(function (f) {
      var m = r.meanings[f[0]];
      return '<div><dt class="' + f[0] + '">' + f[1] + "</dt>" +
        (m ? "<dd>" + esc(m) + "</dd>" : '<dd class="none">hardly used</dd>') + "</div>";
    }).join("");
    card.innerHTML =
      '<div class="top" style="background:' + r.tint + '">' +
      '<div class="big" style="color:' + r.deep + '">' + esc(r.cap) + " " + esc(r.small) + "</div>" +
      '<div><div class="name" style="color:' + r.deep + '">' + r.n + ". " + esc(r.name) + "</div>" +
      '<div class="say">Say <b>' + esc(r.say) + "</b></div>" +
      '<div class="say">Type <span class="mono">' + esc(r.latex) + "</span></div></div></div>" +
      "<dl>" + rows + "</dl>";
    if (focus) card.setAttribute("aria-label", r.name);
  }

  L.forEach(function (r, i) {
    var b = document.createElement("button");
    b.type = "button";
    b.textContent = r.small;
    b.style.background = r.tint;
    b.style.color = r.deep;
    b.setAttribute("aria-label", r.name);
    b.setAttribute("aria-pressed", "false");
    b.addEventListener("click", function () { show(i, true); });
    grid.appendChild(b);
  });
  show(17, false); // sigma, the letter in the free sample
})();
