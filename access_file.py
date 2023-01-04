def input_pos(text: str, func:str):
    """
    Asks for an input until it is in an acceptable form (positive number) and returns the converted input

    :param text: the input text given to the user
    :param func: the form that input should follow (int or float)
    :return: the converted input
    """

    while True:
        var = input(text)

        # converts the input into another object type
        try:
            var = func(var)

        # checks if the input is correct format
        except ValueError:
            print('Please enter a number.')
            continue

        # checks if the input is greater than 0
        if var <= 0:
            print('Please enter a positive number.')
            continue
        else:
            return var


def user_information_and_cal() -> float:
    """
    Asks for some information about user and returns the amount of nutrition they should ideally consume in a day
    :return: ideal calorie to be consumed daily
    """

    print('Please enter the following information about yourself.')

    # asks for the age of the user
    age = input_pos('Enter age: ', int)

    # confirms the input with the user when the value of age is extremely big or small
    if age > 100 or age < 10:
        answer = input(f'You have entered {age} as your age. Is that correct? (y/n): ')

        # asks the user for age once again if they typed something by mistake
        if answer == 'n':
            age = input_pos('Enter age: ', int)

    # asks for the biological sex of the user
    while True:
        sex = input('Enter your biological sex (Male/Female): ')
        sex = sex.lower()

        # checks if the input is in correct format
        if sex != 'male' and sex != 'female':
            print('Enter either male or female.')
            continue
        else:
            break

    # prints the different activity levels for the user
    print('Read below and enter a corresponding activity level:')
    print('''1. Sedentary: little to no exercise, desk job
2. Lightly Active: light exercise/sports 1-3 days/week
3. Moderately Active: moderate exercise/sports 6-7 days/week
4. Very Active: hard exercise every day
5. Extra Active: hard exercise 2 or more times every day''')

    # dictionary containing multiplier value for each activity level
    activity_multiplier = {'1': 1.2, '2': 1.375, '3': 1.55, '4': 1.725, '5': 1.9}

    # asks for the activity level of the user
    while True:
        activity_level = input('Enter an activity level (1,2,3,4,5): ')
        if activity_level not in list(activity_multiplier.keys()):
            print('Activity level has to be one of the 5 values above.')
            continue
        else:
            break

    # asks whether the user will use the imperial or the metric system
    while True:
        system = input('Enter 1 for imperial system (inches and pounds) and 2 for metric system (kgs and cms): ')
        if system != '1' and system != '2':
            print('Please enter 1 or 2 as your response.')
            continue
        else:
            break

    # asks the user for weight and height in metric system
    if system == '2':
        height = input_pos('Enter height (in cms): ', float)
        weight = input_pos('Enter weight (in kgs): ', float)

        # calculates the bmr using all the inputs provides by the user
        if sex == 'male':
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    # asks the user for weight and height in imperial system
    else:
        height = input_pos('Enter height (in inches): ', float)
        weight = input_pos('Enter weight (in pounds): ', float)

        # calculates the bmr using all the inputs provides by the user
        if sex == 'male':
            bmr = (4.536 * weight) + (15.88 * height) - (5 * age) + 5
        else:
            bmr = (4.536 * weight) + (15.88 * height) - (5 * age) - 161

    # raises an Assertion error if the value of bmr is less than 0
    assert bmr > 0, f'''BMR (Basal Metabolic Rate), the minimum amount of calories that you need to survive, was 
calculated to be less than 0, which is impossible. Your input for your weight, height or age was wrong. For your 
information, the age you entered was {age}, the weight was {weight}, and the height was {height}'''

    # calculates the ideal calorie that should be consumed daily by user
    ideal_cal = bmr * activity_multiplier[activity_level]
    return ideal_cal


