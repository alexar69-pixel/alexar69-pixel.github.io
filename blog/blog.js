async function loadPosts() {
  const list = document.getElementById('post-list');
  if (!list) return;
  list.innerHTML = '<div class="mono" style="color: var(--a);">Leyendo registros...</div>';

  const resp = await fetch('/blog/data/posts.json', { cache: 'no-store' });
  const posts = await resp.json();

  if (!Array.isArray(posts) || posts.length === 0) {
    list.innerHTML = '<div class="mono" style="color: var(--td);">Ningún registro activo. [EOF]</div>';
    return;
  }

  const fmt = new Intl.DateTimeFormat('es-ES', { dateStyle: 'long' });

  list.innerHTML = posts
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .map((post) => {
      const tags = (post.tags || []).map((t) => `<span>${t}</span>`).join('');
      return `
        <a class="gusto-card glass-card reveal-up tilt-card mag-btn" href="/blog/post.html?slug=${encodeURIComponent(post.slug)}">
          <div class="gc-glow"></div>
          <div class="gc-emoji">📝</div>
          <div class="gc-corner">// post</div>
          <span class="mono" style="color: var(--a); font-size: 0.72rem; display: block; margin-bottom: 0.25rem;">// ${fmt.format(new Date(post.date))}</span>
          <h3 style="margin-top: 0.25rem; margin-bottom: 0.5rem; font-size: 1.15rem; font-weight: 700; color: var(--t);">${post.title}</h3>
          <p style="font-size: 0.88rem; color: var(--tm); line-height: 1.5; margin-bottom: 1rem;">${post.excerpt || ''}</p>
          <div class="gc-tags">${tags}</div>
        </a>
      `;
    })
    .join('');

  // Vincular efectos interactivos dinámicos a las nuevas tarjetas
  initializeDynamicEffects();
}

function initializeDynamicEffects() {
  const list = document.getElementById('post-list');
  if (!list) return;
  const cards = list.querySelectorAll('.gusto-card');
  const ring = document.getElementById('cursorRing');

  cards.forEach(card => {
    // 1. Efecto Hover en Cursor
    if (ring) {
      card.addEventListener('mouseenter', () => ring.classList.add('hover'));
      card.addEventListener('mouseleave', () => ring.classList.remove('hover'));
    }

    // 2. Efecto Magnético (ajustado para tarjetas grandes)
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const dx = (e.clientX - cx) * 0.15;
      const dy = (e.clientY - cy) * 0.15;
      card.style.transform = `translate(${dx}px, ${dy}px) translateY(-4px)`;
    });
    
    // 3. Efecto Tilt 3D y brillo
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const dx = (e.clientX - rect.left - rect.width / 2) / (rect.width / 2);
      const dy = (e.clientY - rect.top - rect.height / 2) / (rect.height / 2);
      card.style.transform = `translateY(-6px) rotateX(${-dy * 4}deg) rotateY(${dx * 4}deg)`;
      card.style.transformStyle = 'preserve-3d';
      
      const glow = card.querySelector('.gc-glow');
      if (glow) {
        glow.style.background = `radial-gradient(circle at ${(dx + 1) * 50}% ${(dy + 1) * 50}%, rgba(249,115,22,0.1), transparent 60%)`;
        glow.style.opacity = '1';
      }
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
      const glow = card.querySelector('.gc-glow');
      if (glow) glow.style.opacity = '0';
    });
  });

  // 4. Reveal al hacer scroll
  const revObs = new IntersectionObserver((entries) => {
    entries.forEach((e, i) => {
      if (e.isIntersecting) {
        setTimeout(() => e.target.classList.add('vis'), i * 65);
        revObs.unobserve(e.target);
      }
    });
  }, { threshold: 0.05 });
  
  cards.forEach(card => revObs.observe(card));
}

loadPosts().catch((err) => {
  console.error("Error al cargar posts:", err);
  const list = document.getElementById('post-list');
  if (list) {
    list.innerHTML = '<div class="mono" style="color: #ff5f57;">[ERR] No se pudieron cargar los registros.</div>';
  }
});
