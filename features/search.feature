# language: fr
Fonctionnalité: Recherche de vols (EP-01)
  En tant que voyageur
  Je veux rechercher des vols disponibles
  Afin de planifier mon voyage avec NouvelAir

  Contexte:
    Étant donné que la base de données est peuplée

  # ── US-001 : Recherche de vol aller simple ────────────────────────────────

  Scénario: Recherche de vol aller simple TUN vers CDG
    Étant donné l'aéroport "TUN" existe dans la base
    Et l'aéroport "CDG" existe dans la base
    Et un vol "BJ101" de "TUN" à "CDG" est programmé
    Quand je recherche un vol aller simple de "TUN" vers "CDG" avec 1 passager
    Alors le statut de la réponse est 200
    Et je vois les résultats de recherche

  Scénario: Recherche de vol aller simple avec plusieurs passagers
    Étant donné l'aéroport "TUN" existe dans la base
    Et l'aéroport "MRS" existe dans la base
    Et un vol "BJ102" de "TUN" à "MRS" est programmé
    Quand je recherche un vol aller simple de "TUN" vers "MRS" avec 2 passagers
    Alors le statut de la réponse est 200
    Et je vois les résultats de recherche

  # ── US-001 : Recherche aller-retour ────────────────────────────────────────

  Scénario: Recherche de vol aller-retour
    Étant donné l'aéroport "TUN" existe dans la base
    Et l'aéroport "CDG" existe dans la base
    Et un vol "BJ101" de "TUN" à "CDG" est programmé
    Et un vol "BJ103" de "CDG" à "TUN" est programmé
    Quand je recherche un vol aller-retour de "TUN" vers "CDG" avec 1 passager
    Alors le statut de la réponse est 200
    Et je vois les résultats de recherche

  # ── Validation : départ et arrivée identiques ──────────────────────────────

  Scénario: Recherche avec départ et arrivée identiques affiche une erreur
    Étant donné l'aéroport "TUN" existe dans la base
    Quand je recherche un vol aller simple de "TUN" vers "TUN" avec 1 passager
    Alors le statut de la réponse est 200
    Et un message d'erreur contenant "différents" est affiché

  # ── Validation : date dans le passé ────────────────────────────────────────

  Scénario: Recherche avec une date dans le passé affiche une erreur
    Étant donné l'aéroport "TUN" existe dans la base
    Et l'aéroport "CDG" existe dans la base
    Quand je recherche un vol aller simple de "TUN" vers "CDG" pour la date d'hier
    Alors le statut de la réponse est 200
    Et un message d'erreur contenant "passée" est affiché

  # ── US-004 : Résultats triés par prix ──────────────────────────────────────

  Scénario: Résultats de recherche triés par prix croissant
    Étant donné l'aéroport "TUN" existe dans la base
    Et l'aéroport "CDG" existe dans la base
    Et un vol "BJ101" de "TUN" à "CDG" à 250.00 TND est programmé
    Et un vol "BJ520" de "TUN" à "CDG" à 199.00 TND est programmé
    Quand je recherche un vol aller simple de "TUN" vers "CDG" avec 1 passager
    Et je trie les résultats par prix croissant
    Alors le premier résultat a un prix inférieur ou égal au deuxième résultat

  # ── US-005 : Sélection de classe de voyage ─────────────────────────────────

  Plan du scénario: Sélection de classe de voyage modifie le prix affiché
    Étant donné l'aéroport "TUN" existe dans la base
    Et l'aéroport "CDG" existe dans la base
    Et un vol "BJ101" de "TUN" à "CDG" est programmé
    Quand je recherche un vol aller simple de "TUN" vers "CDG" avec 1 passager
    Et je sélectionne la classe "<classe>"
    Alors le prix est affiché en TND
    Et le prix correspond à la classe "<classe>"

    Exemples:
      | classe      |
      | Économie    |
      | Affaires    |

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

  # ── Recherche sans résultat ────────────────────────────────────────────────

  Scénario: Recherche sans résultat ne provoque pas d'erreur
    Étant donné l'aéroport "JFK" existe dans la base
    Et l'aéroport "LHR" existe dans la base
    Quand je recherche un vol aller simple de "JFK" vers "LHR" avec 1 passager
    Alors le statut de la réponse est 200
    Et je ne vois aucun résultat
    Et la page affiche "Aucun vol"
