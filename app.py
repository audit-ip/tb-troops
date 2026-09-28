import streamlit as st
import pandas as pd
import numpy as np

# ==============================================================================
# БАЗА ДАННЫХ ХАРАКТЕРИСТИК ЮНИТОВ
# ==============================================================================
DATABASE = {
    "garage_structure": [
        {"id": "e8_josephine", "tier": "E8", "hp": 91800, "weight": 10},
        {"id": "e9_josephine", "tier": "E9", "hp": 165300, "weight": 10},
        {"id": "s8_duellist", "tier": "S8", "hp": 9200, "weight": 1},
        {"slot": "melee"},
        {"id": "g8_punisher", "tier": "G8", "hp": 9200, "weight": 1},
        {"id": "g9_punisher", "tier": "G9", "hp": 16500, "weight": 1},
        {"id": "s8_legitimist", "tier": "S8", "hp": 9200, "weight": 1},
        {"id": "s8_whitemane", "tier": "S8", "hp": 18400, "weight": 2},
        {"id": "s8_lion", "tier": "S8", "hp": 183600, "weight": 20},
        {"slot": "ranged"},
        {"slot": "mounted"},
        {"slot": "flying"},
        {"id": "g8_purifier", "tier": "G8", "hp": 9200, "weight": 1},
        {"id": "g8_smiter", "tier": "G8", "hp": 18400, "weight": 2},
        {"id": "g8_corax", "tier": "G8", "hp": 183600, "weight": 20},
        {"id": "g9_purifier", "tier": "G9", "hp": 16500, "weight": 1},
        {"id": "g9_smiter", "tier": "G9", "hp": 33100, "weight": 2},
        {"id": "g9_corax", "tier": "G9", "hp": 330600, "weight": 20}
    ],
    "substitutions": {
        "s9": {
            "melee": {"id": "s9_duellist", "tier": "S9", "hp": 16500, "weight": 1},
            "ranged": {"id": "s9_legitimist", "tier": "S9", "hp": 16500, "weight": 1},
            "mounted": {"id": "s9_whitemane", "tier": "S9", "hp": 33100, "weight": 2},
            "flying": {"id": "s9_lion", "tier": "S9", "hp": 330600, "weight": 20}
        },
        "g7": {
            "melee": {"id": "g7_halberdier", "tier": "G7", "hp": 5100, "weight": 1},
            "ranged": {"id": "g7_arbalester", "tier": "G7", "hp": 5100, "weight": 1},
            "mounted": {"id": "g7_knight", "tier": "G7", "hp": 10200, "weight": 2},
            "flying": {"id": "g7_griffin", "tier": "G7", "hp": 102000, "weight": 20}
        }
    },
    "monsters_ordered": [
        {"id": "m9_kraken", "tier": "M9", "hp": 3630000},
        {"id": "m9_phoenix", "tier": "M9", "hp": 3570000},
        {"id": "m9_devastator", "tier": "M9", "hp": 3510000},
        {"id": "m9_trickster", "tier": "M9", "hp": 3450000},
        {"id": "m8_kraken", "tier": "M8", "hp": 2010000},
        {"id": "m8_phoenix", "tier": "M8", "hp": 1980000},
        {"id": "m8_devastator", "tier": "M8", "hp": 1950000},
        {"id": "m8_trickster", "tier": "M8", "hp": 1920000},
        {"id": "m7_wind_lord", "tier": "M7", "hp": 930000},
        {"id": "m7_dragon", "tier": "M7", "hp": 900000},
        {"id": "m7_colossus", "tier": "M7", "hp": 870000},
        {"id": "m7_terror", "tier": "M7", "hp": 840000}
    ],
    "mercenaries_ordered": [
        {"id": "merc_wyvern", "tier": "Merc", "hp": 2070000},
        {"id": "merc_warden", "tier": "Merc", "hp": 1410000},
        {"id": "merc_cannoneer", "tier": "Merc", "hp": 1320000},
        {"id": "merc_salamander", "tier": "Merc", "hp": 1230000},
        {"id": "merc_warregal", "tier": "Merc", "hp": 660000},
        {"id": "merc_jago", "tier": "Merc", "hp": 660000},
        {"id": "merc_ariel", "tier": "Merc", "hp": 330000},
        {"id": "merc_superior_hunter", "tier": "Merc", "hp": 75000},
        {"id": "merc_grove_warden", "tier": "Merc", "hp": 75000},
        {"id": "merc_quicksand", "tier": "Merc", "hp": 66000},
        {"id": "merc_galloper", "tier": "Merc", "hp": 66000},
        {"id": "merc_anteater", "tier": "Merc", "hp": 34200},
        {"id": "merc_chitinous", "tier": "Merc", "hp": 33600},
        {"id": "merc_highlander", "tier": "Merc", "hp": 33000},
        {"id": "merc_slavic", "tier": "Merc", "hp": 33000},
        {"id": "merc_pounder", "tier": "Merc", "hp": 33000},
        {"id": "merc_scarface", "tier": "Merc", "hp": 33000},
        {"id": "merc_wasp_man", "tier": "Merc", "hp": 32400},
        {"id": "merc_grim_stalker", "tier": "Merc", "hp": 31800},
        {"id": "merc_grace", "tier": "Merc", "hp": 16530}
    ]
}

