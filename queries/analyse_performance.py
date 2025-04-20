from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db1 = client['airbnb']
db2 = client['airbnb-optimizovano']
date1 = "2021-01-01T00:00:00.000+0000"
date2 = "2022-01-01T00:00:00.000+0000"
date_format = "%Y-%m-%dT%H:%M:%S.%f%z"

queries_pre_optimization = [
    # QUERY 1
    [
        {"$match": {"host_is_superhost": True}},
        {"$lookup": {"from": "Listing", "localField": "listing_id", "foreignField": "_id", "as": "listing_info"}},
        {"$match": {"host_is_superhost": True}},
        {"$lookup": {"from": "Listing", "localField": "listing_id", "foreignField": "_id", "as": "listing_info"}},
        {"$unwind": "$listing_info"},
        {"$lookup": {"from": "Location", "localField": "listing_id", "foreignField": "listing_id", "as": "location_info"}},
        {"$unwind": "$location_info"},
        {"$group": {
            "_id": "$location_info.city",
            "avg_city_price": {"$avg": "$listing_info.price"},
            "listings": {
                "$push": {
                    "listing_id": "$listing_info._id",
                    "listing_name": "$listing_info.name",
                    "listing_price": "$listing_info.price",
                    "location_info": "$location_info"
                }
            }
         }},
        {"$unwind": "$listings"},
        {"$project": {
            "city": "$_id",
            "avg_city_price": 1,
            "listing_id": "$listings.listing_id",
            "listing_name": "$listings.listing_name",
            "listing_price": "$listings.listing_price",
            "below_avg": {"$lt": ["$listings.listing_price", "$avg_city_price"]}
        }},
        {"$match": {"below_avg": True}},
        {"$project": {"_id": 0, "listing_id": 1, "listing_name": 1}}
    ],
    # QUERY 2
   [
    {"$addFields": {"reviewDate": {"$toDate": "$date"}}},
    {"$match": {"reviewDate": {"$gte": datetime.strptime(date1, date_format), "$lt": datetime.strptime(date2,date_format)}}},
    {"$lookup": {"from": "Location", "localField": "listing_id", "foreignField": "listing_id", "as": "location_info"}},
    {"$unwind": "$location_info"},
    {"$match": {"location_info.city": "Paris"}},
    {"$group": {"_id": "$location_info.city", "total_reviews": {"$sum": 1}, "unique_listings": {"$addToSet": "$listing_id"}}},
    {"$addFields": {"total_listings": {"$size": "$unique_listings"}}},
    {"$project": {"_id": 1, "total_reviews": 1, "total_listings": 1}}
    ],

    # QUERY 3
   [
    {"$match": {"accommodates": {"$exists": True, "$ne": None, "$gt": 2}}},
    {"$lookup": {"from": "ReviewScores", "localField": "listing_id", "foreignField": "listing_id", "as": "reviews_details"}},
    {"$unwind": "$reviews_details"},
    {"$match": {"reviews_details.review_scores_cleanliness": {"$exists": True, "$ne": None, "$gt": 9}}},
    {"$lookup": {"from": "Location", "localField": "listing_id", "foreignField": "listing_id", "as": "location_details"}},
    {"$unwind": "$location_details"},
    {"$addFields": {"city": "$location_details.city", "neighbourhood": "$location_details.neighbourhood"}},
    {"$project": {"_id": 0, "city": 1, "neighbourhood": 1, "listing_id": 1}},
    {"$match": {"city": "New York"}},
    {"$group": {"_id": "$neighbourhood", "total_listings": {"$sum": 1}}},
    {"$project": {"_id": 0, "neighbourhood": "$_id", "total_listings": {"$toInt": "$total_listings"}}}
    ],    

    # QUERY 4
    [
        {"$lookup": {"from": "Location", "localField": "listing_id", "foreignField": "listing_id", "as": "location_details"}},
        {"$unwind": "$location_details"},
        {"$addFields": {"city": "$location_details.city"}},
        {"$match": {"city": "Rome"}},
        {"$lookup": {"from": "Listing", "localField": "listing_id", "foreignField": "_id", "as": "listing_details"}},
        {"$unwind": "$listing_details"},
        {"$addFields": {"price_per_week": {"$multiply": ["$listing_details.price", 7]}}},
        {"$group": {"_id": "$room_type", "average_price_per_week": {"$avg": "$price_per_week"}, "total_listings": {"$sum": 1}}},
        {"$addFields": {"average_price_per_week": {"$round": ["$average_price_per_week", 2]}}},
        {"$project": {"_id": 0, "room_type": "$_id", "average_price_per_week": 1, "total_listings": {"$toInt": "$total_listings"}}}
    ],
    # QUERY 5  
    [
    {"$lookup": {"from": "ReviewScores", "localField": "_id", "foreignField": "listing_id", "as": "review_scores"}},
    {"$unwind": "$review_scores"},
    {"$lookup": {"from": "Location", "localField": "_id", "foreignField": "listing_id", "as": "location_details"}},
    {"$unwind": "$location_details"},
    {"$group": {
        "_id": "$location_details.city",
        "avgPrice": {"$avg": "$price"},
        "aboveAvgCount": {
            "$sum": {
                "$cond": {
                    "if": {
                        "$and": [
                            {"$gt": ["$price", "$avgPrice"]},
                            {"$lt": ["$review_scores.review_scores_rating", 60]}
                        ]
                    },
                    "then": 1,
                    "else": 0
                }
            }
        },
        "totalListings": {"$sum": 1}
    }},
    {"$addFields": {
        "percentage": {
            "$multiply": [
                {"$divide": ["$aboveAvgCount", "$totalListings"]},
                100
            ]
        }
    }},
    {"$project": {
        "_id": 0,
        "city": "$_id",
        "avgPrice": {"$round": ["$avgPrice", 2]},
        "aboveAvgCount": {"$toInt": "$aboveAvgCount"},
        "percentage": {"$round": ["$percentage", 2]}
    }}
    ],

    # QUERY 6
    [
        {"$match": {"city": {"$in": ["Paris", "Sydney", "New York"]}}},
        {"$lookup": {"from": "ReviewScores", "localField": "listing_id", "foreignField": "listing_id", "as": "review_scores_info"}},
        {"$unwind": "$review_scores_info"},
        {"$match": {"review_scores_info.review_scores_accuracy": {"$gt": 9}}},
        {"$lookup": {"from": "PropertyDetails", "localField": "listing_id", "foreignField": "listing_id", "as": "property_details"}},
        {"$unwind": "$property_details"},
        {"$addFields": {"broj_pogodnosti": {"$size": "$property_details.amenities"}}},
        {"$group": {"_id": "$city", "avg_amenities": {"$avg": "$broj_pogodnosti"}}},
        {"$project": {"_id": 0, "grad": "$_id", "prosečan_broj_pogodnosti": "$avg_amenities"}}
    ],

    # QUERY 7
    [
        {"$match": {"host_since": {"$ne": None}}},
        {"$sort": {"host_since": 1}},
        {"$limit": 10},
        {"$lookup": {"from": "ListingPropertyDetailsReviewScores", "localField": "listing_id", "foreignField": "_id", "as": "optimal"}},
        {"$unwind": "$optimal"},
        {"$match": {"optimal.review_scores.review_scores_cleanliness": {"$ne": None}, "optimal.review_scores.review_scores_accuracy": {"$ne": None}}},
        {"$group": {
            "_id": {"host_id": "$_id", "registrationDate": "$host_since"},
            "avg_cleanliness": {"$avg": "$optimal.review_scores.review_scores_cleanliness"},
            "avg_accuracy": {"$avg": "$optimal.review_scores.review_scores_accuracy"}
        }},
        {"$project": {
            "_id": 0,
            "host_id": "$_id.host_id",
            "registrationDate": "$_id.registrationDate",
            "avg_cleanliness": {"$round": ["$avg_cleanliness", 0]},
            "avg_accuracy": {"$round": ["$avg_accuracy", 0]}
        }}
    ],

    # QUERY 8
    [
        {"$addFields": {"reviewDate": {"$toDate": "$date"}}},
        {"$match": {"reviewDate":  {"$gte": datetime.strptime(date1, date_format), "$lt": datetime.strptime(date2,date_format)}}},
        {"$lookup": {"from": "Host", "localField": "listing_id", "foreignField": "listing_id", "as": "host_details"}},
        {"$unwind": "$host_details"},
        {"$lookup": {"from": "ReviewScores", "localField": "listing_id", "foreignField": "listing_id", "as": "review_details"}},
        {"$unwind": "$review_details"},
        {"$addFields": {"host_is_superhost": "$host_details.host_is_superhost", "host_total_listings_count": "$host_details.host_total_listings_count", "admin_review": "$review_details.review_scores_communication"}},
        {"$match": {"host_is_superhost": True, "admin_review": {"$lt": 9}}},
        {"$group": {"_id": None, "total_reviewers": {"$sum": 1}}},
        {"$project": {"_id": 0, "total_reviewers": 1}}

    ],

    # QUERY 9
    [
        {"$match": {
            "property_details.property_type": "Private room in house",
            "$expr": {
                "$gt": [
                    {
                        "$cond": {
                            "if": { "$isArray": "$property_details.amenities" },
                            "then": { "$size": "$property_details.amenities" },
                            "else": 0
                        }
                    },
                    15
                ]
            }
        }},
        {"$lookup": {
            "from": "Host",
            "localField": "_id",
            "foreignField": "listing_id",
            "as": "host_info"
        }},
        {"$unwind": "$host_info"},
        {"$sort": {
            "host_info.host_total_listings_count": -1
        }},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "host_id": "$host_info._id",
            "host_address": "$host_info.host_location"
        }}
    ],
    # QUERY 10
    [
    {"$lookup": {"from": "Listing", "localField": "listing_id", "foreignField": "_id", "as": "listing_info"}},
    {"$unwind": "$listing_info"},
    {"$group": {"_id": "$property_type", "avg_price": {"$avg": "$listing_info.price"}, "min_nights": {"$avg": {"$toInt": "$listing_info.booking_restrictions.minimum_nights"}}, "max_nights": {"$avg": {"$toInt": "$listing_info.booking_restrictions.maximum_nights"}}}},
    {"$addFields": {"night_difference": {"$subtract": ["$min_nights", "$max_nights"]}}},
    {"$group": {"_id": "$_id", "avg_price": {"$first": "$avg_price"}, "average_night_difference": {"$avg": "$night_difference"}}},
    {"$addFields": {"average_night_difference": {"$round": ["$average_night_difference", 0]}}},
    {"$match": {"average_night_difference": {"$ne": None}}},
    {"$sort": {"avg_price": -1}},
    {"$limit": 10},
    {"$project": {"_id": 1, "avg_price": 1, "average_night_difference": 1}}
    ]


    
]

