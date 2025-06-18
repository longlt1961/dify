#!/bin/sh

TEST_DIR="/k6/scripts"
RESULT_DIR="/k6_results"
mkdir -p "$RESULT_DIR"

test_cases=$(find "$TEST_DIR" -maxdepth 1 -type f -name "TC_*.js")

if [ -z "$test_cases" ]; then
    echo "No test cases found in $TEST_DIR"
    exit 0
fi

for script in $test_cases; do   
    test_name=$(basename "$script" .js)
    timestamp=$(date +"%Y%m%d-%H%M%S")
    output_file="$RESULT_DIR/${test_name}.json"
    log_file="$RESULT_DIR/${test_name}.log"

    echo "Running $test_name..."

    # Record start time (in Unix seconds) for Prometheus query
    start_time=$(date +%s)
    echo "START_TIME=$start_time" > "$log_file"

    # Run the test
    k6 run --summary-export="$output_file" "$script"

    # Record end time
    end_time=$(date +%s)
    echo "END_TIME=$end_time" >> "$log_file"

    echo "$test_name finished. Results saved to:"
    echo "  - JSON: $output_file"
    echo "  - Log: $log_file"
    echo
done

echo "All test cases executed."