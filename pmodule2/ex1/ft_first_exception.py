def test_error_types():
    try:
        garden_operations("value")
    except ValueError:
        print("Caught ValueError: invalid literal for int()\n")
    try:
        garden_operations("zero")
    except ZeroDivisionError:
        print("Caught ZeroDivisionError: division by zero\n")
    try:
        garden_operations("file")
    except FileNotFoundError:
            print("Caught FileNotFoundError: No such file 'missing.txt'\n")
#make a dictionary and look up a nonexist word
    try:
        garden_operations("key")
    except KeyError:
        print("Caught KeyError: 'missing_plant'\n")
    try:
        garden_operations("all")
    except (ValueError, ZeroDivisionError, FileNotFoundError, KeyError):
        print("Caught an error, but program continues!")

def garden_operations(error_type):
    if error_type == "value":
        int("abc")
    elif error_type == "zero":
        10/0
    elif error_type == "file":
        open("missing_file")
    elif error_type == "key":
        {"rose": 1} ["missing_plant"]
    elif error_type == "all":
        int("abc")
        10/0
        open("missing_file")
        {"rose": 1} ["missing_plant"]
def main():
    print("=== Garden Error Types Demo ===\n")
    test_error_types()
    print("All error types tested successfully!")

if __name__ == "__main__":
    main()