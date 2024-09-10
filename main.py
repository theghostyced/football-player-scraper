from src.data_fetcher import DataFetcher
from src.stats_analyzer import StatsAnalyzer
from src.chart_generator import ChartGenerator
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    data_fetcher = DataFetcher()

    while True:
        logging.info("Starting new comparison")
        print("\nEnter two player names or nicknames to compare (or 'quit' to exit):")
        player1 = input("Player 1: ").strip()
        if player1.lower() == 'quit':
            logging.info("User chose to quit")
            break

        player2 = input("Player 2: ").strip()
        if player2.lower() == 'quit':
            logging.info("User chose to quit")
            break

        logging.info(f"Fetching stats for {player1}")
        stats1 = data_fetcher.get_player_stats(player1)
        logging.info(f"Stats for {player1}: {stats1}")

        logging.info(f"Fetching stats for {player2}")
        stats2 = data_fetcher.get_player_stats(player2)
        logging.info(f"Stats for {player2}: {stats2}")

        if stats1 and stats2:
            logging.info("Generating comparison")
            comparison = StatsAnalyzer.compare_players(stats1['name'], stats2['name'], stats1, stats2)
            print("\n" + comparison)

            logging.info("Generating comparison chart")
            chart_buffer = ChartGenerator.generate_comparison_chart(stats1['name'], stats2['name'], stats1, stats2)

            # Save the chart as a PNG file
            with open("comparison_chart.png", "wb") as f:
                f.write(chart_buffer.getvalue())
            logging.info("Comparison chart saved as 'comparison_chart.png'")
            print("Comparison chart saved as 'comparison_chart.png'")
        else:
            logging.warning("Unable to generate comparison due to missing data")
            print("Unable to generate comparison due to missing data for one or both players.")

        print("\n---")

if __name__ == "__main__":
    main()
