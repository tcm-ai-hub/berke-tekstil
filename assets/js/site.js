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

  // journey: scroll-driven scenes on desktop; static stacked on mobile / reduced motion
  var jy = $("[data-journey]");
  if (jy) {
    var scenes = $$(".jy-scene", jy), N = scenes.length, hdr = $(".site-h");
    var count = $(".jy-count", jy), bar = $(".jy-bar i", jy), cue = $(".jy-cue", jy), svg = $(".jy-threads", jy);
    var clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
    var loadVid = function (sc) { var v = $("video", sc); if (v && !v.src && v.dataset.src) v.src = v.dataset.src; return v; };
    var live = !reduce && matchMedia("(min-width: 901px)").matches;
    var lines = [];
    var threads = function () {
      if (!svg) return; var img = $("img", scenes[0]); if (!img) return;
      var W = innerWidth, H = innerHeight, iw = img.naturalWidth || 736, ih = img.naturalHeight || 1103;
      var sc = Math.min(W / iw, H / ih), dw = iw * sc, dh = ih * sc, ox = (W - dw) / 2, oy = (H - dh) / 2;
      var cx = ox + dw * 0.46, cy = oy + dh * 0.60, seed = 7, rnd = function () { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; };
      svg.setAttribute("viewBox", "0 0 " + W + " " + H); svg.innerHTML = ""; lines = [];
      for (var k = 0; k < 40; k++) {
        var tx = W * (0.1 + rnd() * 0.8), ty = -10 + rnd() * H * 0.06, sx = cx + (rnd() - 0.5) * dw * 0.2, sy2 = cy + (rnd() - 0.5) * dh * 0.07;
        var l = document.createElementNS("http://www.w3.org/2000/svg", "line");
        l.setAttribute("x1", sx); l.setAttribute("y1", sy2); l.setAttribute("x2", tx); l.setAttribute("y2", ty);
        var len = Math.hypot(tx - sx, ty - sy2); l.style.strokeDasharray = len; l.style.strokeDashoffset = len;
        svg.appendChild(l); lines.push([l, len, rnd() * 0.4]);
      }
    };
    if (!live) {
      // static: play videos only while visible
      if (!reduce && "IntersectionObserver" in window) {
        var jo = new IntersectionObserver(function (es) { es.forEach(function (e) { var v = loadVid(e.target); if (v) { if (e.isIntersecting) play(v); else v.pause(); } }); }, { rootMargin: "200px 0px" });
        scenes.forEach(function (s2) { jo.observe(s2); });
      } else scenes.forEach(loadVid);
      if (hdr) hdr.classList.add("solid");
    } else {
      jy.classList.add("live"); jy.style.setProperty("--n", N + 0.6);
      var raf = 0, cur = -1;
      var update = function () {
        raf = 0;
        var r = jy.getBoundingClientRect(), H = innerHeight, p = clamp(-r.top / (jy.offsetHeight - H)), x = p * N;
        var idx = Math.min(N - 1, Math.floor(x));
        scenes.forEach(function (el, i) {
          var o = i === 0 ? clamp((1.3 - x) / 0.3) : i === N - 1 ? clamp((x - i + 0.3) / 0.3) : clamp((0.65 - Math.abs(x - i - 0.5)) / 0.15);
          el.style.opacity = o;
          var local = clamp(x - i + 0.3) ;
          var m = $(".jy-media", el); if (m) m.style.transform = "scale(" + (1.07 - 0.07 * clamp(local / 1.3)).toFixed(4) + ")";
          var c = $(".jy-copy", el); if (c) c.style.transform = "translateY(" + ((0.5 - clamp(local / 1.3)) * 36).toFixed(1) + "px)";
          if (Math.abs(x - i - 0.5) < 1.2) { var v = loadVid(el); if (v) { if (o > 0.2) { if (v.paused) play(v); } else if (!v.paused) v.pause(); } }
          else { var v2 = $("video", el); if (v2 && !v2.paused) v2.pause(); }
        });
        if (idx !== cur) {
          cur = idx; scenes.forEach(function (el, i) { el.classList.toggle("on", i === idx); });
          if (count) count.textContent = ("0" + (idx + 1)).slice(-2) + " / " + ("0" + N).slice(-2);
          var lt = !!$(".jy-type", scenes[idx]); jy.classList.toggle("dark-ui", lt); if (hdr) hdr.classList.toggle("on-light", lt);
        }
        if (bar) bar.style.width = (p * 100).toFixed(1) + "%";
        var t = clamp(x / 0.9);
        lines.forEach(function (a) { var q = clamp((t - a[2]) / (1 - a[2])); a[0].style.strokeDashoffset = a[1] * (1 - q); });
        if (cue) cue.style.opacity = clamp(1 - x * 3);
        if (hdr) hdr.classList.toggle("solid", r.bottom < 80);
      };
      var req = function () { if (!raf) raf = requestAnimationFrame(update); };
      var img0 = $("img", scenes[0]);
      if (img0 && !img0.complete) img0.addEventListener("load", function () { threads(); req(); });
      threads(); update();
      addEventListener("scroll", req, { passive: true });
      addEventListener("resize", function () { threads(); req(); });
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
