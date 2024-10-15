from bs4 import BeautifulSoup
import requests

currency_names, currency_prices, currency_descriptions = [], [], []


def get_currencies():
    try:
        url = requests.get('https://markets.businessinsider.com/currencies').text
        html_text = BeautifulSoup(url, 'lxml')
        currencies = html_text.find_all('tr', class_='row-hover')
        for currency in currencies:
            currency_names.append(currency.find('td', class_='table__td bold').a.text[4:])
            currency_prices.append(
                currency.find_all('td', class_="table__td text-right")[4].text.strip().replace(',', ''))
            currency_descriptions.append(currency.find_all('td', class_="table__td text-right")[1].text.strip())

        # USD was not on the website list since everything is in terms of USD
        # It is now being added manually in alphabetical order at a null price
        currency_names.insert(currency_names.index('UNI') + 1, "USD")
        currency_prices.insert(currency_names.index('UNI') + 1, "*")
        currency_descriptions.insert(currency_names.index('UNI') + 1, "United States of America")
        return True
    except requests.ConnectionError:
        print("ERROR: No Connection - Please ensure you are connected to the internet")
        return False


def currency_search(currency):
    index_found = -1

    left, right, middle = 0, (len(currency_names)-1), 0

    while left <= right:
        middle = int((left + right) / 2)

        # Compare ASCII; character by character and conduct necessary adjustment to search area
        # Even though currencies are only of length 3 or 4 I've generalized cases for any length
        for index in range(0, len(currency)):
            # Special Case: If we've reached beyond the length of our middle currency
            # (in other words, what we are searching for is longer than the middle currency)
            if index == len(currency_names[middle]):
                left = middle + 1
                break

            if ord(currency[index]) == ord(currency_names[middle][index]):
                # If everything is equal but the middle currency is actually larger than what we're searching for
                if index == len(currency)-1 and len(currency) < len(currency_names[middle]):
                    right = middle - 1
                # If everything is equal, both currency codes are the same length, and we are at the last character
                # comparison
                elif len(currency) == len(currency_names[middle]) and index == len(currency)-1:
                    index_found = middle
                # No need for breaks above since we'd be at the end of the for loop
                # If no cases are triggered then loop continues
            elif ord(currency[index]) > ord(currency_names[middle][index]):
                left = middle + 1
                break
            elif ord(currency[index]) < ord(currency_names[middle][index]):
                right = middle - 1
                break

        # index_found equalling -1 implies that the currency wasn't found
        if index_found != -1:
            break
    return index_found


def make_conversion(currency_one_index, amount_of_currency_one, currency_two_index):
    # USD is a special case since everything is already in terms of USD
    if currency_names[currency_one_index] == "USD":

        # If user is converting USD to USD (for whatever reason...)
        if currency_prices[currency_two_index] == "*":
            return amount_of_currency_one

        return amount_of_currency_one * float(currency_prices[currency_two_index])
    elif float(currency_prices[currency_one_index]) == 0:
        print(f'The price of {currency_names[currency_one_index]} is near '
              f'zero and can unfortunately not be calculated.\n')
        return -1
    elif currency_names[currency_two_index] == "USD":
        return amount_of_currency_one / float(currency_prices[currency_one_index])

    # Regular conversion equation
    return ((amount_of_currency_one / float(currency_prices[currency_one_index])) *
            float(currency_prices[currency_two_index]))


def commands(text_input):
    if text_input == "-h":
        print("\n-c\tDisplay the list of currency codes")
        print("-r\tRefresh currency exchange rates\n")
    elif text_input == "-q":
        return False
    elif text_input == "-c":
        for index in range(0, len(currency_names)):
            if currency_descriptions[index] == "-":
                print(f'{currency_names[index]}')
            else:
                print(f'{currency_names[index]} -> {currency_descriptions[index]}')
        print("")
    elif text_input == "-r":
        if get_currencies():
            print("Currency exchange rates have been successfully refreshed!\n")
    return True


def is_nan(text):
    for character in text:
        char = ord(character)
        if (char < 48 or char > 57) and char != 46:
            return True
    return False


def input_currency(conversion_type):
    while True:
        user_input = input(f'Input the currency you want to convert {conversion_type}: ')
        if user_input == "-h" or user_input == "-q" or user_input == "-c" or user_input == "-r":
            if not commands(user_input):
                return -1
            continue

        index = currency_search(user_input.upper())
        if index == -1:
            print("ERROR: Invalid Currency - If you need a list of currencies, type '-c'\n")
        else:
            return index


running = get_currencies()
if __name__ == "__main__":
    if running:
        print("Welcome to the Currency Conversion App\n")
    while running:
        print("Type '-h' for help & '-q' to exit")
        keyboard, amount, converted = "", 0, 0.0

        index_one = input_currency("from")
        if index_one == -1:
            break

        valid = False
        while not valid:
            keyboard = input("Input the amount of money you want to convert: ")
            if keyboard == "-h" or keyboard == "-q" or keyboard == "-c" or keyboard == "-r":
                # commands() returning false means quit
                if not commands(keyboard):
                    amount = -1
                    break
                continue

            if is_nan(keyboard):
                print("ERROR: Invalid Number - Please Try Again\n")
            else:
                amount = float(keyboard)
                valid = True

        if amount == -1:
            break

        index_two = input_currency("to")
        if index_two == -1:
            break

        converted = make_conversion(index_one, amount, index_two)
        if converted == -1:
            continue

        print(f'${amount:,.2f} {currency_names[index_one]} is equivalent to ${converted:,.2f} '
              f'{currency_names[index_two]}\n')
