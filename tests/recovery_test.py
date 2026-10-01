import threading
import time

from src.bulb.bulb_local import bulb, reconnect, set_color
from src.bulb.worker import start, stop, _recovery_event, set_state
import src.bulb.worker as worker


OLD_STATE = ("color", (0, 1000, 1000))       # RED
NEW_STATE = ("color", (240, 1000, 1000))     # BLUE

old_command_started = threading.Event()
release_old_command = threading.Event()

original_set_color = worker.set_color

call_count = 0
call_lock = threading.Lock()


def test_set_color(h, s, v):
    """Block only the first color command, then use the real function."""

    global call_count

    with call_lock:
        call_count += 1
        current_call = call_count

    if current_call == 1:
        print("TEST: OLD RED command started")
        old_command_started.set()

        print("TEST: holding OLD RED command...")

        release_old_command.wait()

        print("TEST: OLD RED command released")

    # Every command eventually uses the REAL bulb implementation.
    original_set_color(h, s, v)


def main():
    print("Starting deterministic recovery race test...")

    # Replace worker's color function temporarily.
    worker.set_color = test_set_color

    try:
        worker.start()

        # Give the worker a known initial state.
        worker.set_state(*OLD_STATE)

        # Wait until the worker is actually stuck in RED.
        if not old_command_started.wait(timeout=5):
            print("ERROR: OLD RED command never started.")
            return

        print()
        print("1. OLD RED is currently in-flight.")

        # Change desired state while RED is still stuck.
        worker.set_state(*NEW_STATE)

        print("2. Latest desired state changed to BLUE.")

        # Trigger the REAL recovery mechanism.
        print("3. Triggering REAL recovery...")
        worker._recovery_event.set()

        while not worker._recovering:
            time.sleep(0.01)

        # Wait for recovery to finish.
        recovery_timeout = time.time() + 10

        while worker._recovering:
            if time.time() > recovery_timeout:
                print("ERROR: Recovery timed out.")
                return

            time.sleep(0.01)

        print("4. Recovery finished.")

        # Give the recovery thread a moment to complete its state restore.
        time.sleep(0.2)

        print("5. Releasing OLD RED command...")
        release_old_command.set()

        # Let the old worker command finish.
        time.sleep(1)

        print()
        print("Test finished.")

    finally:
        # Always release the blocked command.
        release_old_command.set()

        # Restore the real function.
        worker.set_color = original_set_color

        worker.stop()


if __name__ == "__main__":
    main()


#-----------------------TEST-7-----------------------
# def old_operation():
#     print("OLD: starting RED command")

#     try:
#         set_color(0, 1000, 1000)
#         print("OLD: RED command finished")
#     except Exception as e:
#         print(f"OLD: command failed: {e}")


# print("Starting real recovery race test...")

# start()

# # The state Swift Immerse currently wants.
# set_state("color", (240, 1000, 1000))

# print("Starting old operation...")
# old_thread = threading.Thread(
#     target=old_operation,
#     daemon=True
# )

# old_thread.start()

# # Give the old operation a moment to start.
# time.sleep(0.1)

# print("Triggering recovery...")
# _recovery_event.set()

# # Give recovery time to establish the fresh connection.
# time.sleep(2)

# print("Latest desired state should still be BLUE.")

# old_thread.join(timeout=1)

# print("Old operation alive:", old_thread.is_alive())

# stop()

# print("Test finished.")


# #-----------------------TEST-6-----------------------
# print("Starting recovery event test...")

# start()

# set_state("color", (240, 1000, 1000))
# time.sleep(0.5)

# print("Simulating confirmed failure...")
# _recovery_event.set()

# time.sleep(1)

# print("Stopping worker...")
# stop()

# print("Test finished.")


#-----------------------TEST-5-----------------------
# print("Starting REAL socket recovery test...")

# print("Current bulb:", id(bulb))
# print("Current socket:", bulb.socket)

# # Make sure we have a socket first.
# print("\n1. Sending RED...")
# set_color(0, 1000, 1000)

# print("\n2. Current socket after RED:")
# old_socket = bulb.socket
# print(old_socket)

# if old_socket is None:
#     print("ERROR: No persistent socket exists.")
#     raise SystemExit(1)


# # Simulate the recovery situation by deliberately closing
# # the socket while a command is about to happen.
# def delayed_blue():
#     time.sleep(0.2)

#     print("\nBLUE thread: sending BLUE...")
#     try:
#         bulb.set_hsv(
#             240 / 360,
#             1.0,
#             1.0,
#             nowait=True
#         )
#         print("BLUE thread: command returned.")
#     except Exception as e:
#         print(f"BLUE thread: command failed: {e}")


# print("\n3. Starting BLUE command...")
# thread = threading.Thread(target=delayed_blue, daemon=True)
# thread.start()

# time.sleep(0.1)

# print("\n4. Closing OLD socket...")
# try:
#     old_socket.close()
# except Exception as e:
#     print("Socket close error:", e)

# print("Old socket closed.")

# thread.join(3)

# print("\n5. Reconnecting...")
# _reconnect()

