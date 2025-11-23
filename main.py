"""Application entry point for the weather ETL dashboard."""

from dotenv import load_dotenv

from dashboard.app import app


def main() -> None:
    """Load environment variables and start the Dash development server."""
    load_dotenv()
    print("Dashboard server started. Visit http://127.0.0.1:8050/")
    app.run(debug=True)


if __name__ == "__main__":
    main()