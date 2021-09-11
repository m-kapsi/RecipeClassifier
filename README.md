# Recipe Analysis and Classification for Meal Kit Services


### Background

Meal Kit services are growing increasingly popular, especially in a pandemic situation where many restaurants are closed, a significant number of people are working from home and therefore eating at home, and many people still do not have the time to shop groceries and plan meals for themselves regularly.

Meal Kit services differ from meal delivery systems like Deliveroo or FoodPanda, where meals are prepared by restaurants, or grocery delivery systems like RedMart, where ingredients are delivered a la carte in bulk. A Meal Kit service is an intersection of the two - delivering recipe-specific ingredients of just the right portions.

Meal Kit services help consumers emjoy the benefits of a home cooked meal, without any of the hassle of planning meals, buying groceries, or worrying about food wastage. Helping all kinds of customers find something tasty and exciting to cook is important for any meal kit service to succeed.

Data science and analytics can be leveraged to help improve customers' cooking and eating experiences by improving and creating new recipes. These recipes can be used to create menus that target different customer segments based on culture and dietery preference, and satisfy diverse consumer needs that balance taste, nutrition, and dietery restrictions.

There are many applications of data science to help increase the success of a meal kit service:
* Analyzing user feedback for sentiment analysis to identify the best and worse performing recipes
* Building a personalized recommendation system using user ratings on specific recipes to recommend new recipes to these users
* Analyzing recipe ingredients to understand what ingredients are popular among all recipes which can be useful for raw ingredient procurement
* Gaining insights into the geographical eating habits and preferences through understanding the differences in ingredients or food preperation techniques across different cuisines
* Analyzing the nutritional content of recipes to satisfy customer's daily macronutrient goals
* Creating new, experimental recipes that can be tested and improved to offer customers unique experiences

HomeChef is a start up meal kit service. HomeChef's current business model involves two plans: 1/ A basic plan for novice home cooks where users select recipes every week and are provided pre-measured ingredients for those recipes, and 2/ a flex plan for home cooks who are ready for a challenge and would like to purchase their own ingredients a la carte from HomeChef's marketplace. For the flex plan, HomeChef will offer suggestions for cuisines, recipes, or other ingredients consumers may want to purchase based on their current selection.

As a start up, they are still expanding their customer base and looking to use Natural Language Processing to gain insights on recipes across different cuisines.

The primary goals for HomeChef's data science team are:
1. Gain insights on the similarities and differences between global cuisines in order to provide consumers with the most appropriate ingredients and recipes
2. Predict a cuisine and offer popular recipe suggestions based on ingredients selected
---

### Problem Statement

The goal of this project is to use Natural Language Processing to gain insights on recipes across different cuisines. Specifically, this project aims to:
1. Analyze ingredients to gain insights on the similarities and differences between global cuisines
2. Use multiclass classification algorithms to predict the cuisine of a dish based on the ingredients
3. Provide recommendations for recipes based on available ingredients

---

### Summary of Analysis: Cuisine Classification Model

For this project, I trained multiple models including a baseline model, logistic regression model, random forest classifier, and linear support vector machine.

For each model, I used a stratified k-fold cross-validation to evaluate and further tune the models when there was evidence of overfitting. I used a 5 cross fold strategy and evaluated the performance on the following metrics:

    * Precision (weighted): The proportion of predicted positives that are actually positive
    * Recall (weighted): The proportion of true positives that are correctly classified
    * F1-score (weighted): The harmonic mean of precision and recall. This is useful for cuisine classification because I would want to minimize the false positives and false negatives equally
    * Cohen's Kappa Score: A measure for accuracy that integrates measurements of chance and class imbalance.

Unlike the macro scores (which is the simple arithmetic mean of all metrics across classes), the weighted scores weight the average of the metric by the number of samples for each class. By using the weighted scores, I could account for any class imbalance between cuisines.

The final model I used is a pipeline consisting of:
1. a TF-IDF vectorizer, where the maximum frequency of an ingredient occurring in a recipe is 1 (since all ingredients would only appear once in a given recipe’s list of ingredients) and the maximum document frequency is .95 (so ingredients that appear in more than 95% of recipes are ignored from the bag of words), and
2. a multinomial logistic regression model, where the classifier uses the softmax function instead of the sigmoid function (which is used for binary classification) to predict if the ingredient vector belongs to a certain cuisine class This model has a Kappa score of 0.84 and an F1-score of 0.85. For reference, this can be compared to the baseline model (where a cuisine is randomly assigned to a recipe) which has a Kappa score of 0 and an F1-score of 0.06. Further analysis of the performance of the final model can provide interesting insights on how cuisines influence each other, and the most distinctive ingredients for each cuisine in the dataset.

I chose to use the logistic regression model for the following reasons:
1. The logistic regression model outperformed the multinomial Naive Bayes and Random Forest models (and the Random Forest model has a significantly slower run time)
2. The logistic regression model performed similarly to the linear SVC, however, as the logistic regression model is more explainable (through coefficient analysis) I chose this as my final model
---
### Recipe Recommendation System

