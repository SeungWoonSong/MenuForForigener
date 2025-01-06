import unittest
from datetime import datetime
from db_manager import MenuDatabase

class TestMenuQueries(unittest.TestCase):
    def setUp(self):
        """테스트 시작 전 설정"""
        self.db = MenuDatabase()
        self.today = datetime.now().strftime("%Y%m%d")

    def test_get_lunch_menu(self):
        """특정 날짜의 점심 메뉴 조회 테스트"""
        date = "20250106"  # 테스트용 날짜
        menu_data = self.db.get_menu_by_date(date)
        lunch_menu = menu_data.get("중식", [])
        
        print("\n=== 특정 날짜(20250106)의 점심 메뉴 ===")
        for menu in lunch_menu:
            print(f"\n[{menu['corner_name']}]")
            print(f"메인메뉴: {menu['main_menu']}")
            if menu['sub_menus']:
                print("부가메뉴:")
                for sub in menu['sub_menus']:
                    print(f"  - {sub}")
        
        self.assertTrue(len(lunch_menu) > 0)

    def test_get_dinner_menu(self):
        """특정 날짜의 저녁 메뉴 조회 테스트"""
        date = "20250106"  # 테스트용 날짜
        menu_data = self.db.get_menu_by_date(date)
        dinner_menu = menu_data.get("석식", [])
        
        print("\n=== 특정 날짜(20250106)의 저녁 메뉴 ===")
        for menu in dinner_menu:
            print(f"\n[{menu['corner_name']}]")
            print(f"메인메뉴: {menu['main_menu']}")
            if menu['sub_menus']:
                print("부가메뉴:")
                for sub in menu['sub_menus']:
                    print(f"  - {sub}")
        
        self.assertTrue(len(dinner_menu) > 0)

    def test_get_today_lunch(self):
        """오늘 날짜의 점심 메뉴 조회 테스트"""
        menu_data = self.db.get_menu_by_date(self.today)
        lunch_menu = menu_data.get("중식", [])
        
        print(f"\n=== 오늘({self.today})의 점심 메뉴 ===")
        for menu in lunch_menu:
            print(f"\n[{menu['corner_name']}]")
            print(f"메인메뉴: {menu['main_menu']}")
            if menu['sub_menus']:
                print("부가메뉴:")
                for sub in menu['sub_menus']:
                    print(f"  - {sub}")
        
        self.assertTrue(len(lunch_menu) > 0)

    def test_get_today_corners(self):
        """오늘 날짜의 코너1, 코너2 메뉴 조회 테스트"""
        menu_data = self.db.get_menu_by_date(self.today)
        lunch_menu = menu_data.get("중식", [])
        
        corner1_menu = next((menu for menu in lunch_menu if menu['corner'] == 'A'), None)
        corner2_menu = next((menu for menu in lunch_menu if menu['corner'] == 'B'), None)
        
        print(f"\n=== 오늘({self.today})의 코너 메뉴 ===")
        
        if corner1_menu:
            print("\n[코너1]")
            print(f"메인메뉴: {corner1_menu['main_menu']}")
            if corner1_menu['sub_menus']:
                print("부가메뉴:")
                for sub in corner1_menu['sub_menus']:
                    print(f"  - {sub}")
        
        if corner2_menu:
            print("\n[코너2]")
            print(f"메인메뉴: {corner2_menu['main_menu']}")
            if corner2_menu['sub_menus']:
                print("부가메뉴:")
                for sub in corner2_menu['sub_menus']:
                    print(f"  - {sub}")
        
        self.assertIsNotNone(corner1_menu)
        self.assertIsNotNone(corner2_menu)

    def test_get_today_dessert(self):
        """오늘 중식의 후식 메뉴 조회 테스트"""
        menu_data = self.db.get_menu_by_date(self.today)
        lunch_menu = menu_data.get("중식", [])
        
        dessert_menu = next((menu for menu in lunch_menu if menu['corner'] == 'E'), None)
        
        print(f"\n=== 오늘({self.today})의 후식 메뉴 ===")
        if dessert_menu:
            print(f"메인메뉴: {dessert_menu['main_menu']}")
            if dessert_menu['sub_menus']:
                print("부가메뉴:")
                for sub in dessert_menu['sub_menus']:
                    print(f"  - {sub}")
        
        self.assertIsNotNone(dessert_menu)

if __name__ == '__main__':
    unittest.main(verbosity=2)
