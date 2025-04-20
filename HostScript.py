import csv
import json

csv_file_path = 'Listings.csv'

host_list = []

def unitialized(value):
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
        listing_id = row[0]  # Uklonjen zarez iza definicije listing_id
        host_id = row[2]
        host_since = row[3]
        host_location = row[4]
        host_response_time = row[5]
        host_response_rate = row[6]
        host_acceptance_rate = row[7]
        host_is_superhost = row[8]
        host_total_listings_count = row[9]
        host_has_profile_pic = row[10]
        host_identity_verified = row[11]

           

        host = {
            '_id': host_id,
            'listing_id': listing_id,
            'host_since': unitialized(host_since),
            'host_location': unitialized(host_location),
            'host_response_time': unitialized(host_response_time),
            'host_response_rate': convert_to_int(host_response_rate),
            'host_acceptance_rate': convert_to_int(host_acceptance_rate),
            'host_is_superhost': true_false(host_is_superhost),
            'host_total_listings_count': convert_to_int(host_total_listings_count),
            'host_has_profile_pic': true_false(host_has_profile_pic),
            'host_identity_verified': true_false(host_identity_verified)
        }

          
        host_list.append(host)
            

       
output_file_path = 'C:/Users/PC/Desktop/4GODINA/2semestar/SBP/projekat/Host.json'

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(host_list, output_file, indent=4)

print(f"JSON data exported to {output_file_path}")