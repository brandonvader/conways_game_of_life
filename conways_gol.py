import os
from random import randint
from time import sleep

#Global Variables
rows, cols = (60, 235) #Grid size

#Generate PsudoRandom Array
def generate_random():
    arr_random = [[randint(0 , 1) for _ in range(cols)] for _ in range(rows)]
    return arr_random

#Clear Screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_grid(arr):
    clear_screen()
    for row in arr:
        for cell in row:
            if cell == 1:
                # Indigo color (ANSI escape code for bright magenta)
                print("\033[96m█\033[0m", end="")
            else:
                # Dark grey color (ANSI escape code for grey)
                print("\033[30m█\033[0m", end="")
        print()  # Newline after each row

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
def eval_sustainability(arr0, arr1, arr2, arr3, arr4):
    if eval_extinction(arr0):
        return "extinct"
    elif arr0 == arr1:
        return "static"
    elif arr0 == arr2 or arr0 == arr3 or arr0 == arr4:
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
    arr_n3_eval_grid = [[0 for i in range(cols)] for j in range(rows)] #3 generations previous data
    arr_n4_eval_grid = [[0 for i in range(cols)] for j in range(rows)] #4 generations previous data
    loop_counter = 0
    generation_count=0
    high_score=0
    flag_sustainability = "ok"

    #Grid Display
    print("Starting Array Values:")
    display_grid(arr_starting_grid)

    #User Input

    #Evaluate for Extinction on Startup
    flag_sustainability=eval_sustainability(arr_starting_grid, arr_n0_eval_grid, arr_n1_eval_grid, arr_n2_eval_grid, arr_n3_eval_grid)
    if flag_sustainability=="extinct":
        print("No cells seeded with life. Program halting")
        return 0
    else:
        arr_n0_eval_grid = arr_starting_grid
    
    #Generational Evaluation (Loop until extinct)
    while loop_counter<1000: #Loop for 1000 epochs
        while flag_sustainability == "ok": #Generational Evaluation (Loop until non-viable state)
            generation_count += 1 #Itterate current generation
            arr_n1_eval_grid = arr_n0_eval_grid #Set previous grid before running next generation evaluation
            arr_n0_eval_grid=eval_generation(arr_n0_eval_grid) #Run next generation
            #Check for sustanible patern
            flag_sustainability=eval_sustainability(arr_n0_eval_grid, arr_n1_eval_grid, arr_n2_eval_grid, arr_n3_eval_grid, arr_n4_eval_grid)
            #Display Results
            display_grid(arr_n0_eval_grid)
            match flag_sustainability:
                case "extinct":
                    print("Extinction occured at generation: ", generation_count)
                case "static":
                    print("Static state occured at generation: ", generation_count)
                case "repeating":
                    print("Repeating state occured at generation: ", generation_count)
                case "ok":
                    print("Current Generation: ", generation_count)
                    print(f"Current epoch: {loop_counter+1}/1000")
                    print("Previous high score: ", high_score)
                    arr_n4_eval_grid=arr_n3_eval_grid
                    arr_n3_eval_grid=arr_n2_eval_grid
                    arr_n2_eval_grid=arr_n1_eval_grid
                case _:
                    print("An unexpected flag occured: ", flag_sustainability)

            sleep(0.04166666666666667) #Sleep for 1/24 of a second (40ms) to simulate 24fps

        #Evaluate high score
        if generation_count > high_score:
            high_score=generation_count
            print (f"Current epoch: {loop_counter+1}/1000")
            print ("New High Score! Generations: ", high_score)
        else:
            print (f"Current epoch: {loop_counter+1}/1000")
            print ("Previous high score: ", high_score)
        
        #sleep(2)

        loop_counter += 1

        #Reset starting grid for next run
        arr_n0_eval_grid=generate_random()
        #Reset flag_sustainability
        flag_sustainability="ok"
        #Reset generation count
        generation_count=0
        #Reset previous generations
        arr_n1_eval_grid = [[0 for i in range(cols)] for j in range(rows)]
        arr_n2_eval_grid = [[0 for i in range(cols)] for j in range(rows)]

#Start program
main()