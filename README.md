# Foreign Menu API

식당 메뉴 정보를 가져오고 관리하는 API 클라이언트입니다.

## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. 환경 변수 설정:
`.env.example` 파일을 `.env`로 복사하고 필요한 값들을 설정합니다:
```
# API Credentials
EX_STOR_CD=your_store_code
ACCESS_TOKEN=your_access_token
SEED_KEY=your_seed_key

# Business Location
BUSIPLCD=your_business_location_code

# API URLs
DEV_API_URL=https://devouterpos.ourhome.co.kr
PROD_API_URL=https://outerpos.ourhome.co.kr
```

## 사용 방법

1. 메뉴 정보 업데이트:
```bash
python crawl.py
```

2. 오늘의 메뉴 조회:
```bash
python menu_display.py
```

3. 메뉴 테스트:
```bash
python test_menu_queries.py
```
