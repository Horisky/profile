// i18n.js — tiny language switcher shared across all pages.
// Reads/writes localStorage.profile-lang, drives html[lang], and
// marks the active toggle in .lang-switch.
(function () {
  var KEY = "profile.lang";
  var DEFAULT = "en";

  // Early: set html[lang] BEFORE CSS paints so there's no flash of EN.
  try {
    var saved = localStorage.getItem(KEY) || DEFAULT;
    document.documentElement.lang = saved;
  } catch (e) {
    document.documentElement.lang = DEFAULT;
  }

  function setLang(l) {
    if (l !== "en" && l !== "zh") l = DEFAULT;
    document.documentElement.lang = l;
    try { localStorage.setItem(KEY, l); } catch (e) {}
    document.querySelectorAll(".lang-switch a[data-lang]").forEach(function (a) {
      a.classList.toggle("active", a.dataset.lang === l);
    });
  }

  // delegate click, works even before DOM-ready
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest(".lang-switch a[data-lang]");
    if (!a) return;
    e.preventDefault();
    setLang(a.dataset.lang);
  });

  function init() { setLang(document.documentElement.lang); }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
