import sqlite3
import os
from datetime import datetime

def get_latest_menu():
    db_path = '/home/ubuntu/susong/ForeignMenu/data/menu.db'
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get the latest menu and its translations
    cursor.execute("""
        SELECT 
            m.id,
            m.main_menu as menu_kr,
            m.date,
            MAX(CASE WHEN mt.language = 'en' THEN mt.translated_name END) as menu_en,
            MAX(CASE WHEN mt.language = 'zh' THEN mt.translated_name END) as menu_zh,
            MAX(CASE WHEN mt.language = 'sv' THEN mt.translated_name END) as menu_sv
        FROM main_menu m
        LEFT JOIN menu_translations mt ON m.id = mt.menu_id
        WHERE m.meal_type = '중식'
        GROUP BY m.id
        ORDER BY m.date DESC, m.created_at DESC
        LIMIT 1
    """)
    
    result = cursor.fetchone()
    
    if result:
        menu_id, kr, date, en, zh, sv = result
        print(f"\nLatest lunch menu translations (ID: {menu_id}, Date: {date}):")
        print(f"한국어: {kr}")
        print(f"English: {en}")
        print(f"中文: {zh}")
        print(f"Svenska: {sv}")
    else:
        print("No menu data found")
    
    conn.close()

if __name__ == "__main__":
    get_latest_menu()
