"""
app.py
Минималистичный калькулятор марша Total Battle:
- Вывод только названия отряда и количества
- Полная утилизация лидерства (99-100%)
- Округление монстров кратно 10
- Изолированные сессии пользователей
"""

import math
import streamlit as st
from translations import TRANSLATIONS
from units_data import ENGINEERS, MONSTERS, REGULAR_TROOPS, MERCENARIES_T9

# Настройка страницы
st.set_page_config(
    page_title="Total Battle March Calculator",
    page_icon="🛡️",
    layout="centered"
)

def build_unit_catalog(is_s8_dev: bool):
    """Формирует последовательность ступеней марша сверху вниз."""
    catalog = []
    
    # 1. Осада (E9, E8)
    catalog.append(ENGINEERS["e9_josephine"])
    catalog.append(ENGINEERS["e8_josephine"])
    
    # 2. Автономные монстры M7
    catalog.append(MONSTERS["m7_wind_lord"])
    catalog.append(MONSTERS["m7_black_dragon"])
    catalog.append(MONSTERS["m7_colossus"])
    catalog.append(MONSTERS["m7_ancient_terror"])
    
    # 3. Гараж T8
    catalog.append(REGULAR_TROOPS["s8_duellist"])
    catalog.append(REGULAR_TROOPS["g8_punisher"])
    catalog.append(REGULAR_TROOPS["s8_whitemane"])
    catalog.append(REGULAR_TROOPS["g8_smiter"])
    
    # 4. Гараж T9 (или замена на G7 при S8 Developing)
    if is_s8_dev:
        catalog.append(REGULAR_TROOPS["g7_infantry_sub"])
        catalog.append(REGULAR_TROOPS["g7_mounted_sub"])
    else:
        catalog.append(REGULAR_TROOPS["s9_duellist"])
        catalog.append(REGULAR_TROOPS["g9_punisher"])
        catalog.append(REGULAR_TROOPS["s9_whitemane"])
        catalog.append(REGULAR_TROOPS["g9_smiter"])
        
    # 5. Монстры M9
    catalog.append(MONSTERS["m9_kraken"])
    catalog.append(MONSTERS["m9_trickster"])
    
    # 6. Наемники T9 (Линия 7: специалисты -> гвардейцы -> существа)
    catalog.append(MERCENARIES_T9["merc_pounder"])
    catalog.append(MERCENARIES_T9["merc_galloper"])
    catalog.append(MERCENARIES_T9["merc_slavic_warrior"])
    catalog.append(MERCENARIES_T9["merc_quicksand"])
    catalog.append(MERCENARIES_T9["merc_wyvern"])
    catalog.append(MERCENARIES_T9["merc_warden"])
    
    # 7. Финальный ударный отряд (Superior Epic Monster Hunter)
    catalog.append(MERCENARIES_T9["merc_epic_hunter"])
    
    return catalog

def calculate_ladder(total_leadership: int, is_s8_dev: bool):
    """
    Расчет распределения войск:
    - Максимальная утилизация лидерства (99-100%)
    - Монотонное убывание Total HP
    - Округление монстров кратно 10
    """
    units = build_unit_catalog(is_s8_dev)
    garage_units = [u for u in units if u["is_garage"]]
    n_garage = len(garage_units)
    
    # Весовая кривая для распределения лидерства по гаражу сверху вниз
    weights_curve = [1.0 - (0.42 * (i / max(1, n_garage - 1))) for i in range(n_garage)]
    sum_curve = sum(weights_curve)
    
    target_lead_per_unit = {}
    for idx, u in enumerate(garage_units):
        target_lead_per_unit[u["name_key"]] = (weights_curve[idx] / sum_curve) * total_leadership

    results = []
    used_lead = 0
    prev_hp = float('inf')
    
    for unit in units:
        hp_unit = unit["hp"]
        w = unit["weight"]
        is_garage = unit["is_garage"]
        key = unit["name_key"]
        tier = unit.get("tier", "")
        
        if is_garage:
            alloc_l = target_lead_per_unit[key]
            count = max(1, int(alloc_l / w))
            
            # Контроль лимита лидерства
            if used_lead + (count * w) > total_leadership:
                count = max(1, (total_leadership - used_lead) // w)
                
            total_hp = count * hp_unit
            
            # Коррекция под строгую лесенку (Total HP < prev_hp)
            if total_hp >= prev_hp:
                safe_hp = prev_hp - max(1000, hp_unit)
                count = max(1, int(safe_hp / hp_unit))
                total_hp = count * hp_unit
                
            used_lead += count * w
        else:
            # Расчет для монстров и наемников (без расхода L)
            target_hp = prev_hp * 0.95
            count = max(1, int(target_hp / hp_unit))
            
            # Округление для монстров кратно 10
            if "tier" in unit and tier in ["M7", "M8", "M9"]:
                count = max(10, (count // 10) * 10)
                
            total_hp = count * hp_unit
            
            # Страховка монотонности
            if total_hp >= prev_hp:
                count = max(1, int((prev_hp - 1000) / hp_unit))
                if tier in ["M7", "M8", "M9"] and count >= 10:
                    count = (count // 10) * 10
                total_hp = count * hp_unit
                
        prev_hp = total_hp
        results.append({
            "name_key": key,
            "count": count,
            "is_garage": is_garage,
            "weight": w,
            "hp": hp_unit
        })

    # Добор остатка лидерства до 99.9-100%
    remaining_l = total_leadership - used_lead
    if remaining_l > 0:
        for r in results:
            if r["is_garage"] and r["weight"] > 0:
                add_units = remaining_l // r["weight"]
                if add_units > 0:
                    r["count"] += add_units
                    used_lead += add_units * r["weight"]
                    remaining_l -= add_units * r["weight"]
                    break

    return results, used_lead

def main():
    # Языковой селектор
    lang_map = {
        "ru": "Русский", "en": "English", "de": "Deutsch", "fr": "Français",
        "es": "Español", "it": "Italiano", "pl": "Polski", "tr": "Türkçe",
        "pt": "Português", "zh": "中文"
    }
    selected_lang = st.sidebar.selectbox("Language / Язык", options=list(lang_map.keys()), format_func=lambda x: lang_map[x])
    txt = TRANSLATIONS[selected_lang]
    
    st.title(txt["title"])
    st.caption(txt["subtitle"])
    st.sidebar.markdown("---")
    
    # Ввод параметров
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
        
        # Минималистичная таблица: только отряд и количество
        clean_table = []
        for r in march_plan:
            unit_name = txt.get(r["name_key"], r["name_key"])
            clean_table.append({
                txt["col_name"]: unit_name,
                txt["col_count"]: f"{r['count']:,}"
            })
            
        st.table(clean_table)
        
        # Индикатор расхода лидерства
        usage_pct = (used_leadership / total_leadership) * 100
        st.metric(
            label=txt["lead_used"],
            value=f"{used_leadership:,} / {total_leadership:,} ({usage_pct:.2f}%)"
        )

if __name__ == "__main__":
    main()
