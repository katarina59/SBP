import csv
import json

csv_file_path = 'Listings.csv'

property_details_list = []

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

with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    # Skip the header row
    next(csv_reader)
    
    for idx, row in enumerate(csv_reader, start=1):
        listing_id = row[0]
        property_type = row[17]
        room_type = row[18]
        accommodates = row[19]
        bedrooms = row[20]
        amenities = row[21].split(',')

        property_details = {
            '_id': idx,
            'listing_id': listing_id,
            'property_type': uninitialized(property_type),
            'room_type': uninitialized(room_type),
            'accommodates': int(accommodates),
            'bedrooms': convert_to_int(bedrooms),
            'amenities': [uninitialized(amenity.strip()) for amenity in amenities if amenity.strip()]
        }

        property_details_list.append(property_details)

output_file_path = 'C:/Users/PC/Desktop/4GODINA/2semestar/SBP/projekat/PropertyDetails.json'

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(property_details_list, output_file, indent=4)

print(f"JSON data exported to {output_file_path}")
