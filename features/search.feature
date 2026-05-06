# language: fr
Fonctionnalité: Recherche de vols (EP-01)
  En tant que voyageur
  Je veux rechercher des vols disponibles
  Afin de planifier mon voyage avec NouvelAir

  Contexte:
    Étant donné que la base de données est peuplée



  # ── Page d'accueil ─────────────────────────────────────────────────────────

  Scénario: Les aéroports populaires sont affichés sur la page d'accueil
    Étant donné que la base de données est peuplée
    Quand j'accède à la page "flights:home"
    Alors le statut de la réponse est 200
    Et je vois au moins 3 aéroports populaires

  Scénario: Le formulaire de recherche contient tous les champs nécessaires
    Étant donné que la base de données est peuplée
    Quand j'accède à la page "flights:home"
    Alors le statut de la réponse est 200
    Et le formulaire de recherche contient le champ "origin"
    Et le formulaire de recherche contient le champ "destination"
    Et le formulaire de recherche contient le champ "departure_date"
    Et le formulaire de recherche contient le champ "passengers"
    Et le formulaire de recherche contient le champ "travel_class"
    Et le formulaire de recherche contient le champ "trip_type"


