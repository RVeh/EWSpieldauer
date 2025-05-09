# 🎲 Erwartungswerte bei Setzstrategien – interaktive Analyse mit Python

Dieses Projekt untersucht ein Wahrscheinlichkeits-Spiel mit Chips auf m Feldern.  
Ziel ist es, die **erwartete Anzahl an Würfen** bis zur vollständigen Abräumung zu berechnen – entweder allein oder im Duell mit einer anderen Strategie.

Die zugrunde liegenden Modelle werden **rekursiv berechnet** und exakt mit Brüchen dargestellt.  
Visualisierungen, CSV-Exporte und Bewertungen (Sieg, Niederlage, Unentschieden) runden die Analyse ab.

---

## 🚀 Starte direkt im Browser mit Binder

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/RVeh/EX_Setzstrategien/main?filepath=00_Start.ipynb)

---

## 📚 Inhalte

### 🔹 1. Einzelspieler

- 📌 [`01_Einspieler_Einzelwert.ipynb`](01_Einspieler_Einzelwert.ipynb)  
  Berechne $E(V)$ für eine konkrete Chipverteilung

- 📌 [`01_Einspieler_Alle_Verteilungen.ipynb`](01_Einspieler_AlleVerteilungen.ipynb)  
  Berechne alle $E(V)$ für $\sum v_j = n$ – sortiert, grafisch, als CSV

---

### 🔹 2. Zwei Spieler

- 📌 [`02_Zweispieler_EVW_Einzel.ipynb`](02_Zweispieler_EVW_Einzel.ipynb)  
  Berechne $E(V, W)$ für zwei konkrete Strategien

- 📌 [`02_Zweispieler_V_gegen_alle.ipynb`](02_Zweispieler_V_gegen_alle.ipynb)  
  Fixe Strategie $V$ gegen alle möglichen Gegnerstrategien $W$ – mit Bewertung

---

## 🛠 Voraussetzungen

Nur `pandas` und `matplotlib` werden benötigt.  
Diese werden automatisch von Binder installiert.

```txt
matplotlib
pandas


## 🧪 Hinweise zur Nutzung

- Notebooks lassen sich direkt in Jupyter oder auf Binder öffnen.
- Bei Binder oder JupyterLab bitte in der Menüzeile **"Run All Cells"** auswählen, um alle Ausgaben zu erzeugen.
- Das Projekt verwendet die Python-Standardbibliothek und `matplotlib` für Visualisierungen.


## 🧮 Voraussetzungen

- Python ≥ 3.7
- matplotlib
- pandas


## ✍️ Mitwirkende

- [Reimund Vehling]
- Mit KI-Unterstützung von ChatGPT

---

**Lernen, Spielen und Forschen – alles in einem interaktiven Notebook.**
