# ProgramPlotting

#### Program Plotting Script that outputs a graph and log

###  Requirements
- psutil, installed via pip
- matplotlib, installed via pip

### General Usage

1. Change the variable PROGRAM_NAME to the program name that you want to log
2. To specify the frequency of the log, change the INTERVAL variable
3. To start the python script, make sure to RUN AS ADMIN, by:
   - Using sudo in UNIX or Windows (if sudo is enabled)
   - Running Terminal/CMD Prompt as admin and running the script
   - Alternatively, use the bash script, if running in bash or its derivatives
4. Logging will only run when the program to be logged is running, run the program to start the process
5. To stop the logging, simply quit the program
6. After stopping, the script will produce two graphs, one showing CPU Usage while the other showing memory usage
7. The script will end upon exiting the graph window