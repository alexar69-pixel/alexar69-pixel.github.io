'use strict';

// ══════════════════════════════════════════════════
//  SERVICE WORKER REGISTRATION (PWA)
// ══════════════════════════════════════════════════
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .catch(err => console.log('SW Registration failed: ', err));
  });
}

// ══════════════════════════════════════════════════
//  CURSOR — ring + dot + trail canvas
// ══════════════════════════════════════════════════
const ring = document.getElementById('cursorRing');
const dot = document.getElementById('cursorDot');
const trailCanvas = document.getElementById('trailCanvas');
const tCtx = trailCanvas.getContext('2d');

let mx = -300, my = -300, rx = -300, ry = -300;
let trailPts = [];

function resizeTrail() {
  trailCanvas.width = window.innerWidth;
  trailCanvas.height = window.innerHeight;
}
window.addEventListener('resize', resizeTrail, { passive: true });
resizeTrail();

document.addEventListener('mousemove', e => {
  mx = e.clientX; my = e.clientY;
  dot.style.left = mx + 'px';
  dot.style.top = my + 'px';
  trailPts.push({ x: mx, y: my, life: 1 });
  if (trailPts.length > 28) trailPts.shift();
});
document.addEventListener('mousedown', () => ring.classList.add('click'));
document.addEventListener('mouseup', () => ring.classList.remove('click'));

(function animCursor() {
  rx += (mx - rx) * 0.1;
  ry += (my - ry) * 0.1;
  ring.style.left = rx + 'px';
  ring.style.top = ry + 'px';

  // Trail
  tCtx.clearRect(0, 0, trailCanvas.width, trailCanvas.height);
  trailPts = trailPts.map(p => ({ ...p, life: p.life - 0.045 })).filter(p => p.life > 0);
  for (let i = 1; i < trailPts.length; i++) {
    const p = trailPts[i];
    const pp = trailPts[i - 1];
    tCtx.beginPath();
    tCtx.moveTo(pp.x, pp.y);
    tCtx.lineTo(p.x, p.y);
    tCtx.strokeStyle = `rgba(249,115,22,${p.life * 0.35})`;
    tCtx.lineWidth = p.life * 3;
    tCtx.lineCap = 'round';
    tCtx.stroke();
  }
  requestAnimationFrame(animCursor);
})();

// Hover states
document.querySelectorAll('a, button, .htag, .gusto-card, .tl-card, .cw-item, .vibe-bar, .fbadge, .hologram-card')
  .forEach(el => {
    el.addEventListener('mouseenter', () => ring.classList.add('hover'));
    el.addEventListener('mouseleave', () => ring.classList.remove('hover'));
  });

// ══════════════════════════════════════════════════
//  SCROLL PROGRESS BAR
// ══════════════════════════════════════════════════
const progressBar = document.getElementById('scrollProgress');
window.addEventListener('scroll', () => {
  const max = document.documentElement.scrollHeight - window.innerHeight;
  progressBar.style.width = ((window.scrollY / max) * 100) + '%';
}, { passive: true });

// ══════════════════════════════════════════════════
//  NAVBAR SCROLL
// ══════════════════════════════════════════════════
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 50);
}, { passive: true });

// ══════════════════════════════════════════════════
//  HAMBURGER
// ══════════════════════════════════════════════════
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('nav-links');
hamburger.addEventListener('click', () => {
  const open = navLinks.classList.toggle('open');
  const [s1, s2, s3] = hamburger.querySelectorAll('span');
  if (open) {
    s1.style.cssText = 'transform:translateY(7px) rotate(45deg)';
    s2.style.cssText = 'opacity:0;transform:scaleX(0)';
    s3.style.cssText = 'transform:translateY(-7px) rotate(-45deg)';
  } else {
    [s1, s2, s3].forEach(s => s.style.cssText = '');
  }
});
navLinks.querySelectorAll('.nav-link').forEach(l => {
  l.addEventListener('click', () => {
    navLinks.classList.remove('open');
    hamburger.querySelectorAll('span').forEach(s => s.style.cssText = '');
  });
});

// ══════════════════════════════════════════════════
//  PARALLAX — multiple layers on scroll
// ══════════════════════════════════════════════════
const pLayer1 = document.getElementById('pLayer1');
const pLayer2 = document.getElementById('pLayer2');
const heroInner = document.getElementById('heroInner');

window.addEventListener('scroll', () => {
  const y = window.scrollY;
  // Background layers move slower
  if (pLayer1) pLayer1.style.transform = `translateY(${y * 0.25}px)`;
  if (pLayer2) pLayer2.style.transform = `translateY(${y * -0.15}px)`;
  // Hero content subtle parallax
  if (heroInner) {
    const heroLeft = heroInner.querySelector('.hero-left');
    const heroRight = heroInner.querySelector('.hero-right');
    if (heroLeft) heroLeft.style.transform = `translateY(${y * 0.08}px)`;
    if (heroRight) heroRight.style.transform = `translateY(${y * 0.15}px)`;
  }
}, { passive: true });

// Parallax on individual elements with data-parallax
document.querySelectorAll('[data-parallax]').forEach(el => {
  const speed = parseFloat(el.getAttribute('data-parallax'));
  const obs = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) {
      window.addEventListener('scroll', () => {
        const rect = el.parentElement.getBoundingClientRect();
        el.style.transform = `translateY(${-rect.top * speed}px)`;
      }, { passive: true });
    }
  }, { threshold: 0 });
  obs.observe(el);
});

