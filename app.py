"""
Название: Total Battle March Calculator (Калькулятор марша)
Назначение: Интерактивный веб-инструмент для расчета монотонно убывающей лесенки
суммарного здоровья (Total HP) против эпических монстров.
"""

import streamlit as st

# --- КОНФИГУРАЦИЯ СТРАНИЦЫ ---
st.set_page_config(
    page_title="Total Battle March Calculator",
    page_icon="🛡️",
    layout="wide"
)

# --- БАЗА ДАННЫХ ЮНИТОВ И ХАРАКТЕРИСТИК (Endgame / TB Clan Portal) ---
# hp: базовое здоровье на 1 единицу
# weight: затраты лидерства (L)
# category: категория для сортировки внутри марша
UNIT_DB = {
    # 1. Инженеры / Осадные орудия (10 L)
    "e9_josephine": {"name_key": "e9_josephine", "hp": 165300, "weight": 10, "type": "siege"},
    "e8_josephine": {"name_key": "e8_josephine", "hp": 91800, "weight": 10, "type": "siege"},
    
    # 2. Автономные монстры M7–M9 (0 L)
    "m7_wind_lord": {"name_key": "m7_wind_lord", "hp": 930000, "weight": 0, "type": "monster"},
    "m7_black_dragon": {"name_key": "m7_black_dragon", "hp": 900000, "weight": 0, "type": "monster"},
    "m7_colossus": {"name_key": "m7_colossus", "hp": 870000, "weight": 0, "type": "monster"},
    "m7_ancient_terror": {"name_key": "m7_ancient_terror", "hp": 840000, "weight": 0, "type": "monster"},
    "m8_kraken": {"name_key": "m8_kraken", "hp": 2010000, "weight": 0, "type": "monster"},
    "m8_fire_phoenix": {"name_key": "m8_fire_phoenix", "hp": 1980000, "weight": 0, "type": "monster"},
    "m8_devastator": {"name_key": "m8_devastator", "hp": 1950000, "weight": 0, "type": "monster"},
    "m8_trickster": {"name_key": "m8_trickster", "hp": 1920000, "weight": 0, "type": "monster"},
    "m9_kraken": {"name_key": "m9_kraken", "hp": 3630000, "weight": 0, "type": "monster"},
    "m9_fire_phoenix": {"name_key": "m9_fire_phoenix", "hp": 3570000, "weight": 0, "type": "monster"},
    "m9_devastator": {"name_key": "m9_devastator", "hp": 3510000, "weight": 0, "type": "monster"},
    "m9_trickster": {"name_key": "m9_trickster", "hp": 3450000, "weight": 0, "type": "monster"},

    # 3. Регулярные войска T8 (1 L для пехоты/луков, 2 L для коней, 20 L для тяжелых)
    "s8_duellist": {"name_key": "s8_duellist", "hp": 9200, "weight": 1, "type": "garage"},
    "s8_legitimist": {"name_key": "s8_legitimist", "hp": 9200, "weight": 1, "type": "garage"},
    "s8_whitemane": {"name_key": "s8_whitemane", "hp": 18400, "weight": 2, "type": "garage"},
    "s8_royal_lion": {"name_key": "s8_royal_lion", "hp": 183600, "weight": 20, "type": "garage"},
    "g8_punisher": {"name_key": "g8_punisher", "hp": 9200, "weight": 1, "type": "garage"},
    "g8_purifier": {"name_key": "g8_purifier", "hp": 9200, "weight": 1, "type": "garage"},
    "g8_smiter": {"name_key": "g8_smiter", "hp": 18400, "weight": 2, "type": "garage"},
    "g8_corax": {"name_key": "g8_corax", "hp": 183600, "weight": 20, "type": "garage"},

    # 4. Регулярные войска T9 (Endgame S9 Core)
    "s9_duellist": {"name_key": "s9_duellist", "hp": 16500, "weight": 1, "type": "garage"},
    "s9_legitimist": {"name_key": "s9_legitimist", "hp": 16500, "weight": 1, "type": "garage"},
    "s9_whitemane": {"name_key": "s9_whitemane", "hp": 33100, "weight": 2, "type": "garage"},
    "s9_royal_lion": {"name_key": "s9_royal_lion", "hp": 330600, "weight": 20, "type": "garage"},
    "g9_punisher": {"name_key": "g9_punisher", "hp": 16500, "weight": 1, "type": "garage"},
    "g9_purifier": {"name_key": "g9_purifier", "hp": 16500, "weight": 1, "type": "garage"},
    "g9_smiter": {"name_key": "g9_smiter", "hp": 33100, "weight": 2, "type": "garage"},
    "g9_corax": {"name_key": "g9_corax", "hp": 330600, "weight": 20, "type": "garage"},

    # Замена для профиля S8 Developing (G7)
    "g7_infantry_sub": {"name_key": "g7_infantry_sub", "hp": 5200, "weight": 1, "type": "garage"},
    "g7_mounted_sub": {"name_key": "g7_mounted_sub", "hp": 10400, "weight": 2, "type": "garage"},

    # 5. Наемники T9 (Линия 7, 0 L гаража)
    # Специалисты
    "merc_pounder": {"name_key": "merc_pounder", "hp": 33000, "weight": 0, "type": "merc_spec"},
    "merc_galloper": {"name_key": "merc_galloper", "hp": 66000, "weight": 0, "type": "merc_spec"},
    "merc_scarface": {"name_key": "merc_scarface", "hp": 33000, "weight": 0, "type": "merc_spec"},
    "merc_jago": {"name_key": "merc_jago", "hp": 660000, "weight": 0, "type": "merc_spec"},
    # Гвардейцы
    "merc_slavic_warrior": {"name_key": "merc_slavic_warrior", "hp": 33000, "weight": 0, "type": "merc_guard"},
    "merc_quicksand": {"name_key": "merc_quicksand", "hp": 66000, "weight": 0, "type": "merc_guard"},
    "merc_highlander": {"name_key": "merc_highlander", "hp": 33000, "weight": 0, "type": "merc_guard"},
    "merc_warregal": {"name_key": "merc_warregal", "hp": 660000, "weight": 0, "type": "merc_guard"},
    # Тяжелые монстры и существа
    "merc_ariel": {"name_key": "merc_ariel", "hp": 330000, "weight": 0, "type": "merc_beast"},
    "merc_cannoneer": {"name_key": "merc_cannoneer", "hp": 1320000, "weight": 0, "type": "merc_beast"},
    "merc_salamander": {"name_key": "merc_salamander", "hp": 1230000, "weight": 0, "type": "merc_beast"},
    "merc_warden": {"name_key": "merc_warden", "hp": 1410000, "weight": 0, "type": "merc_beast"},
    "merc_wyvern": {"name_key": "merc_wyvern", "hp": 2070000, "weight": 0, "type": "merc_beast"},
    # Завершающий ударный отряд (внизу марша)
    "merc_epic_hunter": {"name_key": "merc_epic_hunter", "hp": 75000, "weight": 0, "type": "merc_strike"}
}

