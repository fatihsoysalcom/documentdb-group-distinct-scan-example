# DocumentDB Group Distinct Scan Example

This example demonstrates how to efficiently find distinct values in a DocumentDB (or MongoDB) collection using the `$group` aggregation stage. It showcases the specific `$group: { _id: "$field" }` pattern that DocumentDB 0.116 optimizes internally as a 'distinct scan' for improved performance. The script populates a sample collection with duplicate user view data and then queries for unique user IDs.

## Language

`python`

## How to Run

1. Install pymongo: `pip install pymongo`
2. Ensure a MongoDB or DocumentDB instance is running and accessible.
3. Run the script: `python main.py` (Optionally, set `MONGODB_URI` env var: `MONGODB_URI='mongodb://your_host:port/' python main.py`)

## Original Article

This example accompanies the Turkish article: [DocumentDB 0.116: $group ile Benzersiz Veri Taraması (Distinct Scan)](https://fatihsoysal.com/blog/documentdb-0-116-group-ile-benzersiz-veri-taramasi-distinct-scan/).

## License

MIT — see [LICENSE](LICENSE).
