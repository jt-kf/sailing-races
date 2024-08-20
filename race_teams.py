import sys
import random

def create_race_array(teams, races, boats_per_race):
    race_array = []
    team_counter = 0
    
    for _ in range(races):
        race = []
        for _ in range(boats_per_race):
            race.append(team_counter)
            team_counter = (team_counter + 1) % teams
        race_array.append(race)
    
    return race_array

def calculate_co_occurrence(race_array, teams):
    co_occurrence = [[0 for _ in range(teams)] for _ in range(teams)]
    
    for race in race_array:
        for i in range(len(race)):
            for j in range(i+1, len(race)):
                team1, team2 = race[i], race[j]
                co_occurrence[team1][team2] += 1
                co_occurrence[team2][team1] += 1
    
    return co_occurrence

def count_bad_co_occurrence_counts(matrix, good_counts):
    return sum(elem not in good_counts for i, row in enumerate(matrix) for j, elem in enumerate(row) if i != j)

def perform_swap_operation(race_array, teams, good_counts):
    positions = [(i, j) for i, row in enumerate(race_array) 
                     for j, val in enumerate(row)]
    
    # Randomly select one of the positions
    i1, j1 = random.choice(positions)
    
    # Randomly select another row
    i2 = random.choice([i for i in range(len(race_array)) if i != i1])
    
    # Randomly select a position in the other row
    j2 = random.randint(0, len(race_array[i2]) - 1)
    
    # Check if swap would cause duplicates
    if race_array[i1][j1] not in race_array[i2] and race_array[i2][j2] not in race_array[i1]:
        original_bad_counts = count_bad_co_occurrence_counts(calculate_co_occurrence(race_array, teams), good_counts)
        
        # Perform the swap
        race_array[i1][j1], race_array[i2][j2] = race_array[i2][j2], race_array[i1][j1]
        
        # Calculate new co-occurrence matrix
        new_co_occurrence = calculate_co_occurrence(race_array, teams)
        
        # Check if the number of bad co-occurrence counts has increased
        if count_bad_co_occurrence_counts(new_co_occurrence, good_counts) > original_bad_counts:
            # Revert the swap
            race_array[i1][j1], race_array[i2][j2] = race_array[i2][j2], race_array[i1][j1]

def main():
    if len(sys.argv) != 5:
        print("Usage: python script.py teams races boats-per-race bad-counts")
        sys.exit(1)
    
    teams = int(sys.argv[1])
    races = int(sys.argv[2])
    boats_per_race = int(sys.argv[3])
    good_counts = [int(n) for n in sys.argv[4].split(',')]
    
    race_array = create_race_array(teams, races, boats_per_race)
    
    while True:
        perform_swap_operation(race_array, teams, good_counts)
        if count_bad_co_occurrence_counts(calculate_co_occurrence(race_array, teams), good_counts) == 0:
            break

    random.shuffle(race_array)  # Just in case it helps with spreading out a team's races

    print("Race Array:")
    for row in race_array:
        print(" ".join(str(team) for team in row))
    print("Co-occurrence Matrix:")
    print(calculate_co_occurrence(race_array, teams))

if __name__ == "__main__":
    main()
