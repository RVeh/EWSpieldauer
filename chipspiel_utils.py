# chipspiel_utils.py

from fractions import Fraction
from functools import lru_cache
import itertools
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# -------------------------------
# 1. Erwartungswert Einzelspieler
# -------------------------------
@lru_cache(maxsize=None)
def expected_one(V, p):
    if all(v == 0 for v in V):
        return Fraction(0)
    total, s = Fraction(0), Fraction(0)
    for j, vj in enumerate(V):
        if vj > 0:
            Vj = list(V)
            Vj[j] -= 1
            total += p[j] * expected_one(tuple(Vj), p)
            s += p[j]
    return (1 + total) / s

# -------------------------------
# 2. Erwartungswert Zweispieler
# -------------------------------
@lru_cache(maxsize=None)
def expected_two(V, W, p):
    if V == W or all(v == 0 for v in V) or all(w == 0 for w in W):
        return Fraction(0)
    total, s = Fraction(0), Fraction(0)
    for j in range(len(p)):
        if V[j] > 0 or W[j] > 0:
            new_V = list(V)
            new_W = list(W)
            if V[j] > 0: new_V[j] -= 1
            if W[j] > 0: new_W[j] -= 1
            total += p[j] * expected_two(tuple(new_V), tuple(new_W), p)
            s += p[j]
    return (1 + total) / s

# -------------------------------
# 3. Alle gültigen Verteilungen
# -------------------------------
def alle_verteilungen(m, n):
    return [v for v in itertools.product(range(n+1), repeat=m) if sum(v) == n]

# -------------------------------
# 4. Erwartungswerte für alle V
# -------------------------------
def alle_EVs(p, m, n, ev_func=expected_one):
    verteilungen = alle_verteilungen(m, n)
    return sorted([(v, ev_func(tuple(v), tuple(p))) for v in verteilungen], key=lambda x: x[1])

# -------------------------------
# 5. CSV-Datei schreiben
# -------------------------------
def speichere_csv(werte, dateiname):
    df = pd.DataFrame([
        {"Verteilung": str(v), "E(V)": str(ev), "E(V) (float)": float(ev)}
        for v, ev in werte
    ])
    df.to_csv(dateiname, index=False)
    return df

# -------------------------------
# 6. Plot erstellen (2D)
# -------------------------------

def plot_EVs(werte, titel="E(V)", pdf_name="plot.pdf", tick_abstand=1000, zeige_plot=True):
    x_vals = list(range(len(werte)))
    evs = [float(ev) for _, ev in werte]
    labels = [str(v) for v, _ in werte]
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(x_vals, evs, color="black", marker=".", markersize=3, linewidth=1)
    ax.set_ylabel("E(V)", fontsize=12)
    ax.set_xlabel("Verteilungen", fontsize=12)
    ax.set_title(titel, fontsize=12)
    ax.grid(True, linestyle=":", linewidth=0.5)

    if len(labels) <= 28:
        ax.set_xticks(x_vals)
        ax.set_xticklabels(labels, rotation=90, fontsize=8)
    else:
        ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_abstand))

    plt.tight_layout()
    plt.savefig(pdf_name, format="pdf", dpi=300, bbox_inches="tight")

    if zeige_plot:
        plt.show()
    else:
        plt.close()


# ------------------------------
# 7. Duell V gegen alle Gegner W 
# ------------------------------

def duell_gegen_alle(V, p, evw_func=expected_two):
    """
    Berechnet E(V, W) für alle Strategien W mit gleicher Chipsumme wie V.
    Gibt Liste mit Gegner und Erwartungswert zurück.
    """
    n = sum(V)
    m = len(V)
    gegner = alle_verteilungen(m, n)
    ergebnisse = []

    for W in gegner:
        evw = Fraction(0) if V == W else evw_func(V, W, p)

        ergebnisse.append({
            "Gegner": W,
            "E(V,W)": str(evw),
            "E(V,W) (float)": float(evw)
        })

    return ergebnisse

# ------------------------------
# 8. Extremwerte bei E(V,W)
# ------------------------------

def extremwerte_duell(V, p, evw_func=expected_two):
    """
    Gibt das Minimum und Maximum von E(V,W) für W ≠ V zurück,
    inklusive Gegnerstrategie, exakter und float-Wert.
    """
    n = sum(V)
    m = len(V)
    gegner = alle_verteilungen(m, n)

    werte = []
    for W_list in gegner:
        W = tuple(W_list)
        if W != V:
            evw = evw_func(V, W, p)
            werte.append({
                "Gegner": W,
                "E(V,W)": evw,
                "E(V,W) (str)": str(evw),
                "E(V,W) (float)": float(evw)
            })

    if not werte:
        return None, None

    min_row = min(werte, key=lambda r: r["E(V,W) (float)"])
    max_row = max(werte, key=lambda r: r["E(V,W) (float)"])

    return min_row, max_row


        
# -------------------------------
# 9. Plot erstellen (3D)
# -------------------------------

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import numpy as np

def plot_EVs_3D(werte, title="3D-Darstellung", pdf_name="evs_3D.pdf", cmap="viridis", graustufen=False):
    """
    Plottet eine 3D-Fläche für alle Verteilungen V=(v1,v2,v3) → E(V)
    Nur für m = 3 sinnvoll.
    """
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Daten extrahieren
    X, Y, Z = [], [], []
    for (v1, v2, v3), ev in werte:
        X.append(v1)
        Y.append(v2)
        Z.append(float(ev))  # ev ist ein Fraction

    X, Y, Z = np.array(X), np.array(Y), np.array(Z)

    # Farbskala
    if graustufen:
        cmap_used = cm.get_cmap("gray")
    else:
        cmap_used = cm.get_cmap(cmap)

    surf = ax.plot_trisurf(X, Y, Z, cmap=cmap_used, edgecolor="k", linewidth=0.2)

    # Achsen
    ax.set_xlabel("v₁")
    ax.set_ylabel("v₂")
    ax.set_zlabel("E(V)")
    ax.set_title(title)

    # Farbleiste
    cbar = fig.colorbar(surf, shrink=0.5, aspect=10, pad=0.1)
    cbar.set_label("Erwartungswert")

    plt.tight_layout()
    plt.savefig(pdf_name, format="pdf", dpi=300, bbox_inches="tight")
    plt.show()
