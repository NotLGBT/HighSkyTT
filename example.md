What's inside 

./script.sh - Demo version of possible daemon - launching and refreshing jobs by time intervals, which spotted reviewing output.csv file
./programs/prog1/app.py - Flask application, simulating programs workload by using difference json and ports args. 
./file.csv - Sample from Technical Task originally provided by HR manager 
./prog.py - Primary Script used for creation valid queue of jobs for launching


Example of request to app.py
python3 /home/lancelot/Python/Counter/programs/prog1/app.py '{
    "name": "program1",
    "password": "password1",
    "start_time": "10:43",
    "rand_start": "0.3",
    "duration": "5.0",
    "rand_duration": "1.5",
    "ident": "666666"
  }' "5010" 