# ==============================================================================
# СЛОВАРЬ ЛОКАЛИЗАЦИИ (10 ЯЗЫКОВ)
# ==============================================================================
LOCALES = {
    "ru": {
        "title": "Total Battle: Калькулятор марша",
        "lead_input": "Лидерство гаражных войск",
        "chk_no_s9": "Аккаунт без S9 (Замена на G7)",
        "btn_calc": "Рассчитать марш",
        "stat_used": "Использовано лидерства:",
        "stat_free": "Свободный остаток:",
        "col_tier": "Тир",
        "col_unit": "Отряд",
        "col_count": "Количество",
        "sec_garage": "Гаражные войска",
        "sec_monsters": "Монстры",
        "sec_mercs": "Наемники",
        "units": {
            "e8_josephine": "Josephine I", "e9_josephine": "Josephine II",
            "s8_duellist": "Дуэлянт I", "s8_legitimist": "Легитимист I", "s8_whitemane": "Белогривый I", "s8_lion": "Королевский Лев I",
            "s9_duellist": "Дуэлянт II", "s9_legitimist": "Легитимист II", "s9_whitemane": "Белогривый II", "s9_lion": "Королевский Лев II",
            "g8_punisher": "Каратель I", "g8_purifier": "Очиститель I", "g8_smiter": "Сокрушитель I", "g8_corax": "Коракс I",
            "g9_punisher": "Каратель II", "g9_purifier": "Очиститель II", "g9_smiter": "Сокрушитель II", "g9_corax": "Коракс II",
            "g7_halberdier": "Тяжелый Алебардщик VII", "g7_arbalester": "Тяжелый Арбалетчик VII", "g7_knight": "Рыцарь VII", "g7_griffin": "Боевой Грифон VII",
            "m9_kraken": "Кракен II", "m9_phoenix": "Огненный Феникс II", "m9_devastator": "Опустошитель II", "m9_trickster": "Обманщик II",
            "m8_kraken": "Кракен I", "m8_phoenix": "Огненный Феникс I", "m8_devastator": "Опустошитель I", "m8_trickster": "Обманщик I",
            "m7_wind_lord": "Повелитель Ветра", "m7_dragon": "Черный Дракон", "m7_colossus": "Разрушительный Колосс", "m7_terror": "Древний Ужас",
            "merc_wyvern": "Виверна T9", "merc_warden": "Страж", "merc_cannoneer": "Вечный Канонир", "merc_salamander": "Демоническая Саламандра",
            "merc_warregal": "Варрегал", "merc_jago": "Яго", "merc_ariel": "Ариэль", "merc_superior_hunter": "Superior Epic Monster Hunter",
            "merc_grove_warden": "Grove Warden", "merc_quicksand": "Плывун", "merc_galloper": "Скакун", "merc_anteater": "Combat Anteater Leader",
            "merc_chitinous": "Chitinous Defender Leader", "merc_highlander": "Горец", "merc_slavic": "Славянский Воин", "merc_pounder": "Дробитель",
            "merc_scarface": "Шрам", "merc_wasp_man": "Wasp-Man Leader", "merc_grim_stalker": "Grim Stalker Leader", "merc_grace": "Грейс"
        }
    },
    "en": {
        "title": "Total Battle: March Calculator", "lead_input": "Garage Leadership", "chk_no_s9": "Account without S9 (Substitute with G7)",
        "btn_calc": "Calculate March", "stat_used": "Leadership Used:", "stat_free": "Free Buffer:", "col_tier": "Tier", "col_unit": "Unit",
        "col_count": "Count", "sec_garage": "Garage Troops", "sec_monsters": "Monsters", "sec_mercs": "Mercenaries", "units": {}
    },
    "de": {
        "title": "Total Battle: Marsch-Rechner", "lead_input": "Garagen-Führung", "chk_no_s9": "Account ohne S9 (Ersatz durch G7)",
        "btn_calc": "Marsch Berechnen", "stat_used": "Führung genutzt:", "stat_free": "Freier Puffer:", "col_tier": "Rang", "col_unit": "Einheit",
        "col_count": "Menge", "sec_garage": "Garagentruppen", "sec_monsters": "Monster", "sec_mercs": "Söldner", "units": {}
    },
    "fr": {
        "title": "Total Battle: Calculateur de Marche", "lead_input": "Commandement Garage", "chk_no_s9": "Compte sans S9 (Remplacer par G7)",
        "btn_calc": "Calculer la marche", "stat_used": "Commandement utilisé:", "stat_free": "Buffer restant:", "col_tier": "Rang", "col_unit": "Unité",
        "col_count": "Quantité", "sec_garage": "Troupes Garage", "sec_monsters": "Monstres", "sec_mercs": "Mercenaires", "units": {}
    },
    "es": {
        "title": "Total Battle: Calculadora de Marcha", "lead_input": "Liderazgo de Garaje", "chk_no_s9": "Cuenta sin S9 (Sustituir por G7)",
        "btn_calc": "Calcular marcha", "stat_used": "Liderazgo usado:", "stat_free": "Margen libre:", "col_tier": "Rango", "col_unit": "Unidad",
        "col_count": "Cantidad", "sec_garage": "Tropas de Garaje", "sec_monsters": "Monstruos", "sec_mercs": "Mercenarios", "units": {}
    },
    "it": {
        "title": "Total Battle: Calcolatore Marcia", "lead_input": "Leadership Garage", "chk_no_s9": "Account senza S9 (Sostituisci con G7)",
        "btn_calc": "Calcola marcia", "stat_used": "Leadership usata:", "stat_free": "Buffer libero:", "col_tier": "Grado", "col_unit": "Unità",
        "col_count": "Quantità", "sec_garage": "Truppe Garage", "sec_monsters": "Mostri", "sec_mercs": "Mercenari", "units": {}
    },
    "pl": {
        "title": "Total Battle: Kalkulator Marszu", "lead_input": "Dowodzenie Garażu", "chk_no_s9": "Konto bez S9 (Zastąp przez G7)",
        "btn_calc": "Oblicz marsz", "stat_used": "Użyte dowodzenie:", "stat_free": "Wolny bufor:", "col_tier": "Ranga", "col_unit": "Jednostka",
        "col_count": "Ilość", "sec_garage": "Wojska Garażowe", "sec_monsters": "Potwory", "sec_mercs": "Najemnicy", "units": {}
    },
    "pt": {
        "title": "Total Battle: Calculadora de Marcha", "lead_input": "Liderança de Garagem", "chk_no_s9": "Conta sem S9 (Substituir por G7)",
        "btn_calc": "Calcular marcha", "stat_used": "Liderança usada:", "stat_free": "Margem livre:", "col_tier": "Nível", "col_unit": "Unidade",
        "col_count": "Quantidade", "sec_garage": "Tropas de Garagem", "sec_monsters": "Monstros", "sec_mercs": "Mercenários", "units": {}
    },
    "zh": {
        "title": "Total Battle: 行军阶梯计算器", "lead_input": "车库统率值", "chk_no_s9": "无S9账号（由G7替代）",
        "btn_calc": "计算行军配置", "stat_used": "已消耗统率:", "stat_free": "剩余缓冲:", "col_tier": "阶级", "col_unit": "兵种",
        "col_count": "数量", "sec_garage": "车库部队", "sec_monsters": "怪物", "sec_mercs": "雇佣兵", "units": {}
    },
    "vi": {
        "title": "Total Battle: Máy tính Hành quân", "lead_input": "Lãnh đạo Nhà lính", "chk_no_s9": "Tài khoản không có S9 (Thay bằng G7)",
        "btn_calc": "Tính toán", "stat_used": "Lãnh đạo đã dùng:", "stat_free": "Dung lượng trống:", "col_tier": "Bậc", "col_unit": "Đơn vị",
        "col_count": "Số lượng", "sec_garage": "Quân Nhà Lính", "sec_monsters": "Quái vật", "sec_mercs": "Lính đánh thuê", "units": {}
    }
}

