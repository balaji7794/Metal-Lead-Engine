from rich.console import Console
from rich.panel import Panel

from config.settings import APP_NAME, VERSION, HEADLESS
from src.utils.browser import launch_browser

console = Console()

console.print(
    Panel.fit(
        f"[bold green]{APP_NAME}[/bold green]\n"
        f"Version {VERSION}",
        title="Starting",
    )
)

playwright, browser, page = launch_browser(headless=HEADLESS)

page.goto("https://www.google.com/maps")

page.wait_for_timeout(5000)

console.print("[green]Browser opened.[/green]")
console.print("[yellow]Playwright Inspector is opening...[/yellow]")

page.pause()

browser.close()
playwright.stop()