# print("New bulb:", id(bulb))
# print("New socket:", bulb.socket)

# print("\n6. Sending BLUE using fresh bulb...")

# try:
#     bulb.set_hsv(
#         240 / 360,
#         1.0,
#         1.0,
#         nowait=True
#     )

#     print("Fresh BLUE command returned.")

# except Exception as e:
#     print("Fresh BLUE failed:", e)

# print("\nTest finished.")


#-----------------------TEST-4-----------------------
# class FakeSocket:
#     def __init__(self):
#         self.closed = False
#         self.lock = threading.Lock()

#     def send(self, value):
#         print(f"SOCKET: sending {value}")

#         # Simulate a blocked network operation.
#         for _ in range(50):
#             time.sleep(0.1)

#             with self.lock:
#                 if self.closed:
#                     print(f"SOCKET: {value} cancelled")
#                     return False

#         print(f"SOCKET: {value} reached bulb")
#         return True

#     def close(self):
#         with self.lock:
#             self.closed = True

#         print("SOCKET: closed")


# def run_command(socket, value, timeout):
#     result = {}

#     def command():
#         result["success"] = socket.send(value)

#     thread = threading.Thread(target=command, daemon=True)
#     thread.start()

#     thread.join(timeout)

#     if thread.is_alive():
#         print(f"TIMEOUT: {value}")
#         return False

#     return result.get("success", False)


# print("Starting socket recovery test...")

# old_socket = FakeSocket()

# print("\n1. Sending RED through old socket...")
# success = run_command(old_socket, "RED", timeout=1)

# if not success:
#     print("\n2. RED timed out.")
#     print("3. Closing old socket...")
#     old_socket.close()

#     print("4. Creating new socket...")
#     new_socket = FakeSocket()

#     print("5. Sending BLUE through new socket...")
#     new_socket.send("BLUE")

# print("\n6. Waiting for old operation...")
# time.sleep(1)

# print("\nTest finished.")


#-----------------------TEST-3-----------------------
# class FakeBulb:
#     def __init__(self, name):
#         self.name = name

#     def send(self, value, delay):
#         print(f"{self.name}: sending {value}")
#         time.sleep(delay)
#         print(f"{self.name}: finished {value}")


# def run_command(bulb, value, delay, timeout):
#     thread = threading.Thread(
#         target=bulb.send,
#         args=(value, delay),
#         daemon=True,
#     )

#     thread.start()
#     thread.join(timeout)

#     if thread.is_alive():
#         print(f"{bulb.name}: TIMEOUT on {value}")
#         return False

#     return True


# print("Starting recovery race test...")

# old_bulb = FakeBulb("OLD BULB")

# print("\n1. Starting old command...")
# success = run_command(
#     old_bulb,
#     "RED",
#     delay=5,
#     timeout=1,
# )

# if not success:
#     print("\n2. Old command timed out.")
#     print("3. Creating fresh bulb...")

#     new_bulb = FakeBulb("NEW BULB")

#     print("4. Sending latest state through new bulb...")
#     success = run_command(
#         new_bulb,
#         "BLUE",
#         delay=0.1,
#         timeout=1,
#     )

#     if success:
#         print("5. NEW BULB successfully handled BLUE.")
#     else:
#         print("5. NEW BULB FAILED.")

# print("\n6. Main logic continues.")

# # Give the abandoned OLD BULB operation time to finish.
# time.sleep(5)

# print("\nTest finished.")


#-----------------------TEST-2-----------------------
# def fake_bulb_command():
#     print("BULB: command started")

#     # Simulate a TinyTuya/network hang
#     time.sleep(5)

#     print("BULB: command finished")


# def run_bulb_command(timeout=1.0):
#     thread = threading.Thread(
#         target=fake_bulb_command,
#         daemon=True
#     )

#     thread.start()
#     thread.join(timeout)

#     if thread.is_alive():
#         print("BULB: TIMEOUT")
#         return False

#     print("BULB: SUCCESS")
#     return True


# print("Starting recovery worker test...")

# result = run_bulb_command(timeout=1.0)

# if not result:
#     print("RECOVERY: abandoning old operation")
#     print("RECOVERY: creating fresh connection...")
#     time.sleep(0.2)
#     print("RECOVERY: fresh connection ready")
#     print("RECOVERY: sending latest state")

# print("Main logic continues.")

# time.sleep(1)

# print("Test finished.")


#-----------------------TEST-1-----------------------
# def fake_bulb_command():
#     print("FAKE BULB: command started")
#     time.sleep(10)
#     print("FAKE BULB: command finished")


# def run_with_timeout(timeout=1.0):
#     thread = threading.Thread(target=fake_bulb_command)
#     thread.start()

#     thread.join(timeout)

#     if thread.is_alive():
#         print(f"TIMEOUT: bulb command exceeded {timeout}s")
#         return False

#     print("SUCCESS: bulb command finished normally")
#     return True


# print("Starting recovery timeout test...")

# success = run_with_timeout(1.0)

# if not success:
#     print("Recovery path would begin here.")

# print("Test finished.")