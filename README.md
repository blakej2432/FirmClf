# FirmClf

## 나이브 베이즈 분류기를 이용한 IT/통신기업 분류 프로젝트

### 1. 프로젝트 목표

* 기업 소개 텍스트를 바탕으로 해당 기업이 IT/통신 기업인지 판단하는 툴 구현
  * 기업 소개 정보 출처 (캐치)

<img width="500" alt="캐치 소개" src="https://user-images.githubusercontent.com/104886103/173222599-c72cf717-a27e-4664-adfc-d60fabd7fe34.PNG">

--------------------

### 2. 데이터 준비

<img width="550" alt="IT 기업 목록" src="https://user-images.githubusercontent.com/104886103/173228705-1ac81390-d8d7-4f9c-9800-4a98663e1420.PNG">


<img width="576" alt="KT" src="https://user-images.githubusercontent.com/104886103/173222708-e07d0fb8-b146-460c-b44b-4b7a81fe6f6d.PNG">

__수집 기업 수 - IT/통신 : 76개 , 타업종 : 77개__

__나이브 베이즈 학습용 Document(Sentence) 수 - IT/통신 : 374개, 타업종 : 515개__  

#

* Document 빈출 단어 워드클라우드 시각화

* IT/통신 기업 키워드

<img width="350" alt="그림1" src="https://user-images.githubusercontent.com/104886103/173222997-6032605c-e7fb-48fc-8318-d3f87ff456ca.png">

* 타업종 기업 키워드

<img width="350" alt="그림2" src="https://user-images.githubusercontent.com/104886103/173223016-a946f818-0532-4001-8e82-3993f2975d9c.png">

--------------------

### 3. 데이터분석

* 나이브 베이즈 모델 형성

```python
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
```

__정확도 약 86% -> 86%의 확률로 IT/통신과 타업종 기업을 정확히 분류__  

#

* 혼동행렬로 결과 확인

<img width="350" alt="cb1" src="https://user-images.githubusercontent.com/104886103/173223223-922354fa-6473-44ef-9a9d-97351e0ecd87.png">

------------------------------

### 4. 평가전개

* 정확도 86%의 나이브 베이즈 분류기 생성 -> 기업 분류 판단

* 보완점 : 
```python

x_test = cv.transform(Series(' '.join(okt_pos('''아이티윌은 창업 이래 IT 인재양성에 전념해 왔습니다.
현재 IT 분야의 국비지원 과정과 직업상담, 직업알선 등의 종합 서비스를 제공하고 있으며,
전문 취업 지원팀을 운영하여 1:1 맞춤 취업컨설팅을 진행하고 있습니다.
훌륭한 인재를 필요로 하는 기업과 IT 전문인으로서 직업을 갖고자 하는 분들에게
좋은 안내자가 되기 위해 더욱 노력하겠습니다.'''))))
x_test.toarray()
cv.inverse_transform(x_test)
nb.predict(x_test)
```

__'IT'를 가르치는 '교육'업체의 경우, 기업 소개를 입력하면 타업종이 아닌 IT/통신 기업으로 분류하는 오류 존재__

__IT와 타업종이 아닌 9종 전체 기업분류로 분류 학습을 시행하면 정확도를 높일 것으로 기대 됨__










