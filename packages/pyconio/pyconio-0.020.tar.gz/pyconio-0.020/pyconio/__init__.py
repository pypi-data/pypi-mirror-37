import os
import sys

if os.name == "nt" and sys.getwindowsversion()[0] >= 10:
    if sys.getwindowsversion()[2] >= 10586:
        # Starting from Windows 10 TH2, ANSI codes are finally supported.
        import ctypes

        kernel32 = ctypes.windll.kernel32
        # Setting ENABLE_VIRTUAL_TERMINAL_PROCESSING
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        from .pyconio_module import *

    else:
        from .oldwin_pyconio import *

elif os.name == "nt" and sys.getwindowsversion()[0] < 10:
    # Dirty version of pyconio, for older
    # Windows. e.g XP, Vista, 7, 8.x, etc.
    from .oldwin_pyconio import *

else:
    from .pyconio_module import *
