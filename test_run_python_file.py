from functions.run_python_file import run_python_file


def test():
    # Test 1: Run calculator without arguments - should print usage instructions
    print("Test 1: Running calculator without arguments")
    result = run_python_file("calculator", "main.py")
    print(result)
    print("-" * 50)

    # Test 2: Run calculator with arguments
    print("\nTest 2: Running calculator with '3 + 5'")
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result)
    print("-" * 50)

    # Test 3: Run calculator tests
    print("\nTest 3: Running calculator tests")
    result = run_python_file("calculator", "tests.py")
    print(result)
    print("-" * 50)

    # Test 4: Try to execute file outside working directory - should return error
    print("\nTest 4: Attempting to execute '../main.py' (outside scope)")
    result = run_python_file("calculator", "../main.py")
    print(result)
    print("-" * 50)

    # Test 5: Try to execute nonexistent file - should return error
    print("\nTest 5: Attempting to execute nonexistent.py")
    result = run_python_file("calculator", "nonexistent.py")
    print(result)
    print("-" * 50)

    # Test 6: Try to execute non-Python file - should return error
    print("\nTest 6: Attempting to execute lorem.txt (not a Python file)")
    result = run_python_file("calculator", "lorem.txt")
    print(result)
    print("-" * 50)


if __name__ == "__main__":
    test()
