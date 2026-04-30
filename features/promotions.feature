# language: fr
Fonctionnalité: Codes promotionnels (EP-01 / US-006)
  En tant que voyageur
  Je veux appliquer des codes promotionnels
  Afin de bénéficier de réductions sur mes réservations

  Contexte:
    Étant donné que la base de données est peuplée

  # ── US-006 : Application code promo valide ─────────────────────────────────

  Scénario: Application d'un code promotionnel valide
    Étant donné un code promo "NOUVEL25" est actif avec 25% de réduction
    Et un vol est disponible avec un prix de 250.00 TND
    Quand j'applique le code "NOUVEL25" au vol
    Alors la remise est appliquée
    Et le prix final est de 187.50 TND
    Et un message de confirmation est affiché

  Scénario: Application d'un code promo à un vol affaires
    Étant donné un code promo "NOUVEL25" est actif avec 25% de réduction
    Et un vol affaires est disponible avec un prix de 600.00 TND
    Quand j'applique le code "NOUVEL25" au vol
    Alors la remise est appliquée
    Et le prix final est de 450.00 TND

  # ── Code promo expiré ─────────────────────────────────────────────────────

  Scénario: Application d'un code promotionnel expiré affiche une erreur
    Étant donné un code promo "EXPIRED10" est expiré
    Quand j'applique le code "EXPIRED10" au vol
    Alors la remise n'est pas appliquée
    Et un message d'erreur contenant "expiré" est affiché

  # ── Code promo inexistant ─────────────────────────────────────────────────

  Scénario: Application d'un code promotionnel inexistant affiche une erreur
    Étant donné que la base de données est peuplée
    Quand j'applique le code "INCONNU50" au vol
    Alors la remise n'est pas appliquée
    Et un message d'erreur contenant "invalide" est affiché

  # ── US-034 : Newsletter ────────────────────────────────────────────────────

  Scénario: Inscription à la newsletter avec un email valide
    Étant donné je suis un visiteur non connecté
    Quand je m'inscris à la newsletter avec "newsletter@exemple.com"
    Alors l'inscription à la newsletter est confirmée
    Et un message de confirmation est affiché
    Et l'adresse email est enregistrée en base de données

  Scénario: Inscription à la newsletter avec un email déjà enregistré
    Étant donné l'adresse "newsletter@exemple.com" est déjà inscrite à la newsletter
    Quand je m'inscris à la newsletter avec "newsletter@exemple.com"
    Alors l'inscription échoue
    Et un message d'erreur contenant "déjà" est affiché
