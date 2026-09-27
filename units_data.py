"""
units_data.py
Vollständige Datenbank aller Einheiten für Total Battle.
Enthält Basis-HP, STR, Führungskraft-Gewichte (weight) und Klassifizierungen.
"""

# 1. Ingenieure / Belagerungswaffen (Gewicht: 10 L)
ENGINEERS = {
    "e9_josephine": {"name_key": "e9_josephine", "hp": 165300, "str": 27550, "weight": 10, "tier": "E9", "is_garage": True},
    "e8_josephine": {"name_key": "e8_josephine", "hp": 91800, "str": 15310, "weight": 10, "tier": "E8", "is_garage": True}
}

# 2. Autonome Monster M7–M9 (Gewicht: 0 L)
MONSTERS = {
    # M7
    "m7_wind_lord": {"name_key": "m7_wind_lord", "hp": 930000, "str": 310000, "weight": 0, "tier": "M7", "is_garage": False},
    "m7_black_dragon": {"name_key": "m7_black_dragon", "hp": 900000, "str": 300000, "weight": 0, "tier": "M7", "is_garage": False},
    "m7_colossus": {"name_key": "m7_colossus", "hp": 870000, "str": 290000, "weight": 0, "tier": "M7", "is_garage": False},
    "m7_ancient_terror": {"name_key": "m7_ancient_terror", "hp": 840000, "str": 280000, "weight": 0, "tier": "M7", "is_garage": False},
    # M8
    "m8_kraken": {"name_key": "m8_kraken", "hp": 2010000, "str": 670000, "weight": 0, "tier": "M8", "is_garage": False},
    "m8_fire_phoenix": {"name_key": "m8_fire_phoenix", "hp": 1980000, "str": 660000, "weight": 0, "tier": "M8", "is_garage": False},
    "m8_devastator": {"name_key": "m8_devastator", "hp": 1950000, "str": 650000, "weight": 0, "tier": "M8", "is_garage": False},
    "m8_trickster": {"name_key": "m8_trickster", "hp": 1920000, "str": 640000, "weight": 0, "tier": "M8", "is_garage": False},
    # M9
    "m9_kraken": {"name_key": "m9_kraken", "hp": 3630000, "str": 1210000, "weight": 0, "tier": "M9", "is_garage": False},
    "m9_fire_phoenix": {"name_key": "m9_fire_phoenix", "hp": 3570000, "str": 1190000, "weight": 0, "tier": "M9", "is_garage": False},
    "m9_devastator": {"name_key": "m9_devastator", "hp": 3510000, "str": 1170000, "weight": 0, "tier": "M9", "is_garage": False},
    "m9_trickster": {"name_key": "m9_trickster", "hp": 3450000, "str": 1150000, "weight": 0, "tier": "M9", "is_garage": False}
}

