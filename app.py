import numpy as np
import matplotlib.pyplot as plt

def maskingEfficiency(n, lambdaP):
    E_single = 20 * np.log10(lambdaP / (2 * 3e-2))
    E_total = E_single - 20 * np.log10(np.sqrt(n))
    return E_total

f = 3.26e9
c = 3e8
lambdaP = c/f
plateWidth = 50e-2
plateHeight = 50e-2
holeWidth = 2e-2
holeHeight = 3e-2

spacing = 0
Nholes = 0
S = 0

while S < 8:
    spacing += 1e-3
    cols = int(plateWidth // (holeWidth + spacing))
    rows = int(plateHeight // (holeHeight + spacing))
    Nholes = cols * rows
    S = maskingEfficiency(Nholes, lambdaP)

print (f'Liczba otworów: {Nholes}, Skuteczność ekranowania: {S:.2f} dB, Optymalny odstęp: {spacing*100:.1f} mm')

fig, ax = plt.subplots(figsize=(6,6))
for i in range(rows):
    for j in range(cols):
        x = j * (holeWidth + spacing)
        y = i * (holeHeight + spacing)
        rect = plt.rectangle((x,y), holeWidth, edgecolor="black", facecolor='gray')

ax.set_xlim(0, plateWidth)
ax.set_ylim(0, plateHeight)
ax.set_title("Rozmieszczenie otworów w przesłonie")
ax.set_aspect('equal')
plt.gca().invert_yaxis()
plt.show()