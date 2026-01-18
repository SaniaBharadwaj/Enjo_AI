# ENJO - Anthropomorphic AI Assistant
# Copyright (C) 2026 Sania
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

#print(">> DEBUG: main.py has started...")  # If you don't see this, Python isn't running the file.

from enjo import ENJO  # noqa: E402

if __name__ == "__main__":
    #print("\n>> DEBUG: Creating ENJO instance...")
    bot = ENJO()

    #print(">> DEBUG: Starting Main Loop...")
    bot.run()  # <--- This is the critical line that keeps it alive