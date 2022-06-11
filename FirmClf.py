
############### 나이브베이즈 프로젝트 #################
from selenium import webdriver
import urllib
from urllib.request import urlopen
import time
from pandas import DataFrame, Series
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from konlpy.tag import Kkma
kkma = Kkma()

opt = Options()
opt.add_experimental_option('prefs',{'profile.default_content_setting_values.notifications':1})

# 캐치카페 기업 들어가기
url = 'https://www.catch.co.kr/Comp/CompMajor?flag=Search'
driver = webdriver.Chrome('c:/data/chromedriver.exe',options=opt)
driver.get(url)

# IT/통신 
btn = driver.find_element(By.XPATH, '//*[@id="Contents"]/div[2]/div[1]/dl[1]/dd/ul/li[6]/label')
action = ActionChains(driver)
action.move_to_element(btn).perform()
driver.find_element(By.XPATH, '//*[@id="Contents"]/div[2]/div[1]/dl[1]/dd/ul/li[6]/label').click()

# 검색
btn = driver.find_element(By.XPATH, '//*[@id="imgSearch"]')
action = ActionChains(driver)
action.move_to_element(btn).perform()
driver.find_element(By.XPATH, '//*[@id="imgSearch"]').click()



it_df = DataFrame()
name = []
# 페이징
for i in range(2,11):
    try:
        btn = driver.find_element(By.XPATH, '//*[@id="Contents"]/p[3]/a['+str(i)+']')
        action = ActionChains(driver)
        action.move_to_element(btn).perform()
        driver.find_element(By.XPATH, '//*[@id="Contents"]/p[3]/a['+str(i)+']').click()
        time.sleep(1)
        # 기업 선택
        for i in range(1,11):
            try:
                btn = driver.find_element(By.XPATH, '//*[@id="updates"]/tbody/tr['+str(i)+']/td[1]/dl/dt[2]/a')
                action = ActionChains(driver)
                action.move_to_element(btn).perform()
                driver.find_element(By.XPATH, '//*[@id="updates"]/tbody/tr['+str(i)+']/td[1]/dl/dt[2]/a').click()
                time.sleep(1)
            # 기업 소개란 수집
                html = driver.page_source
                soup = BeautifulSoup(html,'html.parser')
                # 기업 이름 수집
                name.append(soup.select_one('div.name > h2').text.strip())
                for i in soup.select('div.corp_bizexp2 > div.left > p'):
                    intro_txt = i.text.strip()
                    for i in kkma.sentences(intro_txt):
                        intro = i
                        field = 'IT/통신' 
                        it_df = it_df.append({'intro':intro,'field':field},ignore_index=True)  
                driver.back()
                time.sleep(2)
            except:
                print('정보없음')
    except:
        print('페이지 오류')
        driver.back()

# 타분야체크
driver.get(url)

for i in range(2,11):
    btn = driver.find_element(By.XPATH, '//*[@id="Contents"]/div[2]/div[1]/dl[1]/dd/ul/li['+str(i)+']/label')
    action = ActionChains(driver)
    action.move_to_element(btn).perform()
    driver.find_element(By.XPATH, '//*[@id="Contents"]/div[2]/div[1]/dl[1]/dd/ul/li['+str(i)+']/label').click()
driver.find_element(By.XPATH, '//*[@id="Contents"]/div[2]/div[1]/dl[1]/dd/ul/li[6]/label').click()


# 검색
btn = driver.find_element(By.XPATH, '//*[@id="imgSearch"]')
action = ActionChains(driver)
action.move_to_element(btn).perform()
driver.find_element(By.XPATH, '//*[@id="imgSearch"]').click()


# 페이징

for i in range(2,11):
    try:
        btn = driver.find_element(By.XPATH, '//*[@id="Contents"]/p[3]/a['+str(i)+']')
        action = ActionChains(driver)
        action.move_to_element(btn).perform()
        driver.find_element(By.XPATH, '//*[@id="Contents"]/p[3]/a['+str(i)+']').click()
        time.sleep(1)
        # 기업 선택
        for i in range(1,11):
            try:
                btn = driver.find_element(By.XPATH, '//*[@id="updates"]/tbody/tr['+str(i)+']/td[1]/dl/dt[2]/a')
                action = ActionChains(driver)
                action.move_to_element(btn).perform()
                driver.find_element(By.XPATH, '//*[@id="updates"]/tbody/tr['+str(i)+']/td[1]/dl/dt[2]/a').click()
                time.sleep(1)
            # 기업 소개란 수집
                html = driver.page_source
                soup = BeautifulSoup(html,'html.parser')
                # 기업 이름 수집
                name.append(soup.select_one('div.name > h2').text.strip())
                for i in soup.select('div.corp_bizexp2 > div.left > p'):
                    intro_txt = i.text.strip()
                    for i in kkma.sentences(intro_txt):
                        intro = i
                        field = '타업종' 
                        it_df = it_df.append({'intro':intro,'field':field},ignore_index=True)
                driver.back()
                time.sleep(2)
            except:
                print('정보없음')
    except:
        print('페이지 오류')


