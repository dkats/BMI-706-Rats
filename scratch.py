import subprocess
import json

def calculate_bp_percentiles(age, sex, height, sbp, dbp):
    male = 1 if sex.lower() == 'male' else 0  # Convert sex to binary representation

    # Call the R script
    process = subprocess.run(
        ['Rscript', 'calculate_bp_percentiles.R', str(sbp), str(dbp), str(age), str(male), str(height)],
        capture_output=True,
        text=True,
        check=True
    )

    # Parse the JSON output from the R script
    results = json.loads(process.stdout)

    return results['sbp_percentile'], results['dbp_percentile']

# Example usage
age = 10
sex = 'Male'
height = 140
sbp = 120
dbp = 80

systolic_percentile, diastolic_percentile = calculate_bp_percentiles(age, sex, height, sbp, dbp)
print(f'Systolic Percentile: {systolic_percentile}')
print(f'Diastolic Percentile: {diastolic_percentile}')