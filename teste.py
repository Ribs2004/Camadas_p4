import time

# Function to activate the timer
def activate_timer():
    return time.time()

# Function to calculate and return elapsed time
def elapsed_time(start_time):
    if start_time is None:
        return "Timer has not been activated yet."
    else:
        elapsed_seconds = time.time() - start_time
        return f"Elapsed time: {elapsed_seconds:.2f} seconds"

# Activate the timer
start_time = activate_timer()

# Check the elapsed time
print(elapsed_time(start_time))

# Wait for some time (simulating activity)
time.sleep(5)

# Check the elapsed time again
print(elapsed_time(start_time))



