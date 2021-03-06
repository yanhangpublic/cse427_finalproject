import sys
import csv
import shutil
import os
import random

topK_dict = {}
with open(sys.argv[1]) as topK_file:
  for line in topK_file:
    movieID_1, neighbor = line.split('\t')
    movieID_2, similarity = neighbor.replace("(", "").replace(")", "").replace("\n", "").split(",")
    movieID_1 = int(movieID_1)
    movieID_2 = int(movieID_2)
    similarity = float(similarity)
    if not movieID_1 in topK_dict:
      topK_dict[movieID_1] = {}
    topK_dict[movieID_1][movieID_2] = similarity

#print(topK_dict)


test_dict = {}
with open('TestingRatings.txt') as test_file:
  for line in csv.reader(test_file, delimiter=","):
    movieID = int(line[0])
    userID = int(line[1])
    rating = float(line[2])
    if not movieID in test_dict:
      test_dict[movieID] = {}
    test_dict[movieID][userID] = rating
 
#print(test_dict)


ratings_to_read = {}
for movieID, user_rating_dict in test_dict.iteritems():
  if not movieID in topK_dict:
    print(str(movieID) + ' not in topK dict')
    break
  for movieID_2 in topK_dict[movieID]:
    for user in user_rating_dict:
      if not movieID_2 in ratings_to_read:
        ratings_to_read[movieID_2] = {}
      ratings_to_read[movieID_2][user] = -1
      
#print(ratings_to_read)

rating_sum = 0.0
num = 0
movie_rating_sums = {}
movie_nums = {}
user_rating_sums = {}
user_nums = {}

with open('TrainingRatings.txt') as test_file:
  for line in csv.reader(test_file, delimiter=","):
    movieID = int(line[0])
    userID = int(line[1])
    rating = float(line[2])
    
    rating_sum += rating
    num += 1
    if not movieID in movie_rating_sums:
      movie_rating_sums[movieID] = 0.0
    movie_rating_sums[movieID] += rating
    if not movieID in movie_nums:
      movie_nums[movieID] = 0
    movie_nums[movieID] += 1
    
    if not userID in user_rating_sums:
      user_rating_sums[userID] = 0.0
    user_rating_sums[userID] += rating
    if not userID in user_nums:
      user_nums[userID] = 0
    user_nums[userID] += 1
    
    if movieID in ratings_to_read:
      if userID in ratings_to_read[movieID]:
        ratings_to_read[movieID][userID] = rating

#print(ratings_to_read)
average_rating = rating_sum / num
movie_average_ratings = {}
for movieID, rating_sum in movie_rating_sums.iteritems():
  movie_average_ratings[movieID] = rating_sum / movie_nums[movieID]
user_average_ratings = {}
for userID, rating_sum in user_rating_sums.iteritems():
    user_average_ratings[userID] = rating_sum / user_nums[userID]


average_prediction_dict = {}
weighted_average_prediction_dict = {}
#unpredicted_movies = {}
num_unpredicted_items = 0
num_predicted_items = 0

AE_sum = 0
weighted_AE_sum = 0
SE_sum = 0
weighted_SE_sum = 0

AE_sum_round = 0
weighted_AE_sum_round = 0
SE_sum_round = 0
weighted_SE_sum_round = 0

AE_sum_predicted = 0
weighted_AE_sum_predicted = 0
SE_sum_predicted = 0
weighted_SE_sum_predicted = 0

