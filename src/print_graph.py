from pathlib import Path

from dotenv import load_dotenv
from main_graph import main_graph

load_dotenv()

OUTPUT_DIR = Path("/app/output")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    try:
        png_data = main_graph.get_graph(xray=True).draw_mermaid_png()
        png_file = OUTPUT_DIR / "graph_main.png"
        png_file.write_bytes(png_data)
        print(f"✅ Saved to {png_file} ({len(png_data)} bytes)")
    except Exception as e:
        print(f"❌ Failed: {e}")


if __name__ == "__main__":
    main()
