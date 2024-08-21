import sys
import random

class CoOccurrence(object):
    def __init__(self, race_array, teams, good_counts):
        self.good_counts = good_counts

        co_occurrence = [[0 for _ in range(teams)] for _ in range(teams)]
        
        for race in race_array:
            for i in range(len(race)):
                for j in range(i+1, len(race)):
                    team1, team2 = race[i], race[j]
                    co_occurrence[team1][team2] += 1
                    co_occurrence[team2][team1] += 1
        
        self.co_occurrence = co_occurrence

        self.loss = sum(elem not in good_counts for i, row in enumerate(co_occurrence) for j, elem in enumerate(row) if i != j)

    def update_helper(self, arr, team1, team2):
        for t in arr:
            if t == team1:
                continue
            self.loss -= 2 * int(self.co_occurrence[t][team1] not in self.good_counts)
            self.loss += 2 * int(self.co_occurrence[t][team1] - 1 not in self.good_counts)
            self.co_occurrence[t][team1] -= 1
            self.co_occurrence[team1][t] -= 1
            self.loss -= 2 * int(self.co_occurrence[t][team2] not in self.good_counts)
            self.loss += 2 * int(self.co_occurrence[t][team2] + 1 not in self.good_counts)
            self.co_occurrence[t][team2] += 1
            self.co_occurrence[team2][t] += 1

    def update_with_swap(self, race_array, i1, j1, i2, j2):
        team1 = race_array[i1][j1]
        team2 = race_array[i2][j2]
        self.update_helper(race_array[i1], team1, team2)
        self.update_helper(race_array[i2], team2, team1)

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

def perform_swap_operation(race_array, co_occurrence, positions_in_race_array):
    # Randomly select one of the positions
    i1, j1 = random.choice(positions_in_race_array)
    
    # Randomly select another row
    i2 = random.choice([i for i in range(len(race_array)) if i != i1])
    
    # Randomly select a position in the other row
    j2 = random.randint(0, len(race_array[i2]) - 1)
    
    # Check if swap would cause duplicates
    if race_array[i1][j1] not in race_array[i2] and race_array[i2][j2] not in race_array[i1]:
        prev_loss = co_occurrence.loss

        # Perform the swap
        co_occurrence.update_with_swap(race_array, i1, j1, i2, j2)
        race_array[i1][j1], race_array[i2][j2] = race_array[i2][j2], race_array[i1][j1]
        
        # Check if the number of bad co-occurrence counts has increased
        if co_occurrence.loss > prev_loss:
            # Revert the swap
            co_occurrence.update_with_swap(race_array, i1, j1, i2, j2)
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
    
    positions_in_race_array = [(i, j) for i, row in enumerate(race_array) 
                     for j, val in enumerate(row)]
    
    co_occurrence = CoOccurrence(race_array, teams, good_counts)

    while True:
        perform_swap_operation(race_array, co_occurrence, positions_in_race_array)
        if co_occurrence.loss == 0:
            break

    random.shuffle(race_array)  # Just in case it helps with spreading out a team's races

    print("Race Array:")
    for row in race_array:
        print(" ".join(str(team) for team in row))
    print("Co-occurrence Matrix:")
    print(co_occurrence.co_occurrence)

if __name__ == "__main__":
    main()
