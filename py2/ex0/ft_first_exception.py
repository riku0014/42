def input_temperature(temp_str: str) -> int:
    temperature = int(temp_str)
    return temperature


def test_temperature() -> None:
    print("=== Garden Temperature ===")

    try:
        temp_data = "25"
        print(f"Input data is '{temp_data}'")
        temperature = input_temperature(temp_data)
        print(f"Temperature is now {temperature}°C")

        temp_data = "abc"
        print(f"Input data is '{temp_data}'")
        temperature = input_temperature(temp_data)
        print(f"Temperature is now {temperature}°C")

    except Exception as error:
        print(f"Caught input_temperature error: {error}")

    print("All tests completed- program didn't crash!")


if __name__ == "__main__":
    test_temperature()
