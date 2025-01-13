import csv
from datetime import datetime, timedelta
import random, os

def read_csv(file_path):
    """Reads input CSV file and returns a list of programs."""
    programs = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            programs.append(row)
    return programs

def write_csv(file_path, programs):
    """Writes scheduled programs to output CSV file."""
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(programs)



def correct_schedule(programs, current_start):
    """Adjusts the schedule to meet the requirements."""
    scheduled = []
    active_programs = []  # Tracks active programs by time

    for program in programs:
        name, password, pid, start_time, rand_start, duration, rand_duration, *_ = program 
        identifier = program[-1]

        base_start = datetime.strptime(start_time, "%H:%M")
        rand_start = float(rand_start)
        duration = float(duration)
        rand_duration = float(rand_duration)
        match current_start:
            case "min":
              current_start = base_start - timedelta(hours=rand_start)
            case "max":
              current_start = base_start + timedelta(hours=rand_start)
            # case _:
            #   current_start = input("Specify start condition: ")

        

        # start_min = base_start - timedelta(hours=rand_start)
        # start_max = base_start + timedelta(hours=rand_start)
        # Formula
        # current_start = start_min 
        while True:
            # Check max concurrent programs
            active_programs = [p for p in active_programs if p[1] > current_start]
            if len(active_programs) < 4:
                # Check identifier spacing
                if all(
                    p[2] != identifier or (current_start - p[0]).total_seconds() >= 3600
                    for p in active_programs
                ):
                    # Check for 1-minute difference for different identifiers
                    if all(
                        abs((current_start - p[0]).total_seconds()) >= 60
                        for p in active_programs if p[2] != identifier
                    ):
                        break
            current_start += timedelta(minutes=1)

        # Schedule program
        program_start = current_start
        program_end = program_start + timedelta(hours=duration + rand_duration)
        active_programs.append((program_start, program_end, identifier))
        scheduled.append([
            name, password, pid, program_start.strftime("%H:%M"), rand_start,
            duration, rand_duration, *program[7:]
        ])

    # Sort scheduled programs by their start time
    scheduled.sort(key=lambda x: datetime.strptime(x[3], "%H:%M"))
    
    return scheduled

if __name__ == "__main__":
    input_file = input("Specify file: ") or "file.csv" 
    # input_file = (input("Specify file: ")+'{ext}'.format(ext = '.csv')) or "file.csv" # Assuming unnecessary to input a fullname  
    L = ["max", "min"]

    type_of_start = input("Define start condition: ") or (random.choice(L)) # Semaforical randomizer
    output_file = "output.csv"

    # Read input data
    programs = read_csv(input_file)

    # Adjust schedule
    scheduled_programs = correct_schedule(programs, type_of_start)
    # Write to output
    write_csv(output_file, scheduled_programs)

    print("Output saved to", output_file,)