for movieID, user_rating_dict in test_dict.iteritems():

  if not movieID in average_prediction_dict:
    average_prediction_dict[movieID] = {}
  if not movieID in weighted_average_prediction_dict:
    weighted_average_prediction_dict[movieID] = {}

  movie_average_rating = average_rating
  if movieID in movie_average_ratings:
    movie_average_rating = movie_average_ratings[movieID]
    
  if not movieID in topK_dict:
    print(str(movieID) + ' not in topK dict')
    for user, rating in user_rating_dict.iteritems():
      user_movie_average_rating = movie_average_rating
      #if user in user_average_ratings:
        #user_movie_average_rating += user_average_ratings[user] - average_rating
      average_prediction_dict[movieID][user] = user_movie_average_rating #random.randrange(5) + 1
      weighted_average_prediction_dict[movieID][user] = user_movie_average_rating #random.randrange(5) + 1
      num_unpredicted_items += 1
    break

  for user, rating in user_rating_dict.iteritems():
    rating_sum = 0
    num_ratings = 0
    weighted_rating_sum = 0
    similarity_sum = 0

    similarity_rating_pairs = []
    for movieID_2, similarity in topK_dict[movieID].iteritems():
      neighbor_rating = ratings_to_read[movieID_2][user]
      if neighbor_rating != -1:
        similarity_rating_pairs.append([similarity, neighbor_rating])

    if len(sys.argv) == 3:
      k = int(sys.argv[2])
      if len(similarity_rating_pairs) > k:
        similarity_rating_pairs = sorted(similarity_rating_pairs, key=lambda pair: pair[0], reverse=True)
        similarity_rating_pairs = similarity_rating_pairs[:k]

    for similarity_rating_pair in similarity_rating_pairs:
      similarity = similarity_rating_pair[0]
      neighbor_rating = similarity_rating_pair[1]
      rating_sum += neighbor_rating
      num_ratings += 1
      weighted_rating_sum += similarity * neighbor_rating
      similarity_sum += similarity
    
    if num_ratings == 0:
      #print(str(movieID) + " " + str(user) + " have no prediction")
      user_movie_average_rating = movie_average_rating
      #if user in user_average_ratings:
        #user_movie_average_rating += user_average_ratings[user] - average_rating
      average_prediction_dict[movieID][user] = user_movie_average_rating #random.randrange(5) + 1
      weighted_average_prediction_dict[movieID][user] = user_movie_average_rating #random.randrange(5) + 1
      #unpredicted_movies[movieID] = 1
      num_unpredicted_items += 1
    else:
      average_prediction_dict[movieID][user] = rating_sum / num_ratings
      weighted_average_prediction_dict[movieID][user] = weighted_rating_sum / similarity_sum
      num_predicted_items += 1

      E_predicted = rating - average_prediction_dict[movieID][user]
      AE_sum_predicted += abs(E_predicted)
      SE_sum_predicted += pow(E_predicted, 2)
    
      weighted_E_predicted = rating - weighted_average_prediction_dict[movieID][user]
      weighted_AE_sum_predicted += abs(weighted_E_predicted)
      weighted_SE_sum_predicted += pow(weighted_E_predicted, 2)


    #average_prediction_dict[movieID][user] = random.randrange(5) + 1
    #weighted_average_prediction_dict[movieID][user] = random.randrange(5) + 1
    E = rating - average_prediction_dict[movieID][user]
    AE_sum += abs(E)
    SE_sum += pow(E, 2)
      
    weighted_E = rating - weighted_average_prediction_dict[movieID][user]
    weighted_AE_sum += abs(weighted_E)
    weighted_SE_sum += pow(weighted_E, 2)

    E_round = rating - round(average_prediction_dict[movieID][user])
    AE_sum_round += abs(E_round)
    SE_sum_round += pow(E_round, 2)
    
    weighted_E_round = rating - round(weighted_average_prediction_dict[movieID][user])
    weighted_AE_sum_round += abs(weighted_E_round)
    weighted_SE_sum_round += pow(weighted_E_round, 2)


num_items = num_unpredicted_items + num_predicted_items
print(AE_sum / num_items)
print(pow(SE_sum / num_items, 0.5))
print(weighted_AE_sum / num_items)
print(pow(weighted_SE_sum / num_items, 0.5))
print(AE_sum_round / num_items)
print(pow(SE_sum_round / num_items, 0.5))
print(weighted_AE_sum_round / num_items)
print(pow(weighted_SE_sum_round / num_items, 0.5))
print(AE_sum_predicted / num_items)
print(pow(SE_sum_predicted / num_items, 0.5))
print(weighted_AE_sum_predicted / num_items)
print(pow(weighted_SE_sum_predicted / num_items, 0.5))
print(num_unpredicted_items)
print(num_unpredicted_items + num_predicted_items)

#print(len(average_prediction_dict))
#print(len(unpredicted_movies))
#print(average_prediction_dict)
#print(weighted_average_prediction_dict)
