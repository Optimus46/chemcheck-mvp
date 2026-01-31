def generate_report(results):
    report = ""
    harmful = []

    for r in results:
        report += f"- {r['ingredient']} : {r['risk']} risk\n"
        if r['risk'] == "High":
            harmful.append(r['ingredient'])

    if harmful:
        report += "\n⚠️ Harmful Ingredients Detected:\n"
        report += ", ".join(harmful)
    else:
        report += "\n✅ Product appears safe."

    return report
