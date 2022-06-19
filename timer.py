class Timer:
    def __init__(self, fps: int, a_limit: int = 10):

        self.fps = fps
        self.frame = 0
        self.second = 0
        self.limit = a_limit

    def run_timer(self) -> bool:
        """returns the bool value for the timer limit. If limit not reached
        will increase frame and second"""
        if not self.timer_finished():
            self.frame += 1
            self.second = self.frame // self.fps

        return self.timer_finished()

    def get_second(self) -> int:
        """returns the second"""
        return self.second

    def reset_timer(self) -> None:
        """resets the seconds and frame to zero"""
        self.frame = 0
        self.second = 0

    def set_timer_limit(self, limit: int) -> None:
        """sets the limit"""
        self.limit = limit

    def get_limit(self) -> int:
        """returns the limit"""
        return self.limit

    def timer_finished(self) -> bool:
        """Returns true if the seconds have reached the timer, else false"""
        return self.get_second() >= self.get_limit()
