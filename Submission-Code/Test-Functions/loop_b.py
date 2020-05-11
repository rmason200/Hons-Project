# import relevant libraries
# system libraries
import time
import threading

# loop counter
count = 0


def data_send():
	print("DATA SEND")


while True:
	# sets up time variable needed to ensure loop happens once a second
	# rather than <code runtime> + 1 second
	starttime = time.time()
	
	# prints counter to display progress of loop
	print("\nCount: " + str(count))
	
	# receives status of signal from API, prints to terminal
	print("DATA READ")
	
	if count == 10:
		# creates a thread to allow the data send process to run in parallel
		data_send_thread = threading.Thread(target = data_send)
		# starts the thread
		data_send_thread.start()
		
		# resets count to start loop again
		count = 0
     
	# increments loop
	count += 1
	# sleeps process for the rest of the second
	# takes process time and removes it from the second, then sleeps for remaining time
	time.sleep(1.0 - ((time.time() - starttime) % 60))
