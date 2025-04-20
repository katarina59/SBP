import csv
import json

csv_file_path = 'Listings.csv'

review_scores_list = []

def uninitialized(value):
    if value == '':
        return None
    try:
        return value
    except ValueError:
        return None 
    
    
def true_false(value):
    if value.lower() == 't':
        return True
    elif value.lower() == 'f':
        return False
    return None

def convert_to_int(value):
    if value == '':
        return None
    try:
        return int(value)
    except ValueError:
        return None 


with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    # Skip the header row
    next(csv_reader)
    
    for idx, row in enumerate(csv_reader, start=1):
        listing_id = row[0]
        review_scores_rating = row[26]
        review_scores_accuracy = row[27]
        review_scores_cleanliness = row[28]
        review_scores_checkin = row[29]
        review_scores_communication = row[30]
        review_scores_location = row[31]
        review_scores_value = row[32]

        review_scores = {
            '_id': idx,
            'listing_id': listing_id,
            'review_scores_rating': convert_to_int(review_scores_rating),
            'review_scores_accuracy': convert_to_int(review_scores_accuracy),
            'review_scores_cleanliness': convert_to_int(review_scores_cleanliness),
            'review_scores_checkin': convert_to_int(review_scores_checkin),
            'review_scores_communication': convert_to_int(review_scores_communication),
            'review_scores_location': convert_to_int(review_scores_location),
            'review_scores_value': true_false(review_scores_value)
        }

        review_scores_list.append(review_scores)

output_file_path = 'C:/Users/PC/Desktop/4GODINA/2semestar/SBP/projekat/ReviewScores.json'

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(review_scores_list, output_file, indent=4)

print(f"JSON data exported to {output_file_path}")
