"""
Streamlit-Anwendung zur Berechnung von Umsatz‑, Personal- und Gewinnkennzahlen

Voraussetzungen:
  pip install streamlit
Ausführen:
  streamlit run app.py

Hinweis: Diese Anwendung ist komplett auf Deutsch und ermöglicht Eingaben ohne Entwicklerumgebung.
"""

import streamlit as st
from typing import List, Dict

# -----------------------------------------------------------------------------
# Kernlogik
# -----------------------------------------------------------------------------

def calculate_metrics(fte: float, weekly_hours: List[float], daily_rates: List[float]) -> Dict[str, float]:
    """Berechnet alle Kennzahlen und gibt sie in einem Dictionary zurück."""

    total_weekly_hours = sum(weekly_hours)
    total_daily_rates = sum(daily_rates)

    weekly_rate_sum = total_daily_rates * 7
    revenue_per_hour = weekly_rate_sum / total_weekly_hours if total_weekly_hours else 0.0

    required_fte = total_weekly_hours / 0.76 / 40  # 76 % Nettoarbeitszeit, 40 h Woche
    fte_diff = fte - required_fte
    available_weekly_hours = fte * 40

    weekly_revenue = total_weekly_hours * revenue_per_hour
    monthly_revenue_estimate = weekly_revenue * 4.35  # Durchschnittliche Monatswochen

    monthly_client_revenues = [rate * 31 for rate in daily_rates]
    total_monthly_revenue = sum(monthly_client_revenues)

    return {
        "Summe wöchentlicher Betreuungsstunden": total_weekly_hours,
        "Summe Tagessätze pro Tag": total_daily_rates,
        "Wochen‑Tagessatzsumme": weekly_rate_sum,
        "Erlös pro Fachleistungsstunde": revenue_per_hour,
        "Benötigte FTE": required_fte,
        "Differenz FTE (Verfügbar – Benötigt)": fte_diff,
        "Verfügbare Wochenarbeitsstunden": available_weekly_hours,
        "Wochen‑Umsatz": weekly_revenue,
        #"Monats‑Umsatz (Schätzung)": monthly_revenue_estimate,
        "Monatsumsätze je Klient": monthly_client_revenues,
        "Gesamt‑Monatsumsatz": total_monthly_revenue,
    }

# -----------------------------------------------------------------------------
# Streamlit UI
# -----------------------------------------------------------------------------

def main():
    st.set_page_config(page_title="Umsatz- & Personalrechner", page_icon="💶", layout="centered")
    st.title("💶 Umsatz- & Personalrechner")
    st.write("Füllen Sie die Felder aus und klicken Sie auf **Berechnen**, um alle Kennzahlen zu erhalten.")

    with st.form("input_form"):
        fte = st.number_input("Gesamt-Vollzeitäquivalente (FTE)", min_value=0.0, step=0.1, value=0.0)
        num_clients = st.number_input("Anzahl der Klienten", min_value=1, step=1, value=4, format="%d")

        st.markdown("### Angaben pro Klient")
        weekly_hours = []
        daily_rates = []
        for i in range(int(num_clients)):
            cols = st.columns(2)
            hours = cols[0].number_input(
                f"Wöchentliche Betreuungsstunden Klient {i+1}", min_value=0.0, step=0.5, key=f"wh_{i}")
            rate = cols[1].number_input(
                f"Tagessatz (EUR) Klient {i+1}", min_value=0.0, step=1.0, key=f"dr_{i}")
            weekly_hours.append(hours)
            daily_rates.append(rate)

        personnel_costs = st.number_input("Monatliche Personalkosten (EUR)", min_value=0.0, step=100.0, value=0.0)

        submitted = st.form_submit_button("Berechnen 💡")

    if submitted:
        metrics = calculate_metrics(fte, weekly_hours, daily_rates)
        total_monthly_revenue = metrics["Gesamt‑Monatsumsatz"]
        profit = total_monthly_revenue - personnel_costs

        st.success("Berechnung abgeschlossen!")

        st.metric("Gesamt‑Monatsumsatz", f"{total_monthly_revenue:,.2f} €")
        st.metric("Monatsgewinn (Umsatz – Personalkosten)", f"{profit:,.2f} €")

        st.markdown("---")
        st.subheader("Detailübersicht")

        # Einzelne Kennzahlen
        for label, value in metrics.items():
            if label == "Monatsumsätze je Klient":
                st.write(f"**{label}:**")
                for idx, val in enumerate(value, start=1):
                    st.write(f"&nbsp;&nbsp;• Klient {idx}: {val:,.2f} €")
            else:
                suffix = "€" if "Umsatz" in label or "Erlös" in label else ""
                st.write(f"**{label}:** {value:,.2f} {suffix}")

        st.markdown("---")
        st.caption("© 2025 Chris Schweiger – Alle Angaben ohne Gewähr")


if __name__ == "__main__":
    main()
