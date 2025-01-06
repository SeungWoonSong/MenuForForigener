# Menu For Foreigner

외국인을 위한 식당 메뉴 정보 시스템입니다.

## 프로젝트 구조

이 프로젝트는 세 개의 주요 컴포넌트로 구성되어 있습니다:

### 1. Menu Crawler (`/menu_crawler`)
- API에서 메뉴 정보를 가져와 데이터베이스에 저장
- 자동 업데이트 스케줄링
- 데이터베이스 관리

### 2. Menu Frontend (`/menu_frontend`)
- 메뉴 정보를 웹 페이지로 표시
- 반응형 웹 디자인
- AI 챗봇과의 상호작용 UI
- 다국어 지원

### 3. Menu Agent (`/menu_agent`)
- 메뉴 설명 AI 챗봇
- 알레르기 정보 제공
- 메뉴 추천
- 영양 정보 제공

## 설치 및 실행

각 컴포넌트별 설치 및 실행 방법은 해당 디렉토리의 README.md를 참조하세요.

### 전체 시스템 실행
1. Menu Crawler 설정 및 실행
```bash
cd menu_crawler
pip install -r requirements.txt
./src/update_menu.sh
```

2. Menu Frontend 실행
```bash
cd menu_frontend
npm install
npm start
```

3. Menu Agent 실행
```bash
cd menu_agent
pip install -r requirements.txt
python src/agent.py
```

## 기여하기

1. 이 저장소를 포크합니다.
2. 새로운 브랜치를 만듭니다.
3. 변경사항을 커밋합니다.
4. 브랜치에 푸시합니다.
5. Pull Request를 생성합니다.
