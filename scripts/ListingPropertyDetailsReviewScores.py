import csv
import json

csv_file_path = 'Listings.csv'

listings_list = []

def uninitialized(value):
    if value == '':
        return None
    try:
        return value
    except ValueError:
        return None
    
def convert_to_int(value):
    if value == '':
        return None
    try:
        return int(value)
    except ValueError:
        return None 

def true_false(value):
    if value.lower() == 't':
        return True
    elif value.lower() == 'f':
        return False
    return None


with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    # Skip the header row
    next(csv_reader)
    
    for idx, row in enumerate(csv_reader, start=1):
        listing_id = row[0]
        name = row[1]
        price = row[24]
        minimum_nights = row[25]
        maximum_nights = row[26]
        instant_bookable = row[27]
        property_type = row[17]
        room_type = row[18]
        accommodates = row[19]
        bedrooms = row[20]
        amenities = row[21].split(',')
        review_scores_rating = row[26]
        review_scores_accuracy = row[27]
        review_scores_cleanliness = row[28]
        review_scores_checkin = row[29]
        review_scores_communication = row[30]
        review_scores_location = row[31]
        review_scores_value = row[32]

        booking_restrictions = {
            'minimum_nights': uninitialized(minimum_nights),
            'maximum_nights': uninitialized(maximum_nights)
        }

        property_details = {
            'property_type': uninitialized(property_type),
            'room_type': uninitialized(room_type),
            'accommodates': int(accommodates),
            'bedrooms': convert_to_int(bedrooms),
            'amenities': [uninitialized(amenity.strip()) for amenity in amenities if amenity.strip()]
        }

        review_scores = {
            'review_scores_rating': convert_to_int(review_scores_rating),
            'review_scores_accuracy': convert_to_int(review_scores_accuracy),
            'review_scores_cleanliness': convert_to_int(review_scores_cleanliness),
            'review_scores_checkin': convert_to_int(review_scores_checkin),
            'review_scores_communication': convert_to_int(review_scores_communication),
            'review_scores_location': convert_to_int(review_scores_location),
            'review_scores_value': true_false(review_scores_value)
        }

        listing = {
            '_id': listing_id,
            'name': uninitialized(name),
            'price': float(price),
            'booking_restrictions': booking_restrictions,
            'instant_bookable': uninitialized(instant_bookable),
            "property_details": property_details,
            "review_scores": review_scores
        }

        listings_list.append(listing)

output_file_path = "./ListingPropertyDetailsReviewScores.json"

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(listings_list, output_file, indent=4)

print(f"JSON data exported to {output_file_path}")
