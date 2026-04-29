import os


def create_archive(filename: str) -> None:
    print("=== CYBER ARCHIVES- PRESERVATION SYSTEM ===")
    print()

    if not os.path.exists(filename):
        print("ERROR: Storage vault not found")
        return

    print(f"Initializing new storage unit: {filename}")

    text_to_add: list[str] = [
        "New quantum algorithm discovered",
        "Efficiency increased by 347%",
        "Archived by Data Archivist trainee"
    ]

    try:
        with open(filename, 'w', encoding='utf-8') as Vault:
            print(f"Storage unit created successfully...")
            print()

            print("Inscribing preservation data...")
            for i, content in enumerate(text_to_add, start = 1):
                content_to_write = f"[ENTRY {i:03}] {content}\n"
                Vault.write(content_to_write)
                print(f"[ENTRY {i:03}] {content}")

    except Exception as e:
        print(f"Error has occured: Type:{type(e).__name__} Args:{e.args}")
        return
    
    print()
    print("Data inscription complete. Storage unit sealed.")
    print(f"Archive '{filename}' ready for long-term preservation.")


if __name__ == "__main__":
    create_archive("new_discovery.txt")