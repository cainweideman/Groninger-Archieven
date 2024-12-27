import json
import os
import re
import tqdm
from llama_index.core import PromptTemplate
from templates.system_message import system_message
from templates.json_schema import json_schema
from templates.prompt import prompt_template
from templates.page_object import create_page_object
from openai import Client, OpenAI


def make_system_message(system_message=system_message, schema=json_schema):
    """
    Generates a system message by formatting a predefined system message template with a given JSON schema.

    This function takes a system message template and a JSON schema, formats the message by inserting the schema into the template, and returns the generated system message.

    Args:
        system_message (str, optional): The template for the system message. Defaults to the predefined `system_message` value.
        schema (dict, optional): The JSON schema that will be inserted into the system message template. Defaults to the predefined `json_schema`.

    Returns:
        str: The formatted system message with the JSON schema inserted into the template.

    Notes:
        - The function uses the `PromptTemplate` class to format the system message template with the JSON schema.
        - If no `system_message` or `schema` is provided, the default `system_message` and `json_schema` values will be used.
    """
    system_prompt = PromptTemplate(system_message)
    evaluated_system_prompt = system_prompt.format(jsonschema=schema)
    return evaluated_system_prompt


def make_human_message(record, template=prompt_template):
    """
    Generates the human input message for a LLM by formatting a provided record using a predefined template.

    This function takes a record (e.g., data or text) and formats it into a prompt message using a specified template. 
    The template is applied using the `PromptTemplate` class, and the resulting message is returned as a string.

    Args:
        record (str or dict): The data or record that will be inserted into the template for message generation.
        template (str, optional): The template used for formatting the record. Defaults to `prompt_template`.

    Returns:
        str: The formatted message with the record inserted into the template.

    Notes:
        - The function uses the `PromptTemplate` class to format the `record` according to the provided `template`.
        - If no template is provided, the default `prompt_template` will be used.
        - The `record` can be a string, dictionary, or any other data type that can be formatted using the specified template.
    """
    prompt = PromptTemplate(template)
    evaluated_human_prompt = prompt.format(record = record)
    return evaluated_human_prompt


def ask_llama(system, user):
    """
    Sends a message to the Llama API to get a response based on system and user messages.

    This function constructs a message with a predefined system instruction and a user-provided input, then sends
    it to the Llama API for processing. The response from the API is returned as a string.

    Args:
        system (str): The system-level message that provides context or instructions for the API model.
        user (str): The user message or query to which the model will respond.

    Returns:
        str or None: The model's response to the user input as a string, or `None` if the API request fails.

    Notes:
        - The function makes use of the `client.chat.completions.create()` method to interact with the Llama model API.
        - If the API request is successful, the function returns the response content as a string.
        - If there is an error with the API request (e.g., network issue, invalid request), the function prints the error
          and returns `None`.

    Exceptions:
        - `Exception`: Any error during the API request (e.g., network failure, invalid parameters) will be caught
          and printed as an error message.
    """
    try:
        messages = [{"role": "system", "content": system}, {"role":"user","content":user}]
        completion = client.chat.completions.create(model=MODEL, messages=messages)
        return completion.choices[0].message.content
    except Exception as e:
        print(f"API request failed: {e}")
        return None


