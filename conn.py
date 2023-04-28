import pymysql

# Create a connection object
cnx = pymysql.connect(
  host="ec2-3-231-39-248.compute-1.amazonaws.com",
  password='password',
  user="bernard",
  database="fingertips"
)

# Create a cursor object for executing SQL queries
cursor = cnx.cursor()

# Execute a SQL query
cursor.execute("SHOW TABLES")

# Fetch the results of the query
results = cursor.fetchall()
print(results)

# Close the cursor and connection objects
cursor.close()
cnx.close()

