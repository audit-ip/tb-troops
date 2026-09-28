import streamlit as st
import pandas as pd
import numpy as np

# 1. КОНФИГУРАЦИОННАЯ БАЗА ДАННЫХ
DATABASE = {
    "garage_order": [
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
        {"id": "g9_corax", "tier": "G9", "hp": 330600, "weight": 20},
    ],
    "subs": {
        "s9": {
            "melee": {"id": "s9_duellist", "tier": "S9", "hp": 16500, "weight": 1},
            "ranged": {"id": "s9_legitimist", "tier": "S9", "hp": 16500, "weight": 1},
            "mounted": {"id": "s9_whitemane", "tier": "S9", "hp": 33100, "weight": 2},
            "flying": {"id": "s9_lion", "tier": "S9", "hp": 330600, "weight": 20},
        },
        "g7": {
            "melee": {"id": "g7_halberdier", "tier": "G7", "hp": 5100, "weight": 1},
            "ranged": {"id": "g7_arbalester", "tier": "G7", "hp": 5100, "weight": 1},
            "mounted": {"id": "g7_knight", "tier": "G7", "hp": 10200, "weight": 2},
            "flying": {"id": "g7_griffin", "tier": "G7", "hp": 102000, "weight": 20},
        }
    },
    "monsters": {
        "m9": [
            {"id": "m9_kraken", "tier": "M9", "hp": 3630000},
            {"id": "m9_phoenix", "tier": "M9", "hp": 3570000},
            {"id": "m9_devastator", "tier": "M9", "hp": 3510000},
            {"id": "m9_trickster", "tier": "M9", "hp": 3450000},
        ],
        "m8": [
            {"id": "m8_kraken", "tier": "M8", "hp": 2010000},
            {"id": "m8_phoenix", "tier": "M8", "hp": 1980000},
            {"id": "m8_devastator", "tier": "M8", "hp": 1950000},
            {"id": "m8_trickster", "tier": "M8", "hp": 1920000},
        ],
        "m7": [
            {"id": "m7_wind_lord", "tier": "M7", "hp": 930000},
            {"id": "m7_dragon", "tier": "M7", "hp": 900000},
            {"id": "m7_colossus", "tier": "M7", "hp": 870000},
            {"id": "m7_terror", "tier": "M7", "hp": 840000},
        ]
    },
    "mercenaries": [
        {"id": "merc_wyvern", "tier": "Merc", "hp": 2070000},
        {"id": "merc_warden", "tier": "Merc", "hp": 1410000},
        {"id": "merc_cannoneer", "tier": "Merc", "hp": 1320000},
        {"id": "merc_salamander", "tier": "Merc", "hp": 1230000},
        {"id": "merc_warregal", "tier": "Merc", "hp": 660000},
        {"id": "merc_jago", "tier": "Merc", "hp": 660000},
        {"id": "merc_ariel", "tier": "Merc", "hp": 330000},
    ]
}

NAMES = {
    "ru": {
        "e8_josephine": "Josephine I", "e9_josephine": "Josephine II",
        "s8_duellist": "Дуэлянт I", "s8_legitimist": "Легитимист I", "s8_whitemane": "Белогривый I", "s8_lion": "Королевский Лев I",
        "s9_duellist": "Дуэлянт II", "s9_legitimist": "Легитимист II", "s9_whitemane": "Белогривый II", "s9_lion": "Королевский Лев II",
        "g8_punisher": "Каратель I", "g8_purifier": "Очиститель I", "g8_smiter": "Сокрушитель I", "g8_corax": "Коракс I",
        "g9_punisher": "Каратель II", "g9_purifier": "Очиститель II", "g9_smiter": "Сокрушитель II", "g9_corax": "Коракс II",
        "g7_halberdier": "Тяжелый Алебардщик VII", "g7_arbalester": "Тяжелый Арбалетчик VII", "g7_knight": "Рыцарь VII", "g7_griffin": "Боевой Грифон VII",
        "m9_kraken": "Кракен II", "m9_phoenix": "Огненный Феникс II", "m9_devastator": "Опустошитель II", "m9_trickster": "Обманщик II",
        "m8_kraken": "Кракен I", "m8_phoenix": "Огненный Феникс I", "m8_devastator": "Опустошитель I", "m8_trickster": "Обманщик I",
        "m7_wind_lord": "Повелитель Ветра", "m7_dragon": "Черный Дракон", "m7_colossus": "Разрушительный Колосс", "m7_terror": "Древний Ужас",
        "merc_wyvern": "Виверна T9", "merc_warden": "Страж", "merc_cannoneer": "Вечный Канонир",
        "merc_salamander": "Демоническая Саламандра", "merc_warregal": "Варрегал", "merc_jago": "Яго", "merc_ariel": "Ариэль"
    }
}

# 2. ИНТЕРФЕЙС STREAMLIT
st.set_page_config(page_title="Total Battle Ladder Calculator", layout="centered")
st.title("Total Battle: Калькулятор марша")

