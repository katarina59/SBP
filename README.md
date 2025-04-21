### Workshop Analytics MongoDB Microservice
Welcome to the Workshop Analytics MongoDB Microservice! This repository contains a microservice-based system for analyzing workshop data in a psychological clinic, using MongoDB as the document-oriented NoSQL database. The project involves data ingestion, complex querying, performance optimization, and visualization, developed by a two-member team as part of a data analytics project.
Project Overview
The project analyzes a large dataset (≥100MB) sourced from Kaggle, adapted to represent workshop sessions, participants, and feedback in a psychological clinic. Data is ingested into MongoDB, queried to answer 10 analytical questions, optimized for performance, and visualized using Metabase. The implementation includes schema design, data preprocessing, query optimization, and performance comparison.

### Dataset Description

Source: Kaggle (e.g., an Airbnb-inspired dataset adapted for psychological workshop analytics).
Theme: Data on workshop sessions, participants, feedback, and locations in a psychological clinic context.
Files:
host.csv: Details about workshop organizers (hosts).
listing.csv: Details about workshop sessions.
reviewscores.csv: Feedback and ratings for sessions.
location.csv: Location details for sessions (e.g., city, neighborhood).
listingReview.csv: Individual feedback entries for sessions.
propertyDetails.csv: Additional session details (e.g., session type, amenities).


Size: Approximately 120MB, with ~500,000 records across all files.
Example Data Propagation: A host (ID: 1466919) organizes a session (listing_id: 281420) in Paris, recorded in listing.csv. Feedback for this session (rating: 10) is stored in reviewscores.csv, with location details (city: Paris) in location.csv and session specifics (e.g., amenities) in propertyDetails.csv.


### Implementation Details
1. Data Ingestion

Language: Python
Libraries: pymongo, csv, json
Process:
Read CSV files (host.csv, listing.csv, etc.) using the csv module.
Clean data (e.g., handle nulls, convert booleans, parse dates) using helper functions like unitialized, true_false, and convert_to_int.
Transform data into JSON-like documents and insert into MongoDB collections (Sessions, Hosts).


Script: Adapted from the provided csv_to_json.py, which processes host.csv and outputs a JSON file for MongoDB import.

2. Query Analysis

Objective: Answer 10 analytical questions, such as:
Which sessions in 2024 had average feedback ratings >8 in Paris?
How many reviews were submitted for sessions in 2021-2022 by city?
Which neighborhoods in New York had sessions accommodating >2 participants with cleanliness ratings >9?
What is the average weekly cost of sessions by room type in Rome?
Which cities have sessions with above-average prices but low ratings (<60)?
What is the average number of amenities for sessions with accuracy ratings >9 in Paris, Sydney, or New York?
Who are the top 10 earliest-registered hosts with high cleanliness and accuracy ratings?
How many reviews in 2021-2022 were for superhost-led sessions with communication ratings <9?
Which hosts offer sessions with >15 amenities in group workshops, sorted by session count?
What are the top 10 session types by average price and duration difference?


Queries: Implemented using MongoDB’s aggregation pipeline with operators like $match, $lookup, $unwind, $group, and $project. Queries are complex, involving joins, filtering, and aggregations.

3. Performance Analysis

Methodology: Used MongoDB’s explain() to collect execution stats (e.g., execution time, keys examined, documents scanned).
Findings: Identified bottlenecks, such as redundant $lookup operations and unindexed fields causing slow queries.

4. Optimization

Schema Restructuring:
Embedded location and feedback data in the Sessions collection to reduce $lookup operations.
Consolidated listing.csv, reviewscores.csv, and propertyDetails.csv data into a single Sessions collection where appropriate.


Indexing:
Created indexes on frequently queried fields (e.g., listing_id, city, rating, date).
Example: db.Sessions.createIndex({"location.city": 1, "feedback.rating": 1}).


Query Rewriting:
Moved $match stages earlier to leverage indexes.
Replaced multiple $lookup operations with single joins using optimized collections (e.g., ListingPropertyDetailsReviewScores).



5. Optimized Queries

Rewrote queries to align with the new schema, using indexed fields and fewer joins. Example: Query 1 was optimized by embedding listing details, reducing execution time.

6. Performance Comparison

Analysis: Compared pre- and post-optimization metrics using pymongo and matplotlib.
Results: Post-optimization queries showed significant improvements (e.g., 30-50% reduction in execution time).
Visualization: Bar charts comparing execution time and keys examined, saved as performance_comparison.png.

7. Visualization with Metabase

Tool: Metabase
Process:
Connected Metabase to MongoDB.
Created dashboards for query results (e.g., bar charts for session counts by city, line charts for rating trends).
Example: A dashboard showing the top 10 session types by average rating and participant count.



### Installation
Prerequisites

Python 3.8+
MongoDB
Metabase
Python libraries: pymongo, pandas, matplotlib

### Setup

Clone the repository:git clone https://github.com/your-repository-url.git


Navigate to the project directory:cd workshop-analytics-mongodb


Install dependencies:pip install -r requirements.txt


Start MongoDB and Metabase servers.
Run the data ingestion script:python ingest_data.py



### Configuration

MongoDB: Update the connection string in scripts (e.g., MongoClient('mongodb://localhost:27017/')).
Metabase: Configure MongoDB connection in the Metabase admin panel.

### Usage

Ingest Data: Run ingest_data.py to load CSV files into MongoDB.
Run Queries: Execute queries.py to perform pre- and post-optimization queries and generate performance analysis.
Visualize Results: Access Metabase at http://localhost:3000 to view dashboards.
Performance Analysis: View charts in visualizations/performance_comparison.png.

### Contribution
To contribute:

Fork the repository.
Create a feature or bugfix branch.
Commit changes and push to your fork.
Submit a pull request with a detailed description.

### Project Structure

ingest_data.py: Script for CSV-to-MongoDB data ingestion.
queries.py: Script for pre- and post-optimization queries, performance analysis, and visualization.
data/: Directory for CSV files (host.csv, listing.csv, etc.).
visualizations/: Directory for performance comparison charts.
requirements.txt: Python dependencies.

This project showcases a robust implementation of MongoDB for workshop analytics, with optimized queries and insightful visualizations, meeting all specified requirements.
