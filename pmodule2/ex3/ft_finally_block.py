def water_plants(plant_list):
    print("Opening watering system")
    try:
        for plant in plant_list:
            if plant == None:
                raise ValueError("Cannot water None- invalid plant!")
            print(f"Watering {plant}")

    except ValueError as e:
            print(f"Error: {e}")
    finally:
        print("Closing watering system (cleanup)")

def test_watering_system():
    print("== Garden Watering System ===")
    print()
    print("Testing normal watering...")
    normal_plants = ["tomato", "lettuce", "carrots"]
    water_plants(normal_plants)
    print("Watering completed successfully!")
    print()
    print("Testing with error...")
    bad_plants = ["tomato", None, "carrots"]
    water_plants(bad_plants)
    print()
    print("Cleanup always happens, even with errors!")

test_watering_system()