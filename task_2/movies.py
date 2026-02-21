# Initial movie data
movies = [
    ("Eternal Sunshine of the Spotless Mind", 20000000),
    ("Memento", 9000000),
    ("Requiem for a Dream", 4500000),
    ("Pirates of the Caribbean: On Stranger Tides", 379000000),
    ("Avengers: Age of Ultron", 365000000),
    ("Avengers: Endgame", 356000000),
    ("Incredibles 2", 200000000)
]

# ----------------------------
# OPTIONAL: Let user add movies
# ----------------------------

add_more = input("Do you want to add more movies? (yes/no): ").lower()

if add_more == "yes":
    num = int(input("How many movies do you want to add? "))

    for i in range(num):
        name = input("Enter movie name: ")
        budget = float(input("Enter movie budget: "))
        movies.append((name, budget))

# ----------------------------
# Calculate Average Budget
# ----------------------------

total_budget = 0

for movie in movies:
    total_budget += movie[1]

average_budget = total_budget / len(movies)

print("\nAverage Budget: $", average_budget)

# ----------------------------
# Find Movies Above Average
# ----------------------------

count = 0

print("\nMovies with above-average budget:\n")

for movie in movies:
    name = movie[0]
    budget = movie[1]

    if budget > average_budget:
        difference = budget - average_budget
        print(f"{name} spent ${difference:,.2f} more than average.")
        count += 1

print(f"\nNumber of movies above average: {count}")