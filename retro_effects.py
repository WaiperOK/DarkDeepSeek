"""
🎨 Дополнительные ретро-эффекты для терминала в стиле 90-х
"""
import time
import random
import os
from rich.console import Console
from rich.text import Text
from rich.panel import Panel

class RetroEffects:
    """English docstring"""

    def __init__(self, console: Console):
        self.console = console
        self.primary_color = "bright_green"
        self.amber_color = "yellow"
        self.cyan_color = "bright_cyan"

    def crt_flicker(self, duration: float = 2.0):
        """English docstring"""
        end_time = time.time() + duration

        while time.time() < end_time:
            for _ in range(random.randint(1, 3)):
                y_pos = random.randint(0, 24)
                noise_line = "".join(random.choices("░▒▓█", k=80))

                self.console.print(f"\033[{y_pos};0H{noise_line}", style="dim white", end="")
                time.sleep(0.02)

                self.console.print(f"\033[{y_pos};0H{' ' * 80}", end="")

            time.sleep(random.uniform(0.1, 0.3))

    def boot_disk_check(self):
        """English docstring"""
        self.console.print("Checking file system on C:", style=self.amber_color)
        self.console.print("The type of the file system is NTFS.", style=self.amber_color)
        self.console.print("Volume label is DARKDEEPSEEK.", style=self.amber_color)
        self.console.print()

        total_sectors = 2048576
        bad_sectors = 0

        for i in range(0, total_sectors, 8192):
            if random.random() < 0.001:
                bad_sectors += 1
                self.console.print(f"Bad sector found at {i}", style="bright_red")

            if i % 65536 == 0:
                percent = (i / total_sectors) * 100
                self.console.print(f"Checking sectors: {percent:.1f}%", style=self.amber_color, end="\r")
                time.sleep(0.1)

        self.console.print()
        self.console.print(f"Disk check complete. {bad_sectors} bad sectors found.", style=self.primary_color)
        self.console.print()

    def modem_connection(self):
        """English docstring"""
        modem_sounds = [
            "ATDT1234567890",
            "CONNECT 56000",
            "CARRIER 56000",
            "PROTOCOL: LAP-M",
            "COMPRESSION: V.42BIS"
        ]

        self.console.print("Initializing modem...", style=self.amber_color)
        time.sleep(0.5)

        for sound in modem_sounds:
            self.console.print(sound, style=self.cyan_color)
            time.sleep(random.uniform(0.5, 1.5))

        self.console.print("♪♫♪♪♫♪♫♪", style="bright_yellow")
        time.sleep(1)

        self.console.print("Connected to DarkNet BBS", style=self.primary_color)
        self.console.print("Welcome to the Underground", style=self.primary_color)
        self.console.print()

    def ascii_art_hacker(self):
        """English docstring"""
        hacker_art = """
                    .-""""""-.
                  .'          '.
                 /   O      O   \\
                :           `    :
                |                |
                :    .------.    :
                 \\  '        '  /
                  '.          .'
                    '-.......-'

            ╔═══════════════════════════════╗
            ║        ELITE HACKER           ║
            ║      ACCESS GRANTED           ║
            ╚═══════════════════════════════╝
        """

        for line in hacker_art.split('\n'):
            self.console.print(line, style=self.primary_color)
            time.sleep(0.1)

    def loading_bar_retro(self, text: str, duration: float = 3.0):
        """English docstring"""
        self.console.print(f"{text}:", style=self.amber_color)

        bar_length = 50
        chars = "░▒▓█"

        for i in range(bar_length + 1):
            percent = (i / bar_length) * 100
            filled = "█" * i
            empty = "░" * (bar_length - i)

            bar = f"[{filled}{empty}] {percent:3.0f}%"
            self.console.print(f"\r{bar}", style=self.primary_color, end="")
            time.sleep(duration / bar_length)

        self.console.print(" COMPLETE", style=self.primary_color)

    def terminal_login_sequence(self):
        """English docstring"""
        self.console.print("DarkDeepSeek Security System v2.4", style=self.amber_color)
        self.console.print("Unauthorized access is prohibited", style="bright_red")
        self.console.print("All activities are monitored and logged", style="bright_red")
        self.console.print()

        self.console.print("Login: ", style=self.amber_color, end="")
        time.sleep(0.5)
        self.console.print("root", style=self.primary_color)

        self.console.print("Password: ", style=self.amber_color, end="")
        time.sleep(1)
        self.console.print("*" * 12, style=self.primary_color)

        time.sleep(1)
        self.console.print("Authenticating...", style=self.amber_color)
        time.sleep(2)

        self.console.print("Access granted", style=self.primary_color)
        self.console.print("Welcome, Elite Hacker", style=self.primary_color)
        self.console.print()

    def matrix_rain(self, duration: float = 5.0):
        """English docstring"""
        matrix_chars = "0123456789ABCDEF!@#$%^&*()_+-=[]{}|;:,.<>?"
        columns = 80
        drops = [0] * columns

        end_time = time.time() + duration

        while time.time() < end_time:
            self.console.print("\033[2J\033[H", end="")

            for i in range(25):
                line = ""
                for j in range(columns):
                    if drops[j] > i:
                        line += " "
                    elif drops[j] == i:
                        line += random.choice(matrix_chars)
                    else:
                        line += random.choice(matrix_chars) if random.random() < 0.1 else " "

                self.console.print(line, style=self.primary_color)

            for j in range(columns):
                if drops[j] == 0 and random.random() < 0.075:
                    drops[j] = 1
                elif drops[j] > 25:
                    drops[j] = 0
                else:
                    drops[j] += 1

            time.sleep(0.1)

    def old_computer_startup(self):
        """English docstring"""
        startup_messages = [
            "Phoenix BIOS 4.0 Release 6.0",
            "Copyright 1985-1995 Phoenix Technologies Ltd.",
            "CPU: Intel 80486 DX2-66",
            "Memory Test: 640K OK",
            "Extended Memory: 7168K OK",
            "Fixed Disk 0: 540MB",
            "Floppy A: 1.44MB 3.5\"",
            "",
            "Press DEL to enter SETUP",
            "",
            "Loading MS-DOS...",
            "",
            "Microsoft(R) MS-DOS(R) Version 6.22",
            "Copyright (C) Microsoft Corp 1981-1994.",
            "",
            "C:\\>"
        ]

        for msg in startup_messages:
            if msg:
                self.console.print(msg, style=self.amber_color)
                time.sleep(random.uniform(0.2, 0.8))
            else:
                self.console.print()
                time.sleep(0.3)

    def glitch_effect(self, text: str):
        """English docstring"""
        glitch_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"

        for _ in range(5):
            glitched = ""
            for char in text:
                if random.random() < 0.1:
                    glitched += random.choice(glitch_chars)
                else:
                    glitched += char

            self.console.print(f"\r{glitched}", style="bright_red", end="")
            time.sleep(0.1)

        self.console.print(f"\r{text}", style=self.primary_color)

    def cyber_banner(self):
        """English docstring"""
        banner = """
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    █                                                                      █
    █  ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██████╗ ██╗   ██╗███╗   ██╗██╗ █
    █ ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔══██╗██║   ██║████╗  ██║██║ █
    █ ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██████╔╝██║   ██║██╔██╗ ██║██║ █
    █ ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██╔═══╝ ██║   ██║██║╚██╗██║██║ █
    █ ╚██████╗   ██║   ██████╔╝███████╗██║  ██║██║     ╚██████╔╝██║ ╚████║██║ █
    █  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═══╝╚═╝ █
    █                                                                      █
    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
        """

        for line in banner.split('\n'):
            if line.strip():
                self.console.print(line, style=self.cyan_color)
                time.sleep(0.1)
