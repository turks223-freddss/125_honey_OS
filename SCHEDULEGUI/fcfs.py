import time

# Global variable for the array of PCBs
fcfs_pcb_array = []

def fcfs(pcb_array, current_index, num_processes, update_gui_signal):
    global fcfs_pcb_array

    # Add the current process control block to the array
    fcfs_pcb_array.append(pcb_array[current_index])
    if update_gui_signal:
        # Emit signal to update the GUI table
        update_gui_signal.emit(fcfs_pcb_array)

    # Start the processing of the processes
    processing_fcfs(num_processes, update_gui_signal)

def processing_fcfs(num_processes, update_gui_signal):
    global fcfs_pcb_array

    process_index = 0
    while process_index < num_processes:
        pcb = fcfs_pcb_array[process_index]

        # Skip if the process is already terminated (shouldn't happen, but safety check)
        if pcb.get_status() == "Terminate":
            process_index += 1
            continue

        # Set process to running
        pcb.change_status("Running")
        if update_gui_signal:
            update_gui_signal.emit(fcfs_pcb_array)

        # Simulate running by decrementing burst until 0
        while pcb.get_burst() > 0:
            pcb.burst_decrement()
            if update_gui_signal:
                update_gui_signal.emit(fcfs_pcb_array)
            time.sleep(1)

        # Terminate when done
        terminate_process(pcb)
        if update_gui_signal:
            update_gui_signal.emit(fcfs_pcb_array)

        process_index += 1

def terminate_process(pcb):
    pcb.change_status("Terminate")
    pcb.burst_time = 0
