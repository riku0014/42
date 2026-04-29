def main() -> None:
    print("=== Achievement Tracker System ===")
    print()
    alice = set(['first_kill', 'level_10', 'treasure_hunter', 'speed_demon'])
    bob = set(['first_kill', 'level_10', 'boss_slayer', 'collector'])
    charlie = set(
        ['level_10', 'treasure_hunter', 'boss_slayer',
         'speed_demon', 'perfectionist']
        )

    print(f"Player alice achievements: {alice}")
    print(f"Player bob achievements: {bob}")
    print(f"Player charlie achievements: {charlie}")
    print()

    print("=== Achievement Analytics ===")
    unique_ach = alice.union(bob).union(charlie)
    print(f"All unique achievements: {unique_ach}")
    print(f"Total unique achievements: {len(unique_ach)}")
    print()

    common_ach = alice.intersection(bob).intersection(charlie)
    print(f"Common to all players: {common_ach}")

    alice_only = alice.difference(bob).difference(charlie)
    bob_only = bob.difference(alice).difference(charlie)
    charlie_only = charlie.difference(alice).difference(bob)
    rare_ach = alice_only.union(bob_only).union(charlie_only)
    print(f"Rare achievements (1 player): {rare_ach}")
    print()

    alice_bob = alice.intersection(bob)
    alice_unique = alice.difference(bob)
    bob_unique = bob.difference(alice)
    print(f"Alice vs Bob common: {alice_bob}")
    print(f"Alice unique: {alice_unique}")
    print(f"Bob unique: {bob_unique}")


if __name__ == "__main__":
    main()
