from prettytable import PrettyTable
import time

# Global variable for the array of PCBs
priority_pcb_array = []
count = 0

def priority(pcb_array, current_index, num_processes, update_gui_signal):
    global priority_pcb_array

    # add list to array
    priority_pcb_array.append(pcb_array[current_index])

    # Emit signal to update the GUI table
    update_gui_signal.emit(priority_pcb_array)

    # Start the processing of the processes
    processing(num_processes, current_index, update_gui_signal)

def print_current_pcb_details():
    global priority_pcb_array
    for pcb in priority_pcb_array:
        print([pcb.pid, pcb.process_name, pcb.burst_time, pcb.memory_size, pcb.arrival_time, pcb.priority, pcb.status])

def processing(num_processes, current_index, update_gui_signal):
    global priority_pcb_array

    num = current_index + 1
    loop = True
    while True:
        if num == num_processes:
            while not all(pcb.get_status() == "Terminate" for pcb in priority_pcb_array[:num_processes]):
                highest_priority_index = find_highest_priority_non_terminated(num_processes)

                if highest_priority_index is not None:
                    priority_pcb_array[highest_priority_index].burst_decrement()
                    if priority_pcb_array[highest_priority_index].get_burst() == 0:
                        terminate_process(priority_pcb_array[highest_priority_index])
                    else:
                        priority_pcb_array[highest_priority_index].change_status("Running")

                # Set status of other processes to "Ready"
                for i, pcb in enumerate(priority_pcb_array):
                    if i != highest_priority_index and pcb.get_status() != "Terminate":
                        pcb.change_status("Ready")

                # Remove terminated PCBs from the array
                priority_pcb_array = [pcb for pcb in priority_pcb_array if pcb.get_status() != "Terminate"]

                 # Emit signal to update the GUI table
                update_gui_signal.emit(priority_pcb_array)

                time.sleep(1)
        else:
            loop = False
            if num <= 1:
                priority_pcb_array[0].burst_decrement()
                if priority_pcb_array[0].get_burst() == 0:
                    terminate_process(priority_pcb_array[0])
                else:
                    priority_pcb_array[0].change_status("Running")

                # Set status of other processes to "Ready"
                for i, pcb in enumerate(priority_pcb_array):
                    if i != 0 and pcb.get_status() != "Terminate":
                        pcb.change_status("Ready")

                # Remove terminated PCBs from the array
                priority_pcb_array = [pcb for pcb in priority_pcb_array if pcb.get_status() != "Terminate"]

                # Emit signal to update the GUI table
                update_gui_signal.emit(priority_pcb_array)

                # print_table("During processing")
                time.sleep(1)

            else:
                highest_priority_index = find_highest_priority_non_terminated(current_index)
                if highest_priority_index is not None:
                    priority_pcb_array[highest_priority_index].burst_decrement()
                    if priority_pcb_array[highest_priority_index].get_burst() == 0:
                        terminate_process(priority_pcb_array[highest_priority_index])
                    else:
                        priority_pcb_array[highest_priority_index].change_status("Running")

                # Set status of other processes to "Ready"
                for i, pcb in enumerate(priority_pcb_array):
                    if i != highest_priority_index and pcb.get_status() != "Terminate":
                        pcb.change_status("Ready")
                # Emit signal to update the GUI table
                update_gui_signal.emit(priority_pcb_array)

                # display_pcb_table(priority_pcb_array)
                # print_table("During processing")
                time.sleep(1)

        if not loop:
            return


def find_highest_priority_non_terminated(current_index):
    global priority_pcb_array

    lowest_priority_index = None
    for i in range(len(priority_pcb_array)):
        if i != current_index and priority_pcb_array[i].get_status() != "Terminate":
            if (lowest_priority_index is None or
                priority_pcb_array[i].priority < priority_pcb_array[lowest_priority_index].priority or
                (priority_pcb_array[i].priority == priority_pcb_array[lowest_priority_index].priority and
                 priority_pcb_array[i].get_arrival() < priority_pcb_array[lowest_priority_index].get_arrival())):
                lowest_priority_index = i

    return lowest_priority_index

def terminate_process(pcb):
    pcb.change_status("Terminate")