def calculating_ideal_nutrients(ideal_cal: float) -> dict:
    """
    Receives the ideal calorie that should be consumed in a day and returns the ideal amount of other nutrients that
    should be consumed

    :param ideal_cal: the ideal calorie that should be consumed by the user
    :return: a dictionary containing ideal nutrition to be consumed daily
    """

    # creates a new dictionary for ideal nutrients
    ideal_nutrients = dict()

    # adds the range of each nutrient that should be ideally consumed using max and min value
    ideal_nutrients['cal'] = ideal_cal
    ideal_nutrients['min_carb'] = (ideal_cal * 0.45) / 4
    ideal_nutrients['max_carb'] = (ideal_cal * 0.65) / 4
    ideal_nutrients['min_pro'] = (ideal_cal * 0.10) / 4
    ideal_nutrients['max_pro'] = (ideal_cal * 0.35) / 4
    ideal_nutrients['min_fat'] = (ideal_cal * 0.20) / 9
    ideal_nutrients['max_fat'] = (ideal_cal * 0.35) / 9

    return ideal_nutrients


def display_and_receive_food():
    """
    Displays all the food options that are available and accepts inputs of amount of serving the user consumes for
    specific dishes in a day

    :return: a dictionary of the dishes and its corresponding servings consumed by the user in a day

    """

    # opens the csv file that contains list of food and their nutritional values
    try:
        fh = open('food_nutrition.csv', 'r')

    # returns an error output of -999 if the file does not exist
    except FileNotFoundError:
        print('The file food_nutrition.csv does not exist')
        return -999

    # a list containing all the available serial numbers of the food
    food_labels = []

    print('''The following will show a list of common breakfast, lunch, and dinner dishes in the Dining Center of 
Haverford College.''')

    # skips the header of the csv file
    header = fh.readline()

    for line in fh:
        # removes the newline from the end of the line
        food = line[:-1].split(', ')

        # prints headers that separates the food into breakfast, lunch, dinner, and user inputted food
        if food[0] == 'B1':
            print('\nBREAKFAST')
        if food[0] == 'L1':
            print('\nLUNCH')
        if food[0] == 'D1':
            print('\nDINNER')
        if food[0] == 'U1':
            print('\nADDITIONAL DISHES')

        # the label of each food is appended to a list
        food_labels.append(food[0])

        # prints the label and the name of each food
        print(f'{food[0]}: {food[1]}')

    fh.close()

    while True:
        # asks the user if they want to add any dish
        answer = input('Is there any other dish that you would like to add? (y/n): ')

        # checks the answer of the user
        if answer.lower() != 'y':
            break

        # adds a dish to the csv file and adds the label of the new dish to the list containing all lables
        new_food = add_food()
        food_labels.append(new_food['label'])

    # a dictionary that contains the input food label and serving amount of the dishes consumed by the user
    consumption = {}

    print('''\nEnter the label and the amount of serving that you would normally consume in a day for breakfast, lunch, 
and dinner (Example: B1-3, B1 being the label and 3 being the serving). After each entry, press enter to input another 
dish. The amount of serving can be in decimals as well. When finished, simply press enter one more time.\n''')

    while True:
        consume = input('Enter label and serving: ')

        # ends the loop is user enters nothing
        if consume == '':
            break

        # splits the user input into the food label and the serving amount
        consume_list = consume.split('-')
        food_label = consume_list[0]

        if len(consume_list) != 2:
            print('Only the food label and serving amount should be entered')
            continue

        # checks if the entered food label is actually present in the file
        if food_label not in food_labels:
            print(f'The label {food_label} does not exist. Please enter an acceptable label.')
            continue

        # converts the inputted food serving from string into integer
        try:
            serving = float(consume_list[1])

            # checks if the serving is greater than 0
            if not serving > 0:
                print('The value for amount of serving should be a positive integer.')
                continue

        # checks if the value of serving is a float
        except ValueError:
            print('The value for amount of serving should be an integer')
            continue

        # adds the food label and serving amount into the dictionary
        consumption[food_label] = serving

    return consumption


