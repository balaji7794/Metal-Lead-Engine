from src.database.migration import Migration
from src.engines.google_maps_scraper import GoogleMapsScraper
from src.services.lead_service import LeadService
from src.services.website_intelligence_service import WebsiteIntelligenceService


def main():

    print("=" * 70)
    print("METAL LEAD ENGINE V1")
    print("=" * 70)

    # -------------------------------------------------
    # Database
    # -------------------------------------------------

    migration = Migration()
    migration.run()
    migration.close()

    # -------------------------------------------------
    # Search Input
    # -------------------------------------------------

    keyword = input("Keyword : ").strip()

    area = input("Area : ").strip()

    city = input("City : ").strip()

    state = input("State : ").strip()

    radius = input("Radius (KM) : ").strip()

    if not radius:
        radius = "10"

    search_query = keyword

    if area:
        search_query += f" {area}"

    if city:
        search_query += f" {city}"

    if state:
        search_query += f" {state}"

    print()
    print("Searching...")
    print(search_query)
    print()

    # -------------------------------------------------
    # Google Maps Search
    # -------------------------------------------------

    scraper = GoogleMapsScraper()

    scraper.start()

    scraper.search(search_query)

    leads = scraper.scrape_all()

    scraper.stop()

    print()
    print(f"Companies Found : {len(leads)}")
    print()

    # -------------------------------------------------
    # Save Companies
    # -------------------------------------------------

    lead_service = LeadService()

    company_ids = lead_service.save(leads)

    lead_service.close()

    # -------------------------------------------------
    # Website Intelligence
    # -------------------------------------------------

    website_service = WebsiteIntelligenceService()

    website_service.run(company_ids)

    website_service.close()

    # -------------------------------------------------
    # Finished
    # -------------------------------------------------

    print()
    print("=" * 70)
    print("SEARCH COMPLETED")
    print("=" * 70)
    print()

    input("Press ENTER to close...")


if __name__ == "__main__":
    main()

    