from datetime import datetime
from db_manager import MenuDatabase
from typing import Dict, List, Any
import textwrap

class MenuDisplay:
    def __init__(self):
        self.db = MenuDatabase()
        self.today = datetime.now().strftime("%Y%m%d")
        
    def _format_menu_item(self, menu: Dict[str, Any], indent: int = 0) -> str:
        """메뉴 항목을 보기 좋게 포맷팅"""
        indent_str = " " * indent
        output = []
        
        # 메인 메뉴 제목 (박스 스타일)
        title = f"┌{'─' * 50}┐"
        output.append(f"{indent_str}{title}")
        output.append(f"{indent_str}│ {menu['corner_name']:^48} │")
        output.append(f"{indent_str}└{'─' * 50}┘")
        
        # 메인 메뉴
        output.append(f"{indent_str}▶ 메인 메뉴: {menu['main_menu']}")
        
        # 부가 메뉴
        if menu['sub_menus']:
            output.append(f"{indent_str}▶ 부가 메뉴:")
            for sub in menu['sub_menus']:
                output.append(f"{indent_str}   • {sub}")
        
        # 제공 시간
        output.append(f"{indent_str}▶ 제공 시간: {menu['meal_time']}")
        output.append("")  # 빈 줄 추가
        
        return "\n".join(output)

    def display_today_lunch(self):
        """오늘의 점심 메뉴 표시"""
        menu_data = self.db.get_menu_by_date(self.today)
        lunch_menu = menu_data.get("중식", [])
        
        print("\n" + "=" * 60)
        print(f"📅 오늘({self.today}) 점심 메뉴")
        print("=" * 60)
        
        for menu in lunch_menu:
            print(self._format_menu_item(menu))

    def display_today_dinner(self):
        """오늘의 저녁 메뉴 표시"""
        menu_data = self.db.get_menu_by_date(self.today)
        dinner_menu = menu_data.get("석식", [])
        
        print("\n" + "=" * 60)
        print(f"📅 오늘({self.today}) 저녁 메뉴")
        print("=" * 60)
        
        for menu in dinner_menu:
            print(self._format_menu_item(menu))

    def display_today_corners(self):
        """오늘의 코너1, 코너2 메뉴 표시"""
        menu_data = self.db.get_menu_by_date(self.today)
        lunch_menu = menu_data.get("중식", [])
        
        corner1_menu = next((menu for menu in lunch_menu if menu['corner'] == 'A'), None)
        corner2_menu = next((menu for menu in lunch_menu if menu['corner'] == 'B'), None)
        
        print("\n" + "=" * 60)
        print(f"📅 오늘({self.today}) 코너 메뉴")
        print("=" * 60)
        
        if corner1_menu:
            print(self._format_menu_item(corner1_menu))
        if corner2_menu:
            print(self._format_menu_item(corner2_menu))

    def display_today_dessert(self):
        """오늘 중식의 후식 메뉴 표시"""
        menu_data = self.db.get_menu_by_date(self.today)
        lunch_menu = menu_data.get("중식", [])
        
        dessert_menu = next((menu for menu in lunch_menu if menu['corner'] == 'E'), None)
        
        print("\n" + "=" * 60)
        print(f"📅 오늘({self.today}) 후식 메뉴")
        print("=" * 60)
        
        if dessert_menu:
            print(self._format_menu_item(dessert_menu))

def main():
    display = MenuDisplay()
    
    # 모든 메뉴 정보 표시
    display.display_today_lunch()
    display.display_today_dinner()
    display.display_today_corners()
    display.display_today_dessert()

if __name__ == "__main__":
    main()
