"""
app.py
Hauptprogramm: Streamlit Web-Interface und dynamische Optimierung
der Total HP Stufen für den Marsch in Total Battle.
"""

import streamlit as st
from translations import TRANSLATIONS
from units_data import ENGINEERS, MONSTERS, REGULAR_TROOPS, MERCENARIES_T9

st.set_page_config(
    page_title="Total Battle March Calculator",
    page_icon="🛡️",
    layout="wide"
)

def build_unit_catalog(is_s8_dev: bool):
    """
    Kombiniert alle Einheiten in eine geordnete Reihenfolge für die Marschbildung:
    1. Belagerung (E9, E8)
    2. Schwere Monster (M7)
    3. T8 Garagentruppen (Spezialisten -> Gardisten)
    4. T9 Garagentruppen (oder G7 bei S8 Developing)
    5. M9 Monster
    6. T9 Söldner (Spezialisten -> Gardisten -> Kreaturen)
    7. Superior Epic Monster Hunter (Basis)
    """
    catalog = []
    
    # 1. Belagerung
    catalog.append(ENGINEERS["e9_josephine"])
    catalog.append(ENGINEERS["e8_josephine"])
    
    # 2. Monster M7
    catalog.append(MONSTERS["m7_wind_lord"])
    catalog.append(MONSTERS["m7_black_dragon"])
    catalog.append(MONSTERS["m7_colossus"])
    catalog.append(MONSTERS["m7_ancient_terror"])
    
    # 3. T8 Garage
    catalog.append(REGULAR_TROOPS["s8_duellist"])
    catalog.append(REGULAR_TROOPS["g8_punisher"])
    catalog.append(REGULAR_TROOPS["s8_whitemane"])
    catalog.append(REGULAR_TROOPS["g8_smiter"])
    
    # 4. T9 Garage oder G7 Ersatz
    if is_s8_dev:
        catalog.append(REGULAR_TROOPS["g7_infantry_sub"])
        catalog.append(REGULAR_TROOPS["g7_mounted_sub"])
    else:
        catalog.append(REGULAR_TROOPS["s9_duellist"])
        catalog.append(REGULAR_TROOPS["g9_punisher"])
        catalog.append(REGULAR_TROOPS["s9_whitemane"])
        catalog.append(REGULAR_TROOPS["g9_smiter"])
        
    # 5. Monster M9
    catalog.append(MONSTERS["m9_kraken"])
    catalog.append(MONSTERS["m9_trickster"])
    
    # 6. Söldner T9: Spezialisten -> Gardisten -> Schwere Kreaturen
    catalog.append(MERCENARIES_T9["merc_pounder"])
    catalog.append(MERCENARIES_T9["merc_galloper"])
    catalog.append(MERCENARIES_T9["merc_slavic_warrior"])
    catalog.append(MERCENARIES_T9["merc_quicksand"])
    catalog.append(MERCENARIES_T9["merc_wyvern"])
    catalog.append(MERCENARIES_T9["merc_warden"])
    
    # 7. Strike Einheit ganz unten
    catalog.append(MERCENARIES_T9["merc_epic_hunter"])
    
    return catalog

def calculate_ladder(total_leadership: int, is_s8_dev: bool):
    """
    Dynamische Berechnung der Einheitenanzahl (N_i) für streng monotone
    Total HP Abnahme unter Berücksichtigung des Führungskraft-Budgets.
    """
    units = build_unit_catalog(is_s8_dev)
    
    # Skalierung des Ziel-HP-Pools anhand der Führungskraft
    ref_lead = 500000
    scale = max(0.1, total_leadership / ref_lead)
    
    # Ziel-HP der obersten Stufe (Josephine II)
    current_target_hp = 42000000 * scale
    decrement_step = current_target_hp * 0.035  # Schrittweite zwischen den Stufen
    
    results = []
    used_lead = 0
    prev_hp = float('inf')
    
    for idx, unit in enumerate(units, 1):
        hp_unit = unit["hp"]
        weight = unit["weight"]
        is_garage = unit["is_garage"]
        
        # Ideale Anzahl nach mathematischer Stufenformel
        count = max(1, int(current_target_hp / hp_unit))
        
        # Führungskraft-Restriktion für Garagentruppen
        if is_garage:
            cost = count * weight
            if used_lead + cost > total_leadership:
                rem_lead = max(0, total_leadership - used_lead)
                count = max(1, rem_lead // weight) if weight > 0 else count
            used_lead += count * weight
            
        total_hp = count * hp_unit
        
        # Sicherheitskorrektur zur Wahrung der Abnahme
        if total_hp >= prev_hp:
            total_hp = prev_hp - (hp_unit if prev_hp > hp_unit else 1)
            count = max(1, int(total_hp / hp_unit))
            total_hp = count * hp_unit
            
        results.append({
            "step": idx,
            "name_key": unit["name_key"],
            "count": count,
            "hp": hp_unit,
            "total_hp": total_hp,
            "lead_cost": count * weight if is_garage else 0,
            "is_valid": total_hp < prev_hp or idx == 1
        })
        
        prev_hp = total_hp
        current_target_hp = max(hp_unit, total_hp - decrement_step)
        
    return results, used_lead

def main():
    # Sprachauswahl
    lang_map = {
        "ru": "Русский", "en": "English", "de": "Deutsch", "fr": "Français",
        "es": "Español", "it": "Italiano", "pl": "Polski", "tr": "Türkçe",
        "pt": "Português", "zh": "中文"
    }
    selected_lang = st.sidebar.selectbox("Language / Sprache / Язык", options=list(lang_map.keys()), format_func=lambda x: lang_map[x])
    txt = TRANSLATIONS[selected_lang]
    
    st.title(txt["title"])
    st.caption(txt["subtitle"])
    st.sidebar.markdown("---")
    
    # Eingaben
    total_leadership = st.sidebar.number_input(
        txt["lead_label"],
        min_value=50000,
        max_value=2500000,
        value=500000,
        step=25000
    )
    is_s8_dev = st.sidebar.checkbox(txt["s8_dev_label"], value=False)
    calc_pressed = st.sidebar.button(txt["calc_btn"], type="primary")
    
    if calc_pressed:
        march_plan, used_leadership = calculate_ladder(total_leadership, is_s8_dev)
        
        display_rows = []
        for r in march_plan:
            unit_display_name = txt.get(r["name_key"], r["name_key"])
            status_text = f"✅ {txt['status_ok']}" if r["is_valid"] else f"⚠️ {txt['status_adj']}"
            
            display_rows.append({
                txt["col_step"]: r["step"],
                txt["col_name"]: unit_display_name,
                txt["col_count"]: f"{r['count']:,}",
                txt["col_hp"]: f"{r['hp']:,}",
                txt["col_total_hp"]: f"{r['total_hp']:,}",
                txt["col_lead"]: f"{r['lead_cost']:,}",
                txt["col_status"]: status_text
            })
            
        st.table(display_rows)
        st.metric(label=txt["lead_used"], value=f"{used_leadership:,} / {total_leadership:,}")

if __name__ == "__main__":
    main()
