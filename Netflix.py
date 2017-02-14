#!/usr/bin/env python3

# -------
# imports
# -------

from math import sqrt
import pickle
from requests import get
from os import path
from numpy import sqrt, square, mean, subtract


def create_cache(filename):
    """
    filename is the name of the cache file to load
    returns a dictionary after loading the file or
    pulling the file from the public_html page
    """
    cache = {}
    filePath = "/u/fares/public_html/netflix-caches/" + filename

    if path.isfile(filePath):
        with open(filePath, "rb") as f:
            cache = pickle.load(f)
    else:
        webAddress = "http://www.cs.utexas.edu/users/fares/netflix-caches/" + \
            filename
        bytes = get(webAddress).content
        cache = pickle.loads(bytes)

    return cache

def createPersonal_cache():
    # XXX: DONE USING DO NOT RUN ANYMORE
    """
    Creates a cache that gets the average rating per customer
    by year and finds the offest between the total average rating
    by year.
    """
####################

# XXX: for testingonly REMOVE !!!!!!!!!
    pickle_in = open("cache-customerAverageRatingByYear.pickle","rb")
    custAvgRateYear_dict = pickle.load(pickle_in)
    pickle_in.close()

####################
    #open Average Rating By Year pickle file
    infile = open("AverageRatingByYear.pickle","rb")
    avgRateYear_dict = pickle.load(infile)
    cache = {}
    # REPLACE
    # custAvgRateYear = "cache-customerAverageRatingByYear.pickle"
    # custAvgRateYear_dict = create_cache(custAvgRateYear)
    count = 0
    for key in custAvgRateYear_dict:
        count += 1
        cache_key = key
        val = avgRateYear_dict[cache_key[1]]
        #print(key, val)

        try:
            custAverage = custAvgRateYear_dict[key]
            yearAverage = avgRateYear_dict[key[1]]
            cache[key] = (custAverage + yearAverage) / 2
            #old code == custAverage - yearAverage
            #customer yearly - yearly average

        except Exception as e:
            print("Failed", e)
    pickle_out = open("CombinedAveragePerYear.pickle","wb")
    pickle.dump(cache, pickle_out)
    pickle_out.close()


def getPersonal_cache(num):
    """
    USE THIS TO CREATE THE CACHE CUSTOMMER OFFSET CACHE
    Deserializes Customer Offset cache
    cache Schema: {(customerID,Year): OFFSET }
    returns as  : {     (Tuple)     : float  }
    """
    avaliable_files = ["CombinedAveragePerYear.pickle","CustomerOffsetByYear.pickle", "kzk66-movies_and_years.pickle"]

    num = int(num)
    inputFile = avaliable_files[num]
    infile = open(inputFile ,"rb")
    cache = pickle.load(infile)
    infile.close()
    return cache










AVERAGE_RATING = 3.60428996442
# ACTUAL_CUSTOMER_RATING = create_cache(
#     "cache-actualCustomerRating.pickle")
# AVERAGE_MOVIE_RATING_PER_YEAR = create_cache(
#     "cache-movieAverageByYear.pickle")
# YEAR_OF_RATING = create_cache("cache-yearCustomerRatedMovie.pickle")
# CUSTOMER_AVERAGE_RATING_YEARLY = create_cache(
#     "cache-customerAverageRatingByYear.pickle")


actual_scores_cache ={10040: {2417853: 1, 1207062: 2, 2487973: 3}}
movie_year_cache = {10040: 1990}
decade_avg_cache = {1990: 2.4}


# ------------
# netflix_eval
# ------------

def netflix_eval(reader, writer) :
    predictions = []
    actual = []

    # iterate throught the file reader line by line
    for line in reader:
    # need to get rid of the '\n' by the end of the line
        line = line.strip()
        # check if the line ends with a ":", i.e., it's a movie title
        if line[-1] == ':':
    	# It's a movie
            current_movie = line.rstrip(':')
            pred = movie_year_cache[int(current_movie)]
            pred = (pred // 10) *10
            prediction = decade_avg_cache[pred]
            writer.write(line)
            writer.write('\n')
        else:
    	# It's a customer
            current_customer = line
            predictions.append(prediction)
            actual.append(actual_scores_cache[int(current_movie)][int(current_customer)])
            writer.write(str(prediction))
            writer.write('\n')
    # calculate rmse for predications and actuals
    rmse = sqrt(mean(square(subtract(predictions, actual))))
    writer.write("RMSE: " + str(rmse)[:4] + '\n')
