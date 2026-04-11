class GardenError(Exception):
    pass

class PlantError(GardenError):
    pass

class WaterError(GardenError):
    pass

def raise_error(value):
    if value == "plant":
        try:
            raise PlantError("The tomato plant is wilting!")
        except PlantError as e:
            print(f"Caught PlantError: {e}")

    elif value == "water":
        try:
            raise WaterError("Not enough water in the tank!")
        except WaterError as e:
            print(f"Caught WaterError: {e}")

    elif value == "garden":
        try:
            raise PlantError("The tomato plant is wilting!")
        except GardenError as e:
            print(f"Caught a garden error: {e}")
            
        try:
            raise WaterError("Not enough water in the tank!")
        except GardenError as e:
            print(f"Caught a garden error: {e}")

def main():
    print("=== Custom Garden Errors Demo ===")
    print("\nTesting PlantError...")
    raise_error("plant")
    
    print("\nTesting WaterError...")
    raise_error("water")
    
    print("\nTesting catching all garden errors...")
    raise_error("garden")
    
    print("\nAll custom error types work correctly!")

if __name__ == "__main__":
    main()