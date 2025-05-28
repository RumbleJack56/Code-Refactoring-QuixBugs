import subprocess
from pathlib import Path
from code_repair_agent import CodeRepairAgent

def run_test(program_path):
    result = subprocess.run(
        ["python", "tester.py", str(program_path)],
        capture_output=True,
        text=True
    )
    return result.stdout, result.stderr

def process_program(program_path, fixed_dir):
    agent = CodeRepairAgent()
    with open(program_path, 'r') as f:
        code = f.read()
    
    test_output, test_error = run_test(program_path)
    if "FAILED" not in test_output:
        return (program_path.name, False, "Already correct")
    
    fixed_code = agent.fix_code(code, test_error)
    fixed_path = fixed_dir / program_path.name
    with open(fixed_path, 'w') as f:
        f.write(fixed_code)
    
    test_output, _ = run_test(fixed_path)
    return (program_path.name, "PASSED" in test_output, fixed_code)