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

    AverageCustRating = pickle.load(infile_1)
    MovieToYear = pickle.load(infile_2)
    AverageRateForYear = pickle.load(infile_3)
    CustomerAvergeForYear = pickle.load(infile_4)
    infile_1.close()
    infile_2.close()
    infile_3.close()
    infile_4.close()
    #designated chache to populate
    combinedAverage = {}


    for key, value in CustomerAvergeForYear.items():
        #Key = (customer_ID,Year)
        year = key[1]
        TotalAvgForYear = AverageRateForYear[str(year)]
        combinedAvg = round((value + TotalAvgForYear) / 2,6)
        combinedAverage[key] = combinedAvg
    outfile = open("CombinedCustomerAverageByYear.pickle","wb")
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
                        "cache-actualCustomerRating.pickle" ]

    num = int(num)
    inputFile = avaliable_files[num]
    infile = open(inputFile ,"rb")
    cache = pickle.load(infile)
    infile.close()
    return cache

AVERAGE_RATING = 3.60428996442

#Initialize Caches
CombinedAveragePerYear = getPersonal_cache(0)
id_and_year = getPersonal_cache(2)
actual_scores_cache = getPersonal_cache(4) #(customerID,movie_id:rate)
print(len(CombinedAveragePerYear))
print(len(actual_scores_cache))


# ------------
# netflix_eval
# ------------

def netflix_eval(reader, writer) :
    predictions = []
    actual = []

    # iterate throught the file reader line by line
    movie_year = 0
    movie_id = 0
    for line in reader:
        try:
        # need to get rid of the '\n' by the end of the line
            line = line.strip()
            # check if the line ends with a ":", i.e., it's a movie title
            if line[-1] == ':':
        	# It's a movie
                current_movie = line.rstrip(':')
                movie_id = int(current_movie)
                movie_year = int(id_and_year[movie_id])
                writer.write(line)
                writer.write('\n')
            else:
        	# It's a customer
                current_customer = int(line)
                prediction = CombinedAveragePerYear[(current_customer,movie_year)]
                print(prediction)
                predictions.append(prediction)
                actual.append(actual_scores_cache[(current_customer, movie_id)])
                writer.write(str(prediction))
                writer.write('\n')
        except KeyError as e:
            print(e)
            break
    # calculate rmse for predications and actuals
    rmse = sqrt(mean(square(subtract(predictions, actual))))
    writer.write("RMSE: " + str(rmse)[:4] + '\n')
