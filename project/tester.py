import copy
import json
import sys
import subprocess
import types

def py_try(algo, *args, correct=False, fixed=False):
    """Test a Python program with given arguments."""
    if not fixed:
        module = __import__("python_programs." + algo)
    else:
        if not correct:
            module = __import__("fixed_programs." + algo)
        else:
            module = __import__("correct_python_programs." + algo)

    fx = getattr(module, algo)
    try:
        return getattr(fx, algo)(*args)
    except Exception:
        return sys.exc_info()

def prettyprint(o):
    """Format output for printing."""
    if isinstance(o, types.GeneratorType):
        return "(generator) " + str(list(o))
    return str(o)

# Algorithms that require special graph-based testing
graph_based = [
    "breadth_first_search",
    "depth_first_search",
    "detect_cycle",
    "minimum_spanning_tree",
    "reverse_linked_list",
    "shortest_path_length",
    "shortest_path_lengths",
    "shortest_paths",
    "topological_ordering"
]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tester.py <program_name>")
        sys.exit(1)

    algo = sys.argv[1].replace(".py", "").replace("python_programs/", "")

    if algo in graph_based:
        print("\nTesting Graph-Based Algorithm:", algo)
        print("-" * 50)
        
        # Test correct version
        print("[CORRECT VERSION]")
        correct_module = __import__("correct_python_programs." + algo + "_test")
        correct_fx = getattr(correct_module, algo + "_test")
        getattr(correct_fx, "main")()
        
        # Test buggy version
        print("\n[BUGGY VERSION]")
        test_module = __import__("python_programs." + algo + "_test")
        test_fx = getattr(test_module, algo + "_test")
        try:
            getattr(test_fx, "main")()
        except Exception as e:
            print("ERROR:", e)
    else:
        print("\nTesting:", algo)
        print("-" * 50)
        
        try:
            with open("json_testcases/" + algo + ".json", 'r') as f:
                for line in f:
                    testcase = json.loads(line)
                    test_in, test_out = testcase
                    
                    if not isinstance(test_in, list):
                        test_in = [test_in]
                    
                    # Test correct version
                    correct_result = py_try(algo, *copy.deepcopy(test_in), correct=True)
                    print(f"Correct: {prettyprint(correct_result)} (Expected: {test_out})")
                    
                    # Test buggy version
                    buggy_result = py_try(algo, *copy.deepcopy(test_in))
                    print(f"Buggy: {prettyprint(buggy_result)}")
                    
                    # Test fixed version (if exists)
                    try:
                        fixed_result = py_try(algo, *copy.deepcopy(test_in), fixed=True)
                        print(f"Fixed: {prettyprint(fixed_result)}")
                    except ImportError:
                        pass
                    
                    print("-" * 30)
        except FileNotFoundError:
            print(f"No test cases found for {algo} in json_testcases/")