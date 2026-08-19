import time

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.timestamps = []

    def is_allowed(self) -> bool:
        now = time.time()
        self.timestamps = [t for t in self.timestamps if now - t <= self.window_seconds]
        if len(self.timestamps) < self.max_requests:
            self.timestamps.append(now)
            return True
        return False


limiter = RateLimiter(max_requests=3, window_seconds=10)
print(limiter.is_allowed())  # True  (1st request)
print(limiter.is_allowed())  # True  (2nd request)
print(limiter.is_allowed())  # True  (3rd request)
print(limiter.is_allowed())  # False (4th request, over limit)
time.sleep(11)
print(limiter.is_allowed())