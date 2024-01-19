from bs4 import BeautifulSoup
import requests

currency_names, currency_prices, currency_descriptions = [], [], []


def get_currencies():
    url = requests.get('https://markets.businessinsider.com/currencies').text
    html_text = BeautifulSoup(url, 'lxml')
    currencies = html_text.find_all('tr', class_='row-hover')
    for currency in currencies:
        currency_names.append(currency.find('td', class_='table__td bold').a.text[4:])
        currency_prices.append(currency.find_all('td', class_="table__td text-right")[4].text.strip().replace(',', ''))
        currency_descriptions.append(currency.find_all('td', class_="table__td text-right")[0].text.strip())

    # USD was not on the website list since everything is in terms of USD
    # It is now being added manually in alphabetical order at a null price
    currency_names.insert(currency_names.index('UNI')+1, "USD")
    currency_prices.insert(currency_names.index('UNI')+1, "*")
    currency_descriptions.insert(currency_names.index('UNI')+1, "United States of America")


def currency_search(currency):
    index_found = -1
    for index in range(0, len(currency_names)):
        if currency == currency_names[index]:
            index_found = index
            break
    return index_found


def make_conversion(currency_one_index, amount_of_currency_one, currency_two_index):
    if float(currency_prices[currency_one_index]) == 0:
        print(f'The price of {currency_names[currency_one_index]} is near '
              f'zero and can unfortunately not be calculated.\n')
        return -1

    # USD is a special case since everything is already in terms of USD
    if currency_names[currency_one_index] == "USD":

        # If user is converting USD to USD (for whatever reason...)
        if currency_prices[currency_two_index] == "*":
            return amount_of_currency_one

        return amount_of_currency_one * float(currency_prices[currency_two_index])
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
        get_currencies()
        print("Currency exchange rates have been successfully refreshed!\n")
    return True


get_currencies()
print("Welcome to the Currency Conversion App\n")
running = True
while running:
    print("Type '-h' for help & '-q' to exit")
    keyboard, index_one, index_two, amount, converted = "", 0, 0, 0.0, 0.0

    valid = False
    while not valid:
        keyboard = input("Input the currency you want to convert from: ")
        if keyboard == "-h" or keyboard == "-q" or keyboard == "-c" or keyboard == "-r":
            running = commands(keyboard)
            if not running:
                break
            continue

        index_one = currency_search(keyboard)
        if index_one == -1:
            print("ERROR: Invalid Currency - If you need a list of currencies, type '-c'")
        else:
            valid = True

    if not running:
        break

    valid = False
    while not valid:
        keyboard = input("Input the amount of money you want to convert: ")
        if keyboard == "-h" or keyboard == "-q" or keyboard == "-c" or keyboard == "-r":
            running = commands(keyboard)
            if not running:
                break
            continue

        if index_one == -1:
            print("ERROR: Invalid Number - Please Try Again")
        else:
            amount = float(keyboard)
            valid = True

    if not running:
        break

    valid = False
    while not valid:
        keyboard = input("Input the currency you want to convert to: ")
        if keyboard == "-h" or keyboard == "-q" or keyboard == "-c" or keyboard == "-r":
            running = commands(keyboard)
            if not running:
                break
            continue

        index_two = currency_search(keyboard)
        if index_one == -1:
            print("ERROR: Invalid Currency - If you need a list of currencies, type '-c'")
        else:
            valid = True

    if not running:
        break

    converted = make_conversion(index_one, amount, index_two)
    if converted == -1:
        continue
    print(f'${amount:,.2f} {currency_names[index_one]} is equivalent to ${converted:,.2f} '
          f'{currency_names[index_two]}\n')
