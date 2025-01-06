# Menu Crawler

메뉴 정보를 API에서 가져와 데이터베이스에 저장하는 컴포넌트입니다.

## 구조
- `src/crawl.py`: API 호출 및 데이터 수집
- `src/db_manager.py`: 데이터베이스 관리
- `src/update_menu.sh`: 자동 업데이트 스크립트

## 설정
1. `.env.example`을 `.env`로 복사하고 필요한 값들을 설정합니다.
2. `pip install -r requirements.txt`로 필요한 패키지를 설치합니다.

## 실행
```bash
# 메뉴 정보 업데이트
./src/update_menu.sh
```