# --- МУЛЬТИЯЗЫЧНЫЙ СЛОВАРЬ (10 ЯЗЫКОВ) ---
TRANSLATIONS = {
    "ru": {
        "title": "Total Battle: Калькулятор марша",
        "subtitle": "Оптимизация лесенки здоровья против эпических монстров",
        "leadership_input": "Лидерство гаражных войск:",
        "s8_dev_label": "Профиль S8 Developing (замена S9 на G7)",
        "calc_button": "Рассчитать марш",
        "col_step": "№",
        "col_name": "Отряд / Слой",
        "col_count": "Количество",
        "col_hp": "HP за юнит",
        "col_total_hp": "Суммарный HP",
        "col_status": "Статус",
        "status_ok": "Корректно",
        "status_adjust": "Коррекция",
        "used_lead": "Использовано лидерства:",
        # Названия юнитов
        "e9_josephine": "Josephine II (E9)",
        "e8_josephine": "Josephine I (E8)",
        "m7_wind_lord": "Повелитель Ветра (M7)",
        "m7_black_dragon": "Черный Дракон (M7)",
        "m7_colossus": "Разрушительный Колосс (M7)",
        "m7_ancient_terror": "Древний Ужас (M7)",
        "m8_kraken": "Кракен I (M8)",
        "m8_fire_phoenix": "Огненный Феникс I (M8)",
        "m8_devastator": "Опустошитель I (M8)",
        "m8_trickster": "Обманщик I (M8)",
        "m9_kraken": "Кракен II (M9)",
        "m9_fire_phoenix": "Огненный Феникс II (M9)",
        "m9_devastator": "Опустошитель II (M9)",
        "m9_trickster": "Обманщик II (M9)",
        "s8_duellist": "Дуэлянт I (S8)",
        "s8_legitimist": "Легитимист I (S8)",
        "s8_whitemane": "Белогривый I (S8)",
        "s8_royal_lion": "Королевский Лев I (S8)",
        "g8_punisher": "Каратель I (G8)",
        "g8_purifier": "Очиститель I (G8)",
        "g8_smiter": "Сокрушитель I (G8)",
        "g8_corax": "Коракс I (G8)",
        "s9_duellist": "Дуэлянт II (S9)",
        "s9_legitimist": "Легитимист II (S9)",
        "s9_whitemane": "Белогривый II (S9)",
        "s9_royal_lion": "Королевский Лев II (S9)",
        "g9_punisher": "Каратель II (G9)",
        "g9_purifier": "Очиститель II (G9)",
        "g9_smiter": "Сокрушитель II (G9)",
        "g9_corax": "Коракс II (G9)",
        "g7_infantry_sub": "Пехота G7 (Адаптация S8)",
        "g7_mounted_sub": "Кавалерия G7 (Адаптация S8)",
        "merc_pounder": "Наемник Громила (Спец. Пехота)",
        "merc_galloper": "Наемник Иноходец (Спец. Кони)",
        "merc_scarface": "Наемник Шрамолицый (Спец. Луки)",
        "merc_jago": "Наемник Яго (Спец. Птицы)",
        "merc_slavic_warrior": "Наемник Славянский воин (Гвард. Пехота)",
        "merc_quicksand": "Наемник Плывун (Гвард. Кони)",
        "merc_highlander": "Наемник Горец (Гвард. Луки)",
        "merc_warregal": "Наемник Варрегал (Гвард. Птицы)",
        "merc_ariel": "Наемник Ариэль (Осада/Инженеры)",
        "merc_cannoneer": "Наемник Вечные бомбардиры (Артиллерия)",
        "merc_salamander": "Наемник Демоническая Саламандра",
        "merc_warden": "Наемник Страж",
        "merc_wyvern": "Наемник Виверна",
        "merc_epic_hunter": "Superior Epic Monster Hunter (+1000% Эпик)"
    },
    "en": {
        "title": "Total Battle: March Calculator",
        "subtitle": "Total HP Ladder Optimization against Epic Monsters",
        "leadership_input": "Garage Troop Leadership:",
        "s8_dev_label": "S8 Developing Profile (replace S9 with G7)",
        "calc_button": "Calculate March",
        "col_step": "Step",
        "col_name": "Unit / Layer",
        "col_count": "Count",
        "col_hp": "HP per Unit",
        "col_total_hp": "Total HP",
        "col_status": "Status",
        "status_ok": "Valid",
        "status_adjust": "Adjust",
        "used_lead": "Leadership Used:",
        "e9_josephine": "Josephine II (E9)",
        "e8_josephine": "Josephine I (E8)",
        "m7_wind_lord": "Wind Lord (M7)",
        "m7_black_dragon": "Black Dragon (M7)",
        "m7_colossus": "Destructive Colossus (M7)",
        "m7_ancient_terror": "Ancient Terror (M7)",
        "m8_kraken": "Kraken I (M8)",
        "m8_fire_phoenix": "Fire Phoenix I (M8)",
        "m8_devastator": "Devastator I (M8)",
        "m8_trickster": "Trickster I (M8)",
        "m9_kraken": "Kraken II (M9)",
        "m9_fire_phoenix": "Fire Phoenix II (M9)",
        "m9_devastator": "Devastator II (M9)",
        "m9_trickster": "Trickster II (M9)",
        "s8_duellist": "Duellist I (S8)",
        "s8_legitimist": "Legitimist I (S8)",
        "s8_whitemane": "Whitemane I (S8)",
        "s8_royal_lion": "Royal Lion I (S8)",
        "g8_punisher": "Punisher I (G8)",
        "g8_purifier": "Purifier I (G8)",
        "g8_smiter": "Smiter I (G8)",
        "g8_corax": "Corax I (G8)",
        "s9_duellist": "Duellist II (S9)",
        "s9_legitimist": "Legitimist II (S9)",
        "s9_whitemane": "Whitemane II (S9)",
        "s9_royal_lion": "Royal Lion II (S9)",
        "g9_punisher": "Punisher II (G9)",
        "g9_purifier": "Purifier II (G9)",
        "g9_smiter": "Smiter II (G9)",
        "g9_corax": "Corax II (G9)",
        "g7_infantry_sub": "G7 Infantry (S8 Adaptation)",
        "g7_mounted_sub": "G7 Cavalry (S8 Adaptation)",
        "merc_pounder": "Merc Pounder (Spec Infantry)",
        "merc_galloper": "Merc Galloper (Spec Cavalry)",
        "merc_scarface": "Merc Scarface (Spec Ranged)",
        "merc_jago": "Merc Jago (Spec Flying)",
        "merc_slavic_warrior": "Merc Slavic Warrior (Guard Infantry)",
        "merc_quicksand": "Merc Quicksand (Guard Cavalry)",
        "merc_highlander": "Merc Highlander (Guard Ranged)",
        "merc_warregal": "Merc Warregal (Guard Flying)",
        "merc_ariel": "Merc Ariel (Engineer)",
        "merc_cannoneer": "Merc Cannoneers (Artillery)",
        "merc_salamander": "Merc Salamander",
        "merc_warden": "Merc Warden",
        "merc_wyvern": "Merc Wyvern",
        "merc_epic_hunter": "Superior Epic Monster Hunter (+1000% Strike)"
    },
    "de": {
        "title": "Total Battle: Marschrechner",
        "subtitle": "Total HP Stufen-Optimierung gegen epische Monster",
        "leadership_input": "Führungskraft Garagentruppen:",
        "s8_dev_label": "S8 Developing Profil (S9 durch G7 ersetzen)",
        "calc_button": "Marsch berechnen",
        "col_step": "Stufe",
        "col_name": "Einheit / Schicht",
        "col_count": "Anzahl",
        "col_hp": "LP pro Einheit",
        "col_total_hp": "Gesamt-LP",
        "col_status": "Status",
        "status_ok": "Gültig",
        "status_adjust": "Anpassen",
        "used_lead": "Genutzte Führungskraft:",
        "e9_josephine": "Josephine II (E9)",
        "e8_josephine": "Josephine I (E8)",
        "m7_wind_lord": "Windlord (M7)",
        "m7_black_dragon": "Schwarzer Drache (M7)",
        "m7_colossus": "Verheerender Koloss (M7)",
        "m7_ancient_terror": "Uralter Schrecken (M7)",
        "m8_kraken": "Kraken I (M8)",
        "m8_fire_phoenix": "Feuerphönix I (M8)",
        "m8_devastator": "Verwüster I (M8)",
        "m8_trickster": "Trickser I (M8)",
        "m9_kraken": "Kraken II (M9)",
        "m9_fire_phoenix": "Feuerphönix II (M9)",
        "m9_devastator": "Verwüster II (M9)",
        "m9_trickster": "Trickser II (M9)",
        "s8_duellist": "Duellant I (S8)",
        "s8_legitimist": "Legitimist I (S8)",
        "s8_whitemane": "Weißmähne I (S8)",
        "s8_royal_lion": "Königslöwe I (S8)",
        "g8_punisher": "Bestrafer I (G8)",
        "g8_purifier": "Läuterer I (G8)",
        "g8_smiter": "Zerschmetterer I (G8)",
        "g8_corax": "Corax I (G8)",
        "s9_duellist": "Duellant II (S9)",
        "s9_legitimist": "Legitimist II (S9)",
        "s9_whitemane": "Weißmähne II (S9)",
        "s9_royal_lion": "Königslöwe II (S9)",
        "g9_punisher": "Bestrafer II (G9)",
        "g9_purifier": "Läuterer II (G9)",
        "g9_smiter": "Zerschmetterer II (G9)",
        "g9_corax": "Corax II (G9)",
        "g7_infantry_sub": "G7 Infanterie (S8 Ersatz)",
        "g7_mounted_sub": "G7 Kavallerie (S8 Ersatz)",
        "merc_pounder": "Söldner Stampfer (Spez. Infanterie)",
        "merc_galloper": "Söldner Galloper (Spez. Kavallerie)",
        "merc_scarface": "Söldner Narbengesicht (Spez. Fernkampf)",
        "merc_jago": "Söldner Jago (Spez. Fliegend)",
        "merc_slavic_warrior": "Söldner Slawischer Krieger (Garde Infanterie)",
        "merc_quicksand": "Söldner Treibsand (Garde Kavallerie)",
        "merc_highlander": "Söldner Highlander (Garde Fernkampf)",
        "merc_warregal": "Söldner Warregal (Garde Fliegend)",
        "merc_ariel": "Söldner Ariel (Belagerung)",
        "merc_cannoneer": "Söldner Kanoniere (Artillerie)",
        "merc_salamander": "Söldner Salamander",
        "merc_warden": "Söldner Wächter",
        "merc_wyvern": "Söldner Wyvern",
        "merc_epic_hunter": "Überragender Epischer Jäger (Angriff)"
    },
    "fr": {
        "title": "Total Battle: Calculateur de Marche", "subtitle": "Optimisation PV totaux", "leadership_input": "Commandement garage:",
        "s8_dev_label": "Profil S8 Developing (G7 au lieu de S9)", "calc_button": "Calculer la marche", "col_step": "N°",
        "col_name": "Unité / Rang", "col_count": "Quantité", "col_hp": "PV par unité", "col_total_hp": "PV totaux",
        "col_status": "Statut", "status_ok": "Valide", "status_adjust": "Ajuster", "used_lead": "Commandement utilisé:",
        "e9_josephine": "Joséphine II (E9)", "e8_josephine": "Joséphine I (E8)", "merc_epic_hunter": "Chasseur Épique Supérieur",
        "merc_wyvern": "Vouivre T9", "merc_warden": "Gardien T9"
    },
    "es": {
        "title": "Total Battle: Calculadora de Marcha", "subtitle": "Optimización PS totales", "leadership_input": "Liderazgo de garaje:",
        "s8_dev_label": "Perfil S8 Developing (G7 en vez de S9)", "calc_button": "Calcular marcha", "col_step": "N°",
        "col_name": "Unidad / Capa", "col_count": "Cantidad", "col_hp": "PS por unidad", "col_total_hp": "PS totales",
        "col_status": "Estado", "status_ok": "Correcto", "status_adjust": "Ajustar", "used_lead": "Liderazgo usado:",
        "e9_josephine": "Josephine II (E9)", "e8_josephine": "Josephine I (E8)", "merc_epic_hunter": "Cazador Épico Superior",
        "merc_wyvern": "Guiverno T9", "merc_warden": "Guardián T9"
    },
    "it": {
        "title": "Total Battle: Calcolatore di Marcia", "subtitle": "Ottimizzazione PV totali", "leadership_input": "Leadership del garage:",
        "s8_dev_label": "Profilo S8 Developing (G7 invece di S9)", "calc_button": "Calcola marcia", "col_step": "N°",
        "col_name": "Unità / Strato", "col_count": "Quantità", "col_hp": "PV per unità", "col_total_hp": "PV totali",
        "col_status": "Stato", "status_ok": "Valido", "status_adjust": "Correggere", "used_lead": "Leadership usata:",
        "e9_josephine": "Josephine II (E9)", "e8_josephine": "Josephine I (E8)", "merc_epic_hunter": "Cacciatore Epico Superiore",
        "merc_wyvern": "Viverna T9", "merc_warden": "Guardiano T9"
    },
    "pl": {
        "title": "Total Battle: Kalkulator Marszu", "subtitle": "Optymalizacja drabiny PŻ", "leadership_input": "Dowodzenie z garażu:",
        "s8_dev_label": "Profil S8 Developing (G7 zamiast S9)", "calc_button": "Oblicz marsz", "col_step": "N°",
        "col_name": "Jednostka / Warstwa", "col_count": "Liczba", "col_hp": "PŻ na jednostkę", "col_total_hp": "Łączne PŻ",
        "col_status": "Status", "status_ok": "Poprawne", "status_adjust": "Korekta", "used_lead": "Użyte dowodzenie:",
        "e9_josephine": "Josephine II (E9)", "e8_josephine": "Josephine I (E8)", "merc_epic_hunter": "Wyższy Łowca Epicki",
        "merc_wyvern": "Wywerna T9", "merc_warden": "Strażnik T9"
    },
    "tr": {
        "title": "Total Battle: Yürüyüş Hesaplayıcı", "subtitle": "Toplam Can optimizasyonu", "leadership_input": "Garaj Liderliği:",
        "s8_dev_label": "S8 Developing Profili (S9 yerine G7)", "calc_button": "Hesapla", "col_step": "No",
        "col_name": "Birlik / Katman", "col_count": "Adet", "col_hp": "Birim Başı Can", "col_total_hp": "Toplam Can",
        "col_status": "Durum", "status_ok": "Uygun", "status_adjust": "Ayarla", "used_lead": "Kullanılan Liderlik:",
        "e9_josephine": "Josephine II (E9)", "e8_josephine": "Josephine I (E8)", "merc_epic_hunter": "Üstün Epik Avcı",
        "merc_wyvern": "Wyvern T9", "merc_warden": "Muhafız T9"
    },
    "pt": {
        "title": "Total Battle: Calculadora de Marcha", "subtitle": "Otimização de Vida Total", "leadership_input": "Liderança de garagem:",
        "s8_dev_label": "Perfil S8 Developing (G7 em vez de S9)", "calc_button": "Calcular", "col_step": "N°",
        "col_name": "Unidade / Camada", "col_count": "Quantidade", "col_hp": "Vida por unidade", "col_total_hp": "Vida Total",
        "col_status": "Status", "status_ok": "Válido", "status_adjust": "Ajustar", "used_lead": "Liderança usada:",
        "e9_josephine": "Josephine II (E9)", "e8_josephine": "Josephine I (E8)", "merc_epic_hunter": "Caçador Épico Superior",
        "merc_wyvern": "Wyvern T9", "merc_warden": "Guardião T9"
    },
    "zh": {
        "title": "Total Battle: 行军计算器", "subtitle": "总生命值递减阶梯优化", "leadership_input": "车库部队统率力：",
        "s8_dev_label": "S8 Developing 配置（G7 替换 S9）", "calc_button": "计算行军", "col_step": "序号",
        "col_name": "部队 / 层级", "col_count": "数量", "col_hp": "单体生命值", "col_total_hp": "总生命值",
        "col_status": "状态", "status_ok": "正常", "status_adjust": "微调", "used_lead": "已用统率力：",
        "e9_josephine": "约瑟芬 II (E9)", "e8_josephine": "约瑟芬 I (E8)", "merc_epic_hunter": "高级史诗猎手（主力）",
        "merc_wyvern": "毒龙 T9", "merc_warden": "守望者 T9"
    }
}

