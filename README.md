# documentdb-group-distinct-scan-example
This example demonstrates how to efficiently find distinct values in a DocumentDB (or MongoDB) collection using the `$group` aggregation stage. It showcases the specific `$group: { _id: "$field" }` pattern that DocumentDB 0.116 optimizes internally as a 'distinct scan' for improved performance. The script populates a sample collection with duplicat
