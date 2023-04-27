import pymysql

# Create a connection object
cnx = pymysql.connect(
  host="ec2-3-88-168-48.compute-1.amazonaws.com",
  user="ubuntu",
  password="password",
  database="fingertips"
)

# Create a cursor object for executing SQL queries
cursor = cnx.cursor()

# Execute a SQL query
cursor.execute("SELECT * FROM my_table")

# Fetch the results of the query
results = cursor.fetchall()

# Close the cursor and connection objects
cursor.close()
cnx.close()

