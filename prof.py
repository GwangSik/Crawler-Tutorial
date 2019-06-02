from requests import get
from bs4 import BeautifulSoup, Comment
import pymongo
conn = pymongo.MongoClient('127.0.0.1', 27017)

db = conn.get_database('chatbot')
collection = db.get_collection('prof')

target_url1 = 'http://m.tu.ac.kr/tu/html/02_uni/uni_list.jsp#none'

with get(target_url1) as request:
    raw_html = request.text
    soup_obj = BeautifulSoup(raw_html, 'html.parser')

    # 주석처리 된 코드 제거
    for element in soup_obj(text=lambda text: isinstance(text, Comment)):
        element.extract()

    # ul태그 중 클래스 이름이 'menulist_3st' 인 태그 로드
    major_ul_list = soup_obj.select('ul.menulist_3st')

    # 과에 맞게 과 링크 저장
    # {'메카트로닉스공학부' : 'http://m.tu.ac.kr/mechas/index.jsp', '자동차공학부' : 'http://m.tu.ac.kr/automobile/index.jsp'}
    major_url_list = {}
    for major_ul in major_ul_list:
        # li 하위에 있는 a태그 로드
        major_li_list = major_ul.select('li>a')
        for major_li in major_li_list:
            major_url_list[major_li.text] = major_li.get('href').replace('/index.jsp', '')

major_url_key = major_url_list.keys()

for key in major_url_key:
    print(key)
    major_url = major_url_list[key]
    target_url2 = major_url + '/html/01_about/about_04.jsp'

    with get(target_url2) as request2:
        raw_html2 = request2.text
        soup_obj2 = BeautifulSoup(raw_html2, 'html.parser')
        prof_div_list = soup_obj2.select('div.prof_box')
        for prof_div in prof_div_list :
            prof_info = prof_div.select('ul>li')

            for info in prof_info :
                if str(info).find('name') >= 0 :
                    prof_name = info.text
                elif str(info).find('연구실') >= 0 :
                    prof_labs = info.text.replace('연구실 : ', '')
                elif  str(info).find('연락처') >= 0 :
                    prof_tel = info.text.replace('연락처 : ', '')

            collection.insert({'prof_major' : key, 'prof_name' : prof_name, 'prof_lab' : prof_labs, 'prof_tel' : prof_tel})
        input(target_url2)
        print('\n\n')
# print(str(count))
