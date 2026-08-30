// Doxha Church — site interactions

document.addEventListener('DOMContentLoaded', () => {
  /* Sticky nav shadow on scroll */
  const nav = document.querySelector('.nav');
  if (nav) {
    const onScroll = () => {
      if (window.scrollY > 8) {
        nav.style.boxShadow = '0 1px 0 rgba(10,14,26,0.06)';
        nav.style.background = 'rgba(255,255,255,0.86)';
      } else {
        nav.style.boxShadow = 'none';
        nav.style.background = 'rgba(255,255,255,0.72)';
      }
    };
    document.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* Mobile menu toggle */
  const navToggle = document.querySelector('.nav-toggle');
  const mobileMenu = document.querySelector('.mobile-menu');
  if (navToggle && mobileMenu) {
    navToggle.addEventListener('click', () => {
      mobileMenu.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', mobileMenu.classList.contains('open'));
    });
    mobileMenu.querySelectorAll('a').forEach((a) =>
      a.addEventListener('click', () => mobileMenu.classList.remove('open'))
    );
  }

  /* Reveal on scroll */
  const revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealEls.length) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('in-view');
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('in-view'));
  }

  /* FAQ accordion */
  document.querySelectorAll('.faq-item').forEach((item) => {
    const q = item.querySelector('.faq-q');
    if (!q) return;
    q.addEventListener('click', () => {
      const wasOpen = item.classList.contains('open');
      item.parentElement.querySelectorAll('.faq-item.open').forEach((i) => i.classList.remove('open'));
      if (!wasOpen) item.classList.add('open');
    });
  });

  /* Pricing billing toggle (monthly / annual) */
  const switchEl = document.querySelector('.switch');
  if (switchEl) {
    switchEl.addEventListener('click', () => {
      const annual = switchEl.classList.toggle('on');
      switchEl.setAttribute('aria-checked', annual);
      document.querySelectorAll('[data-monthly]').forEach((el) => {
        el.textContent = annual ? el.dataset.annual : el.dataset.monthly;
      });
      document.querySelectorAll('[data-period]').forEach((el) => {
        el.textContent = annual ? '/mois, facturé annuellement' : '/mois';
      });
    });
  }

  /* Contact / auth forms: prevent real submit (static site demo) */
  document.querySelectorAll('form[data-demo-form]').forEach((form) => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const feedback = form.querySelector('.form-feedback');
      if (feedback) {
        feedback.textContent = 'Merci ! Votre demande a bien été enregistrée. Notre équipe vous répond sous 24h.';
        feedback.style.display = 'block';
      }
      form.reset();
    });
  });
});
