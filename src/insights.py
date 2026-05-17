def weather_score(temp, humidity, rain, wind):
    score = 100

    # rain penalty
    score -= rain * 0.4

    # humidity penalty
    score -= humidity * 0.2

    # wind penalty
    score -= wind * 0.5

    # extreme temperature penalty
    if temp > 40:
        score -= 25
    elif temp < 15:
        score -= 20

    return max(0, min(100, score))


def activity_recommendation(score, rain, wind):
    if rain > 70:
        return "🌧 Stay indoors recommended"
    elif wind > 25:
        return "💨 Avoid outdoor activities"
    elif score > 75:
        return "🏕 Perfect for camping / travel / sports"
    elif score > 50:
        return "🚶 Good for light outdoor activity"
    else:
        return "⚠ Not ideal for outdoor plans"