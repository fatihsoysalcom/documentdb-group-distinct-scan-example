import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# --- Configuration ---
# Replace with your DocumentDB/MongoDB connection string.
# Example for DocumentDB: "mongodb://user:password@host:port/?tls=true&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
# For a local MongoDB: "mongodb://localhost:27017/"
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DATABASE_NAME = "blog_db"
COLLECTION_NAME = "user_views"

def main():
    print("Connecting to MongoDB/DocumentDB...")
    try:
        client = MongoClient(MONGODB_URI)
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        print("Successfully connected to the database.")
    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB/DocumentDB: {e}")
        print("Please ensure your MONGODB_URI is correct and the database is running.")
        print("If using DocumentDB, ensure you have the correct TLS/SSL setup.")
        return

    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    # --- Prepare Sample Data ---
    print(f"\nPreparing sample data in '{COLLECTION_NAME}' collection...")
    # Clear existing data for a clean run
    collection.drop()

    sample_data = [
        {"user_id": "userA", "product_id": "prod101", "timestamp": "2023-10-26T10:00:00Z"},
        {"user_id": "userB", "product_id": "prod102", "timestamp": "2023-10-26T10:05:00Z"},
        {"user_id": "userA", "product_id": "prod103", "timestamp": "2023-10-26T10:10:00Z"}, # Duplicate userA
        {"user_id": "userC", "product_id": "prod101", "timestamp": "2023-10-26T10:15:00Z"},
        {"user_id": "userB", "product_id": "prod104", "timestamp": "2023-10-26T10:20:00Z"}, # Duplicate userB
        {"user_id": "userA", "product_id": "prod105", "timestamp": "2023-10-26T10:25:00Z"}, # Duplicate userA
        {"user_id": "userD", "product_id": "prod106", "timestamp": "2023-10-26T10:30:00Z"},
    ]
    collection.insert_many(sample_data)
    print(f"Inserted {len(sample_data)} documents.")
    print(f"Total documents in collection: {collection.count_documents({})}")

    # --- Demonstrate Distinct Scan with $group ---
    print("\nDemonstrating distinct user_ids using $group aggregation:")

    # This specific $group aggregation pattern (grouping by a single field with no accumulators)
    # is optimized by DocumentDB 0.116 to perform a "distinct scan" internally,
    # leading to better performance for finding unique values.
    pipeline = [
        {"$group": {"_id": "$user_id"}}
    ]

    distinct_users_cursor = collection.aggregate(pipeline)
    distinct_users = [doc["_id"] for doc in distinct_users_cursor]

    print(f"Found {len(distinct_users)} unique users:")
    for user in distinct_users:
        print(f"- {user}")

    # --- Compare with traditional distinct (for conceptual understanding) ---
    # Note: DocumentDB's native distinct() command might also be optimized,
    # but the article specifically highlights the $group optimization.
    print("\nComparing with traditional distinct() command (conceptually):")
    traditional_distinct_users = collection.distinct("user_id")
    print(f"Found {len(traditional_distinct_users)} unique users using distinct() command:")
    for user in traditional_distinct_users:
        print(f"- {user}")

    client.close()
    print("\nConnection closed.")

if __name__ == "__main__":
    main()
