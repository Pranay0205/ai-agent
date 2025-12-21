from functions.get_file_content import get_file_content


def test():

    result = get_file_content("calculator", "lorem.txt")
    print("Result for 'lorem.txt':")
    print(result)

    result = get_file_content("calculator", "main.py")
    print("\nResult for 'main.py':")
    print(result)

    result = get_file_content("calculator", "pkg/calculator.py")
    print("\nResult for 'pkg/calculator.py':")
    print(result)

    # this should return an error string
    result = get_file_content("calculator", "/bin/cat")
    print("\nResult for '/bin/cat':")
    print(result)

    # this should return an error string
    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print("\nResult for 'pkg/does_not_exist.py':")
    print(result)


if __name__ == "__main__":
    test()
