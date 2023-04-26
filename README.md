# level1_bookratingprediction-recsys-07
<img src="https://user-images.githubusercontent.com/54920378/234452430-e1afaf0a-24a9-4598-bc97-d392a5892624.png">
일반적으로 책 한 권은 원고지 기준 800~1000매 정도 되는 분량을 가지고 있습니다.  

<br /> 
뉴스기사나 짧은 러닝 타임의 동영상처럼 간결하게 콘텐츠를 즐길 수 있는 ‘숏폼 콘텐츠’는 소비자들이 부담 없이 쉽게 선택할 수 있지만, 책 한권을 모두 읽기 위해서는 보다 긴 물리적인 시간이 필요합니다. 또한 소비자 입장에서는 제목, 저자, 표지, 카테고리 등 한정된 정보로 각자가 콘텐츠를 유추하고 구매 유무를 결정해야 하기 때문에 상대적으로 선택에 더욱 신중을 가하게 됩니다.  

<br /> 
해당 경진대회는 이러한 소비자들의 책 구매 결정에 대한 도움을 주기 위한 개인화된 상품 추천 대회입니다.

<br /> 
책과 관련된 정보와 소비자의 정보, 그리고 소비자가 실제로 부여한 평점, 총 3가지의 데이터 셋(users.csv, books.csv, train_ratings.csv)을 활용하여 이번 대회에서는 각 사용자가 주어진 책에 대해 얼마나 평점을 부여할지에 대해 예측하게 됩니다.

<br /> 

# Contributors
| <img src="https://user-images.githubusercontent.com/54920378/234445940-62c40bf9-793e-4961-82c0-0154641ddccb.png" width=200> | <img src="https://user-images.githubusercontent.com/54920378/234445810-920b34cc-8c3f-411e-980d-3f48d754bc82.png" width=200> | <img src="https://user-images.githubusercontent.com/54920378/234445975-9d02a616-ae78-4bca-9e9e-f0962748c666.png" width=200> | <img src="https://user-images.githubusercontent.com/54920378/234446009-f6bf5790-f164-4c63-a6fb-293dd0ff258b.png" width=200> | 
| :-------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------: | 
|                                           [강은비](https://github.com/ebbbi)                                            |                                           [김철현](https://github.com/Risk-boy)                                            |                                            [이한정](https://github.com/leehanjeong)                                            |                                         [최민수](https://github.com/MSGitt)                                          |                    
EDA, 데이터 전처리, LGBM 최적화 | EDA, 데이터 전처리, CatBoost 모델 최적화 | EDA, 데이터 전처리 | EDA, 데이터 전처리, CatBoost 모델 설계 및 최적화, 팀 목표 설정 및 스케줄 관리 |  

<br /> 

# Project architecture
정리 후 작성
```
예시
├─src
	├─data
	├─ensembles
	├─models
	├─utils.py
├─main.py
├─ensemble.py
├─requirements.txt
```
<br /> 

# Environment Requirements
[requirements.txt](https://github.com/boostcampaitech5/level1_bookratingprediction-recsys-07/blob/main/requirements.txt) 참조

<br /> 

# Model Architecture
### Catboost
● 범주형 변수에 강력한 성능을 보이는 모델  
● Ordered boosting  
● Random permutation  
● Categorical feature combination 

<br />

### LightGBM
● 범주형 변수가 많은 데이터에서 특히 높은 성능을 보임  
● gradient 가 가장 큰 노드부터 분할하는 leaf-wise 방식을 사용해 빠른 속도로 학습 가능  
● Category 형 피처의 자동 변환 및 최적 분할 가능

<br />

### Ensemble
Catboost v1 : Catboost v2 : LigtGBM = 8 : 1 : 1
<br /> 

# Execute
정리 후 작성
1. Setup
```
git clone https://github.com/boostcampaitech5/level1_bookratingprediction-recsys-07.git
pip install -r requirements.txt
```
2. Preprocess data  
```
```
3. Train
```
```
4. Inference
```
```
5. Ensemble
```
```

<br /> 

# Result
<img src="https://user-images.githubusercontent.com/54920378/234447340-7dac13b0-7984-48cd-b3fb-2f485bff7e3a.png">  

|리더보드| RMSE  |     순위     |
|:--------:|:------:|:----------:|
|public| 2.1088 |  **1위**   |
|private| 2.1061 | **1위** |

<br /> 
