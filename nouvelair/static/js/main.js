/**
 * NouvelAir - JavaScript principal
 * Application de Gestion des Réservations
 */

document.addEventListener('DOMContentLoaded', function() {

    // ============================================
    // Newsletter Footer
    // ============================================
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.getElementById('newsletter-email').value;
            fetch('/promotions/newsletter/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: 'email=' + encodeURIComponent(email)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Merci pour votre inscription !', 'success');
                    document.getElementById('newsletter-email').value = '';
                } else {
                    showNotification(data.error, 'danger');
                }
            })
            .catch(() => {
                showNotification('Erreur de connexion. Veuillez réessayer.', 'danger');
            });
        });
    }

    // ============================================
    // Autocomplétion Aéroports
    // ============================================
    const originSelect = document.getElementById('origin-select');
    const destinationSelect = document.getElementById('destination-select');

    // Swap origin/destination
    const swapBtn = document.createElement('button');
    swapBtn.type = 'button';
    swapBtn.className = 'btn btn-outline-secondary btn-sm mt-1';
    swapBtn.innerHTML = '<i class="fas fa-exchange-alt"></i>';
    if (originSelect && destinationSelect) {
        originSelect.parentElement.after(swapBtn);
        swapBtn.addEventListener('click', function() {
            const temp = originSelect.value;
            originSelect.value = destinationSelect.value;
            destinationSelect.value = temp;
        });
    }

    // Mettre à jour la date de retour minimum
    const departureDate = document.querySelector('input[name="departure_date"]');
    const returnDate = document.querySelector('input[name="return_date"]');

    if (departureDate && returnDate) {
        departureDate.addEventListener('change', function() {
            returnDate.min = this.value;
            if (returnDate.value && returnDate.value <= this.value) {
                returnDate.value = '';
            }
        });
    }

    // ============================================
    // Confirmation d'annulation
    // ============================================
    document.querySelectorAll('.cancel-booking-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Êtes-vous sûr de vouloir annuler cette réservation ? Cette action est irréversible.')) {
                e.preventDefault();
            }
        });
    });

    // ============================================
    // Filtrage destinations
    // ============================================
    window.filterDestinations = function(category) {
        const cards = document.querySelectorAll('.destination-card');
        cards.forEach(card => {
            if (category === 'all' || card.dataset.category === category) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });

        // Mettre à jour les boutons actifs
        document.querySelectorAll('.d-flex.justify-content-center button').forEach(btn => {
            btn.classList.remove('btn-outline-nouvelair', 'active');
            btn.classList.add('btn-outline-secondary');
        });
        event.target.classList.remove('btn-outline-secondary');
        event.target.classList.add('btn-outline-nouvelair', 'active');
    };

    // ============================================
    // Animations au scroll
    // ============================================
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card').forEach(card => {
        observer.observe(card);
    });

    // ============================================
    // Gestion des filtres de recherche
    // ============================================
    const filterCheckboxes = document.querySelectorAll('#morning, #afternoon, #evening');
    filterCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            applyFilters();
        });
    });

    function applyFilters() {
        const morning = document.getElementById('morning').checked;
        const afternoon = document.getElementById('afternoon').checked;
        const evening = document.getElementById('evening').checked;

        // Cette fonction peut être étendue pour filtrer via AJAX
        console.log('Filtres appliqués:', { morning, afternoon, evening });
    }

    // ============================================
    // Utilitaires
    // ============================================
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function showNotification(message, type) {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
        alert.style.zIndex = '9999';
        alert.innerHTML = `${message}<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
        document.body.appendChild(alert);
        setTimeout(() => alert.remove(), 5000);
    }

    // Compteur de passagers dynamique
    const passengersInput = document.querySelector('input[name="passengers"]');
    if (passengersInput) {
        passengersInput.addEventListener('change', function() {
            const count = parseInt(this.value);
            if (count < 1) this.value = 1;
            if (count > 9) this.value = 9;
        });
    }

});
