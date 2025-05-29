import random
import time
import os
import numpy as np
from prettytable import PrettyTable
from randomizer import table_randomizer

from shortest_job_first import sjf
from fcfs import fcfs

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
    def get_burst(self):
        return self.burst_time

def display_pcb_table(pcb_array):
    table = PrettyTable()
    table.field_names = ["PID", "Process Name", "Burst Time", "Memory Size", "Arrival Time", "Priority", "Status"]
    for pcb in pcb_array:
        table.add_row([pcb.pid, pcb.process_name, pcb.burst_time, pcb.memory_size, pcb.arrival_time, pcb.priority, pcb.status])
    print(table)

def generate_random_pcb(pid, unique_priorities):
    randomizer = table_randomizer()
    return PCB(
        pid,
        randomizer.pick_process,
        randomizer.burst_time,
        randomizer.memory_size,
        pid - 1,
        unique_priorities.pop(),
        "New"
    )

def main(num_processes, update_gui_signal=None, mode="sjf"):
    unique_priorities = list(range(1, num_processes + 1))
    random.shuffle(unique_priorities)
    pcb_array = np.empty(num_processes, dtype=object)

    for pid in range(1, num_processes + 1):
        if pid > 1:
             if 0 <= pid - 2 < len(pcb_array):
                pcb_array[pid - 2].status = "Waiting"

        pcb = generate_random_pcb(pid, unique_priorities)
        pcb_array[pid - 1] = pcb

        os.system('cls' if os.name == 'nt' else 'clear')
        
        if mode == "sjf":
            sjf(pcb_array[:pid], pid - 1, num_processes, update_gui_signal)
        elif mode == "fcfs":
            fcfs(pcb_array[:pid], pid - 1, num_processes, update_gui_signal)
        # Add other modes like "rr" here later

        time.sleep(1)

if __name__ == "__main__":
    main(random.randint(4, 6))
