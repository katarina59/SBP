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

        booking_restrictions = {
            'minimum_nights': uninitialized(minimum_nights),
            'maximum_nights': uninitialized(maximum_nights)
        }

        listing = {
            '_id': listing_id,
            'name': uninitialized(name),
            'price': float(price),
            'booking_restrictions': booking_restrictions,
            'instant_bookable': uninitialized(instant_bookable)
        }

        listings_list.append(listing)

output_file_path = 'C:/Users/PC/Desktop/4GODINA/2semestar/SBP/projekat/Listing.json'

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(listings_list, output_file, indent=4)

print(f"JSON data exported to {output_file_path}")
