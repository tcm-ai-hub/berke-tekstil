(function () {
  var reduce = false;
  try { reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) {}

  function start(v) {
    v.muted = true;
    if (reduce) { v.pause(); return false; }
    var p = v.play(); if (p && p.catch) p.catch(function () {});
    return true;
  }
  function wireToggle(btn, v) {
    if (!btn || !v) return;
    var setLabel = function () { btn.textContent = v.paused ? btn.dataset.play : btn.dataset.pause; };
    btn.addEventListener("click", function () {
      if (v.paused) { var p = v.play(); if (p && p.catch) p.catch(function () {}); } else { v.pause(); }
    });
    v.addEventListener("play", setLabel); v.addEventListener("pause", setLabel); setLabel();
  }

  // mobile menu
  var mb = document.querySelector(".menu-btn"), nav = document.querySelector(".nav");
  if (mb && nav) {
    mb.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      mb.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (e) { if (e.target.tagName === "A") { nav.classList.remove("open"); mb.setAttribute("aria-expanded", "false"); } });
  }

  // hero chapters
  var hv = document.getElementById("hero-video");
  if (hv) {
    start(hv);
    wireToggle(document.getElementById("hero-toggle"), hv);
    var starts = [0, 2.46, 4.96, 7.46], ends = [2.46, 4.96, 7.46, 10.03];
    var chaps = Array.prototype.slice.call(document.querySelectorAll(".chap[data-i]"));
    chaps.forEach(function (b) {
      b.addEventListener("click", function () { hv.currentTime = starts[+b.dataset.i] + 0.01; });
    });
    hv.addEventListener("timeupdate", function () {
      var t = hv.currentTime, cur = 0;
      for (var i = 0; i < 4; i++) if (t >= starts[i]) cur = i;
      chaps.forEach(function (b, i) {
        var w = i < cur ? 100 : i === cur ? Math.max(0, Math.min(100, (t - starts[i]) / (ends[i] - starts[i]) * 100)) : 0;
        b.querySelector("i").style.width = w.toFixed(1) + "%";
        b.classList.toggle("on", i === cur);
      });
    });
  }

  // embroidery inspector
  var sv = document.getElementById("stitch-video");
  if (sv) {
    start(sv);
    wireToggle(document.getElementById("stitch-toggle"), sv);
    var range = document.getElementById("scrub");
    sv.addEventListener("timeupdate", function () { if (sv.duration && document.activeElement !== range) range.value = (sv.currentTime / sv.duration * 100).toFixed(1); });
    range.addEventListener("input", function () { if (sv.duration) { sv.pause(); sv.currentTime = range.value / 100 * sv.duration; } });
    var pick = function (i) {
      document.querySelectorAll("[data-spot]").forEach(function (el) { el.classList.toggle("on", el.dataset.spot === String(i)); });
      document.querySelectorAll(".spot").forEach(function (el) { el.setAttribute("aria-expanded", el.dataset.spot === String(i) ? "true" : "false"); });
    };
    document.querySelectorAll("[data-spot]").forEach(function (el) { el.addEventListener("click", function () { pick(el.dataset.spot); }); });
  }

  // other autoplay videos
  document.querySelectorAll("video[data-loop]").forEach(start);

  // quote form (demo until a form endpoint is connected)
  document.querySelectorAll("form.form").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      var action = f.getAttribute("action");
      if (action && action !== "#") return;
      e.preventDefault();
      var ok = f.querySelector(".form-ok"); if (ok) ok.style.display = "block";
    });
  });
})();
