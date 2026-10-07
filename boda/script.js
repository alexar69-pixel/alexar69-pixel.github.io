document.addEventListener('DOMContentLoaded', () => {
    // 1. Navbar scroll effect & Hamburger Menu
    const navbar = document.getElementById('navbar');
    const hamburgerBtn = document.getElementById('hamburger-btn');
    const navLinks = document.getElementById('nav-links');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    if (hamburgerBtn && navLinks) {
        hamburgerBtn.addEventListener('click', () => {
            hamburgerBtn.classList.toggle('active');
            navLinks.classList.toggle('active');
        });

        // Close menu when clicking a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                hamburgerBtn.classList.remove('active');
                navLinks.classList.remove('active');
            });
        });
    }

    // 2. Countdown Timer (Target: 26 Jun 2027 20:00 Madrid)
    // Month is 0-indexed in JS Date constructor (0 = Jan, 5 = June)
    const weddingDate = new Date(2027, 5, 26, 20, 0, 0).getTime();

    function updateCountdown() {
        const now = new Date().getTime();
        const difference = weddingDate - now;

        const elDays = document.getElementById('cd-days');
        const elHours = document.getElementById('cd-hours');
        const elMinutes = document.getElementById('cd-minutes');
        const elSeconds = document.getElementById('cd-seconds');

        if (difference > 0) {
            const days = Math.floor(difference / (1000 * 60 * 60 * 24));
            const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((difference % (1000 * 60)) / 1000);

            if (elDays) elDays.textContent = String(days).padStart(2, '0');
            if (elHours) elHours.textContent = String(hours).padStart(2, '0');
            if (elMinutes) elMinutes.textContent = String(minutes).padStart(2, '0');
            if (elSeconds) elSeconds.textContent = String(seconds).padStart(2, '0');
        } else {
            if (elDays) elDays.textContent = '00';
            if (elHours) elHours.textContent = '00';
            if (elMinutes) elMinutes.textContent = '00';
            if (elSeconds) elSeconds.textContent = '00';
        }
    }

    updateCountdown();
    setInterval(updateCountdown, 1000);

    // 3. Intersection Observer for scroll animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right');
    animatedElements.forEach(el => observer.observe(el));

    // 4. Gifts Modal Logic
    const modal = document.getElementById('modal-regalos');
    const btnOpenModal = document.getElementById('btn-open-modal');
    const btnCloseModal = document.getElementById('btn-close-modal');
    const btnCopyIban = document.getElementById('btn-copy-iban');
    const ibanText = document.getElementById('iban-text');
    const copyToast = document.getElementById('copy-toast');

    if (btnOpenModal && modal) {
        btnOpenModal.addEventListener('click', () => {
            modal.classList.add('active');
            modal.setAttribute('aria-hidden', 'false');
        });
    }

    if (btnCloseModal && modal) {
        btnCloseModal.addEventListener('click', () => {
            modal.classList.remove('active');
            modal.setAttribute('aria-hidden', 'true');
        });
    }

    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
                modal.setAttribute('aria-hidden', 'true');
            }
        });
    }

    if (btnCopyIban && ibanText) {
        btnCopyIban.addEventListener('click', () => {
            const cleanIban = ibanText.textContent.replace(/\s+/g, '');
            navigator.clipboard.writeText(cleanIban).then(() => {
                if (copyToast) {
                    copyToast.style.display = 'block';
                    setTimeout(() => {
                        copyToast.style.display = 'none';
                    }, 2500);
                }
            }).catch(err => {
                console.error('Error al copiar IBAN: ', err);
            });
        });
    }

    const btnCopyIbanPage = document.getElementById('btn-copy-iban-page');
    const ibanTextPage = document.getElementById('iban-text-page');
    const copyToastPage = document.getElementById('copy-toast-page');

    if (btnCopyIbanPage && ibanTextPage) {
        btnCopyIbanPage.addEventListener('click', () => {
            const cleanIban = ibanTextPage.textContent.replace(/\s+/g, '');
            navigator.clipboard.writeText(cleanIban).then(() => {
                if (copyToastPage) {
                    copyToastPage.style.display = 'block';
                    setTimeout(() => {
                        copyToastPage.style.display = 'none';
                    }, 2500);
                }
            }).catch(err => {
                console.error('Error al copiar IBAN: ', err);
            });
        });
    }

    // 6. Native Canvas Confetti Generator (Fiesta!)
    function launchConfetti() {
        const canvas = document.createElement('canvas');
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '9999';
        document.body.appendChild(canvas);
        
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        const particles = [];
        const colors = ['#F43F5E', '#D4AF37', '#8B5CF6', '#3B82F6', '#10B981', '#F59E0B', '#EC4899'];
        
        for (let i = 0; i < 120; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height * 0.5 - canvas.height * 0.2,
                size: Math.random() * 8 + 4,
                color: colors[Math.floor(Math.random() * colors.length)],
                speedY: Math.random() * 5 + 3,
                speedX: Math.random() * 4 - 2,
                rotation: Math.random() * 360,
                rotSpeed: Math.random() * 10 - 5
            });
        }
        
        function render() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            let active = false;
            particles.forEach(p => {
                p.y += p.speedY;
                p.x += p.speedX;
                p.rotation += p.rotSpeed;
                if (p.y < canvas.height) active = true;
                
                ctx.save();
                ctx.translate(p.x, p.y);
                ctx.rotate((p.rotation * Math.PI) / 180);
                ctx.fillStyle = p.color;
                ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
                ctx.restore();
            });
            
            if (active) {
                requestAnimationFrame(render);
            } else {
                canvas.remove();
            }
        }
        render();
    }

    // Party Button Floating Trigger
    const btnParty = document.getElementById('btn-party-toggle');
    if (btnParty) {
        btnParty.addEventListener('click', () => {
            launchConfetti();
        });
    }

    const btnHeroRsvp = document.getElementById('btn-hero-rsvp');
    if (btnHeroRsvp) {
        btnHeroRsvp.addEventListener('click', () => {
            launchConfetti();
        });
    }

    // Trigger confetti on page load after short delay for party vibe
    setTimeout(launchConfetti, 800);

    // 5. RSVP Form Handling with LocalStorage Persistence
    const rsvpForm = document.getElementById('rsvp-form');
    const rsvpSuccess = document.getElementById('rsvp-success');

    // Check if user already submitted before
    const existingSubmission = localStorage.getItem('wedding_rsvp');
    if (existingSubmission && rsvpForm && rsvpSuccess) {
        rsvpForm.style.display = 'none';
        rsvpSuccess.style.display = 'block';
    }

    if (rsvpForm) {
        rsvpForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const submitBtn = rsvpForm.querySelector('button[type="submit"]');
            submitBtn.textContent = 'Enviando...';
            submitBtn.disabled = true;

            const name = document.getElementById('name').value;
            const attendance = document.getElementById('attendance').value;
            const plusone = document.getElementById('plusone').value;
            const diet = document.getElementById('diet').value;
            const song = document.getElementById('song').value;

            const formData = { name, attendance, plusone, diet, song, timestamp: new Date().toISOString() };

            setTimeout(() => {
                localStorage.setItem('wedding_rsvp', JSON.stringify(formData));
                rsvpForm.style.display = 'none';
                if (rsvpSuccess) {
                    rsvpSuccess.style.display = 'block';
                }
                launchConfetti();
            }, 1000);
        });
    }

    // 7. Quiz Interactivo ("¿Cuánto conoces a Maqui & Alex?")
    let quizScore = 0;
    let currentQ = 1;

    function initQuiz() {
        const quizBtns = document.querySelectorAll('.quiz-btn');
        quizBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const card = btn.closest('.quiz-card');
                if (!card || card.classList.contains('answered')) return;
                
                card.classList.add('answered');
                const isCorrect = btn.getAttribute('data-correct') === 'true';
                
                if (isCorrect) {
                    btn.classList.add('correct');
                    quizScore++;
                } else {
                    btn.classList.add('incorrect');
                    // Highlight correct option
                    const correctBtn = card.querySelector('[data-correct="true"]');
                    if (correctBtn) correctBtn.classList.add('correct');
                }

                setTimeout(() => {
                    card.style.display = 'none';
                    currentQ++;
                    const nextQ = document.getElementById(`quiz-q${currentQ}`);
                    if (nextQ) {
                        nextQ.style.display = 'block';
                    } else {
                        // End of Quiz
                        const quizResult = document.getElementById('quiz-result');
                        const scoreText = document.getElementById('quiz-score-text');
                        if (quizResult && scoreText) {
                            quizResult.style.display = 'block';
                            scoreText.textContent = `¡Has acertado ${quizScore} de 3 preguntas! ` + 
                                (quizScore === 3 ? '¡Eres un auténtico VIP de Maqui & Alex! 🔥' : '¡Casi perfecto! Nos vemos en la pista.');
                            if (quizScore >= 2) launchConfetti();
                        }
                    }
                }, 1200);
            });
        });

        const retryBtn = document.getElementById('btn-quiz-retry');
        if (retryBtn) {
            retryBtn.addEventListener('click', () => {
                quizScore = 0;
                currentQ = 1;
                document.getElementById('quiz-result').style.display = 'none';
                document.querySelectorAll('.quiz-card').forEach((card, idx) => {
                    card.classList.remove('answered');
                    card.style.display = idx === 0 ? 'block' : 'none';
                    card.querySelectorAll('.quiz-btn').forEach(b => b.classList.remove('correct', 'incorrect'));
                });
            });
        }
    }
    initQuiz();

    // 8. Libro de Visitas Digital (Guestbook)
    const gbForm = document.getElementById('guestbook-form');
    const gbWall = document.getElementById('guestbook-wall');

    // Load saved messages
    const savedMessages = JSON.parse(localStorage.getItem('wedding_guestbook') || '[]');
    savedMessages.forEach(msg => {
        addGuestbookCard(msg.author, msg.text, msg.date, false);
    });

    function addGuestbookCard(author, text, dateStr, prepend = true) {
        if (!gbWall) return;
        const card = document.createElement('div');
        card.className = 'gb-card';
        card.innerHTML = `
            <div class="gb-author">${escapeHtml(author)}</div>
            <div class="gb-text">${escapeHtml(text)}</div>
            <div class="gb-date">${dateStr}</div>
        `;
        if (prepend) {
            gbWall.insertBefore(card, gbWall.firstChild);
        } else {
            gbWall.appendChild(card);
        }
    }

    function escapeHtml(str) {
        return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }

    if (gbForm) {
        gbForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const author = document.getElementById('gb-name').value;
            const text = document.getElementById('gb-message').value;

            if (author && text) {
                const dateStr = 'Justo ahora';
                addGuestbookCard(author, text, dateStr, true);

                // Save to localStorage
                const currentMsgs = JSON.parse(localStorage.getItem('wedding_guestbook') || '[]');
                currentMsgs.unshift({ author, text, date: 'Recientemente' });
                localStorage.setItem('wedding_guestbook', JSON.stringify(currentMsgs));

                // Reset form & trigger confetti
                gbForm.reset();
                launchConfetti();
            }
        });
    }

    // 9. Photo Uploader Logic (Guests Photo Album)
    const photoModal = document.getElementById('modal-upload-foto');
    const btnOpenUploadModal = document.getElementById('btn-open-upload-modal');
    const btnCloseUploadModal = document.getElementById('btn-close-upload-modal');
    const photoForm = document.getElementById('photo-upload-form');
    const photoFileInput = document.getElementById('photo-file');
    const photoPreviewContainer = document.getElementById('photo-preview-container');
    const photoPreviewImg = document.getElementById('photo-preview-img');
    const guestPhotosGrid = document.getElementById('guest-photos-grid');
    const emptyPhotosMsg = document.getElementById('empty-photos-msg');

    if (btnOpenUploadModal && photoModal) {
        btnOpenUploadModal.addEventListener('click', () => {
            photoModal.classList.add('active');
            photoModal.setAttribute('aria-hidden', 'false');
        });
    }

    if (btnCloseUploadModal && photoModal) {
        btnCloseUploadModal.addEventListener('click', () => {
            photoModal.classList.remove('active');
            photoModal.setAttribute('aria-hidden', 'true');
        });
    }

    if (photoModal) {
        photoModal.addEventListener('click', (e) => {
            if (e.target === photoModal) {
                photoModal.classList.remove('active');
                photoModal.setAttribute('aria-hidden', 'true');
            }
        });
    }

    // Preview photo on file select
    if (photoFileInput) {
        photoFileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (evt) => {
                    if (photoPreviewImg && photoPreviewContainer) {
                        photoPreviewImg.src = evt.target.result;
                        photoPreviewContainer.style.display = 'block';
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Render polaroid cards
    const angles = [-3, 2, -2, 4, -4, 3];
    let angleIndex = 0;

    function renderGuestPhoto(author, caption, dataUrl, dateStr, prepend = true) {
        if (!guestPhotosGrid) return;
        if (emptyPhotosMsg) emptyPhotosMsg.style.display = 'none';

        const rot = angles[angleIndex % angles.length];
        angleIndex++;

        const card = document.createElement('div');
        card.className = 'polaroid-card';
        card.style.setProperty('--rotation', `${rot}deg`);
        card.innerHTML = `
            <div class="polaroid-img-wrapper">
                <img src="${dataUrl}" alt="Foto de ${escapeHtml(author)}">
            </div>
            <div class="polaroid-info">
                <div class="polaroid-author">${escapeHtml(author)}</div>
                ${caption ? `<div class="polaroid-caption">"${escapeHtml(caption)}"</div>` : ''}
                <div class="polaroid-date">${dateStr}</div>
            </div>
        `;

        if (prepend) {
            guestPhotosGrid.insertBefore(card, guestPhotosGrid.firstChild);
        } else {
            guestPhotosGrid.appendChild(card);
        }
    }

    // Load saved guest photos from localStorage
    const savedPhotos = JSON.parse(localStorage.getItem('wedding_user_photos') || '[]');
    if (savedPhotos.length > 0) {
        savedPhotos.forEach(p => renderGuestPhoto(p.author, p.caption, p.dataUrl, p.dateStr, false));
    }

    if (photoForm) {
        photoForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const author = document.getElementById('photo-author').value;
            const caption = document.getElementById('photo-caption').value;
            const file = photoFileInput.files[0];

            if (author && file) {
                const submitBtn = photoForm.querySelector('button[type="submit"]');
                submitBtn.textContent = 'Subiendo...';
                submitBtn.disabled = true;

                const reader = new FileReader();
                reader.onload = (evt) => {
                    const dataUrl = evt.target.result;
                    const dateStr = 'En la fiesta 🪩';

                    renderGuestPhoto(author, caption, dataUrl, dateStr, true);

                    // Save to localStorage (limiting max 10 photos for storage safety)
                    try {
                        const currentPhotos = JSON.parse(localStorage.getItem('wedding_user_photos') || '[]');
                        currentPhotos.unshift({ author, caption, dataUrl, dateStr });
                        if (currentPhotos.length > 10) currentPhotos.pop();
                        localStorage.setItem('wedding_user_photos', JSON.stringify(currentPhotos));
                    } catch(err) {
                        console.warn('Storage limit exceeded:', err);
                    }

                    // Reset form & close modal
                    photoForm.reset();
                    if (photoPreviewContainer) photoPreviewContainer.style.display = 'none';
                    submitBtn.textContent = '🚀 Publicar Foto en el Álbum';
                    submitBtn.disabled = false;
                    photoModal.classList.remove('active');
                    photoModal.setAttribute('aria-hidden', 'true');

                    launchConfetti();
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // 10. Apple Calendar / Outlook iCal Download (.ics)
    const btnDownloadIcs = document.getElementById('btn-download-ics');
    if (btnDownloadIcs) {
        btnDownloadIcs.addEventListener('click', () => {
            const icsContent = [
                'BEGIN:VCALENDAR',
                'VERSION:2.0',
                'PRODID:-//Boda Maqui y Alex//ES',
                'CALSCALE:GREGORIAN',
                'METHOD:PUBLISH',
                'BEGIN:VEVENT',
                'SUMMARY:🎉 Boda Fiesta - Maqui & Alex',
                'DESCRIPTION:¡Nos casamos y se viene fiestón! Cóctel cena gourmet, barra libre sin fin y recena en la terraza al aire libre del Centro Nacional de Golf.\\n\\nInfo web: https://alexanderarmentia.com/boda',
                'LOCATION:Centro Nacional de Golf, Calle Arroyo del Monte 5, 28049 Madrid',
                'DTSTART:20270626T180000Z',
                'DTEND:20270627T020000Z',
                'STATUS:CONFIRMED',
                'END:VEVENT',
                'END:VCALENDAR'
            ].join('\r\n');

            const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8;' });
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.setAttribute('download', 'Boda-Maqui-y-Alex.ics');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    }
});


