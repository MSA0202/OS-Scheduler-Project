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
        self.time_since_last_io = 0  # Keep track of time since last I/O request

def stcf_scheduler(processes):
    execution_order = []
    current_time = 0
    queue = []

    while processes or queue:
        # Add processes that have arrived by now to the queue
        while processes and processes[0].arrival_time <= current_time:
            queue.append(processes.pop(0))

        # Sort the queue by burst time, then by whether it's currently executing
        queue = sorted(queue, key=lambda x: (x.duration, x != queue[0]))

        if queue:
            current_process = queue[0]
            execution_order.append(current_process.name)

            current_process.duration -= 1
            current_process.time_since_last_io += 1

            # Check for I/O request
            if current_process.duration > 0 and current_process.time_since_last_io == current_process.io_frequency:
                execution_order.append('!' + current_process.name)
                current_process.time_since_last_io = 0

            # If the burst time is now 0, remove the process from the queue
            if current_process.duration == 0:
                queue.pop(0)

        current_time += 1

    return ' '.join(execution_order)

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

    # Sort processes based on arrival time (This sorting is done here for both schedulers)
    data_set.sort(key=lambda x: x.arrival_time)

    # Use the STCF scheduler function
    execution_order = stcf_scheduler(data_set)

    # Join the execution order and remove extra spaces
    output = execution_order.replace('  ', ' ')
    print(output)
    
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
