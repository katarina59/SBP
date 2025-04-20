import csv
import json

csv_file_path = 'Reviews.csv'

reviews_list = []

def uninitialized(value):
    if value == '':
        return None
    try:
        return value
    except ValueError:
        return None 

with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    # Skip the header row
    next(csv_reader)
    
    for idx, row in enumerate(csv_reader, start=1):
        listing_id = row[0]
        review_id = row[1]
        date = row[2]
        reviewer_id = row[3]

        review = {
            '_id': idx,
            'listing_id': listing_id,
            'review_id': review_id,
            'date': uninitialized(date),
            'reviewer_id': reviewer_id
        }

        reviews_list.append(review)

output_file_path = 'C:/Users/PC/Desktop/4GODINA/2semestar/SBP/projekat/ListingReview.json'

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(reviews_list, output_file, indent=4)

print(f"JSON data exported to {output_file_path}")
