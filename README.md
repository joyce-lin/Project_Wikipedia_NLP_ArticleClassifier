### Predicting Wikipedia Article Categories

Python Code for this project can be found in folder "ipynnb"

#### Wiki_insert_to_MongoDB.py: 
     A Python script to download about 5,000 articles from 8 categories using Wikipedia API to a Mongo Database

#### Part2_1_PreProcessing_DataClearning.ipynb:
     Clean the article text using RegEx

#### Part2_2_FeatureEngineering_LSA.ipynb:
  1. Perform feature engineering using Natural Language Processing techniques - Latent Semantic Analysis (Tfidf and SVD) 
  stored models in Redis database from later article pridiction steps
  2. Plot 2D LSA components to examine how artical vectors cluster in the space using LSA method 
  
#### Part3_Predictor_Supervised.ipynb:
   Examine accuracy score on different supervised machine learning models
   GridSearch Decision Tree and KNeighbors models to get the best accuracy possible for a model that predicts the category of a new article

#### Part3_Predictor_Unsupervised_CosineSimilarity.ipynb:
   Use Cosine Similarity to determine article category

#### Part3_Predictor_UnSupervised_NearestNeighbor.ipynb:
   Create a semantic search engine, where you can input a search term and get a set of articles that are closest to that term, based on  NearestNeighbors algorithm


More Details can be found in /doc/Wiki_NLP_ArticleClassifier.pdf