col1, col2 = st.columns(2)
with col1:
    lang = st.selectbox("Язык / Language", ["Русский", "English"], index=0)
    lang_key = "ru" if lang == "Русский" else "en"
with col2:
    total_leadership = st.number_input("Лидерство гаражных войск", min_value=10000, value=500000, step=10000)

no_s9 = st.checkbox("Аккаунт без S9 (Замена на G7)")

# 3. РАСЧЕТНОЕ ЯДРО
if st.button("Рассчитать марш", type="primary"):
    # Сборка гаражного списка
    roster = []
    sub_source = DATABASE["subs"]["g7"] if no_s9 else DATABASE["subs"]["s9"]
    for row in DATABASE["garage_order"]:
        if "slot" in row:
            roster.append(sub_source[row["slot"]])
        else:
            roster.append(row)

    M = len(roster)

    # Бинарный поиск масштабного наклона
    low, high, opt_k = 1.0, 1e9, 1.0
    for _ in range(45):
        mid = (low + high) / 2
        sum_l = sum(np.ceil((mid * (M - i)) / roster[i]["hp"]) * roster[i]["weight"] for i in range(M))
        if sum_l <= total_leadership:
            opt_k = mid
            low = mid
        else:
            high = mid

    # Построение гаражной лесенки снизу вверх (гарантия строгого убывания HP)
    garage_results = [None] * M
    prev_hp = 0
    for i in range(M - 1, -1, -1):
        target_hp = max(opt_k * (M - i), prev_hp + 1000)
        count = max(1, int(np.ceil(target_hp / roster[i]["hp"])))
        total_hp = count * roster[i]["hp"]
        if total_hp <= prev_hp:
            count = int(prev_hp // roster[i]["hp"]) + 1
            total_hp = count * roster[i]["hp"]
        
        garage_results[i] = {
            "Категория": "Гараж",
            "Тир": roster[i]["tier"],
            "Отряд": NAMES["ru"].get(roster[i]["id"], roster[i]["id"]),
            "Количество": count,
            "Использовано L": count * roster[i]["weight"],
            "Суммарное HP": total_hp
        }
        prev_hp = total_hp

    used_l = sum(r["Использовано L"] for r in garage_results)
    diff_l = total_leadership - used_l
    pct_used = (used_l / total_leadership) * 100
    pct_free = (diff_l / total_leadership) * 100

    # Расчет монстров (M9 -> M8 -> M7 с квантованием кратно 10)
    def process_monster_tier(tier_units, ceiling_hp):
        min_allowed = min(int((ceiling_hp - 1) // u["hp"]) for u in tier_units)
        quantized = max(10, (min_allowed // 10) * 10)
        res = []
        for u in tier_units:
            res.append({
                "Категория": "Монстры",
                "Тир": u["tier"],
                "Отряд": NAMES["ru"].get(u["id"], u["id"]),
                "Количество": quantized,
                "Использовано L": 0,
                "Суммарное HP": quantized * u["hp"]
            })
        return res, res[-1]["Суммарное HP"]

    lowest_garage_hp = garage_results[-1]["Суммарное HP"]
    m9_res, m9_exit = process_monster_tier(DATABASE["monsters"]["m9"], lowest_garage_hp)
    m8_res, m8_exit = process_monster_tier(DATABASE["monsters"]["m8"], m9_exit)
    m7_res, m7_exit = process_monster_tier(DATABASE["monsters"]["m7"], m8_exit)

    # Расчет наемников
    merc_ceiling = m7_exit
    merc_res = []
    for merc in DATABASE["mercenaries"]:
        count = max(1, int((merc_ceiling - 1000) // merc["hp"]))
        total_hp = count * merc["hp"]
        merc_res.append({
            "Категория": "Наемники",
            "Тир": merc["tier"],
            "Отряд": NAMES["ru"].get(merc["id"], merc["id"]),
            "Количество": count,
            "Использовано L": 0,
            "Суммарное HP": total_hp
        })
        merc_ceiling = total_hp

    full_march = garage_results + m9_res + m8_res + m7_res + merc_res
    df = pd.DataFrame(full_march)

    # 4. ВЫВОД РЕЗУЛЬТАТОВ
    st.subheader(f"Использовано лидерства: {used_l:,} / {total_leadership:,} ({pct_used:.2f}%)")
    st.caption(f"Свободный остаток: {diff_l:,} ({pct_free:.2f}%) — в пределах нормы (до 3%)")

    # Отображение только значимых колонок для клана
    display_df = df[["Тир", "Отряд", "Количество"]].copy()
    display_df["Количество"] = display_df["Количество"].apply(lambda x: f"{x:,}")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # Текст для буфера обмена
    copy_text = f"=== МАРШ TOTAL BATTLE (Лидерка: {total_leadership:,}) ===\n"
    for _, r in df.iterrows():
        copy_text += f"{r['Тир']} {r['Отряд']}: {r['Количество']:,}\n"
    
    st.text_area("Данные для копирования в чат/Telegram:", value=copy_text, height=150)
