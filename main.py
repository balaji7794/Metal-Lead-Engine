from src.database.migration import Migration
from src.engines.google_maps_scraper import GoogleMapsScraper
from src.exporters.excel_exporter import ExcelExporter
from src.services.lead_service import LeadService
from src.services.website_intelligence_service import WebsiteIntelligenceService
from src.services.product_intelligence_service import ProductIntelligenceService


def main():

    # -------------------------------
    # Run Database Migrations
    # -------------------------------

    migration = Migration()
    migration.run()
    migration.close()

    # -------------------------------
    # Google Maps Scraper
    # -------------------------------

    scraper = GoogleMapsScraper()

    scraper.start()

    scraper.search(
        "Aluminium Extrusion Manufacturers Bangalore"
    )

    leads = scraper.scrape_all()

    # -------------------------------
    # Save Companies
    # -------------------------------

    lead_service = LeadService()

    lead_service.save(leads)

    lead_service.close()

    # -------------------------------
    # Website Intelligence
    # -------------------------------

    website_service = WebsiteIntelligenceService()

    website_service.run()

    website_service.close()

    # -------------------------------
    # Product Intelligence
    # -------------------------------

    product_service = ProductIntelligenceService()

    product_service.run()

    product_service.close()

    # -------------------------------
    # Export Excel
    # -------------------------------

    exporter = ExcelExporter()

    exporter.export(leads)

    # -------------------------------
    # Close Browser
    # -------------------------------

    scraper.stop()

    input("\nDone. Press ENTER to close...")


if __name__ == "__main__":
    main()