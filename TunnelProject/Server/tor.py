import os
import subprocess


TOR_DIRECTORY = os.path.join(os.getenv("APPDATA"), "tor")
TOR_EXE = "tor.exe"
TOR_CONFIG_FILE = "torrc"


class Tor:

    def __init__(self):
        self._tor_directory = TOR_DIRECTORY
        self._tor_exe_path = os.path.join(self._tor_directory, TOR_EXE)
        self._tor_config_file_path = os.path.join(self._tor_directory, TOR_CONFIG_FILE)
        self._is_tor_set_up = False
        self._tor_process = None

    def setup(self):
        if not self._is_tor_set_up:
            self._tor_process = subprocess.Popen([self._tor_exe_path, "-f", self._tor_config_file_path],
                                                 stdout=subprocess.PIPE)
            self._is_tor_set_up = True

    def teardown(self):
        if self._is_tor_set_up:
            self._tor_process.kill()
            self._tor_process = None
            self._is_tor_set_up = False

    def is_tor_set_up(self):
        return self._is_tor_set_up
