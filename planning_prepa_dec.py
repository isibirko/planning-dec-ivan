import streamlit as st
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt

st.title("🎯 Suivi Préparation DEC 2025 – Ivan")

# Liste des activités
activities = [
    "Mémoire DEC",
    "Power BI",
    "Anglais Coursera",
    "Révision Déontologie EC/CAC",
    "Révision légale (annales)",
    "Sport",
]

# Objectifs hebdomadaires en heures
weekly_goals = {
    "Mémoire DEC": 12,
    "Power BI": 15,
    "Anglais Coursera": 8,
    "Révision Déontologie EC/CAC": 7,
    "Révision légale (annales)": 12,
    "Sport": 2,
}

st.sidebar.header("Saisie des heures réalisées")
st.sidebar.write("Entrez les heures travaillées par activité cette semaine")

data = {}
for activity in activities:
    data[activity] = st.sidebar.number_input(f"{activity} (heures)", min_value=0.0, max_value=40.0, step=0.5, key=activity)

if st.sidebar.button("Valider la semaine"):
    today = date.today()
    new_entry = {"Date": today}
    for activity in activities:
        new_entry[activity] = data[activity]

    try:
        df = pd.read_csv("planning_suivi.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Date"] + activities)

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv("planning_suivi.csv", index=False)
    st.success("Heures enregistrées avec succès ✅")

# Affichage des données
st.header("📅 Historique hebdomadaire")
try:
    df = pd.read_csv("planning_suivi.csv")
    st.dataframe(df.tail(4))

    st.header("📊 Suivi des objectifs")
    latest = df.iloc[-1]
    goal_data = {
        "Activité": [],
        "Heures réalisées": [],
        "Objectif": [],
        "% accompli": []
    }

    for activity in activities:
        goal_data["Activité"].append(activity)
        goal_data["Heures réalisées"].append(latest[activity])
        goal_data["Objectif"].append(weekly_goals[activity])
        goal_data["% accompli"].append(round(100 * latest[activity] / weekly_goals[activity], 1))

    goal_df = pd.DataFrame(goal_data)
    st.dataframe(goal_df)

    # 📈 Ajout du graphique de comparaison
    st.subheader("📈 Graphique : Heures réalisées vs Objectifs")
    fig, ax = plt.subplots()
    bar_width = 0.35
    index = range(len(activities))

    ax.bar(index, goal_df["Objectif"], bar_width, label="Objectif", color='lightgray')
    ax.bar([i + bar_width for i in index], goal_df["Heures réalisées"], bar_width, label="Réalisé", color='skyblue')

    ax.set_xlabel('Activité')
    ax.set_ylabel('Heures')
    ax.set_title('Comparaison hebdomadaire')
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(activities, rotation=45, ha="right")
    ax.legend()
    st.pyplot(fig)

except FileNotFoundError:
    st.info("Aucune donnée saisie pour l’instant. Utilise le menu de gauche pour commencer.")
