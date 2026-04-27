import os
import sys
import csv
import argparse

def load_data():
    """Calls for the loading of data from the CSV files.

    Args:
        We call amphibians, birds, insects, mammals, and reptiles (CSV): These 
            are collections of animal and user data from INaturalist.

    Returns:
        data: a list of strings representing the combined CSV file data of the afformentioned CSVs.
    """
    data = []
    if os.getcwd().endswith("ProductionCode"):
        data = load_individual_data("data/amphibians.csv", data)
        data = load_individual_data("data/birds.csv", data)
        data = load_individual_data("data/insects.csv", data)
        data = load_individual_data("data/mammals.csv", data)
        data = load_individual_data("data/reptiles.csv", data)
    else:
        data = load_individual_data("ProductionCode/data/amphibians.csv", data)
        data = load_individual_data("ProductionCode/data/birds.csv", data)
        data = load_individual_data("ProductionCode/data/insects.csv", data)
        data = load_individual_data("ProductionCode/data/mammals.csv", data)
        data = load_individual_data("ProductionCode/data/reptiles.csv", data)
     #if we are in the ProductionCode directory, we need to move up one level to access the data

    
    # Return for test purposes
    return data

def load_individual_data(FILENAME, data):
    """Loads data from a CSV file and stores it in 'data' 
        Args: 
            FILENAME (String): This is the file path to the CSV data
        
        Returns:
            data (list of strings): This adds the called CSV files into a list, 
                where each new entry in the data (and its associated information) takes up a spot on the list.
    """
    with open(FILENAME, newline='') as datafile:
        csv_file = csv.reader(datafile)
        for row in csv_file:
            data.append(row)

    # Return for test purposes
    return data

def create_leaderboard(common_name_of_animal, data):
    """Gets and adds the animal/user spotting data to the leaderboard list from the CSV and calls
     for the printing and sorting of the leaderboard through helper functions.

    Args:
        common_name_of_animal (str): User inputed animal for which they would like to see a user contribution leaderboard.


    Returns:
        It will end up calling the print_leaders function after creating the leaderboard, ultimately printing the leaderboard.
    """
    data_in_rows = data
    username_counts = {}
    username_key_storage = []
    creature_of_interest = common_name_of_animal
    total_animal_spotted_count = 0
    common_name_index = 7
    user_index = 11
    first_spotting_count = 1
    increment_by_1 = 1

    for row in range(len(data_in_rows)):
        if data_in_rows[row][common_name_index] == creature_of_interest:
            username = data_in_rows[row][user_index]
            total_animal_spotted_count += increment_by_1
            if username in username_counts:
                username_counts[username] += increment_by_1
                username_key_storage = sort_keys(username_key_storage, username_counts, username)
            else:
                username_counts[username] = first_spotting_count
                username_key_storage.append(username)

    # print_leaders(username_counts, username_key_storage, total_animal_spotted_count, common_name_of_animal) 

    # Return for test purposes
    return username_counts, username_key_storage, total_animal_spotted_count, common_name_of_animal
                
def print_leaders(username_counts, username_key_storage, total_animal_spotted_count, common_name_of_animal):
    """Prints from the username_key_storage with the associated sighting count. It also provides the total number of species sightings.

    Args:
        username_counts (dict): This stores the associated sighting count for every username in username_key_storage.
        username_key_storage (str): Every username in this list is in order from their respective username_count
            dictionary values.
        total_animal_spotted_count (int): This tracks the total number of entries/spottings the specific animal of 
            interest has in the dataset.
        common_name_of_animal (str): User inputed animal for which they would like to see a user contribution leaderboard.


    Returns:
        print_index(int): This demonstrates in the test function that the number of users printed is accurate to the list.
    
    Prints:
        This function prints out a leaderboard heading, with total animal of interest sightings recorded in the data set. 
            It then sequentially prints out the top 100 leaderboard and the leaders' respective animal sighting counts.
    """

    max_user_printout = 100
    results = []
    
    for print_index, user in enumerate(username_key_storage):
        results.append({
            "rank": print_index + 1,
            "user": user,
            "count": username_counts[user]
        })
        if print_index == max_user_printout - 1:
            break
    return results

def sort_keys(username_key_storage, username_counts, username)-> list:
    """This function sorts the leaders in the username_storage_list from most to least contributions.
        It does this by comparing the now increased count of the user leftward until its leftward neighbor has a higher count.

    Args:
        username_counts (dict): This stores the associated sighting count for every username in username_key_storage.
        username (str): This is the current username, which has had its count increased.
        username_key_storage (str): Every username in this list is in order from their respective username_count
            dictionary values, except for the new "username" varible.

    Returns: username_key_storage (str): This is now a list of usernames sorted by highest to lowest contribution.
    """

    user_of_interest = username
    index_of_user_place_in_storage = -1
    known_in_order = False

    for place_in_storage in username_key_storage:
        index_of_user_place_in_storage += 1 
        if place_in_storage == user_of_interest:
            break
    
    while known_in_order == False:
        
        user_to_move_location = index_of_user_place_in_storage - 1
        user_to_move = username_key_storage[user_to_move_location]

        if (index_of_user_place_in_storage != 0 and (username_counts[user_of_interest] > username_counts[user_to_move])):
            username_key_storage[index_of_user_place_in_storage] = user_to_move
            username_key_storage[index_of_user_place_in_storage - 1] = user_of_interest
            index_of_user_place_in_storage =  index_of_user_place_in_storage - 1
        else:
            known_in_order = True
    

    return username_key_storage 

def check_for_improper_request(creature_of_interest, data):
    """
    Args:
        creature_of_interest (str): User inputed animal for which they would like to see a user contribution leaderboard.


    Returns:
        True or False (bool): This is based on if the creature of interest is "common name", if it is then the function returns False. Also when False, it will prompt the user to try again with a different animal.
    """
    if creature_of_interest not in [row[7] for row in data]:
        return False
    else:
        return True
    

def main():
    """This function starts the process of the program and prompts/takes user input regarding the animal of interest.
            It also prompts the loading of the data needed. 

    Args: N/A

    Returns: N/A
    """
    
    parser = argparse.ArgumentParser(description="Find the top 100 species-specific contributors to INaturalist in Minnesota")
    parser.add_argument("animal", type=str, help="Remember to use and capitalize an animal's common name and if a name is more than 1 word, put quotes around it, e.g. 'Common Loon'")
    args = parser.parse_args()

    creature_of_interest = args.animal
    
    data = load_data()
    if check_for_improper_request(creature_of_interest):
        create_leaderboard(creature_of_interest, data)
    
if __name__ == "__main__":
    main()

