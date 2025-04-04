import time

# Global variable for the array of PCBs
fcfs_pcb_array = []
count = 0

def fcfs(pcb_array, current_index, num_processes, update_gui_signal):
    global fcfs_pcb_array
    fcfs_pcb_array.append(pcb_array[current_index])
    update_gui_signal.emit(fcfs_pcb_array)
    processing(num_processes, current_index, update_gui_signal)

def print_current_pcb_details():
    global fcfs_pcb_array
    for pcb in fcfs_pcb_array:
        print([pcb.pid, pcb.process_name, pcb.burst_time, pcb.memory_size, pcb.arrival_time, pcb.priority, pcb.status])

def processing(num_processes, current_index, update_gui_signal):
    global fcfs_pcb_array

    num = current_index + 1
    loop = True
    while True:
        if num == num_processes:
            while not all(pcb.get_status() == "Terminate" for pcb in fcfs_pcb_array[:num_processes]):
                for i in range(num_processes):
                    if fcfs_pcb_array[i].get_status() != "Terminate":
                        # Check if the process will be decremented
                        if fcfs_pcb_array[i].get_burst() > 0:
                            fcfs_pcb_array[i].change_status("Running")
                            fcfs_pcb_array[i].burst_decrement()
                            # Set other processes to "Ready"
                            for j in range(num_processes):
                                if j != i and j < len(fcfs_pcb_array):  # Check if index j is within the bounds
                                    fcfs_pcb_array[j].change_status("Ready")
                        else:
                            fcfs_pcb_array[i].change_status("Ready")
                        break
                time.sleep(1)
                # Remove terminated processes and update GUI
                remove_terminated_processes(update_gui_signal)
        else:
            loop = False
            if num <= 1:
                fcfs_pcb_array[0].burst_decrement()
                # Check if the process will be decremented
                if fcfs_pcb_array[0].get_burst() > 0:
                    fcfs_pcb_array[0].change_status("Running")
                else:
                    fcfs_pcb_array[0].change_status("Ready")
                time.sleep(1)
            else:
                for i in range(current_index):
                    if fcfs_pcb_array[i].get_status() != "Terminate":
                        # Check if the process will be decremented
                        if fcfs_pcb_array[i].get_burst() > 0:
                            fcfs_pcb_array[i].change_status("Running")
                            fcfs_pcb_array[i].burst_decrement()
                            # Set other processes to "Ready"
                            for j in range(current_index):
                                if j != i:
                                    fcfs_pcb_array[j].change_status("Ready")
                        else:
                            fcfs_pcb_array[i].change_status("Ready")
                        break
                time.sleep(1)
                # Remove terminated processes and update GUI
                remove_terminated_processes(update_gui_signal)
        if not loop:
            return

def terminate_process(pcb):
    pcb.change_status("Terminate")
    # print(f"Terminating PID {pcb.pid}. Status after setting to terminate: {pcb.status}")
    # Remove terminated processes immediately
    # remove_terminated_processes(update_gui_signal)

def remove_terminated_processes(update_gui_signal):
    global fcfs_pcb_array
    fcfs_pcb_array = [pcb for pcb in fcfs_pcb_array if pcb.get_status() != "Terminate"]
    update_gui_signal.emit(fcfs_pcb_array)