# LIST OF QUERIES AFTER OPITIMIZATION
queries_post_optimization = [
    # QUERY-OPT 1
    [
        { "$match": { "host_is_superhost": True } },
        { "$lookup": { "from": "ListingPropertyDetailsReviewScores", "localField": "listing_id", "foreignField": "_id", "as": "listing_info" } },
        { "$unwind": "$listing_info" },
        { "$lookup": { "from": "Location", "localField": "listing_id", "foreignField": "listing_id", "as": "location_info" } },
        { "$unwind": "$location_info" },
        {
            "$group": {
                "_id": "$location_info.city",
                "avg_city_price": { "$avg": "$listing_info.price" },
                "listings": {
                    "$push": {
                        "listing_id": "$listing_info._id",
                        "listing_name": "$listing_info.name",
                        "listing_price": "$listing_info.price",
                        "location_info": "$location_info"
                    }
                }
            }
        },
        { "$unwind": "$listings" },
        {
            "$project": {
                "city": "$_id",
                "avg_city_price": 1,
                "listing_id": "$listings.listing_id",
                "listing_name": "$listings.listing_name",
                "listing_price": "$listings.listing_price",
                "below_avg": { "$lt": ["$listings.listing_price", "$avg_city_price"] }
            }
        },
        { "$match": { "below_avg": True } },
        { "$project": { "_id": 0, "listing_id": 1, "listing_name": 1 } }
    ],

    # QUERY-OPT 2
    [
        { "$addFields": { "reviewDate": { "$toDate": "$date" } } },
        {
            "$match": {
                "reviewDate": {"$gte": datetime.strptime(date1, date_format), "$lt": datetime.strptime(date2,date_format)
                }
            }
        },
        { "$lookup": { "from": "Location", "localField": "listing_id", "foreignField": "listing_id", "as": "location_info" } },
        { "$unwind": "$location_info" },
        { "$match": { "location_info.city": "Paris" } },
        {
            "$group": {
                "_id": "$location_info.city",
                "total_reviews": { "$sum": 1 },
                "unique_listings": { "$addToSet": "$listing_id" }
            }
        },
        { "$addFields": { "total_listings": { "$size": "$unique_listings" } } },
        {
            "$project": {
                "_id": 1,
                "total_reviews": 1,
                "total_listings": 1
            }
        }
    ],

    #  QUERY-OPT 3
    [
        { "$match": { "property_details.accommodates": { "$exists": True, "$ne": None, "$gt": 2 } } },
        { "$match": { "review_scores.review_scores_cleanliness": { "$exists": True, "$ne": None, "$gt": 9 } } },
        { "$lookup": { "from": "Location", "localField": "_id", "foreignField": "listing_id", "as": "location_details" } },
        { "$unwind": "$location_details" },
        { "$addFields": { "city": "$location_details.city", "neighbourhood": "$location_details.neighbourhood" } },
        { "$project": { "_id": 0, "city": 1, "neighbourhood": 1, "listing_id": 1 } },
        { "$match": { "city": "New York" } },
        { "$group": { "_id": "$neighbourhood", "total_listings": { "$sum": 1 } } },
        { "$project": { "_id": 0, "neighbourhood": "$_id", "total_listings": { "$toInt": "$total_listings" } } }
    ],
  
    #  QUERY-OPT 4
    [
        { "$lookup": { "from": "Location", "localField": "_id", "foreignField": "listing_id", "as": "location_details" } },
        { "$unwind": "$location_details" },
        { "$addFields": { "city": "$location_details.city" } },
        { "$match": { "city": "Rome" } },
        { "$addFields": { "price_per_week": { "$multiply": ["$price", 7] } } },
        {
            "$group": {
                "_id": "$property_details.room_type",
                "average_price_per_week": { "$avg": "$price_per_week" },
                "total_listings": { "$sum": 1 }
            }
        },
        { "$addFields": { "average_price_per_week": { "$round": ["$average_price_per_week", 2] } } },
        {
            "$project": {
                "_id": 0,
                "room_type": "$_id",
                "average_price_per_week": 1,
                "total_listings": { "$toInt": "$total_listings" }
            }
        }
    ],

    #  QUERY-OPT 5
    [
        { "$lookup": { "from": "Location", "localField": "_id", "foreignField": "listing_id", "as": "location_details" } },
        { "$unwind": "$location_details" },
        {
            "$group": {
                "_id": "$location_details.city",
                "avgPrice": { "$avg": "$price" },
                "aboveAvgCount": {
                    "$sum": {
                        "$cond": {
                            "if": {
                                "$and": [
                                    { "$gt": ["$price", "$avgPrice"] },
                                    { "$lt": ["$review_scores.review_scores_accuracy", 7] }
                                ]
                            },
                            "then": 1,
                            "else": 0
                        }
                    }
                },
                "totalListings": { "$sum": 1 }
            }
        },
        {
            "$addFields": {
                "percentage": {
                    "$multiply": [
                        { "$divide": ["$aboveAvgCount", "$totalListings"] },
                        100
                    ]
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "city": "$_id",
                "avgPrice": { "$round": ["$avgPrice", 2] },
                "aboveAvgCount": { "$toInt": "$aboveAvgCount" },
                "percentage": { "$round": ["$percentage", 2] }
            }
        }
    ],

    #  QUERY-OPT 6
    [
        { "$match": { "city": { "$in": ["Paris", "Sydney", "New York"] } } },
        { "$lookup": { "from": "ListingPropertyDetailsReviewScores", "localField": "listing_id", "foreignField": "_id", "as": "optimal" } },
        { "$unwind": "$optimal" },
        { "$match": { "optimal.review_scores.review_scores_accuracy": { "$gt": 9 } } },
        { "$addFields": { "broj_pogodnosti": { "$size": "$optimal.property_details.amenities" } } },
        {
            "$group": {
                "_id": "$city",
                "avg_amenities": { "$avg": "$broj_pogodnosti" }
            }
        },
        {
            "$project": {
                "_id": 0,
                "grad": "$_id",
                "prosečan_broj_pogodnosti": { "$round": ["$avg_amenities", 2] }
            }
        }
    ],

    #  QUERY-OPT 7
    [
        { "$match": { "host_since": { "$ne": None } } },
        { "$sort": { "host_since": 1 } },
        { "$limit": 10 },
        { "$lookup": { "from": "ListingPropertyDetailsReviewScores", "localField": "listing_id", "foreignField": "_id", "as": "optimal" } },
        { "$unwind": "$optimal" },
        {
            "$match": {
                "optimal.review_scores.review_scores_cleanliness": { "$ne": None },
                "optimal.review_scores.review_scores_accuracy": { "$ne": None }
            }
        },
        {
            "$group": {
                "_id": {
                    "host_id": "$_id",
                    "registrationDate": "$host_since"
                },
                "avg_cleanliness": { "$avg": "$optimal.review_scores.review_scores_cleanliness" },
                "avg_accuracy": { "$avg": "$optimal.review_scores.review_scores_accuracy" }
            }
        },
        {
            "$project": {
                "_id": 0,
                "host_id": "$_id.host_id",
                "registrationDate": "$_id.registrationDate",
                "avg_cleanliness": { "$round": ["$avg_cleanliness", 0] },
                "avg_accuracy": { "$round": ["$avg_accuracy", 0] }
            }
        }
    ],

    #  QUERY-OPT 8
    [
        { "$addFields": { "reviewDate": { "$toDate": "$date" } } },
        {
            "$match": {
                "reviewDate":  {"$gte": datetime.strptime(date1, date_format), "$lt": datetime.strptime(date2,date_format)}
            }
        },
        { "$lookup": { "from": "Host", "localField": "listing_id", "foreignField": "listing_id", "as": "host_details" } },
        { "$unwind": "$host_details" },
        { "$lookup": { "from": "ListingPropertyDetailsReviewScores", "localField": "listing_id", "foreignField": "_id", "as": "review_details" } },
        { "$unwind": "$review_details" },
        {
            "$addFields": {
                "host_is_superhost": "$host_details.host_is_superhost",
                "host_total_listings_count": "$host_details.host_total_listings_count",
                "admin_review": "$review_details.review_scores.review_scores_communication"
            }
        },
        {
            "$match": {
                "host_is_superhost": True,
                "admin_review": { "$lt": 9 }
            }
        },
        { "$group": { "_id": None, "total_reviewers": { "$sum": 1 } } },
        { "$project": { "_id": 0, "total_reviewers": 1 } }
    ],

    #  QUERY-OPT 9
    [
        {
            "$match": {
                "property_details.property_type": "Private room in house",
                "$expr": {
                    "$gt": [
                        { "$cond": { "if": { "$isArray": "$property_details.amenities" }, "then": { "$size": "$property_details.amenities" }, "else": 0 } },
                        15
                    ]
                }
            }
        },
        { "$lookup": { "from": "Host", "localField": "_id", "foreignField": "listing_id", "as": "host_info" } },
        { "$unwind": "$host_info" },
        { "$sort": { "host_info.host_total_listings_count": -1 } },
        { "$limit": 10 },
        {
            "$project": {
                "_id": 0,
                "host_id": "$host_info._id",
                "host_address": "$host_info.host_location"
            }
        }
    ],

    #  QUERY-OPT 10
    [
        {"$group": {"_id": "$property_details.property_type", "avg_price": {"$avg": "$price"}, "min_nights": {"$avg": {"$toInt": "$booking_restrictions.minimum_nights"}}, "max_nights": {"$avg": {"$toInt": "$booking_restrictions.maximum_nights"}}}},
        {"$addFields": {"night_difference": {"$subtract": ["$min_nights", "$max_nights"]}}},
        {"$group": {"_id": "$_id", "avg_price": {"$first": "$avg_price"}, "average_night_difference": {"$avg": "$night_difference"}}},
        {"$addFields": {"average_night_difference": {"$round": ["$average_night_difference", 0]}, "avg_price": {"$round": ["$avg_price", 2]}}},
        {"$match": {"average_night_difference": {"$ne": None}}},
        {"$sort": {"avg_price": -1}},
        {"$limit": 10},
        {"$project": {"_id": 1, "avg_price": 1, "average_night_difference": 1}}
    ]
    
]

def get_execution_stats(query, i):
    if i == 0 or i == 6:
        explain_result = db1.command('aggregate', 'Host', pipeline=query, explain=True)
    elif i == 1 or i == 7:
        explain_result = db1.command('aggregate', 'ListingReview', pipeline=query, explain=True)
    elif i == 2 or i == 3 or i == 8 or i == 9:
        explain_result = db1.command('aggregate', 'PropertyDetails', pipeline=query, explain=True)
    elif i == 4:
        explain_result = db1.command('aggregate', 'Listing', pipeline=query, explain=True)
    elif i == 5:
        explain_result = db1.command('aggregate', 'Location', pipeline=query, explain=True)
    print('jej')
    ispis = summarize_execution_time(explain_result)
    print(ispis)
    if 'executionStats' in explain_result:
            return explain_result['executionStats']
    else:
            # Handle case where 'executionStats' key is missing
            print(f"Execution stats not found for query {i}")
            return None

def summarize_execution_time(explain_output):
    total_execution_time_millis = 0

    for stage in explain_output.get('stages', []):
        if '$cursor' in stage:
            cursor_stats = stage['$cursor'].get('executionStats')
            print('cursor')
            print(cursor_stats)
            if cursor_stats:
                total_execution_time_millis += cursor_stats.get('executionTimeMillis', 0)
                
        elif 'executionStats' in stage:
            stats = stage.get('executionStats')
            print('stats')
            print(stats)
            if stats:
                total_execution_time_millis += stats.get('executionTimeMillis', 0)

    return {
        'totalExecutionTimeMillis': total_execution_time_millis
    }


def get_execution_stats_opt(query, i):
    if i == 0 or i == 6:
        explain_result = db2.command('aggregate', 'Host', pipeline=query, explain=True)
    elif i == 1 or i == 2 or i == 3 or i == 4 or i == 7 or i == 8 or i == 9:
        explain_result = db2.command('aggregate', 'ListingPropertyDetailsReviewScores', pipeline=query, explain=True)
    elif i == 5:
        explain_result = db2.command('aggregate', 'Location', pipeline=query, explain=True)

    print('jej')
    print(explain_result)
    if 'executionStats' in explain_result:
            return explain_result['executionStats']
    else:
            print(f"Execution stats not found for query {i}")
            return None



def collect_performance_data(queries):
    performance_data = []
    for i, query in enumerate(queries):
        stats = get_execution_stats(query, i)
        if stats is not None:
            performance_data.append({
                'Query': f'Query {i+1}',
                'Execution Time (ms)': stats.get('executionTimeMillis', 0), 
                'Total Keys Examined': stats.get('totalKeysExamined', 0),
                'Total Docs Examined': stats.get('totalDocsExamined', 0),
                'Number of Documents Returned': stats.get('nReturned', 0)
            })
        else:
            print(f"Execution stats not found for query {i}")

    return performance_data


def collect_performance_data_opt(queries):
    performance_data = []
    for i, query in enumerate(queries):
        stats = get_execution_stats(query, i)
        performance_data.append({
            'Query': f'Query {i+1}',
            'Execution Time (ms)': stats['executionTimeMillis'],
            'Total Keys Examined': stats['totalKeysExamined'],
            'Total Docs Examined': stats['totalDocsExamined'],
            'Number of Documents Returned': stats['nReturned']
        })
    return performance_data


performance_data_pre = collect_performance_data(queries_pre_optimization)
performance_data_post = collect_performance_data_opt(queries_post_optimization)

# CREATING DATAFRAME FOR VISUALIZATION
df_pre = pd.DataFrame(performance_data_pre)
df_post = pd.DataFrame(performance_data_post)

# VDATA VISUALIZATION
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
df_pre.plot(kind='bar', x='Query', y='Execution Time (ms)', ax=axes[0, 0], title='Execution Time (Pre vs Post)')
df_post.plot(kind='bar', x='Query', y='Execution Time (ms)', ax=axes[0, 1], title='Execution Time (Post)')
df_pre.plot(kind='bar', x='Query', y='Total Keys Examined', ax=axes[1, 0], title='Total Keys Examined (Pre)')
df_post.plot(kind='bar', x='Query', y='Total Keys Examined', ax=axes[1, 1], title='Total Keys Examined (Post)')
plt.tight_layout()
plt.show()

# CLOSE CONNECTION
client.close()
