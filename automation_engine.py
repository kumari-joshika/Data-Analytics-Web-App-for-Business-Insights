def generate_insights(df, target_column):
    insights = []

    avg_value = df[target_column].mean()
    latest_value = df[target_column].iloc[-1]

    if latest_value < avg_value:
        insights.append(
            f"⚠️ Latest value ({latest_value:.2f}) is below historical average ({avg_value:.2f})."
        )
    else:
        insights.append(
            f"✅ Latest value ({latest_value:.2f}) is performing above average."
        )

    return insights


def generate_recommendation(df, target_column):
    trend = df[target_column].pct_change().mean()

    if trend < 0:
        return "📉 Recommendation: Investigate declining trend and optimize strategy."
    else:
        return "📈 Recommendation: Continue current strategy and scale operations."
