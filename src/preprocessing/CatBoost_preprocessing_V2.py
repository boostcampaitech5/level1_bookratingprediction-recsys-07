#### Preprocessing ####
## DoyeonLim 님의 'https://github.com/DoyeonLim/level1_bookratingprediction_recsys-level1-recsys-12'를 참고하여 작성하였습니다

#### import module #### 
import pandas as pd 
import numpy as np
import re

#### user ####

path = './data/'
users = pd.read_csv(path + 'users.csv')

# age는 random sampling imputation
users.loc[users['age'].isna(), 'age'] = np.random.choice(users.loc[users['age'].notna(), 'age'], users['age'].isna().sum())

# string type으로 변환해주기
users['age'] = users['age'].astype('str')

### 미션1 코드 + a ###
users['location'] = users['location'].str.replace(r'[^0-9a-zA-Z:,]', '') 

users['location_city'] = users['location'].apply(lambda x: x.split(',')[0].strip())
users['location_state'] = users['location'].apply(lambda x: x.split(',')[1].strip())
users['location_country'] = users['location'].apply(lambda x: x.split(',')[2].strip())

users = users.replace('na', np.nan) 
users = users.replace('',   np.nan)

# country가 na지만 state 정보가 있는 경우 이 정보를 활용해서 country 채워넣기
states_with_null = users[(users['location_state'].notnull()) & (users['location_country'].isna())]['location_state'].values

for state in states_with_null:
    try:
        country = users.loc[(users['location'].str.contains(state)), 'location_country'].value_counts().index[0]
        users.loc[(users['location'].str.contains(state)) & (users['location_country'].isna()), 'location_country'] = country
    except:
        pass

# country가 na지만 city 정보가 있는 경우 이 정보를 활용해서 country 채워넣기
cities_with_null = users[(users['location_city'].notnull()) & (users['location_country'].isna())]['location_city'].values

for city in cities_with_null:
    try:
        country = users.loc[(users['location'].str.contains(city)), 'location_country'].value_counts().index[0]
        users.loc[(users['location'].str.contains(city)) & (users['location_country'].isna()), 'location_country'] = country
    except:
        pass


# 각 나라 별로 users['location']의 최빈값으로 대체
countries_list = users['location_country'].value_counts()
for country in countries_list.index:
    try:
        new_country = users.loc[(users['location'].str.contains(country)), 'location_country'].value_counts().index[0]
        users.loc[(users['location'].str.contains(country)) & (users['location_country'] == country), 
                  'location_country'] = new_country
    except:
        pass

# country가 threshold보다 작은 경우를 다합쳐서 others로 대체
threshold = 30

others_list = users['location_country'].value_counts()[users['location_country'].value_counts() < threshold].index
for country in others_list:
    try:
        users.loc[(users['location_country'] == country), 'location_country'] = 'others'
    except:
        pass

# 남아있는 country의 결측치 경우 최빈값인 random sampling으로 impute
random_country = np.random.choice(users.loc[users['location_country'].notna(), 'location_country'], 
                                  users['location_country'].isna().sum())
users.loc[users['location_country'].isna(), 'location_country'] = random_country

# impute된 country 활용해서 state, city 채워넣기
country_list = users['location_country'].value_counts().index

for country in country_list:
    try:
        random_state = np.random.choice(
            users.loc[(users['location_country'] == country) & (users['location_state'].notna()), 'location_state'],
            users.loc[(users['location_country'] == country), 'location_state'].isna().sum()
        )
        users.loc[(users['location_country'] == country) & (users['location_state'].isna()), 'location_state'] = random_state

        state_list = users.loc[(users['location_country'] == country), 'location_state'].value_counts().index

        for state in state_list:
            random_city = np.random.choice(
                users.loc[(users['location_country'] == country) & 
                          (users['location_state']   == state)   & 
                          (users['location_city'].notna()), 'location_city'],
                users.loc[(users['location_country'] == country) & (users['location_state'] == state), 'location_city'].isna().sum()
            )
            users.loc[(users['location_country'] == country) & 
                      (users['location_state'] == state)     & 
                      (users['location_city'].isna()), 'location_city'] = random_city
    except:
        pass

for country in country_list:
    try:
        random_city = np.random.choice(
            users.loc[(users['location_country'] == country) & (users['location_city'].notna()), 'location_city'],
            users.loc[(users['location_country'] == country), 'location_city'].isna().sum()
        )
        users.loc[(users['location_country'] == country) & (users['location_city'].isna()), 'location_city'] = random_city
    except:
        pass

# drop columns and save processed users.csv
users.drop(['location'], axis=1, inplace=True)

