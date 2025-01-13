#!/bin/bash

CSV_FILE="output.csv"
PYTHON_SCRIPT="/home/lancelot/Python/Counter/programs/prog1/app.py"

# Initialize port counter and define maximum concurrent processes
port_counter=0
max_ports=4 # Maximum number of concurrent processes
base_port=5010 # Starting port number

# Read the CSV file line by line
while IFS=',' read -r program password pid start_time rand_start duration rand_duration field1 field2 field3 field4 ident; do
  ident_number=$(echo "$ident" | grep -oP '(?<=-)\d+')

  # Create JSON string
json_string=$(jq -n \
    --arg name "$program" \
    --arg password "$password" \
    --arg start_time "$start_time" \
    --arg rand_start "$rand_start" \
    --arg duration "$duration" \
    --arg rand_duration "$rand_duration" \
    --arg ident "$ident_number" \
    '{
        name: $name,
        password: $password,
        start_time: $start_time,
        rand_start: $rand_start,
        duration: $duration,
        rand_duration: $rand_duration,
        ident: $ident
    }'
)

  while (( port_counter < max_ports )); do
    port=$((base_port + port_counter))
    echo "Running: python3 $PYTHON_SCRIPT '$json_string' on port $port"
    python3 "$PYTHON_SCRIPT" "$json_string" "$port" &

    port_counter=$((port_counter + 1))
  done

  while (( port_counter >= max_ports )); do
    running_processes=$(pgrep -fc "flask")
    if (( running_processes < max_ports )); then
      port_counter=$((running_processes))
      break
    fi
    echo "Sleeping: $running_processes processes are running."
    sleep 2
  done

  echo "Enough, processes currently running are $port_counter"


done < "$CSV_FILE"
