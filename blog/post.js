function getSlug() {
  const params = new URLSearchParams(window.location.search);
  return params.get('slug');
}

async function renderPost() {
  const postEl = document.getElementById('post');
  const slug = getSlug();

  if (!slug) {
    postEl.innerHTML = '<h1 style="color: var(--t);">Entrada no encontrada</h1>';
    return;
  }

  const [postsResp, htmlResp] = await Promise.all([
    fetch('/blog/data/posts.json', { cache: 'no-store' }),
    fetch(`/blog/posts/${encodeURIComponent(slug)}.html`, { cache: 'no-store' })
  ]);

  if (!postsResp.ok || !htmlResp.ok) {
    postEl.innerHTML = '<h1 style="color: var(--t);">Entrada no encontrada</h1>';
    return;
  }

  const posts = await postsResp.json();
  const meta = posts.find((p) => p.slug === slug);
  const html = await htmlResp.text();

  if (!meta) {
    postEl.innerHTML = '<h1 style="color: var(--t);">Entrada no encontrada</h1>';
    return;
  }

  // Actualizar Título del Documento y Cabecera de Terminal
  document.title = `${meta.title} · Blog · Alexander Armentia`;
  const termSlugEl = document.getElementById('terminal-post-slug');
  if (termSlugEl) {
    termSlugEl.textContent = `${slug}.md`;
  }

  const date = new Intl.DateTimeFormat('es-ES', { dateStyle: 'long' }).format(new Date(meta.date));

  // Inyectar Contenido
  postEl.innerHTML = `
    <span class="mono" style="color: var(--a); font-size: 0.8rem; display: block; margin-bottom: 0.5rem;">// Publicado el ${date}</span>
    <h1 class="post-title" style="margin-top: 0.25rem; margin-bottom: 1.5rem; color: var(--t); font-weight: 800; font-size: clamp(1.8rem, 3.5vw, 2.8rem); line-height: 1.15;">${meta.title}</h1>
    <div class="content">${html}</div>
  `;

  // Configurar Compartición Social
  setupSharePanel(meta.title);
}

function setupSharePanel(postTitle) {
  const url = window.location.href;
  
  const shareLinkedin = document.getElementById('share-linkedin');
  const shareTwitter = document.getElementById('share-twitter');
  const shareCopy = document.getElementById('share-copy');

  if (shareLinkedin) {
    shareLinkedin.href = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`;
  }

  if (shareTwitter) {
    shareTwitter.href = `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(postTitle + " — por Alexander Armentia (Alexar69)")}`;
  }

  if (shareCopy) {
    shareCopy.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(url);
        const copyTxt = document.getElementById('copy-btn-text');
        if (copyTxt) {
          copyTxt.textContent = '¡Copiado! ✓';
          setTimeout(() => {
            copyTxt.textContent = 'Copiar Enlace';
          }, 3000);
        }
      } catch (err) {
        console.error('Error al copiar el enlace:', err);
      }
    });
  }
}

renderPost().catch((err) => {
  console.error("Error al renderizar el post:", err);
  document.getElementById('post').innerHTML = '<h1 style="color: #ff5f57;">[ERR] Error cargando la entrada.</h1>';
});
