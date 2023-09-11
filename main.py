import collections
import math
import requests
import re
from bs4 import BeautifulSoup

def calculate_symbol_frequency(text):
    # Calculate symbol frequency
    symbol_frequency = collections.Counter(text)
    return symbol_frequency


def sort_frequency_asc(symbol_frequency):
    # Sort symbol frequency in ascending order
    sorted_frequency = sorted(symbol_frequency.items(), key=lambda x: x[1])
    return sorted_frequency


def display_symbol_frequency(sorted_frequency):
    # Display symbol frequency1
    print('Symbol Frequency:')
    for i, (symbol, frequency) in enumerate(sorted_frequency, start=1):
        print(f"{repr(symbol)}:{frequency}\t", end='' if i % 4 else '\n')
    print()


def calculate_information(text):
    # Calculate information
    symbol_frequency = calculate_symbol_frequency(text)
    total_symbols = len(text)
    information = -sum(
        (frequency / total_symbols) * (math.log2(frequency / total_symbols)) for frequency in symbol_frequency.values())
    return information


def information_print(language, text):
    information = calculate_information(text)
    information = math.floor(information * 10) / 10
    print(f'Information for {language} text: {information}÷{round(information + 0.10001,1)}\n')


def read_file_contents(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def menu():
    print("\nSelect an action:\n1. Input your text\n2. Parse the site\n3. Exit")
    action = input("Your choice: ")
    if action == '1':
        text = input('Enter text: ')
        sorted_frequency = sort_frequency_asc(calculate_symbol_frequency(text))
        display_symbol_frequency(sorted_frequency)
        information = round(calculate_information(text), 1)
        print(f'Information: {information}÷{round(information + 0.10001, 1)}\n')
        menu()
    elif action == '2':
        url = input('Enter URL: ')

        response = requests.get(url)

        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.find('div', {'class': 'mw-parser-output'}).get_text()
            text = re.sub(r'\n', '\\n', text)  # Line break replacement
            text = re.sub(r'\t', '\\t', text)  # Tab replacement
            sorted_frequency = sort_frequency_asc(calculate_symbol_frequency(text))
            display_symbol_frequency(sorted_frequency)
            information = round(calculate_information(text), 1)
            print(f'Information: {information}÷{round(information + 0.10001, 1)}\n')
        else:
            print(f'Error when requesting the site: {response.status_code}')
        menu()
    else:
        exit(0)

if __name__ == '__main__':
    text1_ua = 'text1_ua.txt'
    text1_en = 'text1_en.txt'
    text1_de = 'text1_de.txt'
    text2_ua = 'text2_ua.txt'
    text2_en = 'text2_en.txt'
    text2_de = 'text2_de.txt'
    texts1 = [(read_file_contents(text1_ua), 'Ukrainian'), (read_file_contents(text1_en), 'English'),
              (read_file_contents(text1_de), 'German')]
    texts2 = [(read_file_contents(text2_ua), 'Ukrainian'), (read_file_contents(text2_en), 'English'),
              (read_file_contents(text2_de), 'German')]

    # output all texts 1
    print("\t\tText 1:")
    for text, language in texts1:
        print(f"\t\t{language} text\n{text}\n")
    for text, language in texts1:
        print(f"\t\t{language} text")
        sorted_frequency = sort_frequency_asc(calculate_symbol_frequency(text))
        display_symbol_frequency(sorted_frequency)
        #print(f'Information for {language} text: {calculate_information(text)}\n')
        information_print(language, text)

    # output all texts 2
    print("\t\tText 2:")
    for text, language in texts2:
        print(f"\t\t{language} text\n{text}\n")
    for text, language in texts2:
        print(f"\t\t{language} text")
        sorted_frequency = sort_frequency_asc(calculate_symbol_frequency(text))
        display_symbol_frequency(sorted_frequency)
        #print(f'Information for {language} text: {calculate_information(text)}\n')
        information_print(language, text)

    menu()



