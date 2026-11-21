(function () {
  var reduce = false;
  try { reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) {}
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var play = function (v) { v.muted = true; var p = v.play(); if (p && p.catch) p.catch(function () {}); };

  // mobile menu
  var mb = $(".menu-btn"), nav = $(".nav");
  if (mb && nav) {
    mb.addEventListener("click", function () { var o = nav.classList.toggle("open"); mb.setAttribute("aria-expanded", o ? "true" : "false"); });
    nav.addEventListener("click", function (e) { if (e.target.tagName === "A") { nav.classList.remove("open"); mb.setAttribute("aria-expanded", "false"); } });
  }

  // hero: sequence of clips (video or image) with chapter bar
  var hero = $("[data-hero]");
  if (hero) {
    var clips = $$(".clip", hero), chaps = $$(".chap[data-i]", hero), toggle = $("#hero-toggle");
    var cur = 0, paused = reduce, t0 = 0, elapsed = 0, raf = null;
    var dur = function (c) { return c.dataset.type === "video" ? (c.duration || 6) : parseFloat(c.dataset.seconds || 3.5); };
    var pos = function (c) { return c.dataset.type === "video" ? c.currentTime : elapsed; };
    function show(i) {
      clips.forEach(function (c, j) {
        var on = j === i;
        c.classList.toggle("on", on);
        if (c.dataset.type === "video") { if (on) { c.currentTime = 0; if (!paused) play(c); } else c.pause(); }
        else if (on) { c.style.animation = "none"; void c.offsetWidth; c.style.animation = ""; }
      });
      cur = i; elapsed = 0; t0 = performance.now();
      chaps.forEach(function (b, j) { b.classList.toggle("on", j === i); });
    }
    function tick(now) {
      var c = clips[cur];
      if (!paused && c.dataset.type !== "video") elapsed += (now - t0) / 1000;
      t0 = now;
      var p = Math.min(1, pos(c) / dur(c));
      chaps.forEach(function (b, j) { b.querySelector("i").style.width = (j < cur ? 100 : j === cur ? p * 100 : 0).toFixed(1) + "%"; });
      if (!paused && (p >= 1 || (c.dataset.type === "video" && c.ended))) show((cur + 1) % clips.length);
      raf = requestAnimationFrame(tick);
    }
    clips.forEach(function (c) { if (c.dataset.type === "video") c.addEventListener("ended", function () { if (!paused) show((cur + 1) % clips.length); }); });
    chaps.forEach(function (b) { b.addEventListener("click", function () { show(+b.dataset.i); }); });
    function setLabel() { if (toggle) toggle.textContent = paused ? toggle.dataset.play : toggle.dataset.pause; }
    if (toggle) toggle.addEventListener("click", function () {
      paused = !paused; var c = clips[cur];
      if (c.dataset.type === "video") { if (paused) c.pause(); else play(c); }
      setLabel();
    });
    show(0); setLabel(); raf = requestAnimationFrame(tick);
    document.addEventListener("visibilitychange", function () { if (document.hidden) cancelAnimationFrame(raf); else { t0 = performance.now(); raf = requestAnimationFrame(tick); } });
  }

  // other looping videos
  $$("video[data-loop]").forEach(function (v) { if (reduce) v.pause(); else play(v); });

  // sample planner
  var pl = $("[data-planner]");
  if (pl) {
    var needs = [];
    try { needs = JSON.parse(pl.dataset.needs); } catch (e) {}
    var val = function (q) { var i = $("fieldset[data-q='" + q + "'] input:checked", pl); return i ? { v: i.value, l: i.dataset.label } : { v: "", l: "" }; };
    function render() {
      ["product", "decor", "qty", "have"].forEach(function (q) { $("[data-out='" + q + "']", pl).textContent = val(q).l; });
      var list = $("[data-out='needs']", pl); list.innerHTML = "";
      (needs[+val("have").v] || []).forEach(function (n) { var li = document.createElement("li"); li.textContent = n; list.appendChild(li); });
    }
    pl.addEventListener("change", render); render();
    var go = $("[data-planner-go]", pl);
    if (go) go.addEventListener("click", function () {
      var f = $("#rfq-form"); if (!f) return;
      var r = $("input[name='product_group'][value='" + val("product").v + "']", f); if (r) r.checked = true;
      var q = $("#f-qty", f); if (q && !q.value) q.value = val("qty").l;
      var n = $("#f-note", f);
      if (n) {
        var lines = $$("dl.pl-sum div", pl).map(function (d) { return $("dt", d).textContent + ": " + $("dd", d).textContent; });
        n.value = lines.join("\n") + (n.value ? "\n\n" + n.value : "");
      }
    });
  }

  // forms: without an endpoint show a thank-you note
  $$("form.form").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      var a = f.getAttribute("action");
      if (a && a !== "#") return;
      e.preventDefault();
      var ok = $(".form-ok", f); if (ok) ok.style.display = "block";
    });
  });
})();