# ==============================================================================
# UI ИНИЦИАЛИЗАЦИЯ
# ==============================================================================
st.set_page_config(page_title="Total Battle Calculator", layout="centered")

LANGUAGES = {
    "Русский": "ru", "English": "en", "Deutsch": "de", "Français": "fr",
    "Español": "es", "Italiano": "it", "Polski": "pl", "Português": "pt",
    "简体中文": "zh", "Tiếng Việt": "vi"
}

selected_lang_name = st.sidebar.selectbox("Language / Язык", list(LANGUAGES.keys()), index=0)
lang_code = LANGUAGES[selected_lang_name]
loc = LOCALES.get(lang_code, LOCALES["ru"])

st.title(loc["title"])

col1, col2 = st.columns(2)
with col1:
    user_leadership = st.number_input(loc["lead_input"], min_value=10000, max_value=500000000, value=1280000, step=10000)
with col2:
    st.write("")
    st.write("")
    use_g7_flag = st.checkbox(loc["chk_no_s9"], value=False)

def get_name(unit_id):
    return loc["units"].get(unit_id) or LOCALES["ru"]["units"].get(unit_id, unit_id)

# ==============================================================================
# ВЫЧИСЛИТЕЛЬНЫЙ АЛГОРИТМ
# ==============================================================================
if st.button(loc["btn_calc"], type="primary"):
    # 1. Построение массива гаража
    garage_roster = []
    sub_dict = DATABASE["substitutions"]["g7"] if use_g7_flag else DATABASE["substitutions"]["s9"]
    for row in DATABASE["garage_structure"]:
        if "slot" in row:
            garage_roster.append(sub_dict[row["slot"]])
        else:
            garage_roster.append(row)

    M = len(garage_roster)

    # 2. Поиск оптимального коэффициента K методом бинарного деления
    low_k, high_k, opt_k = 1.0, 1e12, 1.0
    for _ in range(50):
        mid_k = (low_k + high_k) / 2.0
        sum_lead = 0
        for i in range(M):
            target_hp = mid_k * (M - i)
            units = int(np.ceil(target_hp / garage_roster[i]["hp"]))
            sum_lead += units * garage_roster[i]["weight"]
        if sum_lead <= user_leadership:
            opt_k = mid_k
            low_k = mid_k
        else:
            high_k = mid_k

    # 3. Формирование гаражных ступеней снизу вверх
    garage_march = [None] * M
    accum_hp = 0.0
    for i in range(M - 1, -1, -1):
        target_hp = max(opt_k * (M - i), accum_hp + 1000.0)
        units = max(1, int(np.ceil(target_hp / garage_roster[i]["hp"])))
        total_hp = units * garage_roster[i]["hp"]
        if total_hp <= accum_hp:
            units = int(accum_hp // garage_roster[i]["hp"]) + 1
            total_hp = units * garage_roster[i]["hp"]
        
        garage_march[i] = {
            "section": loc["sec_garage"],
            "tier": garage_roster[i]["tier"],
            "name": get_name(garage_roster[i]["id"]),
            "count": units,
            "hp_per_unit": garage_roster[i]["hp"],
            "weight": garage_roster[i]["weight"],
            "total_hp": total_hp,
            "used_lead": units * garage_roster[i]["weight"]
        }
        accum_hp = total_hp

    total_used_lead = sum(x["used_lead"] for x in garage_march)
    free_buffer = user_leadership - total_used_lead
    pct_used = (total_used_lead / user_leadership) * 100.0
    pct_free = (free_buffer / user_leadership) * 100.0

    # 4. Расчет монстров (без квантования кратно 10, с плотным монотонным шагом)
    prev_hp_level = garage_march[-1]["total_hp"]
    monsters_march = []
    delta_step = max(500000.0, prev_hp_level * 0.005)

    for mon in DATABASE["monsters_ordered"]:
        target_hp = prev_hp_level - delta_step
        count = max(1, int(target_hp // mon["hp"]))
        total_hp = count * mon["hp"]
        
        # Коррекция строгого убывания
        while total_hp >= prev_hp_level and count > 1:
            count -= 1
            total_hp = count * mon["hp"]

        monsters_march.append({
            "section": loc["sec_monsters"],
            "tier": mon["tier"],
            "name": get_name(mon["id"]),
            "count": count,
            "hp_per_unit": mon["hp"],
            "weight": 0,
            "total_hp": total_hp,
            "used_lead": 0
        })
        prev_hp_level = total_hp

    # 5. Расчет наемников (полный реестр, продолжение лесенки)
    mercs_march = []
    for merc in DATABASE["mercenaries_ordered"]:
        target_hp = prev_hp_level - delta_step
        count = max(1, int(target_hp // merc["hp"]))
        total_hp = count * merc["hp"]

        while total_hp >= prev_hp_level and count > 1:
            count -= 1
            total_hp = count * merc["hp"]

        mercs_march.append({
            "section": loc["sec_mercs"],
            "tier": merc["tier"],
            "name": get_name(merc["id"]),
            "count": count,
            "hp_per_unit": merc["hp"],
            "weight": 0,
            "total_hp": total_hp,
            "used_lead": 0
        })
        prev_hp_level = total_hp

    full_march = garage_march + monsters_march + mercs_march

    # ==============================================================================
    # ВЫВОД ИНФОРМАЦИИ
    # ==============================================================================
    st.subheader(f"{loc['stat_used']} {total_used_lead:,} / {user_leadership:,} ({pct_used:.2f}%)")
    st.caption(f"{loc['stat_free']} {free_buffer:,} ({pct_free:.2f}%)")

    # Отображение только значимых колонок для пользователя
    display_rows = []
    for r in full_march:
        display_rows.append({
            loc["col_tier"]: r["tier"],
            loc["col_unit"]: r["name"],
            loc["col_count"]: f"{r['count']:,}"
        })

    st.dataframe(pd.DataFrame(display_rows), use_container_width=True, hide_index=True)

    # Генерация форматированного текста для буфера обмена
    clipboard_text = f"=== MARCH (Leadership: {user_leadership:,}) ===\n"
    current_sec = ""
    for r in full_march:
        if r["section"] != current_sec:
            current_sec = r["section"]
            clipboard_text += f"\n[ {current_sec} ]\n"
        clipboard_text += f"{r['tier']} {r['name']}: {r['count']:,}\n"

    st.text_area("Данные для копирования:", value=clipboard_text, height=220)
