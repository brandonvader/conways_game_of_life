import os
from random import randint
from time import sleep

#Global Variables
rows, cols = (10, 10)

#Generate PsudoRandom Array
def generate_random():
    arr_random = [[randint(0, 1) for _ in range(cols)] for _ in range(rows)]
    return arr_random

#Clear Screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

#Display Grid
def display_grid(arr):
    clear_screen()
    for row in arr:
        print(row)

#Evaluate Extinction
def eval_extinction(arr):
    for i in range(rows):
        for j in range(cols):
            if arr[i][j] == 1: #Any life means no extinction has occured, stop evaluating and return to main
                return False
            else:
                continue

    return True


#Evaluate Generation
def eval_generation(arr):
    #Variable Declaration
    arr_generated_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    for i in range(rows): #Loop through each row
        for j in range(cols): #Loop through each column
            live_neighbors = 0  # Reset for each cell
            
            #Check all 8 neighbors
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    if x == 0 and y == 0:
                        continue  #Skip self
                    
                    ni, nj = i + x, j + y
                    if 0 <= ni < rows and 0 <= nj < cols:
                        if arr[ni][nj] == 1:
                            live_neighbors += 1
            
            # Apply rules (now properly indented under cell loop)
            if arr[i][j] == 1:  # Alive cell
                if live_neighbors < 2 or live_neighbors > 3:
                    arr_generated_grid[i][j] = 0  # Dies
                else:
                    arr_generated_grid[i][j] = 1  # Survives
            else:  # Dead cell
                if live_neighbors == 3:
                    arr_generated_grid[i][j] = 1  # Reproduction
                else:
                    arr_generated_grid[i][j] = 0  # Stays dead
    
    return arr_generated_grid

#Evaluate for Static State
def eval_sustainability(arr1, arr2, arr3):
    if eval_extinction(arr1):
        return "extinct"
    elif arr1 == arr2:
        return "static"
    elif arr1 == arr3:
        return "repeating"
    else:
        return "ok"

#Main

def main():
    #Variable Declaration
    arr_starting_grid = generate_random() #generate random "seed" for testing while there's no user input
    arr_n0_eval_grid = [[0 for i in range(cols)] for j in range(rows)] #active generation data
    arr_n1_eval_grid = [[0 for i in range(cols)] for j in range(rows)] #previous generation data
    arr_n2_eval_grid = [[0 for i in range(cols)] for j in range(rows)] #2 generations previous data
    high_score=0
    flag_sustainability = "ok"

    #Grid Display
    print("Starting Array Values:")
    display_grid(arr_starting_grid)

    #User Input

    #Evaluate for Extinction on Startup
    flag_sustainability=eval_sustainability(arr_starting_grid, arr_n0_eval_grid, arr_n1_eval_grid)
    if flag_sustainability=="extinct":
        print("No cells seeded with life. Program halting")
        return 0
    else:
        arr_n0_eval_grid = arr_starting_grid
    
    #Generational Evaluation (Loop until extinct)
    
    while flag_sustainability == "ok":
        high_score += 1 #Itterate current generation
        arr_n1_eval_grid = arr_n0_eval_grid #Set previous grid before running next generation evaluation
        arr_n0_eval_grid=eval_generation(arr_n0_eval_grid) #Run next generation
        #Check for sustanible patern
        flag_sustainability=eval_sustainability(arr_n0_eval_grid, arr_n1_eval_grid, arr_n2_eval_grid)
        #Display Results
        display_grid(arr_n0_eval_grid)
        match flag_sustainability:
            case "extinct":
                print("Extinction occured at generation: ", high_score)
            case "static":
                print("Static state occured at generation: ", high_score)
            case "repeating":
                print("Repeating state occured at generation: ", high_score)
            case "ok":
                print("Current Generation: ", high_score)
                arr_n2_eval_grid=arr_n1_eval_grid
            case _:
                print("An unexpected flag occured: ", flag_sustainability)

        sleep(0.20)


    #Record High-Score for Session

main()