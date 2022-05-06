from encodings import utf_8_sig
from selenium import webdriver
import pandas as pd
import time
import random
import cx_Oracle

a=pd.read_csv('title.csv',encoding='ANSI')
a=a['title'].values.tolist()
title_list=[]
for i in a:
    title_list.append(i.replace('.pdf',''))

#print(title_list)

driver = webdriver.Chrome('chromedriver.exe')
driver.maximize_window()#전체화면
df=pd.DataFrame()


#검색할 논문 제목 리스트
for j in title_list:

    Time_Limit=random.uniform(4,6)
    # 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
    driver.get('https://www.dbpia.co.kr/')
    driver.find_element_by_id('keyword').send_keys(j)#검색어 넣기
    time.sleep(Time_Limit)

    try:
        driver.find_element_by_xpath("//*[@id='bnHead']/div[3]/div/div[1]/div[1]/a").click()#검색 클릭
        time.sleep(10)
        url=str(driver.find_element_by_xpath("//*[@id='dev_search_list']/li[1]/div/div[2]/h5/a").get_attribute('href'))#맨위 링크얻기
        driver.get(url)
    except:
        continue

    #x창 뜰시
    try:
        time.sleep(Time_Limit)
        driver.find_element_by_xpath("//*[@id=\"#pub_modalOrganPop\"]").click()
    except:
        pass

    time.sleep(Time_Limit)
    
    driver.find_element_by_xpath("//*[@id='#pub_modalUsageChart']/span").click()#이용수 클릭
    

    #표로 넘어가기
    time.sleep(Time_Limit)
    driver.find_element_by_xpath("//*[@id='jcarouselControl']/p/a[2]").click()

    #표데이터 읽기
    time.sleep(Time_Limit)
    table=driver.find_element_by_xpath("//*[@id='pub_jcarousel']/ul/li[2]/div/table")#표 얻어오기
    tbody = table.find_element_by_tag_name("tbody")#데이터만 얻어오기

    year=[];month=[];use=[]
    for tr in tbody.find_elements_by_tag_name("tr"):#행 단위 접근
        a=tr.find_elements_by_tag_name("td")#열단위 접근
        year.append(a[0].text)
        month.append(a[1].text)
        use.append(a[2].text)

    t=[str(j)+'.pdf']*len(year)
    
    data_dic={}
    data_dic['title']=t
    data_dic['year']=year
    data_dic['month']=month
    data_dic['use']=use
    #print(data_dic)
    df = df.append(pd.DataFrame(data=data_dic), ignore_index=True)

    # print(t)
    # print(year)
    # print(month)
    # print(use)
    print(df)   

    time.sleep(Time_Limit)

df.to_csv('result2.csv')
