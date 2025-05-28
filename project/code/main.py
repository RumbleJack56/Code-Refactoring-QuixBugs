from pathlib import Path
from test_harness import process_program
import csv

def main():
    buggy_dir = Path("../python_programs")
    fixed_dir = Path("../fixed_programs")
    fixed_dir.mkdir(exist_ok=True)
    
    results = []
    for program in buggy_dir.glob("*.py"):
        name, success, _ = process_program(program, fixed_dir)
        results.append((name, success))
        print(f"{name}: {'✓' if success else '✗'}")
    
    with open("../results.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Program", "Success"])
        writer.writerows(results)
    
    success_rate = sum(s for _, s in results) / len(results)
    print(f"\nSuccess Rate: {success_rate:.2%}")

if __name__ == "__main__":
    main()