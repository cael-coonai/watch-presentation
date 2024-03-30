import signal
from datetime import datetime, timedelta
from touch_sdk import Watch
from pynput.keyboard import Key, Controller

class MyWatch(Watch):
    def on_tap(self):
        global keyboard
        global last_tap_time
        now = datetime.now()
        if is_double_tap(last_tap_time, now, 1):
            print("Double Tap")
            keyboard.press(Key.right)
            keyboard.release(Key.right)
        else:
            print("Tap")
        last_tap_time = now

    
    def on_touch_up(self, x, y):
        global keyboard
        global touch_pos_start
        touch_pos_end = (x, y)
        screen_height:int = 450
        swipe_distance:float = screen_height / 10

        if abs(touch_pos_start[1] - touch_pos_end[1]) >= swipe_distance:
            if touch_pos_start[1] - touch_pos_end[1] < 0:
                print(f"Swipe Down {x} {y}")
                keyboard.press(Key.right)
                keyboard.release(Key.right)
            else:
                print(f"Swipe Up {x} {y}")
                keyboard.press(Key.left)
                keyboard.release(Key.left)
        else:
            print(f"Touch Up {x} {y}")


    def on_touch_down(self, x, y):
        global touch_pos_start
        print(f"Touch Down {x} {y}")
        touch_pos_start = (x, y)


    def on_rotary(self, direction):
        global keyboard
        print(f"Rotery: {direction}")
        if direction > 0:
            keyboard.press(Key.right)
            keyboard.release(Key.right)
        else:
            keyboard.press(Key.left)
            keyboard.release(Key.left)


watch: MyWatch
last_tap_time: datetime
keyboard: Controller
touch_pos_start: tuple[float, float]

def is_double_tap(first: datetime, second: datetime, diff_sec: float) -> bool:
    difference: timedelta = second - first
    return difference.total_seconds() <= diff_sec
    

def handler(signal, frame) -> None:
    watch.stop()
    exit(0)


def main() -> None:
    signal.signal(signal.SIGINT, handler)
    global watch
    global keyboard
    global last_tap_time
    last_tap_time = datetime.now();
    keyboard = Controller()
    watch = MyWatch()
    watch.start()

main()