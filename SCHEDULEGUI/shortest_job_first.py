import time

# Global variable for the array of PCBs
sjf_pcb_array = []
count = 0

def sjf(pcb_array, current_index, num_processes, update_gui_signal):
    global sjf_pcb_array

    # Add the current process control block to the array
    sjf_pcb_array.append(pcb_array[current_index])

    # if update_gui_signal:
    #     # Emit signal to update the GUI table
    #     update_gui_signal.emit(sjf_pcb_array)

    # Start the processing of the processes
    processing(num_processes, current_index, update_gui_signal)

def print_current_pcb_details():
    global sjf_pcb_array
    for pcb in sjf_pcb_array:
        print([pcb.pid, pcb.process_name, pcb.burst_time, pcb.memory_size, pcb.arrival_time, pcb.priority, pcb.status])

def processing(num_processes, current_index, update_gui_signal):
    global sjf_pcb_array

    num = current_index + 1

    while True:
        if num == num_processes:
            while not all(pcb.get_status() == "Terminate" for pcb in sjf_pcb_array[:num_processes]):
                highest_priority_index = find_highest_priority_non_terminated(num_processes)

                if highest_priority_index is not None:
                    sjf_pcb_array[highest_priority_index].burst_decrement()
                    if sjf_pcb_array[highest_priority_index].get_burst() == 0:
                        terminate_process(sjf_pcb_array[highest_priority_index])
                    else:
                        sjf_pcb_array[highest_priority_index].change_status("Running")

                # Set status of other processes to "Ready"
                for i, pcb in enumerate(sjf_pcb_array):
                    if i != highest_priority_index and pcb.get_status() != "Terminate":
                        pcb.change_status("Ready")

                # Remove terminated PCBs from the array
                sjf_pcb_array = [pcb for pcb in sjf_pcb_array if pcb.get_status() != "Terminate"]

                # # Emit signal to update the GUI table
                # if update_gui_signal:
                #     update_gui_signal.emit(sjf_pcb_array)

                time.sleep(1)
            break  # Exit the outer loop once all processes are terminated
        else:
            if num <= 1:
                sjf_pcb_array[0].burst_decrement()
                if sjf_pcb_array[0].get_burst() == 0:
                    terminate_process(sjf_pcb_array[0])
                else:
                    sjf_pcb_array[0].change_status("Running")

                # Set status of other processes to "Ready"
                for i, pcb in enumerate(sjf_pcb_array):
                    if i != 0 and pcb.get_status() != "Terminate":
                        pcb.change_status("Ready")

                # Remove terminated PCBs from the array
                sjf_pcb_array = [pcb for pcb in sjf_pcb_array if pcb.get_status() != "Terminate"]
                # if update_gui_signal:
                #     # Emit signal to update the GUI table
                #     update_gui_signal.emit(sjf_pcb_array)

                time.sleep(1)
            else:
                highest_priority_index = find_highest_priority_non_terminated(current_index)
                if highest_priority_index is not None:
                    sjf_pcb_array[highest_priority_index].burst_decrement()
                    if sjf_pcb_array[highest_priority_index].get_burst() == 0:
                        terminate_process(sjf_pcb_array[highest_priority_index])
                    else:
                        sjf_pcb_array[highest_priority_index].change_status("Running")

                # Set status of other processes to "Ready"
                for i, pcb in enumerate(sjf_pcb_array):
                    if i != highest_priority_index and pcb.get_status() != "Terminate":
                        pcb.change_status("Ready")

                # Remove terminated PCBs from the array
                sjf_pcb_array = [pcb for pcb in sjf_pcb_array if pcb.get_status() != "Terminate"]
                # if update_gui_signal:
                #     # Emit signal to update the GUI table
                #     update_gui_signal.emit(sjf_pcb_array)

                time.sleep(1)
            return

def find_highest_priority_non_terminated(current_index):
    global sjf_pcb_array

    lowest_priority_index = None
    for i in range(len(sjf_pcb_array)):
        if i != current_index and sjf_pcb_array[i].get_status() != "Terminate":
            if (lowest_priority_index is None or
                sjf_pcb_array[i].priority < sjf_pcb_array[lowest_priority_index].priority or
                (sjf_pcb_array[i].priority == sjf_pcb_array[lowest_priority_index].priority and
                 sjf_pcb_array[i].get_burst() < sjf_pcb_array[lowest_priority_index].get_burst())):
                lowest_priority_index = i

    return lowest_priority_index

def terminate_process(pcb):
    pcb.change_status("Terminate")
    pcb.burst_time = 0