def add_food() -> dict:
    """
    Asks the user if they want to add any additional dish to the csv file and accepts relevant information such as
    calories, carbohydrates, proteins, and fat content. Then appends the information into the csv file.
    """

    # opens the csv file that contains list of food and their nutritional values
    try:
        fh = open('food_nutrition.csv', 'r')

    # returns an error output of -999 if the file does not exist
    except FileNotFoundError:
        print('The file food_nutrition.csv does not exist')
        return

    # finds the the serial number of the last dish in the csv file
    last_line = fh.readlines()[-1]
    last_line_list = last_line.split(', ')
    last_label = last_line_list[0]

    fh.close()

    # creates a serial number for the new dish that the user will add
    if last_label.startswith('D'):
        new_label = 'U1'
    else:
        number = last_label[-1]
        new_number = int(number) + 1
        new_label = 'U' + str(new_number)

    # a dictionary that will contain all the information of the new dish
    new_food = dict()

    # adds the new serial number to the dict
    new_food['label'] = new_label

    # adds the name of the dish
    new_food['name'] = input('Enter the name of the dish: ')

    # adds the calorie content of the dish
    new_food['cal'] = input_pos('Enter the amount of calories the dish contains per serving: ', float)
    new_food['cal'] = str(new_food['cal'])

    # adds the carbohydrate content of the dish
    new_food['carb'] = input_pos('Enter the amount of carbohydrates the dish contains per serving: ', float)
    new_food['carb'] = str(new_food['carb'])

    # adds the protein content of the dish
    new_food['pro'] = input_pos('Enter the amount of proteins the dish contains per serving: ', float)
    new_food['pro'] = str(new_food['pro'])

    # adds the fat content of the dish
    new_food['fat'] = input_pos('Enter the amount of fat the dish contains per serving: ', float)
    new_food['fat'] = str(new_food['fat'])

    # combines all the values of the dictionary new_food into a string
    fh = open('food_nutrition.csv', 'a')
    new_line = ', '.join(list(new_food.values()))

    # the string is appended to the csv file
    fh.write('\n' + new_line)
    fh.close()

    return new_food


def calculating_nutrients(consumption: dict):
    """
    Receives a dictionary containing the food labels and serving amount of the food consumed by user and return a
    dictionary of the total nutritional values that was present in the consumed food

    :param consumption: dictionary containing food labels and serving amount
    :return: a dictionary containing the amount of each consumed nutrition
    """

    # opens the csv file that contains list of food and their nutritional values
    try:
        fh = open('food_nutrition.csv', 'r')

    # returns an error output of -999 if the file does not exist
    except FileNotFoundError:
        print('The file food_nutrition.csv does not exist')
        return

    # creates a variable for each of the nutrients
    cal = 0
    carb = 0
    pro = 0
    fat = 0

    # removes the header of the csv file
    header = fh.readline()

    for line in fh:
        # removes the newline from each line
        food = line[:-1].split(',')
        food_label = food[0]

        # checks if the specific food was consumed by the user
        if food_label in list(consumption.keys()):

            # the nutritional values are multiplied by amount of serving and added to the total nutrient consumption
            serving = consumption[food_label]
            cal += float(food[2]) * serving
            carb += float(food[3]) * serving
            pro += float(food[4]) * serving
            fat += float(food[5]) * serving

    fh.close()

    # creates a dictionary with all the consumed nutrients
    current_nutrients = dict()
    current_nutrients['cal'] = cal
    current_nutrients['carb'] = carb
    current_nutrients['pro'] = pro
    current_nutrients['fat'] = fat

    return current_nutrients


def comparing_range(max: float, min: float, value: float) -> float:
    """
    Calculates how far the value is from the range of a maximum value and a minimum value and returns the difference. If
    the value is within range, 0 is returned

    :param max: maximum value of the range
    :param min: minimum value of the range
    :param value: value of the number
    :return: difference between the value and the range
    """

    # checks if value is greater than max and calculates the difference
    if value > max:
        result = value - max

    # checks if the value is lesser than the min and calculates the difference
    elif value < min:
        result = value - min

    # difference of 0 when value within range
    else:
        result = 0

    return result


