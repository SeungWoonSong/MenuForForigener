import sqlite3
from typing import Dict, List, Any
import json
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

class MenuDatabase:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or os.getenv('DB_PATH', 'menu_data.db')
        self.init_database()

    def init_database(self):
        """Initialize database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 메인 메뉴 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS main_menu (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    meal_type TEXT,  -- 중식/석식
                    meal_time TEXT,  -- 시간대 (예: 1120~1300)
                    corner TEXT,     -- 코너 정보
                    corner_name TEXT,-- 코너 이름
                    main_menu TEXT,  -- 메인 메뉴 이름
                    menu_code TEXT,  -- 메뉴 코드
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(date, meal_type, corner)
                )
            ''')
            
            # 부가 메뉴 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sub_menu (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    main_menu_id INTEGER,
                    menu_name TEXT,
                    FOREIGN KEY (main_menu_id) REFERENCES main_menu(id)
                )
            ''')
            
            conn.commit()

    def insert_menu_data(self, menu_data: Dict[str, Any]) -> bool:
        """
        메뉴 데이터를 데이터베이스에 삽입
        이미 존재하는 데이터는 건너뜀
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 메인 메뉴 정보 삽입
                cursor.execute('''
                    INSERT OR IGNORE INTO main_menu 
                    (date, meal_type, meal_time, corner, corner_name, main_menu, menu_code)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    menu_data['OFFERDT'],
                    menu_data['MEALCLASS_NM'],
                    f"{menu_data['FR_TM']}~{menu_data['TO_TM']}",
                    menu_data['CORNER'],
                    menu_data['CORNERNM'],
                    menu_data['MENUNM'],
                    menu_data['MENU']
                ))
                
                # 방금 삽입한 메인 메뉴의 ID 가져오기
                main_menu_id = cursor.lastrowid
                
                # 부가 메뉴가 있고 새로운 메인 메뉴가 삽입된 경우에만 부가 메뉴 삽입
                if main_menu_id and menu_data.get('SUB_MENU_INFO'):
                    for sub_menu in menu_data['SUB_MENU_INFO']:
                        if sub_menu.get('MENUNM'):  # None이 아닌 경우에만 삽입
                            cursor.execute('''
                                INSERT INTO sub_menu (main_menu_id, menu_name)
                                VALUES (?, ?)
                            ''', (main_menu_id, sub_menu['MENUNM']))
                
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            print(f"데이터베이스 오류: {str(e)}")
            return False

    def get_menu_by_date(self, date: str) -> Dict[str, List[Dict[str, Any]]]:
        """특정 날짜의 메뉴 정보를 조회"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            result = {"중식": [], "석식": []}
            
            # 메인 메뉴와 부가 메뉴 조회
            cursor.execute('''
                SELECT m.*, GROUP_CONCAT(s.menu_name, '|') as sub_menus
                FROM main_menu m
                LEFT JOIN sub_menu s ON m.id = s.main_menu_id
                WHERE m.date = ?
                GROUP BY m.id
                ORDER BY m.meal_type, m.corner
            ''', (date,))
            
            for row in cursor.fetchall():
                menu_item = dict(row)
                # 부가 메뉴 리스트로 변환
                sub_menus = menu_item.pop('sub_menus')
                menu_item['sub_menus'] = sub_menus.split('|') if sub_menus else []
                
                result[menu_item['meal_type']].append(menu_item)
            
            return result

    def get_latest_menu_date(self) -> str:
        """가장 최근 메뉴 날짜 조회"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT MAX(date) FROM main_menu')
            return cursor.fetchone()[0] or ''
