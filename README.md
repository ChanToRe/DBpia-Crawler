## DBpia Crawler

### 소개
 * 누리 미디어에서 운영하고 있는 학술 데이터베이스 브랜드 'DBpia' 내의 논문정보를 크롤링하여 csv, xlsx로 저장하는 프로그램
 * 논문 제목, 저자, 학회, 학보, 볼륨, 날짜
 * 2022/01/25 기준 정상 작동

### 전략
 * Python의 대표적 크롤링 라이브러리인 Beautifulsoup과 Selenium을 사용
 * 'DBpia' 내에서 논문 키워드를 입력하면 해당 키워드가 들어간 논문들의 정보를 수집한다.
 * 크롬 드라이버 사용  [크롬 드라이버 다운로드](https://chromedriver.chromium.org/downloads)
 * 추후 초록 크롤링 기능을 추가할 것

### 설치
```bash
git clone https://github.com/ChanToRe/DBpia-Crawler.git
```
```python3
pip install pandas
pip install selenium
pip install BeautifulSoup
pip install tqdm
```

### 사용법
```python3
#작동
savename = "파일 저장명"
keyword = "검색어"
target_page = 페이지 수
driver = webdriver.Chrome('Chromedriver 주소')

#저장
csv_Name = "저장위치/{}.csv".format(savename)
xlsx_Name = "저장위치/{}.xlsx".format(savename)
```

### 참고
[Chanhee Kang](https://github.com/chanhee-kang/DBpia_crawler.git)
