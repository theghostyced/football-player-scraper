class StatsAnalyzer:
    @staticmethod
    def compare_players(player1, player2, stats1, stats2):
        if stats1 is None or stats2 is None:
            return f"Sorry, I couldn't find stats for one or both players."

        comparison = f"Comparison between {player1} and {player2}:\n"
        comparison += f"Goals: {player1} - {stats1['goals']}, {player2} - {stats2['goals']}\n"
        comparison += f"Assists: {player1} - {stats1['assists']}, {player2} - {stats2['assists']}\n"
        comparison += f"Pass Completion: {player1} - {stats1['passes_completed']}/{stats1['passes_attempted']}, {player2} - {stats2['passes_completed']}/{stats2['passes_attempted']}\n"

        return comparison