# The Role of Education and Emotion in Spreading Misinformation across Social Networks

This repository contains the research report and simulations for an **Agent-Based Modeling (ABM) approach** to studying how misinformation spreads in social networks. The research examines the influence of **education, emotion, and trust** on an individual's susceptibility to misinformation and their ability to fact-check information.

## 📌 Overview
Misinformation is a major issue in today's digital world, with social media platforms amplifying its spread. This study models misinformation dynamics by simulating **agents with varying educational levels and emotional triggers** to analyze how these factors affect belief in misinformation.

The project uses an **SBFC (Susceptible-Believer-Fact Checker) model**, implemented in **Python (NetworkX)**, to simulate agent interactions and measure the impact of interventions such as **community fact-checking**.

## 📊 Key Features
- **Agent-Based Modeling (ABM):** Simulates social networks with different socio-emotional classes.
- **Trust as a Dual Parameter:** Examines trust as both a **logical** and **emotional** factor.
- **Experimental Analysis:** Tests the effects of education, emotion, and misinformation credibility on belief propagation.
- **Intervention Strategies:** Investigates the impact of fact-checking techniques to reduce misinformation spread.

## 📁 What's Inside?
- 📜 Full Report – Detailed analysis of misinformation dynamics.
- 🖥️ Simulation Code – Run experiments with different parameters.
- 📊 Figures & Data – Graphs visualizing the spread of misinformation.

## 🛠️ Setup & Installation
To run the simulation locally, ensure you have Python installed and install the required dependencies:

1. Install dependencies:
```bash
pip install networkx matplotlib numpy pandas
```

2. Run Simulation
```bash
python main.py
```

## 📈 Results & Findings

- **Education reduces susceptibility to misinformation.**  
- **Higher emotional states (e.g., anger) increase belief in misinformation.**  
- **Community fact-checking interventions significantly slow down misinformation spread.**  
- **A minimum threshold of fact-checkers is required to prevent misinformation from dominating.**  

## 📄 Research Paper

For a detailed analysis, refer to the full report: [LaTeX Report.pdf](LaTeX%20Report.pdf).  

## 🎯 Future Work

- Expanding the emotional parameter set beyond anger (e.g., frustration, stubbornness).  
- Incorporating hybrid AI-human fact-checking models.  
- Studying the impact of AI-generated misinformation on social networks.  
