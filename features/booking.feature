# language: fr
Fonctionnalité: Gestion de réservation (EP-02)
  En tant que voyageur
  Je veux créer, consulter et annuler mes réservations
  Afin de gérer mes voyages avec NouvelAir

  Contexte:
    Étant donné que la base de données est peuplée

  # ── US-008 : Création de réservation (utilisateur connecté) ────────────────

  Scénario: Création d'une réservation en tant qu'utilisateur connecté
    Étant donné je suis connecté en tant que "testuser" avec le mot de passe "TestPassword123!"
    Et un vol est disponible pour la réservation
    Quand je réserve le vol avec les informations passager valides
    Alors la réservation est créée avec succès
    Et la réservation a le statut "confirmed"
    Et un numéro de référence est généré

  # ── Consultation de réservation ────────────────────────────────────────────

  Scénario: Consultation d'une réservation existante
    Étant donné je suis connecté en tant que "testuser" avec le mot de passe "TestPassword123!"
    Et une réservation "REF001" existe pour mon compte
    Quand j'accède à la page "bookings:my_bookings"
    Alors le statut de la réponse est 200
    Et je vois la réservation "REF001" dans la liste

  # ── US-010 : Annulation de réservation pending ─────────────────────────────

  Scénario: Annulation d'une réservation en attente
    Étant donné je suis connecté en tant que "testuser" avec le mot de passe "TestPassword123!"
    Et une réservation avec le statut "pending" existe
    Quand j'annule la réservation
    Alors la réservation est annulée
    Et le statut de la réservation est "cancelled"

  # ── Annulation impossible si déjà annulée ──────────────────────────────────

  Scénario: Annulation impossible si la réservation est déjà annulée
    Étant donné je suis connecté en tant que "testuser" avec le mot de passe "TestPassword123!"
    Et une réservation avec le statut "cancelled" existe
    Quand j'essaie d'annuler la réservation
    Alors la réservation reste avec le statut "cancelled"
    Et un message d'erreur est affiché

  # ── Recherche par référence et nom ─────────────────────────────────────────

  Scénario: Recherche de réservation par référence et nom de famille
    Étant donné une réservation pour "Dupont" avec la référence "REF002" existe
    Quand je recherche la réservation avec la référence "REF002" et le nom "Dupont"
    Alors le statut de la réponse est 302
    Et je suis redirigé vers la page de détail de la réservation

  Scénario: Recherche de réservation avec une référence invalide
    Étant donné que la base de données est peuplée
    Quand je recherche la réservation avec la référence "INVALID" et le nom "Dupont"
    Alors le statut de la réponse est 200
    Et un message d'erreur contenant "introuvable" est affiché

  # ── US-008 : Réservation nécessite une connexion ───────────────────────────

  Scénario: La création de réservation nécessite une connexion
    Étant donné je suis un visiteur non connecté
    Et un vol est disponible pour la réservation
    Quand j'essaie de réserver le vol
    Alors je suis redirigé vers la page "accounts:login"

  # ── Consultation de mes réservations sans connexion ────────────────────────

  Scénario: L'accès à mes réservations nécessite une connexion
    Étant donné je suis un visiteur non connecté
    Quand j'accède à la page "bookings:my_bookings"
    Alors je suis redirigé vers la page "accounts:login"
