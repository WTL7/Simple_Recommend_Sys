
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


column_names = ['user_id','item_id','rating','timestamp']
movie_df = pd.read_csv('u.data', sep = '\t' , names = column_names)
movie_title = pd.read_csv('Movie_Id_Titles')

movie_df = pd.merge(movie_df, movie_title, on = 'item_id')

print movie_df.groupby('title')['rating'].mean().sort_values(
        ascending = False).head()
        
print movie_df.groupby('title')['rating'].count().sort_values(
        ascending = False).head()

ratings = pd.DataFrame(movie_df.groupby('title')['rating'].mean()) 
  
ratings['number of reviews'] = pd.DataFrame(
        movie_df.groupby('title')['rating'].count())   
        
print ratings.head()                   
        
plt.figure(figsize = (10,4))

#ratings['number of reviews'].hist()
#plt.show()
sns.distplot(ratings['number of reviews'], bins = 70, color = 'g', kde = False)

plt.figure(figsize = (10,4))
sns.distplot(ratings['rating'], bins = 70, color = 'r', kde = False)


sns.jointplot(x = 'rating', y = 'number of reviews', data = ratings, alpha = 0.5)

plt.show()

moviemat = movie_df.pivot_table(index = 'user_id', columns = 'title', 
        values = 'rating')
        
print moviemat.head()

starwars_user_ratings = moviemat['Star Wars (1977)']  # movie one
liarliar_user_ratings = moviemat['Liar Liar (1997)']  # moive two
print starwars_user_ratings[:20]

similar_to_starwars = moviemat.corrwith(starwars_user_ratings)
corr_starwars = pd.DataFrame(similar_to_starwars, 
        columns = ['Correlation'])
corr_starwars.dropna(inplace = True)        
corr_starwars = corr_starwars.join(ratings['number of reviews']) 

print corr_starwars.head()               


print corr_starwars[corr_starwars['number of reviews'] >=100] \
        ['Correlation'].sort_values(ascending = False).head()

# movie two
similar_to_liarliar = moviemat.corrwith(liarliar_user_ratings)
corr_liarliar = pd.DataFrame(similar_to_liarliar, 
        columns = ['Correlation'])
corr_liarliar.dropna(inplace = True)        
corr_liarliar = corr_liarliar.join(ratings['number of reviews']) 

print corr_liarliar[corr_liarliar['number of reviews'] >=100] \
        ['Correlation'].sort_values(ascending = False).head()



                