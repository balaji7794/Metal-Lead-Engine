from threading import Thread

from src.engines.google_maps_scraper import GoogleMapsScraper
from src.services.lead_service import LeadService
from src.services.website_intelligence_service import WebsiteIntelligenceService


class SearchManager:

    def __init__(self):

        self.running = False
        self.thread = None

        self.progress = {

            "stage": "Idle",
            "current": 0,
            "total": 0,
            "message": ""

        }

    def start(self, keyword):

        if self.running:

            return False

        self.thread = Thread(

            target=self.run,

            args=(keyword,),
            daemon=True

        )

        self.thread.start()

        return True

    def run(self, keyword):

        self.running = True

        self.progress = {

            "stage": "Google Maps",
            "current": 0,
            "total": 0,
            "message": "Opening Google Maps..."

        }

        try:

            # ------------------------------------
            # Google Maps
            # ------------------------------------

            scraper = GoogleMapsScraper()

            scraper.start()

            scraper.search(keyword)

            self.progress["message"] = "Collecting companies..."

            leads = scraper.scrape_all()

            scraper.stop()

            self.progress["stage"] = "Saving Companies"

            self.progress["current"] = len(leads)

            self.progress["total"] = len(leads)

            self.progress["message"] = f"{len(leads)} companies found"

            # ------------------------------------
            # Save
            # ------------------------------------

            lead_service = LeadService()

            company_ids = lead_service.save(

                leads

            )

            lead_service.close()

            if company_ids is None:

                company_ids = []

            # ------------------------------------
            # Website Intelligence
            # ------------------------------------

            self.progress["stage"] = "Website Intelligence"

            website = WebsiteIntelligenceService()

            website.run(

                company_ids,

                self.progress

            )

            website.close()

            self.progress = {

                "stage": "Completed",

                "current": len(leads),

                "total": len(leads),

                "message": "Search Completed"

            }

        except Exception as e:

            self.progress = {

                "stage": "Error",

                "current": 0,

                "total": 0,

                "message": str(e)

            }

        self.running = False

    def status(self):

        return {

            "running": self.running,

            "stage": self.progress.get("stage"),

            "current": self.progress.get("current"),

            "total": self.progress.get("total"),

            "message": self.progress.get("message")

        }


search_manager = SearchManager()