class Timer:
    def __init__(self, fps: int):

        self.fps = fps
        self.second = 0
        self.limit = 0

    def start_timer(self, frame: int) -> None:
        self.second = frame // self.fps

    def get_second(self) -> int:
        return self.second

    def restart_timer(self, frame: int) -> None:
        self.second = 0

    def set_timer_limit(self, limit: int) -> None:
        self.limit = limit

    def get_timer(self) -> int:
        return self.limit

    def hit_timer(self) -> bool:
        return self.get_second() == self.get_timer()
