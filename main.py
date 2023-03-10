import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#reading CSV File
df = pd.read_csv("movie_dataset.csv")
#print(df.columns)

#Contents of a movie used
features = ['keywords','cast','genres','director']

# a column in DF which combines all selected features
for feature in features:
	df[feature] = df[feature].fillna('')  #filling all NaNs with blank string

def combine_features(row):
	try:
		return row['keywords'] +" "+row['cast']+" "+row["genres"]+" "+row["director"]
	except:
		print("Error:", row)

df["combined_features"] = df.apply(combine_features,axis=1)

#print("Combined Features:", df["combined_features"].head())

#creating new CountVectorizer() object
cv = CountVectorizer()

count_matrix = cv.fit_transform(df["combined_features"])  #feeding combined strings(movie contents) to CountVectorizer() object

#computing the Cosine Similarity based on the count_matrix
cosine_sim = cosine_similarity(count_matrix)
movie_user_likes = "Avatar"

def get_title_from_index(index):   #get movie title from movie index
	return df[df.index == index]["title"].values[0]

def get_index_from_title(title):   #get movie index from movie title
	return df[df.title == title]["index"].values[0]


movie_index = get_index_from_title(movie_user_likes)

similar_movies = list(enumerate(cosine_sim[movie_index]))

# a list of similar movies in descending order of similarity score
sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)

# printing titles of first 10 movies
i=0
for element in sorted_similar_movies:
		print(get_title_from_index(element[0]))
		i=i+1
		if i>10:
			break