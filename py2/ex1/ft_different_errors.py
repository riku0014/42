def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("abc")

    elif operation_number == 1:
        result = 10 / 0
        print(result)

    elif operation_number == 2:
        open("missing_garden_file.txt")

    elif operation_number == 3:
        result = "temperature: " + 25
        print(result)

    else:
        return


def test_error_types() -> None:
    print("=== Garden Error Types ===")

    print("Testing operation 0")
    try:
        garden_operations(0)
    except ValueError as error:
        print(f"Caught ValueError: bad number data - {error}")
    print("Program continues after ValueError")

    print("Testing operation 1")
    try:
        garden_operations(1)
    except ZeroDivisionError as error:
        print(f"Caught ZeroDivisionError: cannot divide by zero - {error}")
    print("Program continues after ZeroDivisionError")

    print("Testing operation 2")
    try:
        garden_operations(2)
    except FileNotFoundError as error:
        print(f"Caught FileNotFoundError: file does not exist - {error}")
    print("Program continues after FileNotFoundError")

    print("Testing operation 3")
    try:
        garden_operations(3)
    except TypeError as error:
        print(f"Caught TypeError: cannot mix these data types - {error}")
    print("Program continues after TypeError")

    print("Testing multiple error types with one try block")
    try:
        garden_operations(0)
    except (
        ValueError, ZeroDivisionError, FileNotFoundError, TypeError
    ) as error:
        print(f"Caught one of several possible errors: {error}")

    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    test_error_types()
