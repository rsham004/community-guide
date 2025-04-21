import pandas as pd

# Define the data for the DataFrame
# Using clean keys without trailing spaces for column names
data = {
    "Name": ["John", "Jane", "Doe"],
    "Age": [28, 34, 29],
    "City": ["New York", "Los Angeles", "Chicago"],
}

# Create the DataFrame
df = pd.DataFrame(data)

# Print the DataFrame (using parentheses for Python 3)
print(df)

