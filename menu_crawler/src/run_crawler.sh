#!/bin/bash

# 스크립트 실행 시작 시간 기록
echo "=== Crawler Start: $(date) ===" >> /home/ubuntu/susong/ForeignMenu/menu_crawler/logs/crawler.log

# 작업 디렉토리로 이동
cd /home/ubuntu/susong/ForeignMenu/menu_crawler/src

# Python 가상환경 활성화 (가상환경을 사용하는 경우)
# source /path/to/your/venv/bin/activate

# 크롤러 실행 및 로그 저장
python3 crawl.py >> /home/ubuntu/susong/ForeignMenu/menu_crawler/logs/crawler.log 2>&1
CRAWL_EXIT_CODE=$?

# 크롤러 실행 결과 확인
if [ $CRAWL_EXIT_CODE -eq 0 ]; then
    echo "Crawling successful" >> /home/ubuntu/susong/ForeignMenu/menu_crawler/logs/crawler.log
    
    # 번역 서비스 실행
    python3 translate_service.py >> /home/ubuntu/susong/ForeignMenu/menu_crawler/logs/crawler.log 2>&1
    TRANSLATE_EXIT_CODE=$?
    
    if [ $TRANSLATE_EXIT_CODE -eq 0 ]; then
        echo "Translation successful" >> /home/ubuntu/susong/ForeignMenu/menu_crawler/logs/crawler.log
        
        # Slack 또는 이메일로 성공 알림 보내기 (선택사항)
        # curl -X POST -H 'Content-type: application/json' --data '{"text":"Menu crawler and translator completed successfully"}' YOUR_SLACK_WEBHOOK_URL
        
        echo "=== Crawler End Successfully: $(date) ===" >> /home/ubuntu/susong/ForeignMenu/menu_crawler/logs/crawler.log
        exit 0
    else
        echo "Translation failed with exit code $TRANSLATE_EXIT_CODE" >> /home/ubuntu/susong/ForeignMenu/menu_crawler/logs/crawler.log
        echo "=== Crawler End with Translation Error: $(date) ===" >> /home/ubuntu/susong/ForeignMenu/menu_crawler/logs/crawler.log
        exit 1
    fi
else
    echo "Crawling failed with exit code $CRAWL_EXIT_CODE" >> /home/ubuntu/susong/ForeignMenu/menu_crawler/logs/crawler.log
    echo "=== Crawler End with Crawling Error: $(date) ===" >> /home/ubuntu/susong/ForeignMenu/menu_crawler/logs/crawler.log
    exit 1
fi
