import random #Do not update or remove
import time # going to use this to add delays for better user experience

def main():
    input_filename = "WorldCapitals.txt" #Do not update
    output_filename = "HighScores.txt" #Do not update
    username = "tpra675" #use your username

    # print banner
    print_banner(username)
    # read the world capitals file and create a dictionary
    world_capitals_dict = get_world_capitals_dictionary(input_filename)
    
    # run the quiz and get the final score
    final_score = run_quiz(world_capitals_dict)
    # print result
    print(f"thanks for playing, {username}. Your final score is {final_score}.")
    # handle high scores
    handle_high_scores(username, final_score, output_filename)
    # Ask the user if they want to play again 
    play_again = input("Would you like to play again? (yes/no): ").strip().lower()
    if play_again == "yes":
        run_quiz(world_capitals_dict)
    else:
        print("Thank you for playing! Goodbye.")
         
    print()
    

    




def print_banner(username):
    # This will display the quiz banner and the username
    line = "=" * 40 
    print(line) # thats the top part of the banner
    print(f"=   WORLD CAPITALS QUIZ FOR {username.upper()}    =") # title of the banner
    print(line) # thats the bottom part of the banner
    print() # just a blank line

    

# This reads the file and creates a dictionary of countries and their capitals
def get_world_capitals_dictionary(filename):
    world_capitals = {} # empty dictionary to store capitals
    with (open(filename, 'r')) as file: # opens the file
        for line in file: # this loops through each line of the file
            line = line.strip() # removes any unwanted spaces
            if line == "": # if there is an empty line, skip it
                continue
            parts = line.replace(":",",").split(",") # will split the line into country and capital and also replaces any colons with commas
            if len(parts) != 2: # if there are not exactly 2 parts, skip it
                continue
            country, capital = parts # assigns the country and capital to variables
            world_capitals[country.strip()] = capital.strip() # adds the country and capital to the dictionary, removing any unwanted spaces
    return world_capitals # returns the dictionary
       

    

# This function dusplays the question and gets the player's answer
def get_player_answer(target_country, cities):
    print(f"what is the capital of {target_country}?") # asks the question
    print()
    for index, city in enumerate(cities, start=1): # loops through the cities and displays them with a number
       print(f"{index}.{city}") # displays the city with a number
       print() # blank spacing
   
    answer = input("Enter the number of your answer (1-5): ") # gets the player's answer
       # This will validate the answer without the need for a while True
    while not (answer.isdigit() and 1 <= int(answer) <= 5):
        print("Invalid input. Please enter a number between 1 and 5: ")
        answer = input("Enter the number of your answer (1-5): ")

    return int(answer) # returns the player's answer
    


# This will run a single round of the quiz
def run_round(world_capitals_dict, countries_tested):
    target_country, cities = get_question_data(world_capitals_dict, countries_tested) # gets the question data
    player_choice = get_player_answer(target_country, cities) # asking the player for their answer
    correct_capital = world_capitals_dict[target_country] # checks if the answer is correct
    correct_index = cities.index(correct_capital) + 1
    print("\nChecking answer...") # message to the player
    time.sleep(2) # this delyas it for 2 seconds
    print() # blank spacing 
    if player_choice == correct_index:
        print("✅ Correct! Well done\n")
        time.sleep(1)
        return 1
    else:
        print(f"❌ Wrong! The correct answer is {correct_index}. {correct_capital}\n")
        time.sleep(1)  # Brief pause to see the correct answer
        return 0 

    

#This will rub the full quiz
def run_quiz(world_capitals_dict):
    print("Welcome to the World Capitals Quiz!") # welcome message
    print("You'll be shown a country name and 5 possible capitals.") # instructions
    print("Type the number of the capital you think is correct\n.") # instructions
    print()
    total_countries = len(world_capitals_dict) # gets the total number of countries
    num_questions = input(f"How many questions would you like to answer? (1-{total_countries}): ") # asks how many questions the player wants to answer
    # This will validate the number of questions without the need for a while True
    while not (num_questions.isdigit() and 1 <= int(num_questions) <= total_countries):
        print(f"Invalid input. Please enter a number between 1 and {total_countries}: ")
        num_questions = input(f"How many questions would you like to answer? (1-{total_countries}): ")
    num_questions = int(num_questions) # converts the number of questions to an integer
   
  
    print() # blank spacing

    # Run the quiz
    score = 0
    countries_tested = [] 
    for i in range(num_questions):
        print(f"Question {i + 1} of {num_questions}:") # displays the question number
        score += run_round(world_capitals_dict, countries_tested) # adds the score for each round
        print("--------------------------------") # separator between rounds
        print()
    # final score
    print(f"Quiz complete! Your final score is {score} out of {num_questions}.")
    print()
    return score
    
    

# This is going to read the high scores from the file
def read_high_scores(filename):
    high_scores = {} # initializes an empty dictionary to store high scores

    try: # "try:" prevents the program from crashing if the file does not exist
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or "," not in line: # if the line is empty or does not contain a comma, skip it
                    continue
                username, score = line.split(",")
                if score.isdigit(): # checks if the score is a digit
                     high_scores[username] = int(score)
    except FileNotFoundError: # if the file does not exist, just return an empty dictionary
        pass
    return high_scores

# This will update the high scores in the file
def update_high_scores(filename, username, high_scores, new_score):
    if username not in high_scores or new_score > high_scores[username]:
        high_scores[username] = new_score # so basically if the username is not in the high scores or the new score is greater than the existing score, update the high score
    sorted_scores = sorted(high_scores.items(), key=lambda x: x[1], reverse=True) # sorts the high scores in descending order
    with open(filename, 'w') as file: # sends a message saying we want to write in the file
        for name, score in sorted_scores:
            file.write(f"{name},{score}\n") # writes the name and score to the file

    

# This will handle the high score logic
def handle_high_scores(username, new_score, filename):
    print("Saving your score...") # message to the player

    # read the existing high scores
    high_scores = read_high_scores(filename)
    # update the high scores with the new score
    update_high_scores(filename, username, high_scores, new_score)
    updated_scores = read_high_scores(filename) # read the updated high scores
    print("================= High Scores ================") # prints the high scores banner
    for name, score in sorted(updated_scores.items(), key=lambda x: x[1], reverse=True): # sorts the high scores in descending order
        print(f"{name}: {score}") # prints the name and score
    print("==============================================") # prints the bottom of the banner
    

#Do not update or remove
def get_question_data(world_capitals_dict, countries_tested):
    countries = list(world_capitals_dict.keys())
    target_country = countries[random.randrange(0, len(countries))]
    while target_country in countries_tested:
        target_country = countries[random.randrange(0, len(countries))]
    countries_tested.append(target_country)
    countries.remove(target_country)
    cities = [world_capitals_dict[target_country]]
    while len(cities) < 5:
        country = countries[random.randrange(0, len(countries))]
        countries.remove(country)
        cities.append(world_capitals_dict[country])
    random.shuffle(cities)
    return target_country, cities




if __name__ == "__main__":
    #Do not update or remove  
    main()
   
 
