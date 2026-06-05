// Gallery lightbox — click any gallery plate to view the full, uncropped image.
// Click anywhere or press Esc to close. No dependencies.
(function () {
  function init() {
    var imgs = document.querySelectorAll('.gal-grid .img-slot img');
    if (!imgs.length) return;

    var lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.innerHTML = '<span class="lb-close" aria-hidden="true">✕</span><img alt="" />';
    document.body.appendChild(lb);
    var lbImg = lb.querySelector('img');

    function open(src, alt) {
      lbImg.src = src;
      lbImg.alt = alt || '';
      lb.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
    function close() {
      lb.classList.remove('open');
      document.body.style.overflow = '';
      lbImg.removeAttribute('src');
    }

    imgs.forEach(function (img) {
      img.addEventListener('click', function () {
        open(img.currentSrc || img.src, img.alt);
      });
    });
    lb.addEventListener('click', close);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && lb.classList.contains('open')) close();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
