import threading
import time

class ExampleClass:
    def __init__(self):
        self.shared_data = 0  # Example shared data

    def method_part_one(self):
        for i in range(5):
            self.shared_data += 1
            print(f"Part One: Shared data = {self.shared_data}")
            time.sleep(1)

    def method_part_two(self):
        for i in range(5):
            self.shared_data += 2
            print(f"Part Two: Shared data = {self.shared_data}")
            time.sleep(1)

    def run_threads(self):
        # Create threads for the methods
        thread_one = threading.Thread(target=self.method_part_one)
        thread_two = threading.Thread(target=self.method_part_two)

        # Start the threads
        thread_one.start()
        thread_two.start()

        # Wait for threads to finish
        thread_one.join()
        thread_two.join()

        print("Both threads have finished.")

# Example usage
example = ExampleClass()
example.run_threads()
