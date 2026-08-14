import ctypes
from ctypes import wintypes


_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

_CreateMutexW = _kernel32.CreateMutexW
_CreateMutexW.argtypes = [
    wintypes.LPVOID,
    wintypes.BOOL,
    wintypes.LPCWSTR,
]
_CreateMutexW.restype = wintypes.HANDLE

_CloseHandle = _kernel32.CloseHandle
_CloseHandle.argtypes = [wintypes.HANDLE]
_CloseHandle.restype = wintypes.BOOL


class SingleInstance:
    def __init__(self, name="SwiftImmerse"):
        self.name = name
        self.handle = None

    def acquire(self):
        self.handle = _CreateMutexW(None, False, self.name)

        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())

        # ERROR_ALREADY_EXISTS = 183
        if ctypes.get_last_error() == 183:
            _CloseHandle(self.handle)
            self.handle = None
            return False

        return True

    def release(self):
        if self.handle:
            _CloseHandle(self.handle)
            self.handle = None