// ══════════════════════════════════════════════════
//  TEXT SCRAMBLE EFFECT — hero name
// ══════════════════════════════════════════════════
const CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
function scramble(el, finalText, duration = 1500) {
  const totalFrames = Math.round(duration / 30);
  let frame = 0;
  const interval = setInterval(() => {
    const progress = frame / totalFrames;
    const revealed = Math.floor(progress * finalText.length);
    let result = '';
    for (let i = 0; i < finalText.length; i++) {
      if (i < revealed) {
        result += finalText[i];
      } else {
        result += CHARS[Math.floor(Math.random() * CHARS.length)];
      }
    }
    el.textContent = result;
    frame++;
    if (frame >= totalFrames) {
      clearInterval(interval);
      el.textContent = finalText;
    }
  }, 30);
}

window.addEventListener('load', () => {
  const nameEl = document.getElementById('heroName');
  if (nameEl) {
    setTimeout(() => scramble(nameEl, 'Alexander', 1800), 400);
  }
});

// Scramble on nav logo hover
const logoText = document.querySelector('.logo-text');
if (logoText) {
  logoText.addEventListener('mouseenter', () => scramble(logoText, 'ALEX', 500));
}

// ══════════════════════════════════════════════════
//  TERMINAL BAR — typing effect
// ══════════════════════════════════════════════════
const termCmd = document.getElementById('termCmd');
const cmds = [
  'init --personal-site',
  'coffee.brew() ☕',
  'git commit -m "hola mundo"',
  'sudo make me_cool',
  'cd ~/ideas && ls',
  'npm run build-dreams',
];
let cmdIdx = 0;

function typeCmd(text, cb) {
  if (!termCmd) return;
  termCmd.textContent = '';
  let i = 0;
  const t = setInterval(() => {
    termCmd.textContent = text.slice(0, ++i) + '▋';
    if (i >= text.length) {
      clearInterval(t);
      termCmd.textContent = text + ' ✓';
      setTimeout(cb, 1800);
    }
  }, 60);
}

function cycleCmd() {
  typeCmd(cmds[cmdIdx], () => {
    cmdIdx = (cmdIdx + 1) % cmds.length;
    setTimeout(cycleCmd, 500);
  });
}
window.addEventListener('load', () => setTimeout(cycleCmd, 800));

// ══════════════════════════════════════════════════
//  COUNTER ANIMATION — HUD stats
// ══════════════════════════════════════════════════
function animCounter(el) {
  const target = +el.getAttribute('data-target');
  const dur = 2000, start = performance.now();
  const update = now => {
    const t = Math.min((now - start) / dur, 1);
    const eased = 1 - Math.pow(1 - t, 3);
    el.textContent = Math.round(eased * target);
    if (t < 1) requestAnimationFrame(update);
  };
  requestAnimationFrame(update);
}
const hudObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.querySelectorAll('.hud-val').forEach(animCounter);
      hudObs.unobserve(e.target);
    }
  });
}, { threshold: 0.5 });
const hud = document.querySelector('.hud-stats');
if (hud) hudObs.observe(hud);

// ══════════════════════════════════════════════════
//  REVEAL ON SCROLL
// ══════════════════════════════════════════════════
const revEls = document.querySelectorAll('.reveal-up, .reveal-fade, .reveal-word, .tl-card, .gusto-card, .cw-item, .big-quote, .avail-card, .vibe-bar, .callout');
const revObs = new IntersectionObserver((entries) => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) {
      setTimeout(() => e.target.classList.add('vis'), i * 65);
      revObs.unobserve(e.target);
    }
  });
}, { threshold: 0.08 });
revEls.forEach(el => revObs.observe(el));

// ══════════════════════════════════════════════════
//  MAGNETIC BUTTONS
// ══════════════════════════════════════════════════
document.querySelectorAll('.mag-btn').forEach(btn => {
  btn.addEventListener('mousemove', e => {
    const rect = btn.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    const dx = (e.clientX - cx) * 0.35;
    const dy = (e.clientY - cy) * 0.35;
    btn.style.transform = `translate(${dx}px, ${dy}px)`;
  });
  btn.addEventListener('mouseleave', () => {
    btn.style.transform = '';
  });
});

// ══════════════════════════════════════════════════
//  TILT — 3D card effect
// ══════════════════════════════════════════════════
document.querySelectorAll('.tilt-card, .tl-card').forEach(card => {
  card.addEventListener('mousemove', e => {
    const rect = card.getBoundingClientRect();
    const dx = (e.clientX - rect.left - rect.width / 2) / (rect.width / 2);
    const dy = (e.clientY - rect.top - rect.height / 2) / (rect.height / 2);
    card.style.transform = `translateY(-6px) rotateX(${-dy * 6}deg) rotateY(${dx * 6}deg)`;
    card.style.transformStyle = 'preserve-3d';
    // Move glow
    const glow = card.querySelector('.gc-glow');
    if (glow) {
      glow.style.background = `radial-gradient(circle at ${(dx + 1) * 50}% ${(dy + 1) * 50}%, rgba(249,115,22,0.12), transparent 60%)`;
      glow.style.opacity = '1';
    }
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = '';
    const glow = card.querySelector('.gc-glow');
    if (glow) glow.style.opacity = '0';
  });
});

