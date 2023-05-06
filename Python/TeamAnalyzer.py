import sqlite3  # This is the package for all sqlite3 access in Python
import sys
from unicodedata import name      # This helps with command-line parameters

conn = sqlite3.connect('../pokemon.sqlite')
c = conn.cursor()

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    pokedex = int(arg)
    pokemon_query = c.execute("SELECT name FROM pokemon WHERE id= " + arg)
    
    name = pokemon_query.fetchone()
    print(name[0])
    
    type_query = c.execute("SELECT * FROM pokemon_types_view WHERE name = '" + name[0] + "'")
    types = type_query.fetchall()
    print(types[0][1:3])

    strengths = []
    weaknesses = []
    for t in types:
            against = "against_" + t[0]
            c.execute("SELECT {} FROM pokemon_types_battle_view WHERE type1name = ? AND type2name = ?".format(against), 
            (types))
            against_values = c.fetchone()[0]
            if against_values > 1:
                strengths.append(t)
            elif against_values < 1:
                weaknesses.append(t)
    print("Analyzing", arg)
    print(name, "(" + types, ")", "is strong against", strengths, "but weak against", weaknesses)
    team.append((name, arg))
 

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")

conn.close()