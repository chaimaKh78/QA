# language: fr
Fonctionnalité: Compte utilisateur (EP-06)
  En tant que visiteur ou utilisateur
  Je veux m'inscrire, me connecter et gérer mon profil
  Afin de bénéficier des services personnalisés de NouvelAir

  Contexte:
    Étant donné que la base de données est peuplée

  # ── US-027 : Inscription avec données valides ──────────────────────────────

  Scénario: Inscription avec des données valides
    Étant donné je suis un visiteur non connecté
    Quand je m'inscris avec les données valides suivantes:
      | username | prenom  | nom     | email              | mot_de_passe    | confirmation   |
      | newuser  | Pierre  | Martin  | pierre@exemple.com | SecurePass123!  | SecurePass123! |
    Alors le compte est créé avec succès
    Et je suis connecté automatiquement
    Et je suis redirigé vers la page "flights:home"
    Et un profil utilisateur est créé automatiquement

  # ── Inscription avec email dupliqué ────────────────────────────────────────

  Scénario: Inscription avec un email déjà utilisé affiche une erreur
    Étant donné je suis un visiteur non connecté
    Quand je m'inscris avec les données suivantes ayant un email dupliqué:
      | username   | prenom | nom  | email              | mot_de_passe    | confirmation   |
      | otheruser  | Marie  | Curie| test@example.com   | SecurePass123!  | SecurePass123! |
    Alors le compte n'est pas créé
    Et un message d'erreur contenant "email" est affiché

  # ── US-028 : Connexion réussie ─────────────────────────────────────────────

  Scénario: Connexion avec des identifiants valides
    Étant donné je suis un visiteur non connecté
    Quand je me connecte avec "testuser" et "TestPassword123!"
    Alors je suis connecté avec succès
    Et je suis redirigé vers la page "flights:home"

  # ── Connexion échouée ─────────────────────────────────────────────────────

  Scénario: Connexion échouée avec un mauvais mot de passe
    Étant donné je suis un visiteur non connecté
    Quand je me connecte avec "testuser" et "wrongpass"
    Alors je ne suis pas connecté
    Et un message d'erreur est affiché
    Et je reste sur la page "accounts:login"

  # ── US-028 : Déconnexion ──────────────────────────────────────────────────

  Scénario: Déconnexion d'un utilisateur connecté
    Étant donné je suis connecté en tant que "testuser" avec le mot de passe "TestPassword123!"
    Quand je me déconnecte
    Alors je suis déconnecté
    Et je suis redirigé vers la page "flights:home"

  # ── US-030 : Mise à jour du profil ────────────────────────────────────────

  Scénario: Mise à jour du profil utilisateur
    Étant donné je suis connecté en tant que "testuser" avec le mot de passe "TestPassword123!"
    Quand je mets à jour mon profil avec les données suivantes:
      | prenom      | nom       | email                | telephone     | ville   | pays      |
      | JeanModifié | DupontMod | modified@exemple.com | +21698765432  | Sousse  | Tunisie   |
    Alors le profil est mis à jour avec succès
    Et les informations sont sauvegardées en base de données

  # ── Accès profil nécessite connexion ───────────────────────────────────────

  Scénario: L'accès au profil nécessite une connexion
    Étant donné je suis un visiteur non connecté
    Quand j'accède à la page "accounts:profile"
    Alors je suis redirigé vers la page "accounts:login"
