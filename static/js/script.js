/**
 * AURIC — Premium Digital Experience v3.0
 * Full interaction + motion system
 */

document.addEventListener('DOMContentLoaded', () => {

    // ── Scroll Header ──────────────────
    const header = document.getElementById('mainHeader');
    window.addEventListener('scroll', () => {
        header?.classList.toggle('header--scrolled', window.scrollY > 60);
    }, { passive: true });


    // ── Reveal Animations ──────────────
    const revealObs = new IntersectionObserver((entries) => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                e.target.classList.add('reveal--visible');
                revealObs.unobserve(e.target);
            }
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    document.querySelectorAll('.reveal').forEach(el => revealObs.observe(el));


    // ── Mobile Menu ────────────────────
    const menuToggle  = document.getElementById('menuToggle');
    const menuClose   = document.getElementById('menuClose');
    const mobileNav   = document.getElementById('mobileNav');

    const openMenu  = () => { mobileNav?.classList.add('mobile-nav--active');    document.body.style.overflow='hidden'; };
    const closeMenu = () => { mobileNav?.classList.remove('mobile-nav--active'); document.body.style.overflow=''; };

    menuToggle?.addEventListener('click', openMenu);
    menuClose?.addEventListener('click', closeMenu);
    document.querySelectorAll('.mobile-nav__link').forEach(l => l.addEventListener('click', closeMenu));

    // Close on backdrop click
    mobileNav?.addEventListener('click', (e) => { if (e.target === mobileNav) closeMenu(); });


    // ── Smooth Scroll ──────────────────
    document.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener('click', e => {
            const target = document.querySelector(a.getAttribute('href'));
            if (target) {
                e.preventDefault();
                window.scrollTo({ top: target.offsetTop - 80, behavior: 'smooth' });
            }
        });
    });


    // ── Auto-dismiss Messages ──────────
    document.querySelectorAll('.message').forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'opacity .5s ease, transform .5s ease';
            msg.style.opacity = '0'; msg.style.transform = 'translateX(20px)';
            setTimeout(() => msg.remove(), 500);
        }, 4000);
    });


    // ── Image Parallax on Hero ─────────
    const heroVisual = document.querySelector('.hero__visual .hero__image');
    if (heroVisual) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            heroVisual.style.transform = `scale(1) translateY(${scrolled * 0.12}px)`;
        }, { passive: true });
    }


    // ── Checkout form styling ──────────
    document.querySelectorAll('.form-group input, .form-group textarea, .form-group select').forEach(input => {
        input.classList.add('form-control');
    });

});
