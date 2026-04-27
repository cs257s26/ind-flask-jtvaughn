import argparse
import csv
import random
from collections import Counter
import os


FILENAME = "data/mammals.csv"

data = []

def load_data():
    """Loads in data from a CSV file and stores it in `data`"""
    with open(FILENAME, newline='') as datafile:
        csv_file = csv.reader(datafile)
        for row in csv_file:
            data.append(row)
    return data
    
def makeRandomLocation(data):
    '''Gets a random location from the column of locations'''
    rowCount=len(data)
    randomLine = random.randint(1, rowCount) #get a random line from the CSV
    randomLocationName = data[randomLine][10] #10 is the column that contains the locations
    return randomLocationName

def makeRandomLocationList(randomLocationName: str, data)-> list:   
    '''makes a new list that only contains rows with entries of randomLocationName then makes it ordered by the frequency of that animal sighting at a location '''
    locationList = []
    for row in data:
        if row[10] == randomLocationName: #if an entry is found at the random location we chose, then add it to locationList
            locationList.append(row)
    animalsList = [entry[7] for entry in locationList] #10 is the column that contains "place_guess"
    countedAnimalsList = Counter(animalsList) #We get a dictionary of how many times each animal appears in "animalList".
    mostCommon = countedAnimalsList.most_common() #'most_common()'is a funcion from Counter that will give us a sorted list
    print(mostCommon)
    return mostCommon

def getCorrectAnswers(mostCommon: list) -> tuple[str, str]:
    '''Gets the most common animal and it's sighting frequency and sets that to be the correct answer. '''
    correctAnswer = mostCommon[0]
    correctAnswerAnimal = correctAnswer[0]
    correctAnswerCount = correctAnswer[1]
    return correctAnswerAnimal, correctAnswerCount

def top5AnimalsList(mostCommon: list)-> list[list]: 
    '''Makes a new list of just the top 5 animals then shuffles. '''
    top5Animals = mostCommon[0:5]
    random.shuffle(top5Animals)
    return top5Animals

def game(data):
    '''This function will have randomly chose a location
   and players will need to choose from 5 options which the most common animal reported at that location. '''
    randomLocationName = makeRandomLocation(data)
    mostCommon = makeRandomLocationList(randomLocationName, data)
    top5Animals = top5AnimalsList(mostCommon)
    correctAnswerAnimal, correctAnswerCount = getCorrectAnswers(mostCommon)

    print("Which is the most commonly reported species in ", randomLocationName, "?")
    print("Choose one: ", ", ".join(animal[0] for animal in top5Animals))
    userAnswer = input("Type your guess here: ")
    if correctAnswerAnimal == userAnswer:
        print("Correct!")
    else:
        print("Incorrect, the most commonly reported animal is: ", correctAnswerAnimal, ", reported ", correctAnswerCount, " times.")

def main():
    data= load_data()
    parser = argparse.ArgumentParser()
    parser.add_argument("game")
    game(data)

if __name__=='__main__':
    main()


    #in the future possibly deal with the case where multiple values equal correctAnswerCount
    #and the case where there are less than 3 animals in a location.. then choose a new location
