import matplotlib.pyplot as plt
import io

class ChartGenerator:
    @staticmethod
    def generate_comparison_chart(player1, player2, stats1, stats2):
        categories = ['Goals', 'Assists', 'Passes Completed']
        player1_stats = [stats1['goals'], stats1['assists'], stats1['passes_completed']]
        player2_stats = [stats2['goals'], stats2['assists'], stats2['passes_completed']]

        x = range(len(categories))
        width = 0.35

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar([i - width/2 for i in x], player1_stats, width, label=player1)
        ax.bar([i + width/2 for i in x], player2_stats, width, label=player2)

        ax.set_ylabel('Values')
        ax.set_title(f'Comparison: {player1} vs {player2}')
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()

        plt.tight_layout()

        # Save the chart to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf