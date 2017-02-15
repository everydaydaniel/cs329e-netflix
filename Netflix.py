#!/usr/bin/env python3
# This program wil try to predict user ratings by taking in Caches
# that have movie averages and customer offsets by year.
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

    """
    Creates a cache that gets the average rating per customer
    by year and the total average rating for that year and takes the average.
    The returned dictionary values are...
    { (customer_ID,year) : combined_Average }

    """
    # TODO: create a cache that has a customers combined average by year
    #Average customer rating
    #(int(customer_ID):float(average_rating))
    infile_1 = open("cache-averageCustomerRating.pickle","rb")

    #(int(movie_id) : string(year))
    infile_2 = open("kzk66-movies_and_years.pickle","rb")

    #(string(year):float(averageRatingForThatYear))
    infile_3 = open("kzk66-year_rating_avg.pickle","rb")

    #((customer_ID,year) : rating)
    infile_4 = open("cache-customerAverageRatingByYear.pickle","rb")

    #(movie_ID : rating)
    infile_5 = open("cache-averageMovieRating.pickle", "rb")

    AverageCustRating = pickle.load(infile_1)
    MovieToYear = pickle.load(infile_2)
    AverageRateForYear = pickle.load(infile_3)
    CustomerAvergeForYear = pickle.load(infile_4)
    movieAverageRating = pickle.load(infile_5)
    infile_1.close()
    infile_2.close()
    infile_3.close()
    infile_4.close()
    infile_5.close()
    #designated chache to populate
    combinedAverage = {}


    for key, value in CustomerAvergeForYear.items():
        #Key = (customer_ID,Year)
        year = key[1]
        TotalAvgForYear = AverageRateForYear[str(year)]
        combinedAvg = round((value + TotalAvgForYear) / 2,6)
        combinedAverage[key] = combinedAvg
    outfile = open("AvereageCustMovYear.pickle","wb")
    pickle.dump(combinedAverage,outfile)
    outfile.close()

def getPersonal_cache(num):
    """
    USE THIS TO CREATE THE CACHE CUSTOMMER OFFSET CACHE
    Deserializes Customer Offset cache
    cache Schema: {(customerID,Year): OFFSET }
    returns as  : {     (Tuple)     : float  }
    """
    avaliable_files = ["CombinedCustomerAverageByYear.pickle","kzk66-year_rating_avg.pickle",
                        "kzk66-movies_and_years.pickle","kzk66-year_rating_avg.pickle",
                        "cache-actualCustomerRating.pickle","cache-averageMovieRating.pickle",
                        "olr248-ecw583-customerAverageOffset.pickle",
                        "yl23553-dlh3393-yearlyAverageOffset.pickle","amm7366-rs45899-customerAverageOffset.pickle"]


    num = int(num)
    inputFile = avaliable_files[num]
    infile = open(inputFile ,"rb")
    cache = pickle.load(infile)
    infile.close()
    return cache

AVERAGE_RATING = 3.60428996442

#Initialize Caches

movieAverageRating = getPersonal_cache(5) #cache-averageMovieRating.pickle
actual_scores_cache = getPersonal_cache(4) #(customerID,movie_id:rate)
customerAverageOffset = getPersonal_cache(8)
YearOfMovie = getPersonal_cache(2)


# ------------
# netflix_eval
# ------------
def netflix_eval(reader, writer) :
    """
    This function will produce predictions. At the end it
    will compare the prediction values with the actual values. 
    """
    predictions = []
    actual = []

    # iterate throught the file reader line by line
    movieAverage = 0
    movie_id = 0
    movieYear = 0
    #print("Start of loop")
    for line in reader:
        try:
        # need to get rid of the '\n' by the end of the line
            line = line.strip()
            # check if the line ends with a ":", i.e., it's a movie title
            if line[-1] == ':':
        	# It's a movie
                #print("if statement\nmovie ID Movie  Agerage")
                current_movie = line.rstrip(':')
                movie_id = int(current_movie)
                movieYear = int(YearOfMovie[movie_id])
                movieAverage = int(movieAverageRating[movie_id])
                #print(movie_id,movieAverage)
                writer.write(line)
                writer.write('\n')
            else:
        	# It's a
                #print("Else statement\ncustomer Offset prediction")
                current_customer = int(line)
                currentoffset = customerAverageOffset[current_customer]
                pred = round((movieAverage + currentoffset),3)
                #print(current_customer, currentoffset, pred)
                predictions.append(pred)
                actual.append(actual_scores_cache[(current_customer, movie_id)])
                writer.write(str(pred))
                writer.write('\n')

        except KeyError as e:
            print(e,"KeyError")
            break




    rmse = sqrt(mean(square(subtract(predictions, actual))))
    writer.write("RMSE: " + str(rmse)[:4] + '\n')