// ══════════════════════════════════════════════════
//  PARTICLE CANVAS — bg
// ══════════════════════════════════════════════════
(function bgParticles() {
  const c = document.getElementById('bgCanvas');
  const ctx = c.getContext('2d');
  let W, H, pts = [];
  const N = 70, LINK = 110;

  function resize() {
    W = c.width = innerWidth;
    H = c.height = innerHeight;
  }
  window.addEventListener('resize', resize, { passive: true });
  resize();

  function rnd(a, b) { return Math.random() * (b - a) + a; }

  class P {
    constructor() {
      this.x = rnd(0, W); this.y = rnd(0, H);
      this.vx = rnd(-.2, .2); this.vy = rnd(-.2, .2);
      this.r = rnd(.8, 2.2); this.a = rnd(.15, .5);
      this.col = (['249,115,22', '129,140,248', '34,211,238'])[Math.floor(Math.random() * 3)];
    }
    tick() {
      this.x += this.vx; this.y += this.vy;
      if (this.x < 0 || this.x > W) this.vx *= -1;
      if (this.y < 0 || this.y > H) this.vy *= -1;
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${this.col},${this.a})`;
      ctx.fill();
    }
  }
  for (let i = 0; i < N; i++) pts.push(new P());

  let pmx = -999, pmy = -999;
  document.addEventListener('mousemove', e => { pmx = e.clientX; pmy = e.clientY; });

  function draw() {
    ctx.clearRect(0, 0, W, H);
    pts.forEach(p => {
      const dx = p.x - pmx, dy = p.y - pmy, d = Math.sqrt(dx * dx + dy * dy);
      if (d < 80) { p.vx += dx * .0005; p.vy += dy * .0005; }
      const sp = Math.sqrt(p.vx * p.vx + p.vy * p.vy);
      if (sp > 1.0) { p.vx *= .93; p.vy *= .93; }
      p.tick(); p.draw();
    });
    for (let i = 0; i < pts.length; i++) {
      for (let j = i + 1; j < pts.length; j++) {
        const dx = pts[i].x - pts[j].x, dy = pts[i].y - pts[j].y;
        const d = Math.sqrt(dx * dx + dy * dy);
        if (d < LINK) {
          const a = (1 - d / LINK) * .18;
          ctx.beginPath();
          ctx.moveTo(pts[i].x, pts[i].y);
          ctx.lineTo(pts[j].x, pts[j].y);
          ctx.strokeStyle = `rgba(249,115,22,${a})`;
          ctx.lineWidth = .7;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(draw);
  }
  draw();
})();

// ══════════════════════════════════════════════════
//  VIBE TRACK ROTATOR
// ══════════════════════════════════════════════════
const tracks = [
  'Pont Aeri — Flying Free',
  'Chimo Bayo — Así me gusta a mí',
  'Paco Pil — Viva la Fiesta',
  'Scorpia — Hypnose',
  'X-Que — X-Que Vol. 1',
  'Pastis & Buenri — Pildo',
  'DJ Marta — The Woman',
  'Viceversa — Tu Piel Morena',
  'Ku Minerva — Estoy Llorando por Ti',
  'New Limit — Smile',
  'Double Vision — Knockin',
  'Julio Posadas — Pi',
  'DJ Neil — Boomerang',
];
const vibeEl = document.getElementById('vibeTrack');
const vibeTime = document.getElementById('vibeTime');

function pickTrack() {
  if (!vibeEl) return;
  const t = tracks[Math.floor(Math.random() * tracks.length)];
  vibeEl.style.opacity = '0';
  vibeEl.style.transform = 'translateY(8px)';
  setTimeout(() => {
    vibeEl.textContent = t;
    vibeEl.style.opacity = '1';
    vibeEl.style.transform = 'translateY(0)';
  }, 350);
}

if (vibeEl) {
  vibeEl.style.transition = 'opacity .35s ease, transform .35s ease';
  pickTrack();
  setInterval(pickTrack, 8000);
}

// Fake timer
if (vibeTime) {
  let secs = Math.floor(Math.random() * 60);
  let mins = Math.floor(Math.random() * 3);
  setInterval(() => {
    secs++;
    if (secs >= 60) { secs = 0; mins++; }
    vibeTime.textContent = `${mins}:${String(secs).padStart(2, '0')}`;
  }, 1000);
}

// ══════════════════════════════════════════════════
//  NOC CLOCK & SYSTEM SYNC
// ══════════════════════════════════════════════════
function updateNocClock() {
  const clockEl = document.getElementById('nocClock');
  if (!clockEl) return;
  const now = new Date();
  clockEl.textContent = now.toLocaleTimeString('es-ES', {
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
}
setInterval(updateNocClock, 1000);
updateNocClock();

// Simulation Jitter for NOC Stats
function applyNocJitter() {
  const rttEls = document.querySelectorAll('.noc-svc-rtt');
  rttEls.forEach(el => {
    const base = parseInt(el.textContent);
    if (!isNaN(base)) {
      const jitter = (Math.random() * 4 - 2); // -2ms to +2ms
      const newVal = Math.max(1, Math.round(base + jitter));
      el.textContent = newVal + 'ms';
    }
  });
}
setInterval(applyNocJitter, 3500);

// ══════════════════════════════════════════════════
//  CONTACT FORM
// ══════════════════════════════════════════════════
const form = document.getElementById('contact-form');
const success = document.getElementById('form-success');
if (form) {
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    const btnText = btn.querySelector('.btn-text');
    const originalText = btnText.textContent;

    // UI Feedback
    btn.disabled = true;
    btnText.textContent = 'Enviando... 📡';

    const formData = new FormData(form);

    try {
      const response = await fetch(form.action, {
        method: form.method,
        body: formData,
        headers: {
          'Accept': 'application/json'
        }
      });

      if (response.ok) {
        form.reset();
        success.textContent = '¡Recibido! Te respondo pronto 😊';
        success.classList.add('show');
        setTimeout(() => success.classList.remove('show'), 5000);
      } else {
        const data = await response.json();
        throw new Error(data.error || 'Error en el servidor');
      }
    } catch (err) {
      console.error('Form Submission Error:', err);
      success.textContent = 'Hubo un error. Inténtalo de nuevo.';
      success.style.color = '#ff5f57'; // Error color
      success.classList.add('show');
      setTimeout(() => success.classList.remove('show'), 5000);
    } finally {
      btn.disabled = false;
      btnText.textContent = originalText;
    }
  });
}

// ══════════════════════════════════════════════════
//  AL3X_OS TERMINAL
// ══════════════════════════════════════════════════
const osBtn = document.getElementById('btn-os');
const osOverlay = document.getElementById('osOverlay');
const osClose = document.getElementById('osClose');
const osBody = document.getElementById('osBody');
const osActions = document.getElementById('osActions');
const matrixCanvas = document.getElementById('matrixCanvas');
const mCtx = matrixCanvas ? matrixCanvas.getContext('2d') : null;

let typingTimeout;
let matrixInterval;
let matrixRunning = false;

if (osBtn && osOverlay) {
  osBtn.addEventListener('click', () => {
    osOverlay.classList.add('active');
    startBootSequence();
  });

  osClose.addEventListener('click', () => {
    osOverlay.classList.remove('active');
    osOverlay.classList.remove('matrix-active');
    stopMatrix();
    clearTimeout(typingTimeout);
  });
}

function appendLine(text, className = '') {
  const p = document.createElement('p');
  p.className = className;
  p.innerHTML = text;
  osBody.appendChild(p);
  osBody.scrollTop = osBody.scrollHeight;
}

function typeLines(lines, idx = 0, cb = null) {
  if (idx >= lines.length) {
    if (cb) cb();
    return;
  }
  const { t, c, d } = lines[idx];
  appendLine(t, c);
  typingTimeout = setTimeout(() => typeLines(lines, idx + 1, cb), d || 400);
}

function startBootSequence() {
  osBody.innerHTML = '';
  osActions.style.opacity = '0';
  osActions.style.pointerEvents = 'none';

  const seq = [
    { t: 'AL3X_OS v9.4.2 [Modo Seguro Off]', c: 'sys-msg', d: 300 },
    { t: 'Autenticando usuario invitado...', c: 'sys-msg', d: 600 },
    { t: '[OK] Acceso concedido.', c: 'ai-msg', d: 300 },
    { t: 'Cargando módulos neuronales...', c: 'sys-msg', d: 800 },
    { t: 'Inicializando interfaz neuronal de Alexander...', c: 'sys-msg', d: 500 },
    { t: 'Hola. Soy la instancia digital de Alexander Armentia. ¿Qué necesitas saber?', c: 'ai-msg', d: 100 }
  ];

  typeLines(seq, 0, () => {
    osActions.style.opacity = '1';
    osActions.style.pointerEvents = 'all';
  });
}

document.querySelectorAll('.os-btn').forEach(btn => {
  btn.addEventListener('click', (e) => {
    const cmd = e.target.getAttribute('data-cmd');
    osActions.style.opacity = '0';
    osActions.style.pointerEvents = 'none';

    if (cmd === 'cv') {
      appendLine('> ./ejecutar_cv.sh', '');
      const resp = [
        { t: 'Extrayendo datos de carrera...', c: 'sys-msg', d: 400 },
        { t: '■ 1998-2000: La Salle (Informática de Gestión)', c: 'ai-msg', d: 200 },
        { t: '■ 2001-2009: Organización Campus Party (8 ediciones)', c: 'ai-msg', d: 200 },
        { t: '■ 2003-2007: Locutor Radio Digital (Emisión Digital, RadioGu)', c: 'ai-msg', d: 200 },
        { t: '■ Experiencia en Emprendimiento: EventDay (Eventos) y NochesDBoda (Bodas)', c: 'ai-msg', d: 200 },
        { t: '■ Actualidad: Técnico de Sistemas en Hewlett Packard CDS (Madrid)', c: 'ai-msg', d: 400 },
        { t: 'Fin de la transmisión [EOF]', c: 'sys-msg', d: 100 }
      ];
      typeLines(resp, 0, () => {
        osActions.style.opacity = '1';
        osActions.style.pointerEvents = 'all';
      });
    }
    else if (cmd === 'skills') {
      appendLine('> cat skills.txt', '');
      const resp = [
        { t: 'Leyendo archivos de habilidades...', c: 'sys-msg', d: 500 },
        { t: '=> SISTEMAS: Windows Server, Linux, Redes, Hardware, Virtualización', c: 'ai-msg', d: 200 },
        { t: '=> COMUNICACIÓN: Locución, Presentaciones, Oratoria (NochesDBoda)', c: 'ai-msg', d: 200 },
        { t: '=> GESTIÓN: Organización de grandes eventos (Campus Party, EventDay)', c: 'ai-msg', d: 200 },
        { t: '=> EXTRA: Energía inagotable por cafeína/taurina (Red Bull)', c: 'ai-msg', d: 200 }
      ];
      typeLines(resp, 0, () => {
        osActions.style.opacity = '1';
        osActions.style.pointerEvents = 'all';
      });
    }
    else if (cmd === 'incident') {
      appendLine('> sudo resolve_P1', 'err-msg');
      const scenarios = [
        [ // Escenario 1: Redes / BGP
          { t: '[ALERTA] Incidencia Crítica Detectada. Impacto: Crítico (P1).', c: 'err-msg', d: 600 },
          { t: 'Iniciando protocolo Incident Manager...', c: 'sys-msg', d: 500 },
          { t: '>> Abriendo puente técnico [WAR ROOM] puente-p1-alpha.', c: 'sys-msg', d: 700 },
          { t: '>> Solicitando escalado a equipos nivel 2/3...', c: 'sys-msg', d: 400 },
          { t: '  └─ [SISTEMAS] Conectado (3 técnicos)', c: 'ai-msg', d: 200 },
          { t: '  └─ [REDES] Conectado (2 técnicos)', c: 'ai-msg', d: 200 },
          {
            t: `
<pre class="ascii-map" style="color:#ffbd2e">
 [MADRID_CORE] ===X==> [ISP_PRIMARY] (LINK DOWN) 
                \\===> [ISP_BACKUP]  (STDBY)
</pre>`, c: '', d: 800
          },
          { t: '>> Analizando impacto. [REDES]: Tráfico de BGP enrutando mal. [FUNCIONALES]: Pagos detenidos.', c: 'sys-msg', d: 900 },
          { t: '>> Coordinando acciones de mitigación simultáneas...', c: 'sys-msg', d: 500 },
          { t: '>> [REDES] Forzando caída de BGP primary, failover a ISP_BACKUP.', c: 'sys-msg', d: 700 },
          {
            t: `
<pre class="ascii-map">
 [MADRID_CORE] =======> [ISP_BACKUP] (ACTIVE) &#x1F7E2;
</pre>`, c: '', d: 600
          },
          { t: '[RESOLVED] Tráfico restablecido. Pagos online de nuevo.', c: 'ai-msg', d: 500 },
          { t: 'Cerrando War Room. Empezando RCA. Red Bull consumido: +2 latas.', c: 'ai-msg', d: 300 }
        ],
        [ // Escenario 2: Base de datos y carga
          { t: '[ALERTA] Latencia extrema en Base de Datos Principal. (P1).', c: 'err-msg', d: 600 },
          { t: 'Iniciando protocolo Incident Manager...', c: 'sys-msg', d: 500 },
          { t: '>> Abriendo puente técnico [WAR ROOM] y convocando DBAs...', c: 'sys-msg', d: 600 },
          { t: '  └─ [DBAs] Conectados (2 técnicos)', c: 'ai-msg', d: 300 },
          {
            t: `
<pre class="ascii-map" style="color:#ff5f57">
 [DB_MAIN] CPU: &#x1F7E9;&#x1F7E9;&#x1F7E9;&#x1F7E9;&#x1F7E9;&#x1F7E9;&#x1F7E9;&#x1F7E9;&#x1F7E9;&#x1F7E5; 99% (CRITICAL)
 [QueryQueue]: 14,502 locked requests
</pre>`, c: '', d: 1000
          },
          { t: '>> [DBA] "Un query mal optimizado (del último deploy) está provocando deadlocks".', c: 'sys-msg', d: 800 },
          { t: '>> [INCIDENT_MANAGER] Ordenando KILL PROC masivo preventivo...', c: 'sys-msg', d: 700 },
          { t: '>> [SISTEMAS] Levantando 2 Read-Replicas extra para absorber la carga...', c: 'sys-msg', d: 600 },
          {
            t: `
<pre class="ascii-map">
 [DB_MAIN] CPU: &#x1F7E9;&#x1F7E9;&#x1F7E9;&#x2B1B;&#x2B1B;&#x2B1B;&#x2B1B;&#x2B1B;&#x2B1B;&#x2B1B; 32% (STABLE)
</pre>`, c: '', d: 600
          },
          { t: '[RESOLVED] Cuello de botella solucionado. Backend respondiendo a &lt;45ms.', c: 'ai-msg', d: 500 },
          { t: 'Tensión liberada. Adrenalina al límite. Volvemos al flow de SysAdmin.', c: 'ai-msg', d: 400 }
        ],
        [ // Escenario 3: Hardware y Storage
          { t: '[ALERTA] Degradación severa IOPS en SAN Storage. (P1).', c: 'err-msg', d: 700 },
          { t: '>> Abriendo [WAR ROOM] de urgencia - HW &amp; Infra...', c: 'sys-msg', d: 600 },
          { t: '  └─ [STORAGE_ENG] (2 técnicos)', c: 'ai-msg', d: 300 },
          { t: '  └─ [SISTEMAS] (3 sysadmins)', c: 'ai-msg', d: 300 },
          {
            t: `
<pre class="ascii-map" style="color:#ffbd2e">
 ARRAY_ALPHA:
 (O) Disk_01 ONLINE
 (O) Disk_02 ONLINE
 (X) Disk_03 FAILED (Offline)
 (O) Disk_04 ONLINE
 RAID 5 DEGRADED &#x26A0;&#xFE0F;
</pre>`, c: '', d: 1200
          },
          { t: '>> [STORAGE] "Fallo HW físico en cabina principal".', c: 'sys-msg', d: 700 },
          { t: '>> [SISTEMAS] "Comandos encolados, máquinas virtuales congelándose".', c: 'sys-msg', d: 600 },
          { t: '>> Activando Hot-spare (Disco 05) de forma automática y balanceando paths de SAN.', c: 'sys-msg', d: 800 },
          {
            t: `
<pre class="ascii-map">
 ARRAY_ALPHA [Rebuilding]: [|||||||.....] 55%
</pre>`, c: '', d: 800
          },
          { t: '>> Re-silver al 100%. Latencia de LUNs normalizada.', c: 'sys-msg', d: 600 },
          { t: '[RESOLVED] Máquinas reanudando I/O. Ningún dato perdido.', c: 'ai-msg', d: 500 },
          { t: 'Punto para infraestructura de resiliencia de HP. Abre una lata nueva.', c: 'ai-msg', d: 400 }
        ]
      ];
      const resp = scenarios[Math.floor(Math.random() * scenarios.length)];
      typeLines(resp, 0, () => {
        osActions.style.opacity = '1';
        osActions.style.pointerEvents = 'all';
      });
    }
    else if (cmd === 'monitor') {
      appendLine('> sudo infra_monitor', '');
      const resp = [
        { t: 'Comprobando estado de la infraestructura global...', c: 'sys-msg', d: 600 },
        {
          t: `
<div class="dash-grid">
  <div>[SYS_CORE] &nbsp;&nbsp;[||||||||||&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;] 68% OK</div>
  <div>[DB_MAIN]  &nbsp;&nbsp;&nbsp;[|||||||||||||&nbsp;&nbsp;] 84% OK</div>
  <div>[NET_EDGE] &nbsp;&nbsp;[||||&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;] 22% OK</div>
  <div>[BACKUPS] &nbsp;&nbsp;&nbsp;[|||||||||||||||] 100% OK</div>
</div>
        `, c: 'ai-msg', d: 800
        },
        { t: 'Analizando nodos geográficos principales...', c: 'sys-msg', d: 500 },
        {
          t: `
<pre class="ascii-map">
       . -- .
    _(        )_
  (   MADRID   )  => NODO [ONLINE] Latency: 12ms
 (_          _)
   ' -- . -- '
    \\
     *==> [LDN] 24ms | [FRA] 30ms | [AMS] 18ms
</pre>
        `, c: 'ai-msg', d: 1000
        },
        { t: `Datacenters respondiendo: <span style="color:var(--mint)">3/3 disponibles.</span> Todo verde.`, c: '', d: 300 }
      ];
      typeLines(resp, 0, () => {
        osActions.style.opacity = '1';
        osActions.style.pointerEvents = 'all';
      });
    }
    else if (cmd === 'matrix') {
      appendLine('> sudo matrix_mode', '');
      appendLine('Accediendo al mainframe...', 'sys-msg');
      setTimeout(() => {
        appendLine('Wake up, Neo...', 'ai-msg');
        osOverlay.classList.add('matrix-active');
        startMatrix();
        setTimeout(() => {
          osActions.style.opacity = '1';
          osActions.style.pointerEvents = 'all';
        }, 1000);
      }, 1000);
    }
  });
});

// Matrix Rain
let drops = [];
let matrixTimer;
function startMatrix() {
  if (matrixRunning) return;
  matrixRunning = true;
  matrixCanvas.style.opacity = '0.15';

  const w = matrixCanvas.width = window.innerWidth;
  const h = matrixCanvas.height = window.innerHeight;
  const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*'.split('');
  const fontSize = 16;
  const colCount = w / fontSize;

  drops = [];
  for (let x = 0; x < colCount; x++) drops[x] = 1;

  matrixInterval = setInterval(() => {
    mCtx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    mCtx.fillRect(0, 0, w, h);

    mCtx.fillStyle = '#34d399';
    mCtx.font = fontSize + 'px monospace';

    for (let i = 0; i < drops.length; i++) {
      const text = letters[Math.floor(Math.random() * letters.length)];
      mCtx.fillText(text, i * fontSize, drops[i] * fontSize);
      if (drops[i] * fontSize > h && Math.random() > 0.975) drops[i] = 0;
      drops[i]++;
    }
  }, 33);
}

function stopMatrix() {
  matrixRunning = false;
  clearInterval(matrixInterval);
  if (matrixCanvas) matrixCanvas.style.opacity = '0';
}

// ══════════════════════════════════════════════════
//  SKILL BARS — animate on scroll into view
// ══════════════════════════════════════════════════
const skBars = document.querySelectorAll('.sk-bar');

const skObs = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const bar = entry.target;
      const pct = bar.getAttribute('data-pct');
      // slight stagger based on index within parent
      const siblings = [...bar.parentElement.parentElement.parentElement.querySelectorAll('.sk-bar')];
      const idx = siblings.indexOf(bar);
      setTimeout(() => {
        bar.style.width = pct + '%';
        bar.classList.add('animated');
      }, idx * 80);
      skObs.unobserve(bar);
    }
  });
}, { threshold: 0.2 });

skBars.forEach(bar => skObs.observe(bar));

// Stagger skr-dots reveal for soft skills
const skrItems = document.querySelectorAll('.skr-item');
const skrObs = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      const dots = entry.target.querySelectorAll('.skr-dot.active');
      dots.forEach((dot, di) => {
        dot.style.opacity = '0';
        dot.style.transform = 'scale(0)';
        dot.style.transition = `opacity .3s ease ${di * 80}ms, transform .3s ease ${di * 80}ms, box-shadow .3s ease`;
        // force reflow
        void dot.offsetWidth;
        setTimeout(() => {
          dot.style.opacity = '';
          dot.style.transform = '';
        }, 20);
      });
      skrObs.unobserve(entry.target);
    }
  });
}, { threshold: 0.4 });

skrItems.forEach(item => skrObs.observe(item));

// ══════════════════════════════════════════════════
//  NOC DASHBOARD
// ══════════════════════════════════════════════════
const NOC_SERVICES = [
  { id: 'CORE_BNK', name: 'Core Banking', status: 'ok', uptime: 99.98, rtt: 24 },
  { id: 'AUTH_SVC', name: 'Auth Service', status: 'ok', uptime: 99.97, rtt: 18 },
  { id: 'API_GW', name: 'API Gateway', status: 'ok', uptime: 99.99, rtt: 11 },
  { id: 'PAYMENTS', name: 'Payments Engine', status: 'ok', uptime: 99.95, rtt: 31 },
  { id: 'NET_INFRA', name: 'Network Infra', status: 'ok', uptime: 100.00, rtt: 8 },
];

const NOC_HISTORY = [
  { time: '09:14:22', type: 'ok', svc: 'API_GW', msg: 'Gateway 503 burst — 3.2k req/s spike', ttr: '6min' },
  { time: '12:37:04', type: 'ok', svc: 'AUTH_SVC', msg: 'Auth latency degraded — token service', ttr: '8min' },
  { time: '16:42:11', type: 'ok', svc: 'PAYMENTS', msg: 'Payment timeout ↑ — 847 txns afectadas', ttr: '11min' },
  { time: 'Ayer 02:14', type: 'ok', svc: 'CORE_BNK', msg: 'DB connection pool exhausted — P1 declared', ttr: '19min' },
  { time: 'Hace 2d', type: 'ok', svc: 'NET_INFRA', msg: 'BGP route flap — upstream failover activado', ttr: '4min' },
];

let nocLogTotal = NOC_HISTORY.length;

function nocStatusLabel(s) {
  return s === 'ok' ? 'OPERATIONAL' : s === 'warn' ? 'DEGRADED' : 'INCIDENT';
}

function renderNocServices() {
  const el = document.getElementById('nocServicesList');
  if (!el) return;
  el.innerHTML = NOC_SERVICES.map(s => `
    <div class="noc-svc${s.status === 'p1' ? ' noc-incident-row' : s.status === 'warn' ? ' noc-warn-row' : ''}" id="noc-row-${s.id}">
      <span class="noc-svc-name">${s.name}</span>
      <span class="noc-svc-status s-${s.status}">
        <span class="noc-svc-dot"></span>
        <span class="noc-svc-txt">${nocStatusLabel(s.status)}</span>
      </span>
      <span class="noc-svc-uptime">${s.uptime.toFixed(2)}%</span>
      <span class="noc-svc-rtt">${s.rtt}ms</span>
    </div>`).join('');
}

function updateNocRow(svc) {
  const row = document.getElementById('noc-row-' + svc.id);
  if (!row) return;
  row.className = `noc-svc${svc.status === 'p1' ? ' noc-incident-row' : svc.status === 'warn' ? ' noc-warn-row' : ''}`;
  const statusEl = row.querySelector('.noc-svc-status');
  if (statusEl) statusEl.className = `noc-svc-status s-${svc.status}`;
  const txtEl = row.querySelector('.noc-svc-txt');
  if (txtEl) txtEl.textContent = nocStatusLabel(svc.status);
}

function updateNocGlobal() {
  const anyP1 = NOC_SERVICES.some(s => s.status === 'p1');
  const anyWarn = NOC_SERVICES.some(s => s.status === 'warn');
  const gEl = document.getElementById('nocGlobalStatus');
  const p1El = document.getElementById('nocActiveP1s');
  const kpiEl = document.getElementById('noc-kpi-p1');
  if (gEl) {
    if (anyP1) {
      gEl.textContent = '⚠ INCIDENT_ACTIVE — RESPONDING';
      gEl.className = 'noc-global-status noc-incident';
      if (p1El) p1El.textContent = '1';
      if (kpiEl) kpiEl.classList.add('noc-p1-active');
    } else {
      gEl.textContent = '● ALL_SYSTEMS_OPERATIONAL';
      gEl.className = 'noc-global-status';
      if (p1El) p1El.textContent = '0';
      if (kpiEl) kpiEl.classList.remove('noc-p1-active');
    }
  }
}

function addNocLog(entry) {
  const body = document.getElementById('nocLogBody');
  if (!body) return;
  const colorClass = entry.type === 'ok' ? 'noc-log-ok' : entry.type === 'warn' ? 'noc-log-warn' : 'noc-log-p1';
  const typeLabel = entry.type === 'ok' ? 'RESOLVED' : entry.type === 'warn' ? 'WARN' : 'P1_ACTIVE';
  const div = document.createElement('div');
  div.className = 'noc-log-entry';
  div.innerHTML = `<span class="noc-log-time">[${entry.time}]</span><span class="${colorClass}">${typeLabel}</span><span class="noc-log-svc">${entry.svc}</span><span class="noc-log-msg">${entry.msg}</span>${entry.ttr ? `<span class="noc-log-ttr">TTR:${entry.ttr}</span>` : ''}`;
  body.insertBefore(div, body.firstChild);
  nocLogTotal++;
  const countEl = document.getElementById('nocLogCount');
  if (countEl) countEl.textContent = `${nocLogTotal} eventos`;
}

function nowStr() {
  const d = new Date();
  return [d.getHours(), d.getMinutes(), d.getSeconds()].map(n => String(n).padStart(2, '0')).join(':');
}

let incidentTimer;
let currentResolveSvc = null;

function scheduleNocIncident() {
  incidentTimer = setTimeout(() => {
    const svc = NOC_SERVICES[Math.floor(Math.random() * NOC_SERVICES.length)];
    currentResolveSvc = svc;

    // warn phase
    svc.status = 'warn';
    updateNocRow(svc);
    addNocLog({ time: nowStr(), type: 'warn', svc: svc.id, msg: 'Anomaly detected — escalating...' });

    // P1 phase after 3.5s
    incidentTimer = setTimeout(() => {
      svc.status = 'p1';
      updateNocRow(svc);
      updateNocGlobal();
      addNocLog({ time: nowStr(), type: 'p1', svc: svc.id, msg: 'P1 declared — war room iniciada' });

      const btn = document.getElementById('nocBtnResolve');
      if (btn) btn.classList.add('active');

      // Manual or Auto resolution
      const ttrS = 8 + Math.floor(Math.random() * 8);
      incidentTimer = setTimeout(() => {
        resolveIncident(svc, ttrS, 'AUTO');
      }, ttrS * 1000);
    }, 3500);
  }, 18000 + Math.random() * 22000);
}

function resolveIncident(svc, ttrS, mode = 'AUTO') {
  if (svc.status === 'ok') return;

  svc.status = 'ok';
  updateNocRow(svc);
  updateNocGlobal();

  const btn = document.getElementById('nocBtnResolve');
  if (btn) btn.classList.remove('active');

  const msg = mode === 'MANUAL' ? 'Manual fix applied — Master Incident Manager in action' : 'Incident resolved — RCA en progreso';
  addNocLog({ time: nowStr(), type: 'ok', svc: svc.id, msg: msg, ttr: ttrS + 's' });

  clearTimeout(incidentTimer);
  currentResolveSvc = null;
  scheduleNocIncident();
}

function initNOC() {
  if (!document.getElementById('nocServicesList')) return;
  renderNocServices();
  // pre-load history (oldest at bottom, newest at top)
  [...NOC_HISTORY].reverse().forEach(e => addNocLog(e));
  // clock
  const clockEl = document.getElementById('nocClock');
  const tick = () => { if (clockEl) clockEl.textContent = nowStr(); };
  tick(); setInterval(tick, 1000);
  // RTT jitter
  const baseRtt = { CORE_BNK: 24, AUTH_SVC: 18, API_GW: 11, PAYMENTS: 31, NET_INFRA: 8 };
  setInterval(() => {
    NOC_SERVICES.forEach(s => {
      s.rtt = Math.max(1, baseRtt[s.id] + Math.round((Math.random() - .5) * 10));
      const el = document.querySelector(`#noc-row-${s.id} .noc-svc-rtt`);
      if (el) el.textContent = s.rtt + 'ms';
    });
  }, 2000);
  scheduleNocIncident();

  // Resolution Button Interaction
  const btn = document.getElementById('nocBtnResolve');
  if (btn) {
    btn.addEventListener('click', () => {
      if (currentResolveSvc) {
        // Visual feedback
        document.body.classList.add('crisis-flicker');
        setTimeout(() => document.body.classList.remove('crisis-flicker'), 300);

        // Success Toast
        showNocToast('INCIDENT_RESOLVED // Resiliencia restablecida al 100%');

        // Logic
        resolveIncident(currentResolveSvc, 2, 'MANUAL');
      }
    });
  }
}