# 3. Reguläre Truppen (T8, T9 und G7-Ersatz)
REGULAR_TROOPS = {
    # T8 Spezialisten und Gardisten
    "s8_duellist": {"name_key": "s8_duellist", "hp": 9200, "str": 3060, "weight": 1, "tier": "S8", "is_garage": True},
    "s8_legitimist": {"name_key": "s8_legitimist", "hp": 9200, "str": 3060, "weight": 1, "tier": "S8", "is_garage": True},
    "s8_whitemane": {"name_key": "s8_whitemane", "hp": 18400, "str": 6120, "weight": 2, "tier": "S8", "is_garage": True},
    "s8_royal_lion": {"name_key": "s8_royal_lion", "hp": 183600, "str": 61180, "weight": 20, "tier": "S8", "is_garage": True},
    "g8_punisher": {"name_key": "g8_punisher", "hp": 9200, "str": 3060, "weight": 1, "tier": "G8", "is_garage": True},
    "g8_purifier": {"name_key": "g8_purifier", "hp": 9200, "str": 3060, "weight": 1, "tier": "G8", "is_garage": True},
    "g8_smiter": {"name_key": "g8_smiter", "hp": 18400, "str": 6120, "weight": 2, "tier": "G8", "is_garage": True},
    "g8_corax": {"name_key": "g8_corax", "hp": 183600, "str": 61190, "weight": 20, "tier": "G8", "is_garage": True},
    # T9 Core
    "s9_duellist": {"name_key": "s9_duellist", "hp": 16500, "str": 5510, "weight": 1, "tier": "S9", "is_garage": True},
    "s9_legitimist": {"name_key": "s9_legitimist", "hp": 16500, "str": 5510, "weight": 1, "tier": "S9", "is_garage": True},
    "s9_whitemane": {"name_key": "s9_whitemane", "hp": 33100, "str": 11010, "weight": 2, "tier": "S9", "is_garage": True},
    "s9_royal_lion": {"name_key": "s9_royal_lion", "hp": 330600, "str": 110150, "weight": 20, "tier": "S9", "is_garage": True},
    "g9_punisher": {"name_key": "g9_punisher", "hp": 16500, "str": 5510, "weight": 1, "tier": "G9", "is_garage": True},
    "g9_purifier": {"name_key": "g9_purifier", "hp": 16500, "str": 5510, "weight": 1, "tier": "G9", "is_garage": True},
    "g9_smiter": {"name_key": "g9_smiter", "hp": 33100, "str": 11010, "weight": 2, "tier": "G9", "is_garage": True},
    "g9_corax": {"name_key": "g9_corax", "hp": 330600, "str": 110150, "weight": 20, "tier": "G9", "is_garage": True},
    # G7 Developing Ersatz
    "g7_infantry_sub": {"name_key": "g7_infantry_sub", "hp": 5200, "str": 1730, "weight": 1, "tier": "G7", "is_garage": True},
    "g7_mounted_sub": {"name_key": "g7_mounted_sub", "hp": 10400, "str": 3460, "weight": 2, "tier": "G7", "is_garage": True}
}

# 4. T9 Söldner (Linie 7, kein Verbrauch von Garagen-Führungskraft)
MERCENARIES_T9 = {
    # Spezialisten
    "merc_pounder": {"name_key": "merc_pounder", "hp": 33000, "str": 11000, "weight": 0, "class": "spec_melee", "is_garage": False},
    "merc_galloper": {"name_key": "merc_galloper", "hp": 66000, "str": 22000, "weight": 0, "class": "spec_mounted", "is_garage": False},
    "merc_scarface": {"name_key": "merc_scarface", "hp": 33000, "str": 11000, "weight": 0, "class": "spec_ranged", "is_garage": False},
    "merc_grace": {"name_key": "merc_grace", "hp": 16530, "str": 5510, "weight": 0, "class": "spec_scout", "is_garage": False},
    "merc_jago": {"name_key": "merc_jago", "hp": 660000, "str": 220000, "weight": 0, "class": "spec_flying", "is_garage": False},
    # Gardisten
    "merc_slavic_warrior": {"name_key": "merc_slavic_warrior", "hp": 33000, "str": 11000, "weight": 0, "class": "guard_melee", "is_garage": False},
    "merc_quicksand": {"name_key": "merc_quicksand", "hp": 66000, "str": 22000, "weight": 0, "class": "guard_mounted", "is_garage": False},
    "merc_highlander": {"name_key": "merc_highlander", "hp": 33000, "str": 11000, "weight": 0, "class": "guard_ranged", "is_garage": False},
    "merc_warregal": {"name_key": "merc_warregal", "hp": 660000, "str": 220000, "weight": 0, "class": "guard_flying", "is_garage": False},
    # Schwere Kreaturen / Belagerung
    "merc_ariel": {"name_key": "merc_ariel", "hp": 330000, "str": 55000, "weight": 0, "class": "siege", "is_garage": False},
    "merc_salamander": {"name_key": "merc_salamander", "hp": 1230000, "str": 410000, "weight": 0, "class": "beast", "is_garage": False},
    "merc_cannoneer": {"name_key": "merc_cannoneer", "hp": 1320000, "str": 440000, "weight": 0, "class": "siege", "is_garage": False},
    "merc_warden": {"name_key": "merc_warden", "hp": 1410000, "str": 470000, "weight": 0, "class": "beast", "is_garage": False},
    "merc_wyvern": {"name_key": "merc_wyvern", "hp": 2070000, "str": 690000, "weight": 0, "class": "flying", "is_garage": False},
    # Letzte Stufe (Strike-Einheit mit +1000 % gegen Epics)
    "merc_epic_hunter": {"name_key": "merc_epic_hunter", "hp": 75000, "str": 25000, "weight": 0, "class": "strike", "is_garage": False}
}
