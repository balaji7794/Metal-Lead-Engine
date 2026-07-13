from src.crawlers.website_crawler import WebsiteCrawler

crawler = WebsiteCrawler()

html = crawler.download("https://lightmetals.in")

if html:

    emails = crawler.extract_emails(html)

    print("\n========================")
    print("EMAILS FOUND")
    print("========================\n")

    if len(emails) == 0:

        print("No emails found.")

    else:

        for email in emails:

            print(email)