# --- ОСНОВНАЯ ФУНКЦИЯ ПРИЛОЖЕНИЯ ---
def main():
    # Выбор языка в боковой панели
    lang_labels = {
        "ru": "Русский", "en": "English", "de": "Deutsch", "fr": "Français",
        "es": "Español", "it": "Italiano", "pl": "Polski", "tr": "Türkçe",
        "pt": "Português", "zh": "中文"
    }
    selected_lang = st.sidebar.selectbox("Language / Язык", options=list(lang_labels.keys()), format_func=lambda x: lang_labels[x])
    txt = TRANSLATIONS[selected_lang]

    st.title(txt["title"])
    st.caption(txt["subtitle"])

    st.sidebar.markdown("---")
    total_leadership = st.sidebar.number_input(
        txt["leadership_input"],
        min_value=10000,
        max_value=2000000,
        value=500000,
        step=10000
    )

    is_s8_dev = st.sidebar.checkbox(txt["s8_dev_label"], value=False)
    run_calc = st.sidebar.button(txt["calc_button"], type="primary")

    if run_calc:
        # План марша: Осада -> Монстры -> Гараж (с подменой S9 на G7 при S8 Dev) -> Наемники -> Ударный эпик
        march_sequence = [
            ("e9_josephine", 253),
            ("e8_josephine", 452),
            ("m7_wind_lord", 43),
            ("m7_black_dragon", 46),
            ("s8_duellist", 3904),
            ("g8_punisher", 3864),
            ("g7_infantry_sub" if is_s8_dev else "s9_duellist", 1344),
            ("g7_mounted_sub" if is_s8_dev else "g9_punisher", 1304),
            ("m9_kraken", 2),
            ("m9_trickster", 1),
            # Линия 7: Наемники (специалисты -> гвардейцы -> существа -> эпик)
            ("merc_pounder", 500),
            ("merc_slavic_warrior", 500),
            ("merc_wyvern", 10),
            ("merc_warden", 15),
            ("merc_epic_hunter", 100)
        ]

        table_rows = []
        lead_used = 0
        prev_hp = float('inf')

        for idx, (unit_key, count) in enumerate(march_sequence, 1):
            unit_info = UNIT_DB.get(unit_key, {"hp": 10000, "weight": 0, "name_key": unit_key})
            unit_hp = unit_info["hp"]
            total_hp = count * unit_hp
            lead_cost = count * unit_info["weight"]
            lead_used += lead_cost

            # Проверка монотонности лесенки Total HP
            is_valid = (total_hp < prev_hp) or (idx == 1)
            status_text = txt["status_ok"] if is_valid else txt["status_adjust"]
            prev_hp = total_hp

            # Отображение локализованного имени
            unit_name = txt.get(unit_info["name_key"], unit_key)

            table_rows.append({
                txt["col_step"]: idx,
                txt["col_name"]: unit_name,
                txt["col_count"]: f"{count:,}",
                txt["col_hp"]: f"{unit_hp:,}",
                txt["col_total_hp"]: f"{total_hp:,}",
                txt["col_status"]: f"✅ {status_text}" if is_valid else f"⚠️ {status_text}"
            })

        st.table(table_rows)
        st.metric(label=txt["used_lead"], value=f"{lead_used:,} / {total_leadership:,}")

if __name__ == "__main__":
    main()