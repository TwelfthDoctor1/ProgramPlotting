#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  TwelfthDoctor1's ProgramPlotting
#
#  > Main - ProgramPlotting
#
#  (C) Copyright TD1 & TWoCC 2025
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Licensed under MIT License
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#
#  Codes from other parties are not part of the License and Copyright.
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  REQUIREMENTS
#
#  - psutil, installed via pip
#  - matplotlib, installed via pip
#
#  GENERAL USAGE
#
#  1. Change the variable PROGRAM_NAME to the program name that you want to log
#  2. To specify the frequency of the log, change the INTERVAL variable
#  3. To start the python script, make sure to RUN AS ADMIN, by:
#     - Using sudo in UNIX or Windows (if sudo is enabled)
#     - Running Terminal/CMD Prompt as admin and running the script
#     Alternatively, use the bash script, if running in bash or its derivatives
#  4. Logging will only run when the program to be logged is running, run the
#     program to start the process
#  5. To stop the logging, simply quit the program
#  6. After stopping, the script will produce two graphs, one showing CPU Usage.
#     while the other showing memory usage
#  7. The script will end upon exiting the graph window
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import psutil
import time
import matplotlib.pyplot as plt
from UtilLib.Logging import LoggerClass

PROGRAM_NAME = "tictactoe"  # <-- Change the program name accordingly
INTERVAL = 0.1

cpu_usage = []
memory_usage = []
time_track = []

# Logger
logger = LoggerClass(
    module_name="ProgramPlotting",
    main_owner=PROGRAM_NAME,
    additional_context=f"ProgramPlotting of {PROGRAM_NAME}",
)


def get_pid_by_name(name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.name() == name:
            return proc.pid
    return None


if __name__ == '__main__':
    while True:
        try:
            pid = get_pid_by_name(PROGRAM_NAME)
            if pid is None:
                raise ValueError

            process = psutil.Process(pid)
            break

        except ValueError:
            print(f"Cannot find program named {PROGRAM_NAME}. Check if the program is running.")
            # Disabled, will cause flooding of logfile
            # logger.warn(f"Cannot find program named {PROGRAM_NAME}")

    logger.info(f"Program named {PROGRAM_NAME} is running. Starting logging...")

    start_time = time.time()

    while True:
        # print(psutil.pid_exists(pid))
        try:
            cpu_usage_i = process.cpu_percent() / psutil.cpu_count()
            memory_info = process.memory_info()
            memory_usage_i = memory_info.rss / (1024 * 1024)
            time_track_i = time.time() - start_time

            logger.info(f"[{time_track_i}] | CPU usage: {cpu_usage_i}% | Memory usage: {memory_usage_i}MB")

            cpu_usage.append(cpu_usage_i)
            memory_usage.append(memory_usage_i)
            time_track.append(time_track_i)

            time.sleep(INTERVAL)

            if not psutil.pid_exists(pid):
                break

        except psutil.NoSuchProcess:
            print(f"Process {PROGRAM_NAME} terminated.")
            logger.error(f"Process {PROGRAM_NAME} terminated.")
            break
        except Exception as e:
            print(f"Exception: {e}")
            logger.error(f"Exception: {e}")

    logger.info(f"Logging finished. Total time: {time.time()-start_time}")

    # plt.subplot(1, 2, 1)
    plt.figure(1)
    plt.plot(time_track, cpu_usage, label="CPU Usage (%)", color="blue")

    plt.xlabel("Time (s)")
    plt.ylabel("CPU Usage (%)")
    plt.title(f"CPU & Usage of {PROGRAM_NAME}")

    plt.legend()
    plt.grid()

    # plt.subplot(1, 2, 2)
    plt.figure(2)
    plt.plot(time_track, memory_usage, label="Memory Usage (MB)", color="red")

    plt.xlabel("Time (s)")
    plt.ylabel("Memory Usage (MB)")
    plt.title(f"Memory Usage of {PROGRAM_NAME}")

    plt.legend()
    plt.grid()

    plt.show()

    exit(0)