data_path = './data/'
users.to_csv(data_path + 'my_users.csv', index=False)

#### book ####

path = './data/'
books = pd.read_csv(path + 'books.csv')

# summary, img_url, img_path는 안쓸거기 때문에 drop
books.drop(['summary', 'img_url', 'img_path'], axis=1, inplace=True)

# ISBN 첫번째 값을 기준으로 language impute
null_lang = books.loc[books['language'].isna(), 'isbn'].apply(lambda x: x[:1]).value_counts().to_dict()

for i in range(10):
    i = str(i)
    possible_lang = books.loc[
        (books['isbn'].apply(lambda x: x[:1]) == i) & (books['language'].notna()), 
        'language'].values
    try:
        books.loc[(books['isbn'].apply(lambda x: x[:1]) == i) & (books['language'].isna()),
                'language'] = np.random.choice(possible_lang, null_lang[i])
    except:
        pass

# 남은 langugage 결측치는 random sampling imputation
random_lang = np.random.choice(books['language'], books['language'].isna().sum())
books.loc[(books['language']).isna(), 'language'] = random_lang

# publisher 전처리
books['publisher'] = books['publisher'].str.replace("'s", 's') # reader's digest 같은 출판사 이름을 간단하게
books['publisher'] = books['publisher'].str.replace("s'", 's')

books.loc[books[books['publisher'].notnull()].index, 'publisher'] = books[books['publisher'].notnull()]['publisher'].apply(lambda x: re.sub('[\W_]+',' ',x).strip())
books['publisher'] = books['publisher'].str.lower()
books['publisher'] = books['publisher'].str.strip()

# 출판한 책이 10개가 넘는 출판사로 출판사 이름을 포함하는 경우 이름 바꿔주기
# 예를들어 penguin books ltd 의 경우 penguin books 를 포함하니까 penguin books로 바꿔주기
threshold = 10

publisher_list = books['publisher'].value_counts()[books['publisher'].value_counts() > threshold].index
for publisher in publisher_list:
    try:
        books.loc[books['publisher'].str.contains(publisher), 'publisher'] = publisher
    except:
        pass

# 책을 10개 이하로 출판한 출판사는 others로 바꾸기
threshold = 10

publisher_list = books['publisher'].value_counts()[books['publisher'].value_counts() > threshold].index

books.loc[books['publisher'].notna() & books['publisher'].apply(lambda x: x not in publisher_list), 'publisher'] = 'others'
books['publisher'].value_counts()

# year_of_publication string으로 변환
books['year_of_publication'] = books['year_of_publication'].astype('str')

# category 전처리
books.loc[books[books['category'].notnull()].index, 'category'] = books[books['category'].notnull()]['category'].apply(lambda x: re.sub('[\W_]+',' ',x).strip())
books['category'] = books['category'].str.lower()
books['category'].value_counts()

# 대표적인 카테고리와 상위 카테고리를 만들기
categories = {   
    'animal'         : ['animal', 'bird', 'pets', 'cats', 'dogs', 'bears', 'dino'],
    'arts'           : ['art', 'photography', 'architecture', 'music', 'criticism', 'perform', 'design', 'paint', 
                        'decorat', 'draw', 'act', 'picture', 'author', 'composer'],
    'biographies'    : ['biography', 'memoir'],
    'business'       : ['business', 'money', 'economic', 'finance', 'invest', 'management', 'sales', 'marketing'],
    'comic'          : ['comic', 'graphic'],
    'computer'       : ['computer', 'technology', 'software'],
    'cook'           : ['cook', 'food', 'wine', 'baking', 'desserts', 'beverage', 'alcohol'],
    'education'      : ['education', 'teach', 'test', 'study', 'book'],
    'engineering'    : ['engineer', 'transportation', 'electronic'],
    'entertainment'  : ['humor', 'entertainment', 'game'],
    'family'         : ['child', 'famil', 'parent', 'relationship', 'marriage', 'baby', 'wedding', 'brother', 
                        'sister', 'boy', 'girl', 'aunt'],
    'health'         : ['health', 'fitness', 'diet', 'body', 'mind'],
    'history'        : ['history'],
    'hobby'          : ['craft', 'hobby', 'home', 'garden', 'landscape', 'collect'],
    'juvenile'       : ['student', 'school', 'teen', 'young', 'juvenile', 'friendship', 'adolescence'],
    'law'            : ['law', 'legal', 'divorce'],
    'life'           : ['life'],
    'medical'        : ['medical', 'pharmacology', 'medicine', 'dentistry', 'disease'],
    'mystery'        : ['mystery', 'extraterrestrial', 'fairy', 'curiosit', 'wonder', 'magic', 'ghost'],
    'reference'      : ['reference'],
    'religion'       : ['christian', 'bible', 'religion', 'spirit', 'church', 'catholic', 'angel', 'buddhism', 
                        'bereavement'],
    'self_help'      : ['help', 'interpersonal', 'relation', 'behavior', 'love'],
    'sports'         : ['sport', 'outdoor'],
    'thriller'       : ['thriller', 'suspense', 'crim', 'horror', 'murder', 'death'],
    'travel'         : ['travel', 'voyage'],
    'world'          : ['english', 'england', 'australia', 'brit', 'africa', 'states', 'france', 'canada', 'america', 
                        'china', 'egypt', 'germa', 'ireland', 'california', 'europe'],
    'social_science' : ['social', 'politic', 'psychology', 'philosophy', 'politic', 'government', 'geography',],
    'science'        : ['science', 'nature', 'math'],
    'literature'     : ['literature', 'science fiction', 'fiction', 'fantasy', 'drama', 'poetry', 'stories', 
                        'collections', ' fairy tale', 'horror', 'romance', 'adultery', 'adventure'],
}

