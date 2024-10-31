import sys
import asyncio

from src.launcher import main
from src.deeplchain import log, mrh, clear, banner

if __name__ == "__main__":
    clear()
    banner()
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt as e:
            log(mrh + f"Keyboard interrupted by users.")
            sys.exit()