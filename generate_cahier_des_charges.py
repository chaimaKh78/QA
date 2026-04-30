# -*- coding: utf-8 -*-
"""
Generateur du Cahier des Charges - Projet NouvelAir
====================================================
Executez ce script sur votre machine :
    pip install reportlab
    python generate_cahier_des_charges.py

Le fichier PDF sera cree dans le meme dossier : NouvelAir_Cahier_des_Charges.pdf
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import hashlib

# =============================================================================
# CONFIGURATION
# =============================================================================
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "NouvelAir_Cahier_des_Charges.pdf")

# --- Couleurs ---
PRIMARY = colors.HexColor("#1B3A5C")       # Bleu sombre NouvelAir
ACCENT = colors.HexColor("#C3243F")        # Rouge accent
LIGHT_BLUE = colors.HexColor("#E8F0FE")
LIGHT_GRAY = colors.HexColor("#F5F5F5")
MED_GRAY = colors.HexColor("#CCCCCC")
TEXT_DARK = colors.HexColor("#1A1A1A")
TEXT_MUTED = colors.HexColor("#666666")
TABLE_HEADER = colors.HexColor("#1B3A5C")
TABLE_ROW_ODD = colors.HexColor("#F0F4FA")

# --- Polices (noms Windows courants, ReportLab les trouve automatiquement) ---
try:
    pdfmetrics.registerFont(TTFont('Calibri', 'C:/Windows/Fonts/calibri.ttf'))
    BODY_FONT = 'Calibri'
except:
    BODY_FONT = 'Helvetica'

try:
    pdfmetrics.registerFont(TTFont('CalibriB', 'C:/Windows/Fonts/calibrib.ttf'))
    BOLD_FONT = 'CalibriB'
except:
    BOLD_FONT = 'Helvetica-Bold'

try:
    pdfmetrics.registerFont(TTFont('TimesNR', 'C:/Windows/Fonts/times.ttf'))
    TITLE_FONT = 'TimesNR'
except:
    TITLE_FONT = 'Times-Roman'

try:
    pdfmetrics.registerFont(TTFont('TimesNRB', 'C:/Windows/Fonts/timesbd.ttf'))
    TITLE_BOLD_FONT = 'TimesNRB'
except:
    TITLE_BOLD_FONT = 'Times-Bold'

# =============================================================================
# STYLES
# =============================================================================
styles = getSampleStyleSheet()

cover_title = ParagraphStyle(
    'CoverTitle', fontName=TITLE_BOLD_FONT, fontSize=36,
    leading=44, alignment=TA_CENTER, textColor=PRIMARY,
    spaceAfter=12
)
cover_subtitle = ParagraphStyle(
    'CoverSubtitle', fontName=BODY_FONT, fontSize=16,
    leading=22, alignment=TA_CENTER, textColor=TEXT_MUTED,
    spaceAfter=6
)
cover_info = ParagraphStyle(
    'CoverInfo', fontName=BODY_FONT, fontSize=12,
    leading=18, alignment=TA_CENTER, textColor=TEXT_MUTED,
    spaceAfter=4
)

h1_style = ParagraphStyle(
    'H1Custom', fontName=TITLE_BOLD_FONT, fontSize=22,
    leading=28, textColor=PRIMARY, spaceBefore=24, spaceAfter=12,
    borderWidth=0, borderColor=PRIMARY, borderPadding=0,
)
h2_style = ParagraphStyle(
    'H2Custom', fontName=BOLD_FONT, fontSize=16,
    leading=22, textColor=PRIMARY, spaceBefore=18, spaceAfter=8,
)
h3_style = ParagraphStyle(
    'H3Custom', fontName=BOLD_FONT, fontSize=13,
    leading=18, textColor=TEXT_DARK, spaceBefore=12, spaceAfter=6,
)
body_style = ParagraphStyle(
    'BodyCustom', fontName=BODY_FONT, fontSize=11,
    leading=17, textColor=TEXT_DARK, alignment=TA_JUSTIFY,
    spaceBefore=2, spaceAfter=6, firstLineIndent=0,
)
body_indent = ParagraphStyle(
    'BodyIndent', parent=body_style, leftIndent=20,
)
bullet_style = ParagraphStyle(
    'BulletCustom', fontName=BODY_FONT, fontSize=11,
    leading=17, textColor=TEXT_DARK, leftIndent=30,
    bulletIndent=15, spaceBefore=2, spaceAfter=3,
)
table_header_style = ParagraphStyle(
    'TableHeader', fontName=BOLD_FONT, fontSize=10,
    leading=14, textColor=colors.white, alignment=TA_CENTER,
)
table_cell_style = ParagraphStyle(
    'TableCell', fontName=BODY_FONT, fontSize=10,
    leading=14, textColor=TEXT_DARK, alignment=TA_LEFT,
)
table_cell_center = ParagraphStyle(
    'TableCellCenter', fontName=BODY_FONT, fontSize=10,
    leading=14, textColor=TEXT_DARK, alignment=TA_CENTER,
)
footer_style = ParagraphStyle(
    'Footer', fontName=BODY_FONT, fontSize=8,
    leading=10, textColor=TEXT_MUTED, alignment=TA_CENTER,
)

# =============================================================================
# TOC DOCUMENT TEMPLATE
# =============================================================================
class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'bookmark_name'):
            level = getattr(flowable, 'bookmark_level', 0)
            text = getattr(flowable, 'bookmark_text', '')
            key = getattr(flowable, 'bookmark_key', '')
            self.notify('TOCEntry', (level, text, self.page, key))


def add_heading(text, style, level=0):
    key = 'h_%s' % hashlib.md5(text.encode()).hexdigest()[:8]
    p = Paragraph('<a name="%s"/>%s' % (key, text), style)
    p.bookmark_name = text
    p.bookmark_level = level
    p.bookmark_text = text
    p.bookmark_key = key
    return p


def make_table(headers, rows, col_widths=None):
    """Create a styled table from headers and rows."""
    data = [[Paragraph('<b>%s</b>' % h, table_header_style) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), table_cell_style) for c in row])

    avail = A4[0] - 2.5*cm - 2.5*cm
    if col_widths is None:
        n = len(headers)
        col_widths = [avail / n] * n

    t = Table(data, colWidths=col_widths, hAlign='CENTER')
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, MED_GRAY),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(data)):
        bg = TABLE_ROW_ODD if i % 2 == 0 else colors.white
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))
    t.setStyle(TableStyle(style_cmds))
    return t


def hr():
    return HRFlowable(width="100%", thickness=1, color=MED_GRAY,
                      spaceBefore=6, spaceAfter=6)


# =============================================================================
# PAGE NUMBER CALLBACK
# =============================================================================
def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont(BODY_FONT, 8)
    canvas.setFillColor(TEXT_MUTED)
    page_num = canvas.getPageNumber()
    if page_num > 1:
        text = "NouvelAir - Cahier des Charges  |  Page %d" % page_num
        canvas.drawCentredString(A4[0] / 2, 1.2*cm, text)
    canvas.restoreState()


# =============================================================================
# DOCUMENT BUILD
# =============================================================================
def build_document():
    doc = TocDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm,
        leftMargin=2.5*cm,
        rightMargin=2.5*cm,
        title="NouvelAir - Cahier des Charges Detaille",
        author="NouvelAir",
        subject="Specification fonctionnelle et technique du systeme de gestion de reservations",
    )

    story = []
    avail_width = A4[0] - 5*cm  # available content width

    # ===================== PAGE DE COUVERTURE =====================
    story.append(Spacer(1, 3*cm))

    # Bande colorée en haut via un tableau
    band_data = [[""]]
    band = Table(band_data, colWidths=[avail_width + 4*cm], rowHeights=[8])
    band.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PRIMARY),
        ('LINEBELOW', (0, 0), (-1, -1), 0, colors.white),
    ]))
    story.append(band)
    story.append(Spacer(1, 2.5*cm))

    story.append(Paragraph("NOUVELAIR", ParagraphStyle(
        'Brand', fontName=TITLE_BOLD_FONT, fontSize=48,
        leading=54, alignment=TA_CENTER, textColor=PRIMARY,
    )))
    story.append(Spacer(1, 0.5*cm))
    story.append(hr())
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "Cahier des Charges Detaille",
        cover_title
    ))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "Systeme de Gestion de Reservations Aeriennes",
        cover_subtitle
    ))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph(
        "Application Web Django 4.2  |  Formation Test / QA",
        cover_info
    ))
    story.append(Paragraph(
        "Version 1.0  -  Avril 2026",
        cover_info
    ))
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph(
        "Document confidentiel - Usage interne et formation",
        ParagraphStyle('Conf', fontName=BODY_FONT, fontSize=10,
                       leading=14, alignment=TA_CENTER, textColor=ACCENT)
    ))
    story.append(Spacer(1, 2*cm))

    band2 = Table(band_data, colWidths=[avail_width + 4*cm], rowHeights=[8])
    band2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PRIMARY),
    ]))
    story.append(band2)

    story.append(PageBreak())

    # ===================== TABLE DES MATIERES =====================
    story.append(Paragraph("Table des Matieres", h1_style))
    story.append(Spacer(1, 0.5*cm))

    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle('TOC1', fontName=BOLD_FONT, fontSize=13,
                       leading=20, leftIndent=20, spaceBefore=6),
        ParagraphStyle('TOC2', fontName=BODY_FONT, fontSize=11,
                       leading=18, leftIndent=40, spaceBefore=3),
        ParagraphStyle('TOC3', fontName=BODY_FONT, fontSize=10,
                       leading=16, leftIndent=60, spaceBefore=2),
    ]
    story.append(toc)
    story.append(PageBreak())

    # ===================== 1. INTRODUCTION =====================
    story.append(add_heading("1. Introduction", h1_style, 0))

    story.append(add_heading("1.1 Contexte du Projet", h2_style, 1))
    story.append(Paragraph(
        "NouvelAir est une compagnie aerienne tunisienne qui souhaite moderniser son systeme de gestion "
        "de reservations. Actuellement, la gestion des vols, des reservations et des clients est "
        "effectuee de maniere partiellement manuelle, ce qui entraine des problemes d'efficacite, "
        "des erreurs de saisie et une experience client sous-optimale. Le projet consiste a developper "
        "une application web complete basee sur le framework Django 4.2 qui couvrira l'ensemble du "
        "cycle de reservation, depuis la recherche de vols jusqu'a la confirmation et la gestion "
        "post-reservation.", body_style))
    story.append(Paragraph(
        "Ce projet a egalement une vocation pedagogique : il sert de support pour la formation "
        "en test et assurance qualite (QA). L'application a ete concue avec une couverture de "
        "tests unitaires et d'integration, ainsi qu'un module de test assiste par intelligence "
        "artificielle, permettant aux apprenants de se familiariser avec les bonnes pratiques "
        "de test dans un environnement Django realiste.", body_style))

    story.append(add_heading("1.2 Objectifs du Document", h2_style, 1))
    story.append(Paragraph(
        "Ce cahier des charges a pour objectif de definir de maniere exhaustive et structuree "
        "les specifications fonctionnelles et techniques du systeme NouvelAir. Il servira de "
        "reference tout au long du cycle de developpement et sera utilise comme base pour la "
        "planification des sprints, la redaction des cas de test et la validation des livrables. "
        "Le document couvre les aspects suivants : les besoins fonctionnels detailles pour chaque "
        "module, l'architecture technique, le schema de la base de donnees, la structure des URLs, "
        "les exigences non-fonctionnelles, et la strategie de test.", body_style))

    story.append(add_heading("1.3 Portee du Projet", h2_style, 1))
    story.append(Paragraph(
        "Le systeme NouvelAir est decoupe en cinq modules principaux, chacun correspondant "
        "a une application Django distincte. Cette architecture modulaire facilite la maintenance, "
        "les evolutions futures et les tests isoles de chaque composant. Les cinq modules sont : "
        "Gestion des Vols (flights), Gestion des Reservations (bookings), Gestion des Comptes "
        "Utilisateurs (accounts), Gestion des Destinations (destinations) et Gestion des Promotions "
        "(promotions). Chaque module dispose de ses propres modeles, vues, formulaires, templates "
        "et tests unitaires.", body_style))

    # Tableau recapitulatif des modules
    story.append(Spacer(1, 12))
    story.append(make_table(
        ["Module", "Application Django", "Responsabilite principale"],
        [
            ["Gestion des Vols", "flights", "Recherche, affichage et gestion des vols et aeroports"],
            ["Reservations", "bookings", "Creation, suivi et annulation des reservations"],
            ["Comptes", "accounts", "Inscription, connexion et profils utilisateurs"],
            ["Destinations", "destinations", "Pages d'information sur les destinations"],
            ["Promotions", "promotions", "Codes promo et offres speciales"],
        ],
        col_widths=[3.5*cm, 3.5*cm, avail_width - 7*cm]
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<i>Tableau 1 : Recapitulatif des modules de l'application NouvelAir</i>",
        ParagraphStyle('Caption', fontName=BODY_FONT, fontSize=9,
                       leading=13, alignment=TA_CENTER, textColor=TEXT_MUTED)
    ))

    story.append(add_heading("1.4 Technologies Utilisees", h2_style, 1))
    story.append(Paragraph(
        "Le choix technologique s'est porte sur un stack Python/Django reconnu pour sa robustesse, "
        "sa securite et sa communaute active. Les technologies suivantes sont utilisees dans le "
        "projet :", body_style))
    story.append(make_table(
        ["Technologie", "Version", "Usage"],
        [
            ["Python", "3.12.4", "Langage principal"],
            ["Django", "4.2.30", "Framework web full-stack"],
            ["SQLite", "3", "Base de donnees (developpement)"],
            ["Bootstrap 5", "5.3", "Framework CSS responsive"],
            ["crispy-forms", "2.x", "Rendu elegante des formulaires Django"],
            ["django-countries", "7.x", "Champs de pays normalises"],
            ["django-phonenumber-field", "7.x", "Validation des numeros de telephone"],
            ["Pillow", "10.x", "Traitement des images (avatars, photos)"],
        ],
        col_widths=[4.5*cm, 2.5*cm, avail_width - 7*cm]
    ))

    # ===================== 2. SPECIFICATIONS FONCTIONNELLES =====================
    story.append(add_heading("2. Specifications Fonctionnelles", h1_style, 0))

    # --- 2.1 Module Vols ---
    story.append(add_heading("2.1 Module Gestion des Vols (flights)", h2_style, 1))
    story.append(Paragraph(
        "Le module Gestion des Vols est le coeur fonctionnel de l'application. Il permet aux "
        "utilisateurs de rechercher des vols disponibles, de consulter les details de chaque vol "
        "et de parcourir la liste des aeroports desservis. Ce module interagit etroitement avec "
        "le module de reservations, car la recherche de vols constitue la premiere etape du "
        "parcours de reservation.", body_style))

    story.append(add_heading("2.1.1 Modeles de Donnees", h3_style, 2))
    story.append(Paragraph(
        "Le module flights definit quatre modeles principaux qui structurent l'ensemble des "
        "donnees liees aux operations aeriennes. Ces modeles sont concus pour refléter "
        "fidèlement la realite operationnelle d'une compagnie aérienne.", body_style))

    story.append(Paragraph("<b>Modele Airport :</b> Represente un aeroport avec ses coordonnees "
        "geographiques. Chaque aeroport est identifie de maniere unique par un code IATA "
        "(par exemple TUN pour Tunis-Carthage, CDG pour Paris-Charles de Gaulle). Les champs "
        "incluent le code (CharField, max 3 caracteres), le nom complet, la ville, le pays, "
        "ainsi que la latitude et la longitude en FloatField pour le positionnement GPS. "
        "La base de donnees est peuplee avec 10 aeroports couvrant la Tunisie et les "
        "principales destinations europeennes et moyen-orientales.", body_style))

    story.append(Paragraph("<b>Modele Aircraft :</b> Decrit chaque appareil de la flotte. "
        "Les champs principaux sont model_name (designation commerciale de l'appareil), "
        "registration (immatriculation unique de l'avion), total_seats, economy_seats, "
        "business_seats (repartition des places par classe) et is_active (indique si l'appareil "
        "est actuellement en service). La flotte comprend 4 appareils de types differents "
        "pour simuler une flotte reelle.", body_style))

    story.append(Paragraph("<b>Modele Flight :</b> Represente un vol specifique avec ses "
        "caracteristiques operationnelles. Les champs incluent flight_number (numero de vol "
        "unique), origin et destination (cles etrangeres vers Airport), aircraft (cle etrangere "
        "vers Aircraft), departure_time et arrival_time (DateTimeField), base_price_economy "
        "et base_price_business (DecimalField pour les tarifs de base), available_seats_economy "
        "et available_seats_business (IntegerField pour le suivi des places disponibles), "
        "status (choix : scheduled, boarding, in_flight, landed, cancelled) et une methode "
        "get_current_price_economy qui calcule le prix dynamique. Le modele inclut egalement "
        "une methode get_duration_display qui formate la duree du vol de maniere lisible. "
        "La base contient 284 vols repartis sur plusieurs semaines.", body_style))

    story.append(Paragraph("<b>Modele FlightPriceHistory :</b> Enregistre l'historique des "
        "variations de prix pour chaque vol, permettant de tracer les evolutions tarifaires "
        "dans le temps.", body_style))

    # Tableau Flight - champs detailles
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Detail des champs du modele Flight :</b>", body_style))
    story.append(make_table(
        ["Champ", "Type", "Description"],
        [
            ["flight_number", "CharField", "Numero unique du vol (ex: NU201)"],
            ["origin", "FK -> Airport", "Aeroport de depart"],
            ["destination", "FK -> Airport", "Aeroport d'arrivee"],
            ["aircraft", "FK -> Aircraft", "Appareil affecte au vol"],
            ["departure_time", "DateTimeField", "Heure de depart (timezone-aware)"],
            ["arrival_time", "DateTimeField", "Heure d'arrivee (timezone-aware)"],
            ["base_price_economy", "DecimalField", "Prix de base classe economie (TND)"],
            ["base_price_business", "DecimalField", "Prix de base classe affaires (TND)"],
            ["available_seats_economy", "IntegerField", "Places disponibles economie"],
            ["available_seats_business", "IntegerField", "Places disponibles affaires"],
            ["status", "CharField (choices)", "scheduled / boarding / in_flight / landed / cancelled"],
        ],
        col_widths=[4*cm, 3.5*cm, avail_width - 7.5*cm]
    ))

    story.append(add_heading("2.1.2 Vues et Fonctionnalites", h3_style, 2))
    story.append(Paragraph(
        "Le module flights implemente cinq vues principales, chacune correspondant a une "
        "fonctionnalite specifique de l'interface utilisateur :", body_style))

    story.append(Paragraph(
        "<b>HomeView (page d'accueil) :</b> Vue principale de l'application. Elle affiche "
        "le formulaire de recherche de vols (origine, destination, date), les vols populaires "
        "ou mis en avant, les destinations recommandees et les promotions actives. C'est le "
        "point d'entree principal de l'application. L'URL correspondante est '/' avec le nom "
        "'home' dans l'espace de noms 'flights'.", body_style))

    story.append(Paragraph(
        "<b>FlightSearchView (recherche de vols) :</b> Traite les requetes de recherche "
        "emises depuis le formulaire d'accueil. Elle accepte les parametres d'origine, de "
        "destination et de date, puis filtre les vols disponibles dans la base de donnees. "
        "Les resultats sont affiches avec les informations essentielles : numero de vol, "
        "trajet, horaires, duree, prix et nombre de places restantes. Un mecanisme "
        "d'autocompletion est disponible pour les champs d'aeroports via l'endpoint "
        "airport_autocomplete. L'URL est '/search/' avec le nom 'flight_search'.", body_style))

    story.append(Paragraph(
        "<b>FlightDetailView (detail d'un vol) :</b> Affiche les informations completes "
        "d'un vol specifique identifie par son identifiant. L'utilisateur peut consulter "
        "les details de l'appareil, les horaires exacts, les tarifs par classe et "
        "proceder a la reservation directement depuis cette page. L'URL utilise le "
        "pattern '/flight/&lt;int:pk&gt;/' avec le nom 'flight_detail'.", body_style))

    story.append(Paragraph(
        "<b>AirportListView (liste des aeroports) :</b> Presente la liste complete des "
        "aeroports desservis par NouvelAir. Chaque aeroport est affiche avec son code IATA, "
        "sa localisation geographique et un lien vers sa page de detail. L'URL est "
        "'/airports/' avec le nom 'airport_list'.", body_style))

    story.append(Paragraph(
        "<b>AirportDetailView (detail d'un aeroport) :</b> Affiche les informations "
        "detaillees d'un aeroport, y compris sa localisation GPS et la liste des vols "
        "au depart et a l'arrivee. L'URL utilise le pattern '/airport/&lt;int:pk&gt;/' "
        "avec le nom 'airport_detail'.", body_style))

    story.append(add_heading("2.1.3 URL Patterns", h3_style, 2))
    story.append(Paragraph(
        "Toutes les URLs du module flights sont prefixees par l'espace de noms 'flights'. "
        "Dans les templates, les URLs doivent imperativement etre references avec la syntaxe "
        "{% url 'flights:home' %} et non {% url 'home' %} uniquement, sinon une erreur "
        "NoReverseMatch sera levee. Voici le mapping complet des URLs :", body_style))
    story.append(make_table(
        ["Pattern URL", "Nom (name)", "Vue associee"],
        [
            ["/", "home", "HomeView"],
            ["/search/", "flight_search", "FlightSearchView"],
            ["/flight/&lt;int:pk&gt;/", "flight_detail", "FlightDetailView"],
            ["/airports/", "airport_list", "AirportListView"],
            ["/airport/&lt;int:pk&gt;/", "airport_detail", "AirportDetailView"],
        ],
        col_widths=[5*cm, 3.5*cm, avail_width - 8.5*cm]
    ))

    # --- 2.2 Module Reservations ---
    story.append(add_heading("2.2 Module Reservations (bookings)", h2_style, 1))
    story.append(Paragraph(
        "Le module Reservations gere l'ensemble du cycle de vie d'une reservation, depuis "
        "sa creation par un utilisateur authentifie jusqu'a son annulation eventuelle. Ce "
        "module est le plus critique sur le plan fonctionnel car il implique des transactions "
        "financieres et doit garantir la coherence des donnees (places disponibles, montants, "
        "statuts). La conception des modeles et des vues prend en compte les contraintes "
        "de concurrence pour eviter les sur-reservations.", body_style))

    story.append(add_heading("2.2.1 Modeles de Donnees", h3_style, 2))
    story.append(Paragraph(
        "<b>Modele Booking :</b> Represente une reservation de vol. Les champs principaux "
        "incluent : booking_reference (chaine unique de reference), user (cle etrangere vers "
        "le modele User de Django), flight (cle etrangere vers Flight), passenger_first_name, "
        "passenger_last_name (noms du passager), passenger_email, passenger_phone, travel_class "
        "(choix : economy, business), number_of_passengers (IntegerField), status (choix : "
        "pending, confirmed, cancelled, completed), total_price (DecimalField), et les "
        "timestamps created_at et updated_at.", body_style))

    story.append(Paragraph(
        "<b>Modele Passenger :</b> Stocke les informations detaillees de chaque passager "
        "associe a une reservation. Ce modele est lie a Booking par une relation many-to-one. "
        "Les champs incluent passport_number, date_of_birth, nationality, gender et "
        "special_needs.", body_style))

    story.append(add_heading("2.2.2 Vues et Fonctionnalites", h3_style, 2))
    story.append(Paragraph(
        "<b>CreateBookingView :</b> Formulaire de creation de reservation accessible "
        "uniquement aux utilisateurs authentifies. Le formulaire collecte les informations "
        "du passager, la classe de voyage et le nombre de passagers. Apres validation, "
        "la reservation est creee avec le statut 'pending' et une reference unique est "
        "generee. URL : '/bookings/create/' (name='create').", body_style))
    story.append(Paragraph(
        "<b>BookingDetailView :</b> Affiche le detail complet d'une reservation specifique. "
        "L'utilisateur peut voir les informations du vol, les coordonnees du passager, le "
        "montant total et le statut actuel. Un bouton d'annulation est disponible si le "
        "statut le permet. URL : '/bookings/&lt;int:pk&gt;/' (name='detail').", body_style))
    story.append(Paragraph(
        "<b>BookingListView :</b> Liste toutes les reservations de l'utilisateur connecte. "
        "URL : '/bookings/' (name='booking_list').", body_style))
    story.append(Paragraph(
        "<b>BookingLookupView :</b> Permet a un utilisateur non authentifie de rechercher "
        "une reservation via sa reference de booking et son nom de famille. URL : "
        "'/bookings/lookup/' (name='lookup').", body_style))
    story.append(Paragraph(
        "<b>CancelBookingView :</b> Permet l'annulation d'une reservation si les conditions "
        "le permettent (delai avant le depart, statut actuel). URL : "
        "'/bookings/&lt;int:pk&gt;/cancel/' (name='cancel').", body_style))

    # --- 2.3 Module Comptes ---
    story.append(add_heading("2.3 Module Comptes Utilisateurs (accounts)", h2_style, 1))
    story.append(Paragraph(
        "Le module accounts gere l'authentification et les profils utilisateurs. Il utilise "
        "le systeme d'authentification natif de Django (AUTH_USER_MODEL='auth.User') associe "
        "a un modele UserProfile complementaire pour stocker les informations personnelles "
        "etendues. Ce choix architectural permet de beneficier de la robustesse du systeme "
        "de Django tout en ajoutant des champs specifiques au contexte d'une compagnie "
        "aerienne.", body_style))

    story.append(add_heading("2.3.1 Modele UserProfile", h3_style, 2))
    story.append(Paragraph(
        "Le modele UserProfile est lie a User par une relation OneToOne. Il stocke les "
        "informations personnelles avancees suivantes : address (adresse postale), avatar "
        "(ImageField pour la photo de profil), city et country, date_of_birth (DateField), "
        "gender (choix), nationality (pays via django-countries), newsletter (BooleanField "
        "pour le consentement marketing), passport_number (numero de passeport), phone "
        "(PhoneNumberField), ainsi que les timestamps created_at et updated_at. Le "
        "chargement des fixtures de test cree deux utilisateurs : admin (superutilisateur) "
        "et testuser, chacun avec un profil complet.", body_style))

    story.append(add_heading("2.3.2 Vues et Fonctionnalites", h3_style, 2))
    story.append(Paragraph(
        "Le module implemente les vues classiques d'un systeme d'authentification : "
        "LoginView (connexion via formulaire username/password avec redirection), "
        "LogoutView (deconnexion avec redirection vers l'accueil), RegisterView "
        "(inscription avec creation de User + UserProfile), et ProfileView (affichage "
        "et modification du profil). Les URL utilisent le prefixe '/accounts/' et "
        "l'espace de noms 'accounts'. Les identifiants de test sont : admin/NouvelAir2025! "
        "et testuser/NouvelAir2025!.", body_style))

    # --- 2.4 Module Destinations ---
    story.append(add_heading("2.4 Module Destinations (destinations)", h2_style, 1))
    story.append(Paragraph(
        "Le module destinations presente les informations touristiques et pratiques sur "
        "les differentes destinations desservies par NouvelAir. Il s'agit d'un module "
        "principalement informatif qui enrichit l'experience utilisateur en fournissant "
        "des details sur chaque ville ou pays accessible via les vols de la compagnie. "
        "Ce module contribue egalement au referencement SEO de l'application en proposant "
        "des pages descriptives riches en contenu pour chaque destination.", body_style))
    story.append(Paragraph(
        "<b>Modele Destination :</b> Les champs incluent name, slug (pour les URLs lisibles), "
        "short_description et description (texte complet), category (choix : beach, culture, "
        "adventure, business), rating (DecimalField pour la note moyenne), is_featured "
        "(BooleanField pour la mise en avant), image (ImageField) et airport (cle etrangere "
        "optionnelle vers Airport). La base contient 5 destinations de types varies. "
        "Les vues incluent DestinationListView ('/destinations/', name='destination_list') "
        "et DestinationDetailView ('/destinations/&lt;slug:slug&gt;/', name='detail').", body_style))

    # --- 2.5 Module Promotions ---
    story.append(add_heading("2.5 Module Promotions (promotions)", h2_style, 1))
    story.append(Paragraph(
        "Le module promotions gere les offres commerciales et codes de reduction proposes "
        "par NouvelAir. Ce module permet de stimuler les ventes en offrant des reductions "
        "temporelles et ciblees. L'implementation inclut la validation automatique des codes "
        "promo lors de la creation de reservation (verification de la validite, de la date "
        "d'expiration et du statut actif).", body_style))
    story.append(Paragraph(
        "<b>Modele Promotion :</b> Les champs incluent code (chaine unique identifiant "
        "la promotion), description, discount_percentage (pourcentage de reduction), "
        "start_date et end_date (dates de validite) et is_active (BooleanField). "
        "La base contient 3 promotions types. Les vues incluent PromotionListView "
        "('/promotions/', name='promotion_list') et PromotionDetailView "
        "('/promotions/&lt;int:pk&gt;/', name='detail').", body_style))

    # ===================== 3. ARCHITECTURE TECHNIQUE =====================
    story.append(add_heading("3. Architecture Technique", h1_style, 0))

    story.append(add_heading("3.1 Structure du Projet", h2_style, 1))
    story.append(Paragraph(
        "Le projet suit la structure standard d'un projet Django 4.2 avec le pattern "
        "projet/applications. Le repertoire principal nouvelair_project contient le "
        "fichier de configuration manage.py et le sous-repertoire nouvelair/ qui "
        "regroupe les parametres globaux du projet. Chaque module fonctionnel est "
        "implemente comme une application Django independante dans son propre "
        "sous-repertoire au meme niveau que le package du projet.", body_style))

    story.append(make_table(
        ["Repertoire", "Contenu"],
        [
            ["nouvelair_project/", "Racine du projet Django"],
            ["  nouvelair/", "Package de configuration (settings, urls, wsgi)"],
            ["  flights/", "Application Gestion des Vols"],
            ["  bookings/", "Application Reservations"],
            ["  accounts/", "Application Comptes Utilisateurs"],
            ["  destinations/", "Application Destinations"],
            ["  promotions/", "Application Promotions"],
            ["  ai_testing/", "Module de test assiste par IA"],
            ["  scripts/", "Scripts utilitaires (populate_test_data.py)"],
            ["  fixtures/", "Donnees initiales (initial_data.json)"],
        ],
        col_widths=[5*cm, avail_width - 5*cm]
    ))

    story.append(add_heading("3.2 Configuration Django (settings.py)", h2_style, 1))
    story.append(Paragraph(
        "Le fichier settings.py configure les parametres essentiels du projet. Les "
        "configurations critiques sont les suivantes :", body_style))
    story.append(make_table(
        ["Parametre", "Valeur", "Description"],
        [
            ["AUTH_USER_MODEL", "'auth.User'", "Utilise le modele User natif de Django"],
            ["USE_TZ", "True", "Support des fuseaux horaires"],
            ["TIME_ZONE", "'Africa/Tunis'", "Fuseau horaire de reference (Tunisie)"],
            ["CURRENCY", "'TND'", "Devise utilisee (Dinar Tunisien)"],
            ["LANGUAGE_CODE", "'fr'", "Langue par defaut (francais)"],
            ["INSTALLED_APPS", "(voir liste)", "5 apps + crispy_forms + countries + phonenumber"],
            ["TEMPLATES DIRS", "[BASE_DIR / 'templates']", "Repertoire des templates globaux"],
            ["LOGIN_URL", "'accounts:login'", "URL de redirection pour authentification"],
            ["LOGIN_REDIRECT_URL", "'flights:home'", "URL apres connexion reussie"],
            ["MEDIA_ROOT / URL", " BASE_DIR / 'media'", "Stockage des fichiers uploades"],
        ],
        col_widths=[3.5*cm, 4*cm, avail_width - 7.5*cm]
    ))

    story.append(add_heading("3.3 Context Processor", h2_style, 1))
    story.append(Paragraph(
        "Un processeur de contexte personnalise est defini dans "
        "nouvelair/context_processors.py. Il injecte automatiquement les variables "
        "site_name (nom du site) et site_tagline (slogan) dans tous les templates, "
        "permettant une personnalisation centralisee de l'interface sans modifier "
        "chaque vue individuellement. Ce processeur est enregistre dans la configuration "
        "TEMPLATES['OPTIONS']['context_processors'].", body_style))

    story.append(add_heading("3.4 Structure des Templates", h2_style, 1))
    story.append(Paragraph(
        "Le systeme de templates utilise le mecanisme d'heritage de Django. Le template "
        "de base (nouvelair/templates/base.html) definit la structure commune de toutes "
        "les pages : barre de navigation (navbar) avec les liens principaux, zone de "
        "contenu principal ({% block content %}) et pied de page (footer) avec les liens "
        "legaux, le formulaire de newsletter et les informations de contact. Chaque "
        "application possede son propre sous-repertoire de templates pour ses pages "
        "specifiques.", body_style))
    story.append(Paragraph(
        "<b>Navigation :</b> La navbar contient les liens suivants avec les espaces de "
        "noms correspondants : Accueil (flights:home), Vols (flights:flight_search), "
        "Destinations (destinations:destination_list), Promotions (promotions:promotion_list), "
        "Ma Reservation (bookings:booking_list, visible si connecte), Login/Logout/Register "
        "(accounts:login, accounts:logout, accounts:register). Les URLs dans les templates "
        "doivent toujours utiliser la syntaxe {% url 'namespace:name' %} pour eviter les "
        "erreurs NoReverseMatch.", body_style))
    story.append(Paragraph(
        "<b>Pied de page :</b> Le footer contient trois colonnes : Acces rapide (liens vers "
        "les pages principales), Assistance (liens vers legal.html et terms.html pour les "
        "mentions legales et conditions generales), et un formulaire d'inscription a la "
        "newsletter. Les pages legales et conditions sont servies par des TemplateView "
        "directes definies dans nouvelair/urls.py.", body_style))

    # ===================== 4. SCHEMA DE BASE DE DONNEES =====================
    story.append(add_heading("4. Schema de la Base de Donnees", h1_style, 0))
    story.append(Paragraph(
        "La base de donnees SQLite est utilisee pour le developpement et les tests. "
        "Elle est peuplee automatiquement via la commande de gestion Django "
        "populate_data (flights/management/commands/populate_data.py). Les donnees de "
        "test sont suffisamment riches pour couvrir la plupart des cas d'utilisation "
        "et des cas de test.", body_style))

    story.append(add_heading("4.1 Donnees de Test", h2_style, 1))
    story.append(make_table(
        ["Entite", "Quantite", "Details"],
        [
            ["Aeroports (Airport)", "10", "Tunisie + Europe + Moyen-Orient"],
            ["Appareils (Aircraft)", "4", "Differents types d'avions"],
            ["Vols (Flight)", "284", "Repartition sur plusieurs semaines"],
            ["Destinations", "5", "Beach, Culture, Adventure, Business"],
            ["Promotions", "3", "Codes de reduction actifs"],
            ["Utilisateurs", "2", "admin + testuser avec profils complets"],
        ],
        col_widths=[4*cm, 2.5*cm, avail_width - 6.5*cm]
    ))

    story.append(add_heading("4.2 Aeroports dans la Base", h2_style, 1))
    story.append(make_table(
        ["Code", "Nom", "Ville", "Pays"],
        [
            ["TUN", "Tunis-Carthage", "Tunis", "Tunisie"],
            ["MIR", "Habib Bourguiba", "Monastir", "Tunisie"],
            ["DJE", "Zarzis", "Djerba", "Tunisie"],
            ["SFA", "Sfax-Thyna", "Sfax", "Tunisie"],
            ["TOE", "Nefta", "Tozeur", "Tunisie"],
            ["CDG", "Charles de Gaulle", "Paris", "France"],
            ["FCO", "Leonardo da Vinci", "Rome", "Italie"],
            ["IST", "Istanbul Airport", "Istanbul", "Turquie"],
            ["CMN", "Mohammed V", "Casablanca", "Maroc"],
            ["ALG", "Houari Boumediene", "Alger", "Algerie"],
        ],
        col_widths=[2*cm, 4.5*cm, 3*cm, avail_width - 9.5*cm]
    ))

    # ===================== 5. EXIGENCES NON-FONCTIONNELLES =====================
    story.append(add_heading("5. Exigences Non-Fonctionnelles", h1_style, 0))

    story.append(add_heading("5.1 Securite", h2_style, 1))
    story.append(Paragraph(
        "La securite est un aspect fondamental du systeme NouvelAir, particulierement "
        "dans le contexte d'une application gerant des donnees personnelles et des "
        "transactions financieres. Les mesures de securite implementees comprennent : "
        "la protection CSRF de Django (automatique via le middleware CsrfViewMiddleware), "
        "le hachage des mots de passe avec l'algorithme PBKDF2 de Django, la protection "
        "contre les injections SQL via l'ORM Django, la validation des donnees en amont "
        "par les formulaires Django et crispy-forms, et la gestion des sessions securisees "
        "via le framework d'authentification de Django. Les vues sensibles (creation de "
        "reservation, profil utilisateur) sont protegees par le decorateur @login_required.", body_style))

    story.append(add_heading("5.2 Performance", h2_style, 1))
    story.append(Paragraph(
        "L'application doit repondre aux exigences de performance suivantes : temps de "
        "chargement des pages inferieur a 3 secondes pour les pages statiques et inferieur "
        "a 5 secondes pour les pages avec requetes base de donnees complexes (recherche de "
        "vols). L'autocompletion des aeroports doit repondre en moins de 500 millisecondes. "
        "Les requetes de recherche doivent utiliser les index de base de donnees de maniere "
        "optimale, notamment sur les champs origin, destination et departure_time du modele "
        "Flight.", body_style))

    story.append(add_heading("5.3 Compatibilite et Responsive Design", h2_style, 1))
    story.append(Paragraph(
        "L'interface utilisateur est concue avec Bootstrap 5 pour garantir une compatibilite "
        "maximale avec les navigateurs modernes (Chrome, Firefox, Safari, Edge) et un design "
        "responsive s'adaptant aux differentes tailles d'ecran (desktop, tablette, mobile). "
        "Les points de rupture Bootstrap standards sont utilises : 576px (sm), 768px (md), "
        "992px (lg) et 1200px (xl). Le framework crispy-forms avec le template "
        "crispy_bootstrap5 assure un rendu coherent des formulaires sur tous les peripheriques.", body_style))

    story.append(add_heading("5.4 Internationalisation", h2_style, 1))
    story.append(Paragraph(
        "Le projet est initialement developpe en francais (LANGUAGE_CODE='fr') avec le "
        "fuseau horaire de la Tunisie (Africa/Tunis). La monnaie utilisee est le Dinar "
        "Tunisien (TND). L'architecture du projet permet une future internationalisation "
        "via le systeme i18n de Django si necessaire, bien que cette fonctionnalite ne "
        "soit pas implementee dans la version actuelle. Les noms de pays sont geres par "
        "la bibliotheque django-countries qui supporte les noms en plusieurs langues.", body_style))

    # ===================== 6. CARTOGRAPHIE DES URLs =====================
    story.append(add_heading("6. Cartographie Complete des URLs", h1_style, 0))
    story.append(Paragraph(
        "Le tableau ci-dessous presente la cartographie complete de toutes les URLs de "
        "l'application. Il est essentiel de respecter les espaces de noms (app_name) "
        " lors de la creation ou la modification des templates pour eviter les erreurs "
        "de resolution URL. Chaque application Django definit son propre app_name dans "
        "son fichier urls.py.", body_style))

    story.append(add_heading("6.1 Module Flights", h2_style, 1))
    story.append(make_table(
        ["URL", "Nom", "Vue", "Methode"],
        [
            ["/", "flights:home", "HomeView", "GET"],
            ["/search/", "flights:flight_search", "FlightSearchView", "GET/POST"],
            ["/flight/&lt;int:pk&gt;/", "flights:flight_detail", "FlightDetailView", "GET"],
            ["/airports/", "flights:airport_list", "AirportListView", "GET"],
            ["/airport/&lt;int:pk&gt;/", "flights:airport_detail", "AirportDetailView", "GET"],
        ],
        col_widths=[3.5*cm, 3.5*cm, 4*cm, avail_width - 11*cm]
    ))

    story.append(add_heading("6.2 Module Bookings", h2_style, 1))
    story.append(make_table(
        ["URL", "Nom", "Vue", "Methode"],
        [
            ["/bookings/create/", "bookings:create", "CreateBookingView", "GET/POST"],
            ["/bookings/&lt;int:pk&gt;/", "bookings:detail", "BookingDetailView", "GET"],
            ["/bookings/", "bookings:booking_list", "BookingListView", "GET"],
            ["/bookings/lookup/", "bookings:lookup", "BookingLookupView", "GET/POST"],
            ["/bookings/&lt;int:pk&gt;/cancel/", "bookings:cancel", "CancelBookingView", "POST"],
        ],
        col_widths=[4*cm, 3.5*cm, 4*cm, avail_width - 11.5*cm]
    ))

    story.append(add_heading("6.3 Module Accounts", h2_style, 1))
    story.append(make_table(
        ["URL", "Nom", "Vue", "Methode"],
        [
            ["/accounts/login/", "accounts:login", "LoginView", "GET/POST"],
            ["/accounts/logout/", "accounts:logout", "LogoutView", "GET"],
            ["/accounts/register/", "accounts:register", "RegisterView", "GET/POST"],
            ["/accounts/profile/", "accounts:profile", "ProfileView", "GET"],
        ],
        col_widths=[4*cm, 3.5*cm, 4*cm, avail_width - 11.5*cm]
    ))

    story.append(add_heading("6.4 Module Destinations", h2_style, 1))
    story.append(make_table(
        ["URL", "Nom", "Vue"],
        [
            ["/destinations/", "destinations:destination_list", "DestinationListView"],
            ["/destinations/&lt;slug:slug&gt;/", "destinations:detail", "DestinationDetailView"],
        ],
        col_widths=[5*cm, 5*cm, avail_width - 10*cm]
    ))

    story.append(add_heading("6.5 Module Promotions", h2_style, 1))
    story.append(make_table(
        ["URL", "Nom", "Vue"],
        [
            ["/promotions/", "promotions:promotion_list", "PromotionListView"],
            ["/promotions/&lt;int:pk&gt;/", "promotions:detail", "PromotionDetailView"],
        ],
        col_widths=[5*cm, 5*cm, avail_width - 10*cm]
    ))

    story.append(add_heading("6.6 Pages Legales (TemplateView)", h2_style, 1))
    story.append(Paragraph(
        "Les pages legales sont definies directement dans nouvelair/urls.py en utilisant "
        "des TemplateView generic de Django, sans espace de noms. Les templates "
        "correspondants (legal.html et terms.html) sont stockes dans le repertoire "
        "nouvelair/templates/.", body_style))
    story.append(make_table(
        ["URL", "Nom", "Template"],
        [
            ["/legal/", "legal", "legal.html"],
            ["/terms/", "terms", "terms.html"],
        ],
        col_widths=[5*cm, 3.5*cm, avail_width - 8.5*cm]
    ))

    # ===================== 7. STRATEGIE DE TEST =====================
    story.append(add_heading("7. Strategie de Test et Assurance Qualite", h1_style, 0))
    story.append(Paragraph(
        "Le projet NouvelAir integre une strategie de test complete, concue a la fois "
        "pour garantir la qualite du code et pour servir de support pedagogique dans "
        "le cadre de la formation Test/QA. La strategie couvre trois niveaux : les tests "
        "unitaires, les tests d'integration et les tests de bout en bout assistes par IA.", body_style))

    story.append(add_heading("7.1 Tests Unitaires", h2_style, 1))
    story.append(Paragraph(
        "Chaque application Django dispose de son propre fichier de tests unitaires "
        "(tests/test_models.py) qui valide le comportement des modeles. Les tests "
        "verifient notamment : la creation correcte des objets en base de donnees, "
        "les contraintes d'integrite (champs uniques, valeurs nulles interdites), "
        "les methodes personnalisees (get_duration_display, get_current_price_economy), "
        "et les proprietes calculees. Les tests sont executables via la commande "
        "python manage.py test.", body_style))

    story.append(add_heading("7.2 Tests d'Integration", h2_style, 1))
    story.append(Paragraph(
        "Les tests d'integration verifient le bon fonctionnement des interactions entre "
        "les differents composants de l'application : vues + modeles + templates + URLs. "
        "Ces tests simulent des requetes HTTP completes et valident les reponses (statut "
        "200, contenu attendu, redirections correctes). L'outil Django Test Client est "
        "utilise pour ces tests, permettant de simuler le comportement d'un navigateur "
        "sans necessite de serveur web actif.", body_style))

    story.append(add_heading("7.3 Tests End-to-End avec IA", h2_style, 1))
    story.append(Paragraph(
        "Le module ai_testing (repertoire ai_testing/) implemente un framework de tests "
        "de bout en bout assistes par intelligence artificielle. Les fichiers principaux "
        "sont ai_test_tools.py (outils et utilitaires pour les tests IA) et "
        "tests_e2e.py (scenarios de test end-to-end). Ce module permet d'automatiser "
        "la generation de cas de test, la detection d'anomalies et l'analyse des resultats "
        "de test en utilisant des modeles d'intelligence artificielle. Il constitue un "
        "element pedagogique important pour la formation, demontrant l'integration de "
        "l'IA dans les processus d'assurance qualite.", body_style))

    # ===================== 8. GUIDE DE DEPLOIEMENT =====================
    story.append(add_heading("8. Guide de Deploiement et Installation", h1_style, 0))

    story.append(add_heading("8.1 Prerequis", h2_style, 1))
    story.append(Paragraph(
        "Pour installer et faire fonctionner le projet NouvelAir sur votre machine, "
        "les prerequis suivants sont necessaires :", body_style))
    story.append(make_table(
        ["Composant", "Version minimale", "Note"],
        [
            ["Python", "3.10+", "3.12.4 recommandee"],
            ["pip", "Derniere version", "Gestionnaire de paquets Python"],
            ["Navigateur web", "Moderne", "Chrome, Firefox, Safari ou Edge"],
            ["Editeur de code", "Au choix", "VS Code, PyCharm recommandes"],
        ],
        col_widths=[4*cm, 3.5*cm, avail_width - 7.5*cm]
    ))

    story.append(add_heading("8.2 Procedure d'Installation", h2_style, 1))
    story.append(Paragraph(
        "<b>Etape 1 - Creer l'environnement virtuel (recommande) :</b><br/>"
        "Ouvrez un terminal et executez les commandes suivantes pour creer et activer "
        "un environnement virtuel Python isole. Cette pratique est vivement recommandee "
        "pour eviter les conflits de dependances avec d'autres projets.", body_style))
    story.append(Paragraph(
        "<b>Etape 2 - Installer les dependances :</b><br/>"
        "Executez 'pip install -r requirements.txt' dans le repertoire du projet. "
        "Le fichier requirements.txt contient toutes les bibliotheques necessaires : "
        "Django, crispy-forms, crispy-bootstrap5, django-countries, django-phonenumber-field "
        "et Pillow. Si vous rencontrez des erreurs d'installation, verifiez que pip "
        "est a jour avec 'python -m pip install --upgrade pip'.", body_style))
    story.append(Paragraph(
        "<b>Etape 3 - Initialiser la base de donnees :</b><br/>"
        "Executez 'python manage.py makemigrations' puis 'python manage.py migrate' "
        "pour creer les tables de la base de donnees SQLite. Ces commandes lisent les "
        "fichiers de migration de chaque application et creent les tables correspondantes.", body_style))
    story.append(Paragraph(
        "<b>Etape 4 - Peupler la base de donnees :</b><br/>"
        "Executez 'python manage.py populate_data' pour inserer les donnees de test "
        "(10 aeroports, 4 appareils, 284 vols, 5 destinations, 3 promotions, 2 utilisateurs). "
        "Cette commande peut prendre quelques secondes en raison du volume de donnees generees.", body_style))
    story.append(Paragraph(
        "<b>Etape 5 - Lancer le serveur :</b><br/>"
        "Executez 'python manage.py runserver' puis ouvrez votre navigateur a l'adresse "
        "http://127.0.0.1:8000/ pour acceder a l'application.", body_style))

    story.append(add_heading("8.3 Comptes de Test", h2_style, 1))
    story.append(make_table(
        ["Identifiant", "Mot de passe", "Profil", "Role"],
        [
            ["admin", "NouvelAir2025!", "Superutilisateur", "Administration complete"],
            ["testuser", "NouvelAir2025!", "Utilisateur standard", "Reservation et navigation"],
        ],
        col_widths=[3*cm, 3.5*cm, 4*cm, avail_width - 10.5*cm]
    ))

    # ===================== 9. PROBLEMES CONNUS ET SOLUTIONS =====================
    story.append(add_heading("9. Problemes Connus et Solutions", h1_style, 0))
    story.append(Paragraph(
        "Cette section documente les problemes rencontres lors du developpement et du "
        "deploiement initial du projet, ainsi que les solutions appliquees. Elle sert "
        "de reference pour les developpeurs et les testeurs qui travaillent sur le projet.", body_style))

    story.append(add_heading("9.1 Erreurs de Namespace URL", h2_style, 1))
    story.append(Paragraph(
        "Chaque application Django definit un app_name dans son urls.py, creant un espace "
        "de noms pour ses URLs. Les templates doivent imperativement utiliser la syntaxe "
        "complete {% url 'namespace:name' %} (par exemple {% url 'flights:home' %}). "
        "L'utilisation de {% url 'home' %} sans le prefixe provoque une erreur "
        "NoReverseMatch. Cette regle s'applique a tous les liens dans les templates, "
        "y compris ceux du fichier base.html (navbar et footer).", body_style))

    story.append(add_heading("9.2 Champs de Modele", h2_style, 1))
    story.append(Paragraph(
        "Attention aux noms de champs specifiques lors de l'ecriture de requetes ou "
        "de scripts de population. Les erreurs suivantes ont ete rencontrees et corrigees : "
        "Aircraft utilise 'registration' (et non 'code') et 'model_name' (et non 'name') ; "
        "UserProfile est accessible via 'user' (cle etrangere) et non 'username' ; "
        "Airport utilise 'latitude' et 'longitude' en FloatField (NOT NULL, valeurs "
        "reelles requises). Ces ecarts entre les noms attendus et les noms reels des "
        "champs sont une source frequente de bugs et doivent etre verifies avant toute "
        "modification du code.", body_style))

    story.append(add_heading("9.3 Filtres de Template", h2_style, 1))
    story.append(Paragraph(
        "Le filtre de template 'duration_format' n'existe pas par defaut dans Django. "
        "La solution adoptee a ete de remplacer son utilisation dans les templates par "
        "l'appel de la methode de modele get_duration_display() directement sur l'objet "
        "Flight. Par exemple, au lieu de {{ flight.departure_time|duration_format:flight.arrival_time }}, "
        "utilisez {{ flight.get_duration_display }}. Cette methode est definie dans le "
        "modele Flight et calcule automatiquement la duree a partir des champs departure_time "
        "et arrival_time.", body_style))

    story.append(add_heading("9.4 Pages Legales Manquantes", h2_style, 1))
    story.append(Paragraph(
        "Le footer de base.html contient des liens vers les pages legales (legal) et "
        "conditions generales (terms). Si ces pages ne sont pas configurees dans "
        "nouvelair/urls.py, une erreur NoReverseMatch sera levee a chaque chargement de "
        "page. La solution consiste a ajouter les patterns URL suivants dans "
        "nouvelair/urls.py : deux chemins pointant vers TemplateView avec les templates "
        "legal.html et terms.html, stockes dans le repertoire nouvelair/templates/. "
        "L'import de TemplateView depuis django.views.generic est necessaire.", body_style))

    # ===================== 10. GLOSSAIRE =====================
    story.append(add_heading("10. Glossaire", h1_style, 0))
    story.append(make_table(
        ["Terme", "Definition"],
        [
            ["NoReverseMatch", "Erreur Django quand une URL ne peut pas etre resolue depuis un nom"],
            ["app_name", "Espace de noms d'une application Django dans la resolution des URLs"],
            ["TemplateView", "Vue generique Django qui rend un template sans logique metier"],
            ["Context Processor", "Fonction injectant des variables globales dans tous les templates"],
            ["ORM", "Object-Relational Mapping : couche d'abstraction base de donnees de Django"],
            ["Migration", "Fichier de modification du schema de base de donnees versionne"],
            ["CRUD", "Create, Read, Update, Delete - operations de base sur les donnees"],
            ["TND", "Dinar Tunisien - devise officielle de la Tunisie"],
            ["IATA", "Association Internationale du Transport Aerien (codes aeroports)"],
            ["QA", "Quality Assurance - Assurance Qualite"],
        ],
        col_widths=[3.5*cm, avail_width - 3.5*cm]
    ))

    # ===================== BUILD =====================
    print("Generation du PDF en cours...")
    doc.multiBuild(story, onLaterPages=add_page_number, onFirstPage=add_page_number)
    print("Fichier genere avec succes :")
    print(f"  {OUTPUT_FILE}")
    print(f"  Taille : {os.path.getsize(OUTPUT_FILE) / 1024:.1f} Ko")


if __name__ == '__main__':
    build_document()
