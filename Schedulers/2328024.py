import sys
import json
import heapq

# load configuration settings from a JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# define the process data class
class Process:
    def __init__(self, name, duration, arrival_time, io_frequency):
        self.name = name
        self.duration = duration
        self.arrival_time = arrival_time
        self.io_frequency = io_frequency
        self.time_since_last_io = 0  # track time since last I/O request

    # define comparison methods for the Process class to work with the heapq
    def __lt__(self, other):
        return self.duration < other.duration

    def __eq__(self, other):
        return self.duration == other.duration

# implement the Shortest Time to Completion First (STCF) scheduler
def stcf_scheduler(processes):
    execution_order = []  # records the execution order of processes
    current_time = 0  # current time in the simulation
    queue = []  # priority queue for processes ready to execute
    io_queue = []  # priority queue for processes waiting for I/O

    while processes or queue or io_queue:
        # add processes that have arrived by the current time to the queue
        while processes and processes[0].arrival_time <= current_time:
            process = processes.pop(0)
            heapq.heappush(queue, process)

        if queue:
            # select the process with the shortest remaining duration
            current_process = heapq.heappop(queue)
            execution_order.append(current_process.name)

            # execute the process for one time unit
            current_process.duration -= 1
            current_process.time_since_last_io += 1

            # check for I/O request
            if current_process.duration > 0 and current_process.time_since_last_io == current_process.io_frequency:
                heapq.heappush(io_queue, current_process)
                current_process.time_since_last_io = 0

            # if the burst time is not zero, put it back in the queue
            if current_process.duration > 0:
                heapq.heappush(queue, current_process)

        elif io_queue:
            # execute the process waiting for I/O
            current_process = heapq.heappop(io_queue)
            execution_order.append('!' + current_process.name)

        current_time += 1

    # return the execution order as a string
    return ' '.join(execution_order)

# main function to run the scheduler
def main():
    # check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        return 1

    # extract the input file name from the command line arguments
    input_file_name = f"Process_List/{config['dataset']}/{sys.argv[1]}"

    # initialize variables
    num_processes = 0
    data_set = []  # list to store process data

    # open the file for reading
    try:
        with open(input_file_name, "r") as file:
            # read the number of processes from the file
            num_processes = int(file.readline().strip())

            # read process data from the file and populate the data_set list
            for _ in range(num_processes):
                line = file.readline().strip()
                name, duration, arrival_time, io_frequency = line.split(',')
                process = Process(name, int(duration), int(arrival_time), int(io_frequency))
                data_set.append(process)

    except FileNotFoundError:
        print("Error opening the file.")
        return 1

    # sort processes based on arrival time
    data_set.sort(key=lambda x: x.arrival_time)

    # use the STCF scheduler function to determine the execution order
    execution_order = stcf_scheduler(data_set)

    # clean up the execution order by removing extra spaces
    output = execution_order.replace('  ', ' ')
    #print(output)
    
    # open a file for writing the output
    try:
        output_path = f"Schedulers/template/{config['dataset']}/template_out_{sys.argv[1].split('_')[1]}"
        with open(output_path, "w") as output_file:
            # write the final result to the output file
            output_file.write(output)

    except IOError:
        print("Error opening the output file.")
        return 1

    return 0

# entry point of the script
if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
