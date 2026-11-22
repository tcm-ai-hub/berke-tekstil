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

  // scroll-driven cotton → yarn → product
  var sy = $("[data-scrolly]");
  if (sy) {
    var layers = $$(".sc-layer", sy), texts = $$(".sc-text p", sy), svg = $(".sc-threads", sy), cot = $("[data-cotton]", sy), cue = $(".sc-cue", sy);
    var hdr = $(".site-h"), N = layers.length, lines = [], seeded = 0;
    var rnd = function () { seeded = (seeded * 9301 + 49297) % 233280; return seeded / 233280; };
    var build = function () {
      var W = innerWidth, H = innerHeight, iw = 736, ih = 1103;
      var sc = Math.min(W / iw, H / ih), dw = iw * sc, dh = ih * sc, ox = (W - dw) / 2, oy = (H - dh) / 2;
      var cx = ox + dw * 0.46, cy = oy + dh * 0.60;   // lower cotton boll
      svg.setAttribute("viewBox", "0 0 " + W + " " + H); svg.innerHTML = ""; lines = []; seeded = 7;
      for (var k = 0; k < 46; k++) {
        var tx = W * (0.08 + rnd() * 0.84), ty = -10 + rnd() * H * 0.08;
        var sx = cx + (rnd() - 0.5) * dw * 0.22, s2 = cy + (rnd() - 0.5) * dh * 0.08;
        var l = document.createElementNS("http://www.w3.org/2000/svg", "line");
        l.setAttribute("x1", sx); l.setAttribute("y1", s2); l.setAttribute("x2", tx); l.setAttribute("y2", ty);
        var len = Math.hypot(tx - sx, ty - s2); l.style.strokeDasharray = len; l.style.strokeDashoffset = len;
        svg.appendChild(l); lines.push([l, len, rnd() * 0.35]);
      }
    };
    var clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
    var last = -1;
    var update = function () {
      var r = sy.getBoundingClientRect(), H = innerHeight;
      var p = clamp(-r.top / (sy.offsetHeight - H)), x = p * N;
      layers.forEach(function (el, i) {
        var o = i === 0 ? clamp((1.25 - x) / 0.35) : clamp((0.62 - Math.abs(x - i - 0.5)) / 0.24);
        if (i === N - 1 && x > N - 0.5) o = 1;
        el.style.opacity = o;
        var v = $("video", el); if (v) { if (o > 0.3 && !reduce) { if (v.paused) play(v); } else if (!v.paused) v.pause(); }
      });
      var t = clamp(x / 0.95);
      lines.forEach(function (a) { var q = clamp((t - a[2]) / (1 - a[2])); a[0].style.strokeDashoffset = a[1] * (1 - q); });
      svg.style.opacity = clamp((1.3 - x) / 0.3);
      texts.forEach(function (el, i) { el.style.opacity = clamp((0.45 - Math.abs(x - i - 0.5)) / 0.18); el.style.transform = "translateY(" + ((x - i - 0.5) * -24).toFixed(1) + "px)"; });
      if (cue) cue.style.opacity = clamp(1 - x * 3);
      if (hdr) hdr.classList.toggle("solid", r.bottom < 80);
    };
    var onScroll = function () { if (last) cancelAnimationFrame(last); last = requestAnimationFrame(update); };
    build(); update();
    addEventListener("scroll", onScroll, { passive: true });
    addEventListener("resize", function () { build(); update(); });
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
