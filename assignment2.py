import urllib.request
import csv
import datetime
import logging
import argparse

# Function to download data from a given URL
def downloadData(url):
    response = urllib.request.urlopen(url)  # Open the URL
    return response.read().decode('utf-8')  # Read and decode the content

# Function to process CSV data
def processData(file_content):
    data_dict = {}  # Dictionary to store ID and person info
    logger = logging.getLogger("assignment2")  # Set up logger
    
    lines = file_content.split("\n")  # Split content into lines
    reader = csv.reader(lines)  # Read CSV data
    next(reader)  # Skip the header row
    
    for line_num, row in enumerate(reader, start=1):
        if len(row) < 3:
            continue  # Skip incomplete lines
        
        id_num, name, birthday = row  # Extract values
        try:
            # Convert birthday string into a date object
            birth_date = datetime.datetime.strptime(birthday, "%d/%m/%Y").date()
            data_dict[int(id_num)] = (name, birth_date)  # Store data in dictionary
        except ValueError:
            # Log error if birthday format is incorrect
            logger.error(f"Error processing line #{line_num} for ID #{id_num}")
    
    return data_dict  # Return processed data

# Function to display person details
def displayPerson(id, personData):
    if id in personData:
        name, birth_date = personData[id]  # Retrieve name and birth date
        print(f"Person #{id} is {name} with a birthday of {birth_date}")  # Display details
    else:
        print("No user found with that id")  # Message if ID not found

# Main function to handle user interaction and processing
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="URL of the CSV file")  # Accept URL parameter
    args = parser.parse_args()
    
    logging.basicConfig(filename="errors.log", level=logging.ERROR)  # Configure logging
    
    try:
        csv_data = downloadData(args.url)  # Download CSV data
        personData = processData(csv_data)  # Process data into dictionary
    except Exception as e:
        print(f"Error: {e}")  # Print error and exit if download fails
        return
    
    while True:
        try:
            user_input = int(input("Enter an ID to lookup: "))  # Get user input
            if user_input <= 0:
                break  # Exit if input is 0 or negative
            displayPerson(user_input, personData)  # Display person info
        except ValueError:
            print("Invalid input. Please enter a number.")  # Handle non-numeric input

# Run the program if script is executed directly
if __name__ == "__main__":
    main()
