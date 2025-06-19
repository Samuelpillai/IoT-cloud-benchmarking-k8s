import requests
import time
import os
import threading

class LoadGenerator:
    def __init__(self, target, frequency):
        self.target = target
        self.frequency = frequency
        self.response_times = []
        self.failures = 0
        self.running = False
        self.response_count = 0

    def generate_load(self):
        while self.running:
            self.response_count += 1
            start_time = time.time()
            try:
                response = requests.get(self.target, timeout=10)
                response.raise_for_status()
                elapsed_time = time.time() - start_time
                self.response_times.append(elapsed_time)
                print(f"Request {self.response_count}: Successful | Failure = 0 | Response Time = {elapsed_time:.2f}s")
            except requests.RequestException as e:
                self.failures += 1
                print(f"Request {self.response_count}: Failed     | Failure = 1 | Response Time = 0.00s")
            time.sleep(self.frequency)
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.generate_load)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def print_results(self):
        total_requests = len(self.response_times) + self.failures
        avg_response_time = (sum(self.response_times) / len(self.response_times) if self.response_times else 0)

        print(f"\nFinal Results:")
        print(f"Total Requests: {total_requests}")
        print(f"Average Response Time: {avg_response_time:.2f} seconds")
        print(f"Total Failures: {self.failures}")

if __name__ == "__main__":
    target_url = os.getenv("TARGET_URL", "http://localhost:8000")
    frequency = float(os.getenv("FREQUENCY", 1.0))

    load_generator = LoadGenerator(target=target_url, frequency=frequency)
    try:
        load_generator.start()
        print(f"Load generator started for {target_url} with frequency {frequency} seconds.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        load_generator.stop()
        load_generator.print_results()
        print("Load generator stopped.")