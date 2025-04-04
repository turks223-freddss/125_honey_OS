# memory_converter.py

def memory_converter(memorySize, label):
    global full_memory_size
    if label == "GB":
        full_memory_size = memorySize * 1000000000
    elif label == "MB":
        full_memory_size = memorySize * 1000000
    else:
        full_memory_size = memorySize * 1000
    print(full_memory_size)
    return full_memory_size