def comparing_nutrients(ideal_n: dict, current_n: dict) -> dict:
    """
    Receives two dictionaries of ideal nutrients that should be consumed and current nutrients consumed. Returns a 
    dictionary of excess/deficit nutrients of the user's current diet

    :param ideal_n: dictionary containing ideal nutrients
    :param current_n: dictionary containing current nutrients consumed
    :return: dictionary of excess/deficit nutrients
    """
    # dictionary containing the value of excess/deficit nutrients
    current_status = dict()

    # the difference between ideal and consumption is calculated for all the 4 nutrients
    current_status['cal'] = current_n['cal'] - ideal_n['cal']
    current_status['carb'] = comparing_range(ideal_n['max_carb'], ideal_n['min_carb'], current_n['carb'])
    current_status['pro'] = comparing_range(ideal_n['max_pro'], ideal_n['min_pro'], current_n['pro'])
    current_status['fat'] = comparing_range(ideal_n['max_fat'], ideal_n['min_fat'], current_n['fat'])

    return current_status


def output_nutrients(name: str, name_value: float, value: float, value_unit: str, category: str):
    """
    Receives a series of names and values and prints out certain sentences incorporating the inputs

    :param name: name of the food
    :param name_value: value of a nutrient in food
    :param value: value of current excess/deficit consumption of a nutrient
    :param value_unit: unit of the nutrient
    :param category: the type of nutrient
    :return:
    """

    # prints that too much of a nutrient is being consumed and give advice
    if value > 0:
        print(f"You are consuming {value} {value_unit} of {category}s more than you should.")
        print(f"""Out of all the food that you consume daily, {name} has/have the highest {category} content with 
{name_value} {value_unit} of {category}s per serving. You should consider reducing the consumption of {name}\n""")

    # prints that too less of a nutrient is being consumed and give advice
    elif value < 0:
        print(f"You are consuming {abs(value)} {value_unit} of {category}s less than you should.")
        print(f"""Out of all the food that you consume daily, {name} has/have the highest {category} content with 
{name_value} {value_unit} of {category}s per serving. You should consider increasing the consumption of {name}\n""")

    # prints that sufficient nutrient is being consumed
    else:
        print(f'Congratulations! You are consuming the right amount of {category}s!\n')


def advice(current_s: dict, consumption: dict):
    """
    Receives dictionary of excess/deficit nutrients in user's current diet and the dishes that the user consumes. Prints
    out advices using the function output_nutrients()

    :param current_s: dictionary containing excess/deficit nutrients of current diet
    :param consumption: dictionary containing the food consumed by user
    """

    # opens the csv file that contains list of food and their nutritional values
    try:
        fh = open('food_nutrition.csv', 'r')

    # returns an error output of -999 if the file does not exist
    except FileNotFoundError:
        print('The file food_nutrition.csv does not exist')
        return

    # a dictionary that will contain food with highest nutrients out of the food consumed by user
    max_n = {'cal_name': '', 'cal': 0, 'carb_name': '', 'carb': 0, 'pro_name': '', 'pro': 0, 'fat_name': '', 'fat': 0}

    # skips the header of the csv file
    header = fh.readline()

    for line in fh:
        # removes the newline from the end of the line
        food = line[:-1].split(',')

        # checks if a certain food was consumed by the user
        if food[0] in list(consumption.keys()):

            cal = float(food[2])
            carb = float(food[3])
            pro = float(food[4])
            fat = float(food[5])

            # finds the food with highest calorie
            if cal > max_n['cal']:
                max_n['cal'] = cal
                max_n['cal_name'] = food[1]

            # finds the food with highest carbohydrates
            if carb > max_n['carb']:
                max_n['carb'] = carb
                max_n['carb_name'] = food[1]

            # finds the food with highest proteins
            if pro > max_n['pro']:
                max_n['pro'] = pro
                max_n['pro_name'] = food[1]

            # finds the food with highest fat
            if fat > max_n['fat']:
                max_n['fat'] = fat
                max_n['fat_name'] = food[1]

    fh.close()

    # prints out advices according to the deficit/excess state of nutrients that are consumed
    output_nutrients(max_n['cal_name'], max_n['cal'], current_s['cal'], 'calories', 'calorie')
    output_nutrients(max_n['carb_name'], max_n['carb'], current_s['carb'], 'grams', 'carbohydrate')
    output_nutrients(max_n['pro_name'], max_n['pro'], current_s['pro'], 'grams', 'protein')
    output_nutrients(max_n['fat_name'], max_n['fat'], current_s['fat'], 'grams', 'fat')

    if current_s['cal'] > 0:
        exercises(current_s['cal'])


