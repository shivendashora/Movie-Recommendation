#!/usr/bin/env python
# coding: utf-8

# In[27]:


#content based filterinmg
#reading the movie and credits data set
import pandas as pd 
movies=pd.read_csv("tmdb_5000_movies.csv")
credit=pd.read_csv("tmdb_5000_credits.csv")
movies.shape


# In[28]:


movies.head(1)


# In[29]:


credit.shape


# In[30]:


credit.head(1)


# In[31]:


movies.rename({'vote_count': 'user_id'}, axis=1, inplace=True)


# In[32]:


movies


# In[33]:


movies=movies.merge(credit,on="title")


# In[34]:


movies.head()


# In[35]:


movies.info()


# In[36]:


#coloums present 
#genere
#id for movie posters
#keywords specific keyword for 
#title as the tilte will be in a=English onl
#overview
#realese date
#cast
#crew

movies=movies[['genres','id','keywords','title','overview','cast','crew','vote_average','user_id']]
movies.head()



# In[37]:


#removing the missing values 
movies.isnull().sum()


# In[38]:


movies.dropna(inplace=True)


# In[39]:


movies


# In[40]:


movies.isnull().sum()


# In[41]:


movies.duplicated().sum()


# In[42]:


movies.iloc[0].genres
#format is list of dictonaries so we now converting it into a single list ocontaing different words for it 


# In[43]:


import ast
def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name']) 
    return L


# In[44]:


movies['genres'] = movies['genres'].apply(convert)
movies.head()


# In[45]:


movies['keywords'] = movies['keywords'].apply(convert)
movies.head()


# In[46]:


movies['cast'][0]


# In[47]:


import ast
def convert3(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter != 3:
            L.append(i['name'])
            counter+=1
    return L 


# In[48]:


movies['cast']=movies['cast'].apply(convert3)


# In[49]:


movies['cast']


# In[50]:


def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L 


# In[51]:


movies['crew']=movies['crew'].apply(fetch_director)


# In[52]:


movies['crew']


# In[53]:


def collapse(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1


# In[54]:


movies['keywords'][0]


# In[55]:


movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)
movies['overview']= movies['overview'].apply(lambda x:x.split())


# In[56]:


movies.head()


# In[57]:


movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']


# In[58]:


movies=movies[['id','title','tags','vote_average','user_id']]
movies.head()


# In[59]:


movies['tags']=movies['tags'].apply(lambda x:" ".join(x))


# In[60]:


movies=movies[['id','title','tags','vote_average','user_id']]
movies.head()


# In[61]:


get_ipython().system('pip install nltk')


# In[63]:


import nltk
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()


# In[64]:


def stem(text):
    y=[]
    for i in text.split():
           y.append(ps.stem(i)) 
    return " ".join(y)



# In[65]:


movies['tags']=movies['tags'].apply(stem)


# In[48]:


movies['tags'][0]


# In[66]:


get_ipython().system('pip install --upgrade scikit-learn')


# In[67]:


#using textvectorisation 
#method="bag of words"- converting all the tags in a single text and then extracting the most repetative 5000 words 
#comparing them with the movie tags for single movie

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')


# In[68]:


cv.fit_transform(movies['tags']).toarray() #spars matrix  


# In[69]:


vectors=cv.fit_transform(movies['tags']).toarray()


# In[70]:


vectors.shape


# In[71]:


vectors[0]#for first movie


# In[72]:


from sklearn.metrics.pairwise import cosine_similarity


# In[73]:


similarity=cosine_similarity(vectors)
similarity


# In[74]:


cosine_similarity(vectors).shape


# In[75]:


sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1]) #we use enumarate so that  


# In[76]:


index=movies[movies['title'] == "The Godfather"].index[0]
print(index)



# In[77]:


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:11]:
        print(movies.iloc[i[0]].title)


# In[78]:


recommend('Batman Begins')


# In[79]:


import pickle


# In[80]:


new_dict=movies.to_dict()
new_dict
df=pd.DataFrame(new_dict)
print(df['title'])


# In[81]:


pickle.dump(movies.to_dict(),open('movies_dict.pkl','wb'))


# In[82]:


pickle.dump(similarity,open('similarity.pkl','wb'))


# In[ ]:




