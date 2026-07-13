from src.engines.google_maps_engine import GoogleMapsEngine


def main():
    engine = GoogleMapsEngine()

    leads = engine.search(
        "Aluminium Extrusion Manufacturers Bangalore"
    )

    print("\nResults\n")

    for lead in leads:
        print("--------------------------")
        print(f"Name      : {lead.name}")
        print(f"Category  : {lead.category}")
        print(f"City      : {lead.city}")
        print(f"Source    : {lead.source}")


if __name__ == "__main__":
    main()