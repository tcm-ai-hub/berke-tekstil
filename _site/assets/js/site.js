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

  // hero video with pause control; honours reduced motion
  var hv = $("#hero-video"), ht = $("#hero-toggle");
  if (hv) {
    if (!reduce) play(hv);
    var label = function () { if (ht) ht.textContent = hv.paused ? ht.dataset.play : ht.dataset.pause; };
    hv.addEventListener("play", label); hv.addEventListener("pause", label); label();
    if (ht) ht.addEventListener("click", function () { if (hv.paused) play(hv); else hv.pause(); });
  }

  // journey: one film scrubbed by scroll on desktop; stacked stills on mobile / reduced motion
  var jy = $("[data-journey]");
  if (jy) {
    var scenes = $$(".jy-scene", jy), N = scenes.length, hdr = $(".site-h");
    var count = $(".jy-count", jy), bar = $(".jy-bar i", jy), cue = $(".jy-cue", jy), film = $(".jy-film", jy);
    var cuts = (jy.dataset.cuts || "").split(",").map(Number);
    var clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
    var live = !reduce && matchMedia("(min-width: 901px)").matches && film && cuts.length === N + 1;
    if (!live) { if (hdr) hdr.classList.add("solid"); }
    else {
      jy.classList.add("live"); jy.style.setProperty("--n", N + 0.5);
      film.preload = "auto"; film.src = film.dataset.src;
      film.addEventListener("error", function () { jy.classList.add("no-film"); });
      var raf = 0, cur = -1, target = 0, shown = 0, ready = false;
      film.addEventListener("loadeddata", function () { ready = true; film.pause(); req(); });
      var timeAt = function (x) {
        var i = Math.min(N - 1, Math.floor(x)), f = clamp(x - i), s0 = cuts[i] + 0.04, s1 = cuts[i + 1] - 0.06;
        return s0 + (s1 - s0) * f;
      };
      var update = function () {
        raf = 0;
        var r = jy.getBoundingClientRect(), H = innerHeight, p = clamp(-r.top / (jy.offsetHeight - H)), x = p * N;
        var idx = Math.min(N - 1, Math.floor(x));
        scenes.forEach(function (el, i) {
          var o = i === 0 ? clamp((0.8 - x) / 0.25) : i === N - 1 ? clamp((x - i + 0.05) / 0.25) : clamp((0.42 - Math.abs(x - i - 0.5)) / 0.17);
          el.style.opacity = o;
          var c = $(".jy-copy", el); if (c) c.style.transform = "translate(-50%," + ((i + 0.5 - x) * 40).toFixed(1) + "px)";
          if (jy.classList.contains("no-film")) { var m = $(".jy-media", el); if (m) m.style.opacity = i === idx ? 1 : 0; }
        });
        if (idx !== cur) {
          cur = idx; scenes.forEach(function (el, i) { el.classList.toggle("on", i === idx); });
          if (count) count.textContent = ("0" + (idx + 1)).slice(-2) + " / " + ("0" + N).slice(-2);
        }
        if (bar) jy.style.setProperty("--p", p.toFixed(4));
        if (cue) cue.style.opacity = clamp(1 - x * 3);
        if (hdr) hdr.classList.toggle("solid", r.bottom < 80);
        target = timeAt(x);
        if (ready) {
          shown += (target - shown) * 0.22;
          if (Math.abs(target - shown) < 0.01) shown = target;
          if (Math.abs(film.currentTime - shown) > 0.015) film.currentTime = shown;
          if (shown !== target) req();
        }
      };
      var req = function () { if (!raf) raf = requestAnimationFrame(update); };
      update();
      addEventListener("scroll", req, { passive: true });
      addEventListener("resize", req);
    }
  }

  // opening film: auto-advancing scenes cotton → product
  var fm = $("[data-film]");
  if (fm) {
    var fl = $$(".fs", fm), fc = $$(".fc", fm), fb = $(".film-bar i", fm), fi = 0, per = 3200, t0 = performance.now();
    var show = function (i) {
      fl.forEach(function (el, j) { var on = j === i; el.classList.toggle("on", on); if (el.tagName === "VIDEO") { if (on) { el.preload = "auto"; el.currentTime = 0; play(el); } else el.pause(); } });
      fc.forEach(function (el, j) { el.classList.toggle("on", j === i); });
    };
    if (reduce) { show(0); }
    else {
      var tick = function (now) {
        var p = (now - t0) / per;
        if (p >= 1) { fi = (fi + 1) % fl.length; t0 = now; p = 0; show(fi); }
        if (fb) fb.style.width = (((fi + p) / fl.length) * 100).toFixed(2) + "%";
        requestAnimationFrame(tick);
      };
      show(0); requestAnimationFrame(tick);
    }
  }

  // scroll story: swap the sticky media as each chapter enters
  var st = $("[data-story]");
  if (st) {
    var layers = $$(".sm", st), idx = $$(".story-index li", st), steps = $$(".ss", st);
    var set = function (i) {
      layers.forEach(function (l, j) {
        var on = j === i; l.classList.toggle("on", on);
        var v = $("video", l);
        if (v) { if (on && !reduce) { v.preload = "auto"; play(v); } else v.pause(); }
      });
      idx.forEach(function (l, j) { l.classList.toggle("on", j === i); });
      st.classList.toggle("light-on", steps[i] && steps[i].classList.contains("light"));
    };
    if ("IntersectionObserver" in window) {
      var so = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) set(+e.target.dataset.i); }); }, { rootMargin: "-45% 0px -45% 0px" });
      steps.forEach(function (s) { so.observe(s); });
    }
    set(0);
  }

  // other looping videos: play only while visible
  var loops = $$("video[data-loop]");
  if (!reduce && loops.length) {
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) play(e.target); else e.target.pause(); }); }, { threshold: 0.25 });
      loops.forEach(function (v) { io.observe(v); });
    } else loops.forEach(play);
  }

  // sample planner → fills the quote form
  var pl = $("[data-planner]");
  if (pl) {
    var needs = [];
    try { needs = JSON.parse(pl.dataset.needs); } catch (e) {}
    var val = function (q) { var i = $("fieldset[data-q='" + q + "'] input:checked", pl); return i ? { v: i.value, l: i.dataset.label } : { v: "", l: "" }; };
    var render = function () {
      ["product", "decor", "qty", "have"].forEach(function (q) { $("[data-out='" + q + "']", pl).textContent = val(q).l; });
      var list = $("[data-out='needs']", pl); list.innerHTML = "";
      (needs[+val("have").v] || []).forEach(function (n) { var li = document.createElement("li"); li.textContent = n; list.appendChild(li); });
    };
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
  $$("form.form, form.form-lite").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      var a = f.getAttribute("action");
      if (a && a !== "#") return;
      e.preventDefault();
      var ok = $(".form-ok", f); if (ok) ok.style.display = "block";
    });
  });
})();
