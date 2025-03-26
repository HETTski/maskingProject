import numpy as np
import matplotlib.pyplot as plt

def maskingEfficiency(n, lambdaP, holeHeight):
    if n <= 0:
        return float('inf')
    E_single = 20 * np.log10(lambdaP / (2 * holeHeight))
    E_total = E_single - 20 * np.log10(np.sqrt(n))
    return E_total

f = 3.26e9 
c = 3e8     
lambdaP = c / f  

plateWidth = 0.5  
plateHeight = 0.5 


holeHeights = np.linspace(0.015, 0.025, 10) 
spacings = np.linspace(0.01, 0.03, 10)      
targetS = 8  

best_N = 0
best_S = -np.inf
best_holeWidth = 0
best_holeHeight = 0
best_spacing = 0
best_openArea = 0

for holeHeight in holeHeights:
    holeWidth = (2/3) * holeHeight  
    for spacing in spacings:
        cols = int(plateWidth // (holeWidth + spacing))
        rows = int(plateHeight // (holeHeight + spacing))
        N = cols * rows
        if N == 0:
            continue
        
        S = maskingEfficiency(N, lambdaP, holeHeight)
        openArea = (N * holeWidth * holeHeight) / (plateWidth * plateHeight) * 100
        

        if (abs(S - targetS) < abs(best_S - targetS)) or \
           (abs(S - targetS) == abs(best_S - targetS) and openArea > best_openArea):
            best_N = N
            best_S = S
            best_holeWidth = holeWidth
            best_holeHeight = holeHeight
            best_spacing = spacing
            best_openArea = openArea

if best_N == 0:
    print("Nie znaleziono rozwiązania. Zmniejsz rozmiar otworów lub zwiększ odstępy.")
else:
    print(f"Optymalne parametry:")
    print(f"- Liczba otworów: {best_N}")
    print(f"- Rozmiar otworu: {best_holeWidth * 1000:.1f} mm × {best_holeHeight * 1000:.1f} mm (2:3)")
    print(f"- Odstęp między otworami: {best_spacing * 1000:.1f} mm")
    print(f"- Skuteczność ekranowania: {best_S:.2f} dB")
    print(f"- Powierzchnia otwarta: {best_openArea:.2f}%")


    fig, ax = plt.subplots(figsize=(6, 6))
    for row in range(int(np.sqrt(best_N))):
        for col in range(int(np.sqrt(best_N))):
            x = best_spacing/2 + col * (best_holeWidth + best_spacing)
            y = best_spacing/2 + row * (best_holeHeight + best_spacing)
            rect = plt.Rectangle((x, y), best_holeWidth, best_holeHeight, 
                                edgecolor='black', facecolor='gray')
            ax.add_patch(rect)

    ax.set_xlim(0, plateWidth)
    ax.set_ylim(0, plateHeight)
    ax.set_title(f"Przesłona: {best_N} otworów, S = {best_S:.1f} dB")
    ax.set_aspect('equal')
    plt.gca().invert_yaxis()
    plt.show()