"""This is going to serve as the entry point for the program

I think the best way to handle the log would be through tracking state changes.
Essentially, there would be an initial state at beginning of day,
then every important event would be logged to array. There would be corresponding array
with times of everything. The thought process behind this is that
in terms of use, it would be annoying in memory to keep the
complete list of package status for every 5 mins. There would be a low
 usage rate of complete status call. I would cache results in a  hash table though then
 have it start at state of closest but lower complete log then use the state
 change log up until that point"""
import hash_table

initPackageList = hash_table.ChainingHashTable()

# This while statement serves mostly for the console application
while True:
    break
