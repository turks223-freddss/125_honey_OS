import random
import time
import os
import numpy as np
from prettytable import PrettyTable
from randomizer import table_randomizer

from shortest_job_first import sjf


class PCB:
    def __init__(self, pid, process_name, burst_time, memory_size, arrival_time, priority, status):
        self.pid = pid
        self.process_name = process_name
        self.burst_time = burst_time
        self.memory_size = memory_size
        self.arrival_time = arrival_time
        self.priority = priority
        self.status = status

    def change_status(self, new_status):
        self.status = new_status

    def get_status(self):
        return self.status
    
    def burst_decrement(self):
        if self.burst_time > 0:
            self.burst_time -= 1
            
        if self.burst_time == 0:
            self.change_status("Terminate")

def display_pcb_table(pcb_array):
    # Creating instance of PrettyTable
    table = PrettyTable()

    table.field_names = ["PID", "Process Name", "Burst Time", "Memory Size", "Arrival Time", "Priority", "Status"]
    for pcb in pcb_array:
        if pcb.priority is not None:
            table.add_row([pcb.pid, pcb.process_name, pcb.burst_time, pcb.memory_size, pcb.arrival_time, pcb.priority, pcb.status])
        else:
            table.add_row([pcb.pid, pcb.process_name, pcb.burst_time, pcb.memory_size, pcb.arrival_time, "", pcb.status])
    print(table)

def generate_random_pcb(pid, unique_priorities):
    randomizer = table_randomizer()
    process_name = randomizer.pick_process
    burst_time = randomizer.burst_time
    memory_size = randomizer.memory_size
    priority = unique_priorities.pop()

    # Status set to "New"
    status = "New"
    return PCB(pid, process_name, burst_time, memory_size, pid - 1, priority, status)

def update_arrival_times(pcb_array):
    for pcb in pcb_array:
        if pcb.arrival_time > 0:
            pcb.arrival_time -= 1

def main(num_processes):
    unique_priorities = list(range(1, num_processes + 1))
    random.shuffle(unique_priorities)
    pcb_array = np.empty(num_processes, dtype=object)

    for pid in range(1, num_processes + 1):
        if pid > 1:
            # Set status of the last PCB to "Waiting"
            pcb_array[pid - 2].status = "Waiting"

        pcb = generate_random_pcb(pid, unique_priorities)
        pcb_array[pid - 1] = pcb

        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')


        sjf(pcb_array[:pid], pid - 1, num_processes)

        # Display the updated table
        # display_pcb_table(sjf_array[:pid])


        # Wait for 1 second and update arrival times
        time.sleep(1)
        # update_arrival_times(pcb_array[:pid])


if __name__ == "__main__":
    num_processes = random.randint(4, 6)  # Random number of processes between 4 and 6

    main(num_processes)
