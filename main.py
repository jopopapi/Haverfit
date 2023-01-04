import access_file as a


def user_interface():
    print('''Welcome to Haverfit.
This program provides you with information about how healthy you are currently eating. But for this to happen, it needs 
some information from you. Don't worry, this program does not store any private information. :)''')

    ideal_cal = a.user_information_and_cal()
    ideal_nutrients = a.calculating_ideal_nutrients(ideal_cal)
    consumption = a.display_and_receive_food()
    current_nutrients = a.calculating_nutrients(consumption)
    current_status = a.comparing_nutrients(ideal_nutrients, current_nutrients)
    a.advice(current_status, consumption)


user_interface()
