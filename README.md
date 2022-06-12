# FirmClf

## 나이브 베이즈 분류기를 이용한 IT/통신기업 분류 프로젝트

### 1. 프로젝트 목표

* 기업 소개 텍스트를 바탕으로 해당 기업이 IT/통신 기업인지 판단하는 툴 구현
  * 기업 소개 정보 출처 (캐치)

<img width="500" alt="캐치 소개" src="https://user-images.githubusercontent.com/104886103/173222599-c72cf717-a27e-4664-adfc-d60fabd7fe34.PNG">

--------------------

### 2. 데이터 준비

<img width="500" alt="IT 기업 목록" src="https://user-images.githubusercontent.com/104886103/173222700-9853f1e5-3c5f-4354-a8cf-481c14f84b21.PNG">

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