it/통신 - 76, 374
타업종 - 77, 515
전체 - 153, 889

it_df.to_csv('c:/data/it_df.csv')


# 워드클라우드
# IT, 타업종 각각 워드클라우드 생성

import operator
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from pandas import DataFrame, Series
import re

k_stopwords = pd.read_csv('c:/data/k_stopwords.csv')
k_s = [i for i in k_stopwords.아]
k_s.append('아')

name = Series(name)
name = name.str.replace('홈페이지','')
name = [i for i in name]
stopwords = name + k_s

def okt_pos(arg):
    token_corpus =[]
    for i in okt.pos(arg):
        if i[1] in ['Noun','Adjective']:
            token_corpus.append(i[0])
    token_corpus = [x for x in token_corpus if len(x) >1]        
    return token_corpus


it_int = ' '.join(it_df.intro[:374])
etc_int = ' '.join(it_df.intro[374:])

cv = CountVectorizer(tokenizer=okt_pos,stop_words=stopwords)
cv_trans = cv.fit_transform(it_df.intro[:374])
cv.vocabulary_
cv.get_feature_names()
cv
df=pd.DataFrame(cv_trans.toarray(),columns=cv.get_feature_names())
df.sum(axis=0)

import matplotlib.pylab as plt
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname='c:/windows/fonts/HMKMMAG.TTF').get_name()
rc('font',family=font_name)
from wordcloud import WordCloud

w = WordCloud(font_path='c:/windows/fonts/HMKMMAG.TTF',
              background_color='white',
              width=900,height=500).generate_from_frequencies(dict(df.sum(axis=0))) 
plt.imshow(w)
plt.axis('off')

cv = CountVectorizer(tokenizer=okt_pos,stop_words=stopwords)
cv_trans = cv.fit_transform(it_df.intro[374:])
cv.vocabulary_
cv.get_feature_names()
cv
df=pd.DataFrame(cv_trans.toarray(),columns=cv.get_feature_names())
df.sum(axis=0)

w = WordCloud(font_path='c:/windows/fonts/HMKMMAG.TTF',
              background_color='white',
              width=900,height=500).generate_from_frequencies(dict(df.sum(axis=0))) 
plt.imshow(w)
plt.axis('off')


# 학습, 테스트 분류
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
from collections import Counter

x_train,x_test,y_train,y_test = train_test_split(it_df['intro'],it_df['field'],test_size=0.2)

cv = CountVectorizer(tokenizer=okt_pos,stop_words=stopwords) 
x_train = cv.fit_transform(x_train) 
cv.get_feature_names()
x_train.toarray()
x_test= cv.transform(x_test)
x_test.toarray()

nb = MultinomialNB()
nb.fit(x_train,y_train)

y_predict = nb.predict(x_test)
sum(y_predict == y_test)
accuracy_score(y_test,y_predict)

from sklearn.metrics import confusion_matrix, classification_report

confusion_matrix(y_test,y_predict)
print(classification_report(y_test,y_predict))

pd.crosstab(y_test,y_predict)


x_test = cv.transform(Series(' '.join(okt_pos('''아이티윌은 창업 이래 IT 인재양성에 전념해 왔습니다.
현재 IT 분야의 국비지원 과정과 직업상담, 직업알선 등의 종합 서비스를 제공하고 있으며,
전문 취업 지원팀을 운영하여 1:1 맞춤 취업컨설팅을 진행하고 있습니다.
훌륭한 인재를 필요로 하는 기업과 IT 전문인으로서 직업을 갖고자 하는 분들에게
좋은 안내자가 되기 위해 더욱 노력하겠습니다.'''))))
x_test.toarray()
cv.inverse_transform(x_test)
nb.predict(x_test)

import pickle
file = open('c:/data/nb.pkl','wb')
pickle.dump(nb,file)
file.close()

file = open('c:/data/nb.pkl','rb')
nb = pickle.load(file)
file.close()