function showNocToast(text) {
  let toast = document.getElementById('nocToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'nocToast';
    toast.className = 'incident-resolved-msg';
    document.body.appendChild(toast);
  }
  toast.innerHTML = `<span style="display:block; font-size:0.8rem; opacity:0.7">&gt; AL3X_OS.fix_complete()</span>${text}`;
  toast.classList.add('active');
  setTimeout(() => toast.classList.remove('active'), 3000);
}

initNOC();

// ══════════════════════════════════════════════════
//  RECRUITER FAB INTERACTION
// ══════════════════════════════════════════════════
(function () {
  const fab = document.getElementById('recruiterFab');
  const fabMain = document.getElementById('fabMain');

  if (fab && fabMain) {
    fabMain.addEventListener('click', (e) => {
      e.stopPropagation();
      fab.classList.toggle('active');
    });

    // Cerrar al hacer clic fuera
    document.addEventListener('click', (e) => {
      if (fab.classList.contains('active') && !fab.contains(e.target)) {
        fab.classList.remove('active');
      }
    });

    // Cerrar al hacer scroll rápido (opcional, para menos intrusión)
    window.addEventListener('scroll', () => {
      if (fab.classList.contains('active')) {
        fab.classList.remove('active');
      }
    }, { passive: true });
  }
})();
