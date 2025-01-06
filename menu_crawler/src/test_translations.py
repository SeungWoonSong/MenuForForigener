import requests
from datetime import datetime
import json
import sqlite3
from typing import Dict, Any
from tabulate import tabulate

def get_latest_menu_date() -> str:
    """Get the latest menu date from database"""
    db_path = "../../data/menu.db"  # 상위 디렉토리의 data 폴더
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT MAX(date) FROM main_menu')
            return cursor.fetchone()[0] or datetime.now().strftime("%Y%m%d")
    except sqlite3.Error:
        return datetime.now().strftime("%Y%m%d")

def test_menu_translations():
    """Test menu translations in different languages"""
    
    # API 기본 URL
    base_url = "http://localhost:8080"
    
    # 데이터베이스에서 최신 메뉴 날짜 가져오기
    menu_date = get_latest_menu_date()
    
    # 테스트할 언어들
    languages = ['ko', 'en', 'zh', 'sv']
    
    # 각 언어별 결과 저장
    results = {}
    
    print("\n=== 메뉴 번역 테스트 ===")
    print(f"테스트 날짜: {menu_date}")
    print("=" * 80 + "\n")
    
    # 각 언어별로 API 호출
    for lang in languages:
        url = f"{base_url}/api/menu/{menu_date}"
        if lang != 'ko':
            url += f"?lang={lang}"
            
        try:
            response = requests.get(url)
            response.raise_for_status()
            results[lang] = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {lang} translation: {str(e)}")
            continue
    
    # 결과 출력
    if results:
        # 중식과 석식 메뉴 각각 출력
        for meal_type in ["lunch", "dinner"]:
            meal_type_kr = "중식" if meal_type == "lunch" else "석식"
            print(f"\n[ {meal_type_kr} 메뉴 번역 결과 ]")
            print("-" * 80)
            
            # 테이블 데이터 준비
            table_data = []
            
            # 각 코너별 메뉴 처리
            corners = set()
            for lang_data in results.values():
                for menu in lang_data.get(meal_type, []):
                    corners.add(menu['corner_name'])
            
            for corner in sorted(corners):
                # 각 언어별 번역 추가
                row_data = {'코너': corner}
                
                for lang in languages:
                    lang_data = results.get(lang, {})
                    menu_list = lang_data.get(meal_type, [])
                    menu = next((m for m in menu_list if m['corner_name'] == corner), None)
                    
                    if menu:
                        menu_text = menu['main_menu']
                        if menu.get('description') and lang != 'ko':
                            menu_text += f"\n({menu['description']})"
                        row_data[lang] = menu_text
                    else:
                        row_data[lang] = 'N/A'
                
                table_data.append(row_data)
            
            # 테이블 출력
            if table_data:
                print(tabulate(
                    table_data,
                    headers={
                        '코너': '코너',
                        'ko': '한국어',
                        'en': '영어',
                        'zh': '중국어',
                        'sv': '스웨덴어'
                    },
                    tablefmt='grid',
                    colalign=('left', 'left', 'left', 'left', 'left')
                ))
            else:
                print(f"No {meal_type} menu data available")
            
            print("\n")

if __name__ == "__main__":
    test_menu_translations()
