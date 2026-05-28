async function loadPosts() {
  const list = document.getElementById('post-list');
  list.textContent = 'Cargando...';

  const resp = await fetch('/blog/data/posts.json', { cache: 'no-store' });
  const posts = await resp.json();

  if (!Array.isArray(posts) || posts.length === 0) {
    list.textContent = 'Todavía no hay entradas publicadas.';
    return;
  }

  const fmt = new Intl.DateTimeFormat('es-ES', { dateStyle: 'long' });

  list.innerHTML = posts
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .map((post) => {
      const tags = (post.tags || []).map((t) => `<span class="tag">${t}</span>`).join('');
      return `
        <a class="card" href="/blog/post.html?slug=${encodeURIComponent(post.slug)}">
          <h2>${post.title}</h2>
          <p class="meta">${fmt.format(new Date(post.date))}</p>
          <p>${post.excerpt || ''}</p>
          <div class="tags">${tags}</div>
        </a>
      `;
    })
    .join('');
}

loadPosts().catch(() => {
  const list = document.getElementById('post-list');
  list.textContent = 'No se pudieron cargar las entradas.';
});
