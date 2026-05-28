function getSlug() {
  const params = new URLSearchParams(window.location.search);
  return params.get('slug');
}

async function renderPost() {
  const postEl = document.getElementById('post');
  const slug = getSlug();

  if (!slug) {
    postEl.innerHTML = '<h1>Entrada no encontrada</h1>';
    return;
  }

  const [postsResp, htmlResp] = await Promise.all([
    fetch('/blog/data/posts.json', { cache: 'no-store' }),
    fetch(`/blog/posts/${encodeURIComponent(slug)}.html`, { cache: 'no-store' })
  ]);

  if (!postsResp.ok || !htmlResp.ok) {
    postEl.innerHTML = '<h1>Entrada no encontrada</h1>';
    return;
  }

  const posts = await postsResp.json();
  const meta = posts.find((p) => p.slug === slug);
  const html = await htmlResp.text();

  if (!meta) {
    postEl.innerHTML = '<h1>Entrada no encontrada</h1>';
    return;
  }

  const date = new Intl.DateTimeFormat('es-ES', { dateStyle: 'long' }).format(new Date(meta.date));
  document.title = `${meta.title} | Blog de Alexander Armentia`;

  postEl.innerHTML = `
    <h1>${meta.title}</h1>
    <p class="meta">${date}</p>
    <div class="content">${html}</div>
  `;
}

renderPost().catch(() => {
  document.getElementById('post').innerHTML = '<h1>Error cargando la entrada</h1>';
});
