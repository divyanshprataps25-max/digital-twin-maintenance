import streamlit as st
import pandas as pd
import pickle
import random
import time
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "model.pkl")
model = pickle.load(open(model_path, "rb"))

st.title("🔧 Digital Twin: Machine Health Monitoring")

st.write("### Enter Initial Machine Parameters")

# Inputs
air_temp = st.number_input("Air Temperature (K)", value=300.0)
process_temp = st.number_input("Process Temperature (K)", value=310.0)
rpm = st.number_input("Rotational Speed (rpm)", value=1500.0)
torque = st.number_input("Torque (Nm)", value=40.0)
wear = st.number_input("Initial Tool Wear (min)", value=10.0)

# Simulation button
if st.button("Start Simulation"):

    st.write(" Running Digital Twin Simulation...")

    history = []
    chart = st.empty()

    for t in range(20):

        # Simulate variation
        air_temp_sim = air_temp + random.uniform(-2, 2)
        process_temp_sim = process_temp + random.uniform(-2, 2)
        rpm_sim = rpm + random.uniform(-200, 200)
        torque_sim = torque + random.uniform(-10, 10)

        # Wear increases with time
        wear = wear + (torque_sim / 50)

        # Create input
        data = pd.DataFrame([{
            'Air temperature [K]': air_temp_sim,
            'Process temperature [K]': process_temp_sim,
            'Rotational speed [rpm]': rpm_sim,
            'Torque [Nm]': torque_sim,
            'Tool wear [min]': wear
        }])

        # Predict
        prob = model.predict_proba(data)[0][1]
        history.append(prob)

        # Show status
        st.write(f"Time {t+1} → Probability: {prob:.2f}")

        if prob > 0.7:
            st.error(" HIGH RISK")
        elif prob > 0.4:
            st.warning(" MEDIUM RISK")
        else:
            st.success(" LOW RISK")

        # Graph
        fig, ax = plt.subplots()
        ax.plot(history)
        ax.set_title("Failure Risk Over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Probability")

        chart.pyplot(fig)

        time.sleep(0.5)
