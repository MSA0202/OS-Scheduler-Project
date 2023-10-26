import sys
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Define the process data class
class Process:
    def __init__(self, name, duration, arrival_time, io_frequency):
        self.name = name
        self.duration = duration
        self.arrival_time = arrival_time
        self.io_frequency = io_frequency

def fcfs_scheduler(processes):
    current_time = 0
    execution_order = []

    for process in processes:
        if current_time < process.arrival_time:
            current_time = process.arrival_time

        remaining_duration = process.duration

        while remaining_duration > 0:
            execution_order.append(process.name)
            current_time += 1
            remaining_duration -= 1

            # If I/O is required and it's not the final unit of the process, perform it and increase the time
            if process.io_frequency > 0 and (process.duration - remaining_duration) % process.io_frequency == 0 and remaining_duration > 0:
                execution_order.append(f"!{process.name}")

    return execution_order

def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        return 1

    # Extract the input file name from the command line arguments
    input_file_name = f"Process_List/{config['dataset']}/{sys.argv[1]}"

    # Define the number of processes
    num_processes = 0

    # Initialize an empty list for process data
    data_set = []

    # Open the file for reading
    try:
        with open(input_file_name, "r") as file:
            # Read the number of processes from the file
            num_processes = int(file.readline().strip())

            # Read process data from the file and populate the data_set list
            for _ in range(num_processes):
                line = file.readline().strip()
                name, duration, arrival_time, io_frequency = line.split(',')
                process = Process(name, int(duration), int(arrival_time), int(io_frequency))
                data_set.append(process)

    except FileNotFoundError:
        print("Error opening the file.")
        return 1
    
    # Sort processes based on arrival time
    data_set.sort(key=lambda x: x.arrival_time) #for the fcfs and stcf schdeuler we need to do this 

    # Use the FCFS scheduler function
    execution_order = fcfs_scheduler(data_set)

    # Join the execution order and remove extra spaces
    output = ' '.join(execution_order).replace('  ', ' ')
    #print(output) #OPTIONAL IF YOU WANT TO SEE OUTPUT IN TERMINAL 

    # Open a file for writing
    try:
        output_path = f"Schedulers/template/{config['dataset']}/template_out_{sys.argv[1].split('_')[1]}"
        with open(output_path, "w") as output_file:
            # Write the final result to the output file
            output_file.write(output)

    except IOError:
        print("Error opening the output file.")
        return 1

    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
