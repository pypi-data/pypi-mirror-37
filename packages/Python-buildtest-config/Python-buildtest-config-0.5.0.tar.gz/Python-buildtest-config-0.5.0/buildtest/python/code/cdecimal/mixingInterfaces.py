from cdecimal import *
c = getcontext()               # Global (thread-local) context

c.traps[Inexact] = True        # Trap the Inexact signal
c.traps[Inexact] = False       # Clear the Inexact signal

c._traps |= DecInexact         # Trap the Inexact signal
c.traps[Inexact]
print c.traps[Inexact]
c._traps &= ~DecInexact        # Clear the Inexact signal
c.traps[Inexact]
print c.traps[Inexact]