In order to identify ingredients that complement each other, I compared two algorithms: a
1. Pointwise Mutual Information (which calculates the likelihood of pairs of ingredients co-occurring) and
2. word2vec (which uses recurrent neural networks to learn the relationship between words).

It is difficult to quantify why algorithm performs better, as complementary ingredients are somewhat subjective, but there were very few overlaps between ingredients suggested by PMI and word2vec.

In order to build a content-based recipe recommendation system, I used TF-IDF to vectorize ingredients per recipe and calculated the cosine similarity between vectorized recipe ingredients. Because the relevance of a recommended recipe to a user is relative, there is no easy metric that can be used to evaluate the quality of the recommendations without user testing.

---

### Conclusion and Recommendations

#### Ingredients and Recipes
Through EDA, there are many useful insights that can help HomeChef identify what type of ingredients and recipes are best to provide consumers. As most of the consumers of HomeChef would be novice home cooks looking for easy and convenient recipes, I would base recipe recommendations on the following factors:
1. Number of ingredients:
  * Dishes in the dataset range between 2 to 40 ingredients. As the mean number of ingredients is 13, I would recommend HomeChef focus on recipes that use between 10-15 ingredients, and excluding common ingredients that are present across all cuisines and most likely consumers would already have in their kitchens (such as salt, pepper, onions, and garlic)
2. Recipe rating:
  * Italian, Mexican, Chinese, Thai, Greek, and Indian are cuisines with the highest average recipe ratings (the mean for these cuisines is above 3.9 out of 5). A higher recipe rating most likely correlates with tastier dishes, and recipes that are easier for users to make. It is worth noting that the data is from Yummly, where users are primarily American and therefore the ratings maybe biased towards American preferences.
3. Cooking time:
  * Dishes in this dataset range from a cooking time of 10 minutes to almost 9000 minutes (for recipes that use slow cookers or involve pot roasts). As the 25 th percentile is 35 minutes and the 75th percentile is 75 minutes, I would suggest providing users with recipes that take between 35 to 75 minutes to make. Therefore I would focus on cuisines where at least 75% of recipes will take under 60 minutes to make. These cuisines are: Indian, Greek, Italian, Hawaiian, Mexican, Japanese, Chinese, and Thai

Based on the criteria above, as well as the clustering analysis, I would suggest HomeChef focus on the following 5 cuisines: Mexican, Italian, Chinese, Indian and French

These cuisines generally have high recipe ratings, manageable cooking times, and have distinguishable ingredients (the cuisines belong to different K-Means clusters) so consumers will have options in terms of taste preferences and will not get bored as easily. While French recipes tend to have a longer cooking time (only 50% of French recipes take under 60 minutes to cook), it is the only cuisine from the European region cluster with an average rating above 3.8. Consumers that are looking for a challenge can try selecting French recipes.

Based on these cuisines, HomeChef can also ensure to stock up on ingredients that have a high relative usage for each cuisine. These ingredients are:
  1. Mexican: queso fresco, guacamole, tomatillo, masa harina, and salsa
  2. Italian: lasagna, meat sauce, pecorino cheese, ricotta cheese, and pasta sauce
  3. Chinese: black vinegar, hoisin sauce, fivespice powder, tangerine, and oyster sauce
  4. Indian: mutton, cassia leaves, rose water, cardamom, and black salt
  5. French: endive, armagnac brandy, pinot noir, bouquet garni (herbs), and lavendar

I also built a plotly dashboard so users can interactively explore cuisines. The dashboard can be found [here](https://homechefexplore.herokuapp.com/).

#### Recipe Recommendation System
I have deployed a telegram bot as a prototype of some of the features that HomeChef will be able to provide its consumers. Consumers can input what ingredients they have on hand, and be offered suggestions for cuisines and recipes to cook based on the logistic regression cuisine classifier and content based recipe recommendation system. The telegram bot can be useful to provide consumers who want to buy ingredients a la carte from HomeChef’s marketplace with suggestions on what other ingredients to add to their cart, or provide consumers with inspiration on what cuisine or recipes to cook next.

The bot can be downloaded [here](https://t.me/recs4homechefs_bot).

---

### Further Steps

The recipes used to gain insight on cuisines and develop the models for this project are from a single source, Yummly. In order to make the model more robust, it would be good to collect recipes from other sources too, especially websites that are popular in different regions so that I can have a full scope of taste preferences and variations.

Furthermore, sentiment analysis on their target consumer base may help HomeChef evaluate how their audience will receive certain cuisines and recipes. For example, as HomeChef is looking to target young, working class people in Singapore who do not much experience with cooking, would this consumer base be interested in learning to cook Asian recipes that they may be already familiar with, or would they want to experiment cooking recipes that are slightly more exotic).

Lastly, we would want to collect user feedback in order to evaluate the performance of the recipe recommendation system. HomeChef could use A/B testing to see if providing recipe suggestions increases the number of ingredients users purchase from their marketplace, or if HomeChef collects reviews and ratings on the recipes they provide this could be used to build a more personalized recipe recommendation system in the future.