def exercises(cal: float):
    """
    Receives the amount of excess calories and asks the user if they want advice on the exercises they can do. If yes,
    gives the user a list of exercises and will print how long they have to do their favorite exercise for.

    :param cal: the amount of excess calories consumed by user
    """

    # ask the user if they want to learn about exercises
    answer = input('Do you wish to learn about exercises to burn the excess calories? (y/n): ')
    if answer.lower() == 'y':

        # opens the csv file that contains list of exercises and the calories they burn
        try:
            fh = open('exercises.csv', 'r')

        # returns an error output of -999 if the file does not exist
        except FileNotFoundError:
            print('The file exercises.csv does not exist')
            return

        print('LIST OF EXERCISES')

        # removes the header of the csv file
        header = fh.readline()

        for line in fh:
            # removes the newline from the end of the line
            exercise = line[:-1].split(', ')

            # prints the serial number and the name of the exercises
            print(f'{exercise[0]}: {exercise[1]}')

        fh.close()

        # asks the user their favorite exercise label and their weight
        num_exercise = input_pos('Enter the number of your favorite exercise: ', int)
        weight = input_pos('Enter your weight in weight in lbs: ', float)

        # assigns the user into one of the three weight categories of 125, 155, 185
        if abs(weight - 125) < abs(weight - 155):
            pos = 2
        elif abs(weight - 155) < abs(weight - 185):
            pos = 3
        else:
            pos = 4

        # opens the csv file that contains list of exercises and the calories they burn
        try:
            fh = open('exercises.csv', 'r')

        # returns an error output of -999 if the file does not exist
        except FileNotFoundError:
            print('The file exercises.csv does not exist')
            return

        # removes the header of the csv file
        header = fh.readline()

        # the amount of calorie their favorite exercise will burn in one hour
        cal_burn = 0

        for line in fh:
            # removes the newline from the end of the line
            exercise = line[:-1].split(', ')

            # finds the user's favorite exercise name and the calorie it burns from the list
            if exercise[0] == str(num_exercise):
                cal_burn = int(exercise[pos])
                fav_exercise = exercise[1]

        fh.close()

        # checks if there is an exercise with the label that was given by the user
        if cal_burn == 0:
            print('The exercise number that you entered does not exist.')

        # calculates and prints the number of minutes the user has to perform the exercise
        else:
            time = 60 * (cal/cal_burn)
            print(f'To burn your excess calories, you must do {fav_exercise} for {int(time)} minutes')


# display_bar_graph({'cal': 300, 'carb': -20, 'pro': 20, 'fat': 0})
# output_nutrients('mushroom', '34', -70, 'calorie', 'calorie')

# current_status_test = {'cal': 170, 'carb': 0, 'pro': 0, 'fat': 5}
# consumption_test = {'B2': 0.5, 'B18': 1, 'L14': 2, 'L26': 1, 'L27': 1, 'D2': 1.5, 'D3': 1.5, 'D7': 1, 'D36': 1}

