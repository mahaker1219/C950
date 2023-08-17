# C950 - Webinar-2 - Getting Greedy, who moved my data?
# W-2_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy.py
# Ref: zyBooks: Figure 7.8.2: Hash table using chaining.
# Ref: zyBooks: 3.3.1: MakeChange greedy algorithm.
"""
Add this file to the project
BestMovies.csv:
-----------------------
ID, Name, Year, Price
1, "CITIZEN KANE", 1941, 25.00
2, "CASABLANCA", 1942, 25.00
3, "THE GODFATHER", 1972, 10.00
4, "GONE WITH THE WIND", 1939, 10.00
5, "LAWRENCE OF ARABIA", 1962, 10.00
6, "THE WIZARD OF OZ", 1939, 10.00
7, "THE GRADUATE", 1967, 5.00
8, "ON THE WATERFRONT", 1954, 5.00
9, "SCHINDLER'S LIST", 1993, 5.00
10, "SINGIN' IN THE RAIN", 1952, 5.00
11, "STAR WARS", 1977, 1.00
-----------------------
"""
import csv
import math

# HashTable class using chaining.
class ChainingHashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=10):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])
      
    # Inserts a new item into the hash table.
    def insert(self, key, item): #  does both insert and update 
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if it is already in the bucket
        for kv in bucket_list:
          #print (key_value)
          if kv[0] == key:
            kv[1] = item
            return True
        
        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        #print(bucket_list)

        # search for the key in the bucket list
        for kv in bucket_list:
          #print (key_value)
          if kv[0] == key:
            return kv[1] # value
        return None

    # Removes an item with matching key from the hash table.
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        for kv in bucket_list:
          #print (key_value)
          if kv[0] == key:
              bucket_list.remove([kv[0],kv[1]])

class Movie:
    def __init__(self, ID, name, year, price, status):
        self.ID = ID
        self.name = name
        self.year = year
        self.price = price
        self.status = status
    
    def __str__(self):  # overwite print(Movie) otherwise it will print object reference 
        return "%s, %s, %s, %s, %s" % (self.ID, self.name, self.year, self.price, self.status)  

def loadMovieData(fileName):
    with open(fileName) as bestMovies:
        movieData = csv.reader(bestMovies, delimiter=',')
        next(movieData) # skip header
        for movie in movieData:
            mID = int(movie[0])
            mName = movie[1]
            mYear = movie[2]
            mPrice = movie[3]
            mStatus = "Loaded"
           
            # movie object
            m = Movie(mID, mName, mYear, mPrice, mStatus)
            #print(m)

            # insert it into the hash table
            myHash.insert(mID, m)

# Hash table instance 
myHash = ChainingHashTable()

# Load movies to Hash Table
loadMovieData('BestMovies.csv')

print("BestMovies from Hashtable:")
# Fetch data from Hash Table
for i in range (len(myHash.table)+1): 
    print("Movie: {}".format(myHash.search(i+1))) # 1 to 11 is sent to myHash.search()


# Greedy Algorithm: Min Expenses => Max Profits
def greedyAlgorithmMinExpenses(budget):
    total = budget
    c25dollar = 0
    c10dollar = 0
    c5dollar = 0
    c1dollar = 0
    while (budget >= 25):
        if c25dollar > 3: # why 3? 0,1,2,3 will not break so 4 times.
            break
        c25dollar += 1
        budget = budget - 25
    while (budget >= 10):
        c10dollar += 1
        budget = budget - 10
    while (budget >= 5):
        c5dollar += 1
        budget = budget - 5
    while (budget > 0):
        if c1dollar > 3:
            break
        c1dollar += 1
        budget = budget - 1
    
    cDVDs = c25dollar + c10dollar + c5dollar + c1dollar

    # expense calculation
    eDVDs = 1.00 * cDVDs # Material cost of DVD: $1.00
    eLabor = 12.00 * (math.ceil(cDVDs/10)) # Labor is $12.00 for every 10 DVDs, $24.00 for 11 DVDs
    eShipping = 0.50 * cDVDs # Shipping cost is $0.50 per DVD
    eTotal = eDVDs + eLabor + eShipping
    profit = total - eTotal

    print("${:.2f}-Budget, {}-DVDs, ${:.2f}-Expense, ${:.2f}-Profit ==>".format(total,cDVDs,eTotal,profit))
    print(" {} x 25 dollar movie = ${:.2f}".format(c25dollar,c25dollar*25.00))
    print(" {} x 10 dollar movie = ${:.2f}".format(c10dollar,c10dollar*10.00))
    print(" {} x 5  dollar movie = ${:.2f}".format(c5dollar,c5dollar*5.00))
    print(" {} x 1  dollar movie = ${:.2f}".format(c1dollar,c1dollar*1.00))

print("\nGreedy Algorithm: Min Expenses => Max Profits")
greedyAlgorithmMinExpenses(102) # $102.00 budget 
greedyAlgorithmMinExpenses(94) # $94.00 budget
greedyAlgorithmMinExpenses(71) # $71.00 budget
greedyAlgorithmMinExpenses(200) # $200.00 budget
