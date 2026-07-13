import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT))

from src.services.product_intelligence_service import ProductIntelligenceService


def main():

    print()
    print("=" * 60)
    print("TEST - PRODUCT INTELLIGENCE")
    print("=" * 60)

    service = ProductIntelligenceService()

    service.run()

    service.close()

    print()
    print("=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)

    input("\nPress ENTER to close...")


if __name__ == "__main__":

    main()