# 기존 category에 해당 단어를 포함하면 해당 단어로 덮어쓰기
# 예 auto-biography -> biography

books['category_high'] = np.NaN	# initialize

for category_high in categories.keys():
    for category in categories[category_high]:
        books.loc[books['category'].notna() & books['category'].str.contains(category), 'category_high'] = category_high
        books.loc[books['category'].notna() & books['category'].str.contains(category), 'category']      = category

# author와 title 전처리

books['book_author'] = books['book_author'].apply(lambda x: re.sub('[\W_]+', ' ', x).strip())
books['book_author'] = books['book_author'].str.lower()
books['book_author'] = books['book_author'].str.strip()

books['book_title']  = books['book_title'].apply(lambda x: re.sub('[\W_]+', ' ', x).strip())
books['book_title']  = books['book_title'].str.lower()
books['book_title']  = books['book_title'].str.strip()

# author가 같은 책은 category도 같게 impute하기
no_cat_authors = books.loc[books['category_high'].isna(), 'book_author'].value_counts()
no_cat_authors = no_cat_authors[no_cat_authors > 1].to_dict()

for author in no_cat_authors:
    try:
        cat_list = books.loc[(books['category_high'].notna()) & (books['book_author'] == author),
                                'category'].values
        cat_high_list = books.loc[(books['category_high'].notna()) & (books['book_author'] == author),
                                'category_high'].values
        cats = np.random.choice(cat_list, no_cat_authors[author])
        cat_highs = np.random.choice(cat_high_list, no_cat_authors[author])

        books.loc[(books['category_high'].isna()) & (books['book_author'] == author), 'category'] = cats
        books.loc[(books['category_high'].isna()) & (books['book_author'] == author), 'category_high'] = cat_highs
    except:
        pass


# publisher가 같은 책이면 category도 같게 impute하기
no_cat_publishers = books.loc[books['category_high'].isna(), 'publisher'].value_counts()
no_cat_publishers = no_cat_publishers[no_cat_publishers > 1].to_dict()

for publisher in no_cat_publishers:
    try:
        cat_list = books.loc[(books['category_high'].notna()) & (books['publisher'] == publisher),
                                'category'].values
        cat_high_list = books.loc[(books['category_high'].notna()) & (books['publisher'] == publisher),
                                'category_high'].values
        cats = np.random.choice(cat_list, no_cat_publishers[publisher])
        cat_highs = np.random.choice(cat_high_list, no_cat_publishers[publisher])

        books.loc[(books['category_high'].isna()) & (books['publisher'] == publisher), 'category'] = cats
        books.loc[(books['category_high'].isna()) & (books['publisher'] == publisher), 'category_high'] = cat_highs
    except:
        pass

books.loc[books['category_high'].isna(), 'category'] = np.NaN
books.loc[books['category_high'].isna(), 'category_high'] = np.random.choice(books.loc[books['category_high'].notna(), 'category_high'],
                                                                            books['category_high'].isna().sum())

for category_high in categories.keys():
    try:
        cat_list = np.random.choice(categories[category_high], books.loc[(books['category_high'] == category_high), 'category'].isna().sum())
        books.loc[(books['category_high'] == category_high) & (books['category'].isna()), 'category'] = cat_list
    except:
        pass

# save processed books.csv
data_path = './data/'

books.to_csv(data_path + 'my_books.csv', index=False)