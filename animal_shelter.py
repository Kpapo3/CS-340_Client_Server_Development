#!/usr/bin/env python
# coding: utf-8

# Set environment variable before running

import os
from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    # CRUD operations for Animal collection in MongoDB Atlas
    def __init__(self, username=None, password=None):
        # Database and collection names
        DB = 'AAC'
        COL = 'animals'
        # MongoDB Atlas connection string stored in environment variable
        uri = os.getenv("MONGO_URI")
        if not uri:
            raise ValueError(
                "MONGO_URI not set.\n"
                "Run in terminal:\n"
                'export MONGO_URI="mongodb+srv://<user>:<pass>@cluster0.rl4sdmo.mongodb.net/?appName=Cluster0"'
            )

        # Initialize Connection
        self.client = MongoClient(uri)
        self.database = self.client[DB]
        self.collection = self.database[COL]

        # Ensure indexes used by common dashboard queries
        self._ensure_indexes()

    # Create indexes that match common dashboard query patterns.
    def _ensure_indexes(self):
        try:
            # Single-field indexes (align with dashboard filter fields)
            self.collection.create_index("animal_type")
            self.collection.create_index("breed")
            self.collection.create_index("sex_upon_outcome")
            self.collection.create_index("age_upon_outcome_in_weeks")

            # Optional compound index (helpful for the rescue filter queries)
            self.collection.create_index([
                ("animal_type", 1),
                ("sex_upon_outcome", 1),
                ("age_upon_outcome_in_weeks", 1),
                ("breed", 1),
            ])
        except Exception as e:
            # Do not crash app if index creation fails (permissions, etc.)
            print(f"Index creation warning: {e}")
        
    # Complete this create method to implement the C in CRUD
    def create(self, data):
        if data is None or not isinstance(data, dict):
            raise ValueError("'data' must be a dictionary.")
        try:
            insertion_result = self.collection.insert_one(data) # Data should be a dictionary
            return insertion_result.acknowledged
        except Exception as e:
            print(f"An error has occurred: {e}")
            return False
    
    # Create method to implement the R in CRUD
    def read(self, query, projection=None, sort=None, limit=0):
        # returns LIST to support DataFrame + Dash + projection/sort/limit support
        if query is None or not isinstance(query, dict):
            raise ValueError("'query' must be a dictionary.")

        if projection is not None and not isinstance(projection, dict):
            raise ValueError("'projection' must be a dictionary or None.")
        
        try:
            cursor = self.collection.find(query, projection)

            if sort is not None:
                cursor = cursor.sort(sort)

            if limit and int(limit) > 0:
                cursor = cursor.limit(int(limit))

            return list(cursor)
            
        except Exception as e:
            print(f"An error has occurred: {e}")
            return []

    # Aggregation pipeline for breed counts
    def aggregate_breed_counts(self, query, topN=10):
        # Return breed counts computed in MongoDB via aggregation pipeline.
        if query is None or not isinstance(query, dict):
            raise ValueError("'query' must be a dictionary.")

        try:
            pipeline = [
                {"$match": query},
                {"$group": {"_id": "$breed", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": int(topN)},
            ]
            return list(self.collection.aggregate(pipeline))
        except Exception as e:
            print(f"An error has occurred: {e}")
            return []

    # Create method to implement the U in CRUD
    def update(self, query, update_data):
        if query is None or not isinstance(query, dict):
            raise ValueError("'query' must be a dictionary.")

        if update_data is None or not isinstance(update_data, dict):
            raise ValueError("'update_data' must be a dictionary.")

        try:
            update_result = self.collection.update_many(query, {'$set': update_data})
            # Return count of modified documents
            return update_result.modified_count
        except Exception as e:
            print(f"An error has occurred: {e}")
            return 0

    # Create method to implement the D in CRUD
    def delete(self, query):
        if query is None or not isinstance(query, dict):
            raise ValueError("'query' must be a dictionary.")
        try:
            delete_result = self.collection.delete_many(query)
            # Return count of deleted documents
            return delete_result.deleted_count
        except Exception as e:
            print(f"An error has occurred: {e}")
            return 0

    # Helper if needing to fetch by MongoDB _id
    def read_by_id(self, id_string, projection=None):
        if not isinstance(id_string, str) or not id_string.strip():
            raise ValueError("'id_string' must be a non-empty string.")

        if projection is not None and not isinstance(projection, dict):
            raise ValueError("'projection' must be a dictionary or None.")

        try:
            return self.collection.find_one({"_id": ObjectId(id_string)}, projection)
        except Exception as e:
            print(f"An error has occurred: {e}")
            return None
