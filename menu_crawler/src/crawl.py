import requests
import datetime
import json
from typing import Dict, Any
from db_manager import MenuDatabase
from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

def generate_ourhomekey(senddttm: str, ex_stor_cd: int, seed_key: int) -> int:
    """Generate OURHOMEKEY based on time information and store code."""
    year = int(senddttm[:4])
    month = int(senddttm[4:6])
    day = int(senddttm[6:8])
    time_part = senddttm[8:14]
    
    time_multiplier = int(f"{time_part[5]}{time_part[3]}{time_part[1]}")

    return (
        (100 - (year // 100)) +  
        (100 - (year % 100)) +   
        (100 - month) +          
        (100 - day) * time_multiplier +  
        ex_stor_cd +             
        seed_key                 
    )

def format_menu_item(menu: Dict[str, Any]) -> str:
    """Format a single menu item into a readable string."""
    output = []
    output.append(f"\n[{menu['OFFERDT']} - {menu['MEALCLASS_NM']}]")
    output.append(f"시간: {menu['FR_TM']}~{menu['TO_TM']}")
    output.append(f"코너: {menu['CORNERNM']}")
    output.append(f"메인메뉴: {menu['MENUNM']}")
    
    if menu.get("SUB_MENU_INFO"):
        output.append("부가메뉴:")
        for sub_menu in menu["SUB_MENU_INFO"]:
            if sub_menu.get('MENUNM'):  # Only add if MENUNM exists and is not None
                output.append(f"  - {sub_menu['MENUNM']}")
                
    return "\n".join(output)

def get_menu_info(test_mode: bool = True) -> Dict[str, Any]:
    """Fetch menu information from the API and return the result."""
    # Get environment variables
    EX_STOR_CD = int(os.getenv('EX_STOR_CD', '1010'))
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', '')
    SEED_KEY = int(os.getenv('SEED_KEY', '62'))
    BUSIPLCD = os.getenv('BUSIPLCD', 'FAN10')
    
    # Get API URL from environment
    base_url = os.getenv('DEV_API_URL') if test_mode else os.getenv('PROD_API_URL')
    if not base_url:
        raise ValueError("API URL not found in environment variables")
    
    url = f"{base_url}/Ex/Stor/MenuInfo"
    
    current_datetime = datetime.datetime.now()
    senddttm = current_datetime.strftime("%Y%m%d%H%M%S")
    
    # Generate API request data
    ourhomekey = generate_ourhomekey(senddttm, EX_STOR_CD, SEED_KEY)
    
    request_data = {
        "EX_STOR_INFO": {
            "EX_STOR_CD": str(EX_STOR_CD),
            "SENDDTTM": senddttm,
            "ACCESS_TOKEN": ACCESS_TOKEN,
            "OURHOMEKEY": str(ourhomekey)
        },
        "REQ_PARAMS": {
            "GUBUN": "EX_STOR_WEEKEND_MENU_S1",
            "BUSIPLCD": BUSIPLCD,
            "FR_DT": current_datetime.strftime("%Y%m%d")
        }
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, json=request_data)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("return") == "1":
            return result
        else:
            print(f"API 오류: {result.get('errmsg', '알 수 없는 오류')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"요청 중 오류 발생: {str(e)}")
    except json.JSONDecodeError:
        print("응답 데이터 파싱 오류")
    except Exception as e:
        print(f"예상치 못한 오류: {str(e)}")

def update_menu_database():
    """메뉴 정보를 가져와서 데이터베이스에 업데이트"""
    db = MenuDatabase()
    
    result = get_menu_info(test_mode=False)

    if not result:
        return
    
    success_count = 0
    for menu in result.get("list", []):
        if db.insert_menu_data(menu):
            success_count += 1
    
    print(f"데이터베이스 업데이트 완료: {success_count}개 메뉴 추가/업데이트됨")

def display_menu_from_db(date: str = None):
    """데이터베이스에서 메뉴 정보를 가져와서 표시"""
    db = MenuDatabase()
    
    if not date:
        date = datetime.datetime.now().strftime("%Y%m%d")
    
    menu_data = db.get_menu_by_date(date)
    
    for meal_type, menus in menu_data.items():
        if menus:
            print(f"\n=== {date} {meal_type} ===")
            for menu in menus:
                print(f"\n[{menu['corner_name']}]")
                print(f"메인메뉴: {menu['main_menu']}")
                if menu['sub_menus']:
                    print("부가메뉴:")
                    for sub_menu in menu['sub_menus']:
                        print(f"  - {sub_menu}")

if __name__ == "__main__":
    update_menu_database()
    
    today = datetime.datetime.now().strftime("%Y%m%d")
    display_menu_from_db(today)