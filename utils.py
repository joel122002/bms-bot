import requests
import logging
from logging.handlers import RotatingFileHandler

# Function to send the message
def send_message(dateCode):
    url = "https://jellyfinn.mooo.com/prod/send-to-user/joelv1202"
    message_data = {
        "message": f"Tickets for {dateCode} are here"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Send the JSON message
    response = requests.post(url, json=message_data, headers=headers)
    
    if response.status_code == 204:
        print(f"Message sent for {dateCode}.")
    else:
        print(f"Failed to send message for {dateCode}.")

def get_nested_value(data, path):
    """
    Retrieves a value from a nested data structure by following a path of keys/indices.
    
    Args:
        data: The nested data structure (dict, list, etc.) to traverse
        path: A list of keys or indices to navigate through the nested structure
        
    Returns:
        The value at the specified path or None if the path is invalid
        
    Example:
        data = {"fruits": [{"label": {"carbohydrates": {"nutrition": 25}}}]}
        get_nested_value(data, ["fruits", 0, "label", "carbohydrates", "nutrition"])
        # Returns 25
    """
    current = data
    
    try:
        for key in path:
            current = current[key]
        return current
    except (KeyError, IndexError, TypeError):
        return None
    
def extract_values_by_key(dict_list, key):
    """
    Extracts all values for a given key from a list of dictionaries.
    
    Args:
        dict_list: A list of dictionaries to extract values from
        key: The key to extract values for
        
    Returns:
        A list containing all values for the specified key
        
    Example:
        movies = [
            {"id": 1, "title": "Inception", "year": 2010},
            {"id": 2, "title": "Interstellar", "year": 2014},
            {"id": 3, "title": "The Dark Knight", "year": 2008}
        ]
        extract_values_by_key(movies, "title")
        # Returns ["Inception", "Interstellar", "The Dark Knight"]
    """
    result = []
    
    # Return empty list if dict_list is None
    if dict_list is None:
        return result
    
    try:
        for item in dict_list:
            # Skip None items
            if item is None:
                continue
            # Ensure item is actually a dictionary before checking for the key
            if isinstance(item, dict) and key in item:
                result.append(item[key])
    except TypeError:
        # Handle case where dict_list is not iterable
        pass
    
    return result

def contains_substring(string_list, substring):
    """
    Checks if any string in the list contains the specified substring (case insensitive).
    
    Args:
        string_list: A list of strings to search through
        substring: The substring to search for
        
    Returns:
        True if any string contains the substring (ignoring case), False otherwise
        
    Example:
        messages = ["Hello world", "Good morning", "Python is fun"]
        contains_substring(messages, "WORLD")  # Returns True
        contains_substring(messages, "java")   # Returns False
    """
    if not string_list or not isinstance(substring, str):
        return False
    
    substring_lower = substring.lower()
    
    try:
        for item in string_list:
            # Skip None items
            if item is None:
                continue
            if isinstance(item, str) and substring_lower in item.lower():
                return True
    except TypeError:
        # Handle case where string_list is not iterable
        return False
    
    return False

def get_logger(name):
    """
    Returns a configured logger with rotating file handler to limit log size.
    
    Args:
        name: The name of the logger and the log file (without .log extension)
        
    Returns:
        A configured logger instance
        
    Example:
        logger = get_logger('bms_bot')  # Creates a logger that writes to bms_bot.log
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Check if logger already has handlers to avoid duplicates
    if not logger.handlers:
        # Rotate when log reaches 5MB, keep 3 backup files
        handler = RotatingFileHandler(f'{name}.log', maxBytes=5*1024*1024, backupCount=3)
        formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger
