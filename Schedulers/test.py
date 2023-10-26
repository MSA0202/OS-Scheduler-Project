class Process:
    def __init__(self, name, burst_time, arrival_time, io_interval):
        self.name = name
        self.remaining_burst_time = burst_time
        self.arrival_time = arrival_time
        self.io_interval = io_interval
        self.time_since_last_io = 0  # Keep track of time since last I/O request
        self.priority = 3  # New processes start at the highest priority
        self.wait_time_at_lowest_priority = 0  # For priority boosting

    def reduce_priority(self):
        if self.priority > 0:  # We don't want to go below the lowest level
            self.priority -= 1

def mlqf_scheduler(processes):
    time = 0
    execution_order = []
    priority_queues = {3: [], 2: [], 1: [], 0: []}
    quantum_map = {3: 1, 2: 2, 1: 3, 0: 4}
    priority_boost_threshold = 11
    
    while processes or any(priority_queues.values()):
        arrived_processes = [p for p in processes if p.arrival_time == time]
        for p in arrived_processes:
            processes.remove(p)
            priority_queues[p.priority].append(p)

        current_process = None
        for priority in [3, 2, 1, 0]:
            if priority_queues[priority]:
                current_process = priority_queues[priority].pop(0)
                break
        
        if current_process:
            quantum = quantum_map[current_process.priority]
            while quantum > 0 and current_process.remaining_burst_time > 0:
                execution_order.append(current_process.name)
                current_process.remaining_burst_time -= 1
                current_process.time_since_last_io += 1
                quantum -= 1
                time += 1
                
                # Check for I/O request and re-prioritize
                if current_process.time_since_last_io == current_process.io_interval:
                    execution_order.append('!' + current_process.name)
                    current_process.time_since_last_io = 0
                    # After I/O, add the process back to the highest priority
                    current_process.priority = 3
                    priority_queues[3].append(current_process)
                    current_process = None
                    break

            # Reduce the priority if not terminated and requeue
            if current_process and current_process.remaining_burst_time > 0:
                current_process.reduce_priority()
                if current_process.priority == 0:
                    current_process.wait_time_at_lowest_priority += quantum_map[0]
                else:
                    current_process.wait_time_at_lowest_priority = 0
                priority_queues[current_process.priority].append(current_process)
            
            # Priority boosting
            for p in priority_queues[0]:
                if p.wait_time_at_lowest_priority >= priority_boost_threshold:
                    priority_queues[0].remove(p)
                    p.priority = 3  # Boost to the highest priority
                    p.wait_time_at_lowest_priority = 0
                    priority_queues[3].append(p)

        else:
            time += 1

    return ' '.join(execution_order)

# Define processes
processes = [
    Process("A", 9, 0, 1),
    Process("B", 9, 0, 1),
    Process("C", 5, 10, 1),
    Process("D", 5, 15, 1)
]

print(mlqf_scheduler(processes))