def load_json(path_to_json):
    """
    Loads a JSON file from the specified path.

    This function attempts to read and parse a JSON file from the provided file path. If the file is not found, or if there
    is an issue with the JSON decoding, it will print an error message and return `None`.

    Args:
        path_to_json (str): The path to the JSON file to be loaded.

    Returns:
        dict or None: The parsed JSON data as a Python dictionary if successful, or `None` if an error occurs.

    Notes:
        - The function handles the following exceptions:
            - `FileNotFoundError`: If the file does not exist at the specified path.
            - `json.JSONDecodeError`: If there is an error in the JSON formatting or syntax.
            - `Exception`: Any other unexpected errors that may occur during file loading.
        - If an error occurs, the function prints the appropriate error message and returns `None`.

    Exceptions:
        - `FileNotFoundError`: Raised if the specified file does not exist.
        - `json.JSONDecodeError`: Raised if there is an issue with the JSON structure (e.g., invalid formatting).
        - Other exceptions will be caught by the generic `Exception` handler.
    """
    try:
        with open(path_to_json, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {path_to_json}")
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None


def get_text(data, first_page, last_page):
    """
    Extracts text from a JSON-like data structure for a specified range of pages.

    This function retrieves the text content of the pages specified by `first_page` and `last_page` from the given `data` object.
    It checks the structure of the input data to ensure that it is valid before attempting to extract the text.

    Args:
        data (dict): The JSON-like dictionary containing the document data. It must have a 'content' key with a list of pages.
        first_page (int): The page number to start extracting text from (inclusive).
        last_page (int): The page number to stop extracting text from (inclusive).

    Returns:
        list: A list of text content from the specified range of pages. If the input structure is invalid or the page range is out of bounds, an empty list is returned.

    Notes:
        - The function expects `data` to be a dictionary with a 'content' key containing a list of pages.
        - The function checks that the `content` key exists and is a list. If not, it will print an error message and return an empty list.
        - The page indices in the input data are zero-based, but `first_page` and `last_page` are one-based. The function adjusts for this by using `first_page - 1` when accessing the data.
        - If the page range is out of bounds (i.e., if `first_page` or `last_page` exceed the number of available pages), the function will catch the `IndexError` and return an empty list.

    Exceptions:
        - If `data` is not a dictionary or does not contain the expected 'content' key, an error message will be printed and an empty list will be returned.
        - If the `content` key does not contain a list, an error message will be printed and an empty list will be returned.
    """
    if not isinstance(data, dict) or 'content' not in data:
        print("Invalid JSON structure.")
        return []
    if not isinstance(data['content'], list):
        print("Expected 'content' to be a list.")
        return []
    
    try:
        return [page['text'] for page in data['content'][first_page - 1 : last_page]]
    except IndexError as e:
        print(f"Page range error: {e}")
        return []


def strip_text(text):
    """
    Cleans and preprocesses the input text by removing unwanted characters, replacing newlines, and making specific substitutions.

    This function performs several transformations on the input text:
    - Replaces newline characters (`\n\n` and `\n`) with spaces.
    - Removes newline characters that occur after a hyphen (`-\n`).
    - Replaces curly braces `{` with parentheses `(`.
    - Removes any characters that are not alphanumeric, spaces, commas, periods, parentheses, curly braces, or hyphens.

    Args:
        text (str): The input text to be cleaned.

    Returns:
        str: The cleaned text with unwanted characters removed or replaced.

    Notes:
        - This function removes unwanted special characters and normalizes spacing and line breaks.
        - The function also makes specific replacements such as turning curly braces into parentheses.
    """
    text = re.sub(r'\n\n|\n', ' ', text)
    text = re.sub(r'-\n', '', text)
    text = re.sub(r'{', '(', text)
    
    regex = re.compile(r"[^a-zA-Z0-9\s,.\(\)\{\}'-]")
    return regex.sub('', text)


def remove_phone_numbers(text):
    """
    Removes phone numbers or telephone references from a given text.

    This function searches for patterns commonly associated with telephone numbers (e.g., 'Tel.', 'Telef.', 'Telefoon.')
    followed by one or more digits and removes them from the input text.

    Args:
        text (str): The input text that may contain telephone references or phone numbers to be removed.

    Returns:
        str: The text with phone numbers and telephone references removed.

    Notes:
        - The function is case-insensitive and will match "Tel.", "Telef.", or "Telefoon." followed by digits.
        - The pattern is designed to remove these references, including the spaces and digits following them.
        - If no telephone references are found, the original text will be returned unchanged.
    """
    pattern = r'\b(?:[Tt]el|[Tt]elef|[Tt]elefoon)\.\s*\d+\b'
    return re.sub(pattern, '', text)


def split_text(text):
    """
    Splits the input text into a list of strings, ensuring that house numbers (numbers possibly followed by 
    suffixes like 'a', 'b', etc.) are preserved with the text that precedes them. The function uses a regular 
    expression to identify and split on house numbers while keeping the house number together with the preceding 
    text.

    Args:
        text (str): The input string containing text with possible house numbers.

    Returns:
        list: A list of strings where each string represents a part of the original text, with house numbers 
              preserved with the text before them.

    Example:
        input_text = "John Doe 123A Main St, Jane Smith 456B Elm St"
        result = split_text(input_text)
        print(result)
        # Output: ['John Doe 123A Main St', 'Jane Smith 456B Elm St']

    Notes:
        - The regular expression pattern is designed to identify house numbers which are a sequence of digits
          possibly followed by alphanumeric suffixes (e.g., '123A', '456B').
        - The function ensures that the house numbers are not lost during the splitting process.
        - Any extra whitespace is removed from the resulting list.
    """
    pattern = r'(\s\d+[a-zA-Z0-9]*)\b'
    split_text = re.split(pattern, text)
    combined_text = []
    for i in range(0, len(split_text) - 1, 2):
        combined_text.append(split_text[i] + split_text[i + 1].strip())

    return [line.strip() for line in combined_text if line.strip()]


def format_initials_and_spacing(text):
    """
    Converts a string with capitalized words into a format where each word is followed by a dot. 
    This function adds spaces between words and places dots after each initial capital letter, 
    effectively separating camel case or Pascal case words and ensuring proper punctuation.

    Args:
        text (str): The input string containing capitalized words, which may be in camel case or Pascal case format.

    Returns:
        str: The input string transformed with spaces between words and dots after each capital letter.

    Example:
        input_text = "ThisIsAString"
        result = format_initials_and_spacing(input_text)
        print(result)  # Output: "This. Is. A. String."

    Notes:
        - This function assumes that the input text contains capitalized words without spaces between them (e.g., camel case).
        - The function handles cases where spaces after periods are missing and ensures the formatting of capitalized initials.
        - The transformation adds dots after each capitalized letter (unless it's already followed by a dot).
    """
    text = re.sub(r'(?<=[.])(?=[^\s])', r' ', text)
    text = re.sub(r'\s+', ' ', text)
    return re.sub(r'(?<=[A-Z])(?!\.)\b', '.', text)


def strip_left_side(sentence):
    """
    Removes any non-alphabetical characters from the beginning (left side) of a given string. 
    This function strips the sentence of unwanted characters such as spaces, punctuation, 
    or numbers that appear before the first alphabetical character.

    Args:
        sentence (str): The input string from which to remove non-alphabetical characters from the beginning.

    Returns:
        str: The input string with any leading non-alphabetical characters removed.

    Example:
        input_string = " 1234Hello World!"
        result = strip_left_side(input_string)
        print(result)  # Output: "Hello World!"

    Notes:
        - The function only removes characters at the beginning of the string.
        - If the string starts with an alphabetic character, it returns the string unchanged.
        - The regular expression `^[^a-zA-Z]+` matches any characters that are not alphabetical (i.e., from `A-Z` and `a-z`) at the beginning of the string.
    """
    return re.sub(r'^[^a-zA-Z]+', '', sentence)


def fix_ocr_mistakes(text):
	"""
    Replaces occurrences of specific digits inside parentheses with the letter 'J'.
    Specifically, it replaces the digit '1' with 'J.', and '3' or '4' with 'J', within parentheses.

    Args:
        text (str): The input string containing text with parentheses and digits.

    Returns:
        str: The updated text where the specified digits inside parentheses are replaced with 'J'.

    Example:
        input_text = "This is a test (H. 1) and another (value 3)."
        result = replace_digits_parentheses(input_text)
        print(result)  # Output: "This is a test (H. J.) and another (value J)."

    Notes:
        - The function specifically looks for digits '1', '3', or '4' inside parentheses and replaces them.
        - The replacement uses the regular expression `\(.*[134].*\)` to match any occurrence of '1', '3', or '4' inside parentheses.
        - The lambda function is used to apply the replacements only to the matched text within parentheses.
    """
	updated_text = re.sub(r'\(.*[134].*\)', lambda match: match.group(0).replace('1', 'J.').replace('3', 'J').replace('4', 'J'), text)
	return updated_text


def process_page(page):
    """
    Processes a page of text by applying a series of text cleaning and formatting operations.
    The function removes phone numbers, strips unwanted characters, splits the text into lines, 
    and filters the lines based on specific conditions.

    Args:
        page (str): The input string representing the content of a page that needs processing.

    Returns:
        list: A list of cleaned and formatted lines from the page that contain parentheses 
              and have a length between 15 and 150 characters.

    Notes:
        - The function first removes phone numbers using the `remove_phone_numbers` function.
        - It then strips unwanted characters (e.g., special characters) using the `strip_text` function.
        - The text is split into individual lines using the `split_text` function.
        - The function filters the lines to include only those that contain parentheses '(' or ')' and 
          have a length between 15 and 150 characters.
        - If an error occurs during the processing, an empty list is returned and the error is printed.

    Exceptions:
        - If the page is empty or `None`, the function returns an empty list.
        - In case of any other error during processing, the function catches the exception and prints the error message.
    """
    if not page:
        return []

    try:
        page = remove_phone_numbers(strip_text(page))
        page_lines = split_text(page)
        return [strip_left_side(line) for line in page_lines if '(' in line or ')' in line and 15 < len(line) < 150]
    except Exception as e:
        print(f"Error processing page: {e}")
        return []


def preprocess_line(line):
    """
    Preprocesses a line of text by applying a series of text corrections and formatting operations. 
    This includes fixing OCR mistakes and adjusting the spacing and formatting of initials.

    Args:
        line (str): The input string representing a line of text that needs preprocessing.

    Returns:
        str: The processed line of text after applying OCR fixes and formatting changes.

    Notes:
        - The function first applies the `fix_ocr_mistakes` function to correct common OCR errors (e.g., replacing 
          digits with letters).
        - It then applies the `format_initials_and_spacing` function to add spaces and periods after capitalized 
          initials, improving the readability of the text.
    """
    line = fix_ocr_mistakes(line)
    line = format_initials_and_spacing(line)
    return line


def process_line(line):
    """
    Processes a line of text by sending it to a language model and extracting structured data from the model's response.
    The function generates a system and human message, sends them to the model, and attempts to parse the JSON-like 
    objects from the output to build a list of person records.

    Args:
        line (str): The input line of text to be processed by the language model.

    Returns:
        list: A list of dictionaries (person records) parsed from the model's response.

    Notes:
        - The function first generates a system and human message using the input line and predefined templates.
        - It then sends the generated messages to a language model (e.g., Llama) to process the information.
        - The model's response is expected to contain one or more JSON-like objects. These objects are extracted using a
          regular expression and parsed into Python dictionaries.
        - In case of an error (e.g., empty response or JSON parsing error), the function will print an error message and 
          return an empty list.

    Exceptions:
        - If the model's response is empty, an error message is printed and an empty list is returned.
        - If parsing the JSON data fails, an error message is printed and the function proceeds without adding any records 
          to the list.
    """
    person_list = []
    system_message = make_system_message
    human_message = make_human_message(line)
    output = ask_llama(system_message, human_message)

    if not output:
        print("Empty response from language model.")
        return person_list

    try:
        json_objects = re.findall(r'\{.*?\}', output, re.DOTALL)
        for obj in json_objects:
            person_list.append(json.loads(obj))
    except Exception as e:
            print(f"Error parsing JSON from model response: {e}")
    
    return person_list


def create_page_json(person_list, page_number, year, output_directory):
    """
    Creates a JSON file containing structured data for a specific page of a document, and saves it to the specified 
    output directory. The data includes information about the people listed on the page, the page number, and the 
    year of the document.

    Args:
        person_list (list): A list of dictionaries representing person records (e.g., names, addresses, etc.).
        page_number (int): The page number of the document being processed.
        year (int): The year associated with the document or page.
        output_directory (str): The directory where the JSON file will be saved. If the directory doesn't exist, 
                                it will be created.

    Notes:
        - The function first checks if the output directory exists; if not, it will be created.
        - It then generates a page object using the provided `person_list`, `page_number`, and `year`.
        - The page object is serialized into a JSON file with the format: `{year}_{page_number}.json`.
        - If there is an error during file creation or writing, an error message is printed.
        - The resulting JSON file will contain structured information about the people on the page and will be saved
          in the specified directory with a filename format that includes the year and page number.

    Exceptions:
        - If there is an error creating the output directory or saving the JSON file, an error message is printed.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory, exist_ok=True)

    page_object = create_page_object(person_list, page_number, year)

    try:
        json_filename = f'{output_directory}/{year}_{page_number}.json'
        with open(json_filename, 'w+') as output_file:
            json.dump(page_object, output_file, indent=4)
    except Exception as e:
        print(f"Failed to save JSON file: {e}")


BASEURL = 'http://localhost:8000/v1/'
APIKEY = 'EMPTY'
MODEL = "meta-llama/Llama-3.1-8B-Instruct"

client = OpenAI(base_url=BASEURL,api_key=APIKEY)

year = "1886"
path_to_json = f"book_text/{year}.json"
output_directory = f'register/{year}'

data = load_json(path_to_json)
first_page, last_page = 44, 45

if data:
    text_list = get_text(data, first_page, last_page)
    for index, page in tqdm(enumerate(text_list), total=len(text_list), desc='Processing Pages', unit='page', ncols=100):
        person_list = []
        page_number = first_page + index
        page_lines = process_page(page)
        for line in page_lines:
            person_list.append(process_line(preprocess_line(line)))
        create_page_json(person_list, page_number, year, output_directory)