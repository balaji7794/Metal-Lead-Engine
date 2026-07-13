from src.database.migration import Migration
from src.engines.google_maps_scraper import GoogleMapsScraper
from src.exporters.excel_exporter import ExcelExporter
from src.services.lead_service import LeadService


def main():

    migration = Migration()
    migration.run()
    migration.close()

    scraper = GoogleMapsScraper()

    scraper.start()

    scraper.search(
        "Aluminium Extrusion Manufacturers Bangalore"
    )

    leads = scraper.scrape_all()

    service = LeadService()

    service.save(leads)

    exporter = ExcelExporter()

    exporter.export(leads)

    service.close()

    scraper.stop()

    input("\nDone. Press ENTER to close...")


if __name__ == "__main__":
    main()