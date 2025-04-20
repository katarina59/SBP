import csv
import json

csv_file_path = 'Listings.csv'

location_list = []

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
        neighbourhood = row[12]
        district = row[13]
        city = row[14]
        latitude = row[15]
        longitude = row[16]

        location = {
            '_id': idx,
            'listing_id': listing_id,
            'neighbourhood': uninitialized(neighbourhood),
            'district': uninitialized(district),
            'city': uninitialized(city),
            'latitude': float(latitude),
            'longitude': float(longitude)
        }

        location_list.append(location)

output_file_path = 'C:/Users/PC/Desktop/4GODINA/2semestar/SBP/projekat/Location.json'

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(location_list, output_file, indent=4)

print(f"JSON data exported to {output_file_path}")
