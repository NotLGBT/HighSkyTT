# Project Overview

This repository demonstrates a daemon-like workflow for launching and refreshing jobs at specified time intervals. It includes scripts and components to simulate workloads and manage job queues effectively.

## Directory Structure

- **`./script.sh`**  
  A demo script simulating a possible daemon process:  
  - Launches and refreshes jobs at predefined intervals.  
  - Reviews and processes the `output.csv` file to determine job configurations.

- **`./programs/prog1/app.py`**  
  A Flask-based application simulating workloads:  
  - Accepts JSON and port arguments to configure and run jobs.  
  - Provides endpoints for health checks and workload simulation.

- **`./file.csv`**  
  A sample CSV file provided as part of the technical task from the HR manager:  
  - Used to generate and configure job queues.

- **`./prog.py`**  
  The primary script for creating a valid queue of jobs:  
  - Parses `file.csv` and prepares configurations for `app.py`.

---

## Example Usage

### Running `app.py`

To launch the Flask application with specific configurations:

```bash
python3 /home/lancelot/Python/Counter/programs/prog1/app.py '{
    "name": "program1",
    "password": "password1",
    "start_time": "10:43",
    "rand_start": "0.3",
    "duration": "5.0",
    "rand_duration": "1.5",
    "ident": "666666"
}' "5010"
