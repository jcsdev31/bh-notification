from fuzzywuzzy import fuzz

# Define two example strings to compare
string1 = "of the Dead will be sp"
string2 = "Dead w"

# Calculate the similarity score between the two strings
ratio = fuzz.partial_ratio(string1, string2)

# Print the similarity score
print(ratio)

# Check if the similarity score is greater than or equal to 80%
if ratio >= 85:
    print("The strings are a match!")
else:
    print("The strings are not a match.")