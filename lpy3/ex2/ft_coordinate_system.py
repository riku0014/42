import sys kokokara
import math


def cal_distance(
        l1: tuple[int, int, int], l2: tuple[int, int, int]
        ) -> float:
    return math.sqrt(
        (l2[0] - l1[0])**2 + (l2[1] - l1[1])**2 + (l2[2] - l1[2])**2
            )


def parse_string(string: str) -> tuple[int, int, int]:
    str_list: list[str, str, str] = string.split(",")
    return tuple(int(s) for s in str_list)
# my_tuple(my_list)ってやればlistをtupleにできる


def main() -> None:
    print("== Game Coordinate System ===")
    print()

    l1: tuple[int, int, int] = (0, 0, 0)
    l2: tuple[int, int, int] = (10, 20, 5)
    print(f"Position created: {l2}")
    ans: float = cal_distance(l1, l2)
    print(f"Distance between {l1} and {l2}: {ans:.2f}")
    print()

    if len(sys.argv) == 2:
        string_location: str = sys.argv[1]
    else:
        string_location: str = "3,4,0"
    try:
        l3: tuple[int, int, int] = parse_string(string_location)
        print(f"Parsing coordinates: \"{string_location}\"")
        print(f"Parsed position: {l3}")
        ans: float = cal_distance(l1, l3)
        print(f"Distance between {l1} and {l3}: {ans:.2f}")
        print()
    except ValueError as e:
        print(f"Parsing invalid coordinates: \"{string_location}\"")
        print(f"Error parsing coordinates: {e}")
        print(f"Error Details - Type: {type(e).__name__}, Args: {e.args}")

    invalid_location: str = "abc,def,ghi"
    print(f"Parsing invalid coordinates: \"{invalid_location}\"")
    try:
        parse_string(invalid_location)
    except ValueError as e:
        print(f"Error parsing coordinates: {e}")
        print(f"Error Details - Type: {type(e).__name__}, Args: {e.args}")
    print()

    print("Unpacking demonstration:")
    try:
        x, y, z = l3
        print(f"Player at x={x}, y={y}, z={z}")
        print(f"Cordinates: x={x}, y={y}, z={z}")
    except Exception as e:
        print(f"Error unpacking demonstration: {e}")
        print(f"Error Details - Type: {type(e).__name__}, Args: {e.args}")


if __name__ == "__main__":
    main()

# 引数
#
# "1,2,abc"
# "1, 2"
