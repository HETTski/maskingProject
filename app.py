import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def maskingEfficiency(n, lambdaP, holeHeight):
    if n <= 0:
        return float('inf')
    E_single = 20 * np.log10(lambdaP / (2 * holeHeight))
    E_total = E_single - 20 * np.log10(np.sqrt(n))
    return E_total

# Parametry fizyczne
f = 3.26e9  # Częstotliwość [Hz]
c = 3e8     # Prędkość światła [m/s]
lambdaP = c / f  # Długość fali [m]

# Wymiary płyty
plateWidth = 0.5  # [m]
plateHeight = 0.5 # [m]

# ZWIĘKSZONA PRZESTRZEŃ POSZUKIWAŃ (do kilku centymetrów)
holeHeights = np.linspace(0.005, 0.05, 20)  # Wysokości: 5-50 mm
spacings_h = np.linspace(0.02, 0.15, 20)    # Odstępy poziome: 20-150 mm  
spacings_v = np.linspace(0.02, 0.15, 20)    # Odstępy pionowe: 20-150 mm

targetS = 8  # Docelowa skuteczność ekranowania [dB]

best_params = {
    'N': 0, 'S': -np.inf, 'width': 0, 'height': 0,
    'spacing_h': 0, 'spacing_v': 0, 'openArea': 0,
    'cols': 0, 'rows': 0
}

for holeHeight in holeHeights:
    holeWidth = (2/3) * holeHeight  # Zachowaj proporcje 2:3
    
    for spacing_h in spacings_h:
        for spacing_v in spacings_v:
            cols = int(plateWidth // (holeWidth + spacing_h))
            rows = int(plateHeight // (holeHeight + spacing_v))
            N = cols * rows
            
            if N == 0:
                continue
            
            S = maskingEfficiency(N, lambdaP, holeHeight)
            openArea = (N * holeWidth * holeHeight) / (plateWidth * plateHeight) * 100
            
            # Kryterium: skuteczność najbliższa 8 dB i nie mniejsza niż 6 dB
            if (abs(S - targetS) < abs(best_params['S'] - targetS)) and (S >= 6):
                best_params.update({
                    'N': N, 'S': S, 'width': holeWidth, 'height': holeHeight,
                    'spacing_h': spacing_h, 'spacing_v': spacing_v,
                    'openArea': openArea, 'cols': cols, 'rows': rows
                })

# Prezentacja wyników
print("\n==============================================")
print("PARAMETRY PODSTAWOWE")
print("==============================================")
print(f"Częstotliwość: {f/1e9:.2f} GHz")
print(f"Długość fali: {lambdaP*100:.2f} cm")
print(f"Wymiary płyty: {plateWidth*100:.0f} cm × {plateHeight*100:.0f} cm")

print("\n==============================================")
print("OPTYMALNA KONFIGURACJA (ZWIĘKSZONA PRZESTRZEŃ POSZUKIWAŃ)")
print("==============================================")
print(f"Liczba otworów: {best_params['N']} ({best_params['cols']}×{best_params['rows']})")
print(f"Wymiary otworu: {best_params['width']*1000:.1f} mm × {best_params['height']*1000:.1f} mm")
print(f"Odstępy poziome: {best_params['spacing_h']*1000:.1f} mm")
print(f"Odstępy pionowe: {best_params['spacing_v']*1000:.1f} mm")
print(f"Skuteczność: {best_params['S']:.2f} dB")
print(f"Powierzchnia otwarta: {best_params['openArea']:.2f}%")

# Wizualizacja
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_title(f"Przesłona: {best_params['N']} otworów\nSkuteczność = {best_params['S']:.1f} dB, Powierzchnia otwarta = {best_params['openArea']:.1f}%", 
             pad=20, fontsize=14)

# Rysowanie otworów
for row in range(best_params['rows']):
    for col in range(best_params['cols']):
        x = best_params['spacing_h']/2 + col * (best_params['width'] + best_params['spacing_h'])
        y = best_params['spacing_v']/2 + row * (best_params['height'] + best_params['spacing_v'])
        rect = Rectangle(
            (x, y), best_params['width'], best_params['height'],
            edgecolor='black', facecolor='#1f77b4', alpha=0.6, lw=1.5
        )
        ax.add_patch(rect)

# Funkcja do rysowania wymiarów
def draw_dimension(ax, x1, y1, x2, y2, text, orientation='h', offset=0.003):
    if orientation == 'h':
        ax.annotate('', xy=(x1, y1-offset), xytext=(x2, y1-offset),
                    arrowprops=dict(arrowstyle='<->', color='red', lw=1.5))
        ax.text((x1+x2)/2, y1-offset-0.005, text,
                ha='center', va='top', color='red', fontsize=10, 
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    else:
        ax.annotate('', xy=(x1-offset, y1), xytext=(x1-offset, y2),
                    arrowprops=dict(arrowstyle='<->', color='red', lw=1.5))
        ax.text(x1-offset-0.005, (y1+y2)/2, text,
                ha='right', va='center', color='red', fontsize=10, rotation=90,
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

# Rysowanie wymiarów na wybranych otworach
if best_params['N'] > 0:
    for i, (row, col) in enumerate([(0,0), (0,1), (1,0)]):
        if row >= best_params['rows'] or col >= best_params['cols']:
            continue
        
        x = best_params['spacing_h']/2 + col * (best_params['width'] + best_params['spacing_h'])
        y = best_params['spacing_v']/2 + row * (best_params['height'] + best_params['spacing_v'])
        
        if i == 0:  # Wymiary otworu
            h_offset = 0.015  # 15 mm od krawędzi
            v_offset = 0.020  # 20 mm od krawędzi
            draw_dimension(ax, x, y - h_offset, x + best_params['width'], y - h_offset,
                         f"{best_params['width']*1000:.1f} mm", 'h', h_offset/2)
            draw_dimension(ax, x - v_offset, y, x - v_offset, y + best_params['height'],
                         f"{best_params['height']*1000:.1f} mm", 'v', v_offset/2)
        
        if i == 1:  # Odstęp poziomy
            next_x = x + best_params['width'] + best_params['spacing_h']
            draw_dimension(ax, x + best_params['width'], y - 0.01, next_x, y - 0.01,
                         f"{best_params['spacing_h']*1000:.1f} mm", 'h')
        
        if i == 2:  # Odstęp pionowy
            next_y = y + best_params['height'] + best_params['spacing_v']
            draw_dimension(ax, x - 0.01, y + best_params['height'], x - 0.01, next_y,
                         f"{best_params['spacing_v']*1000:.1f} mm", 'v')

    # Wymiary całej płyty
    draw_dimension(ax, 0, -0.03, plateWidth, -0.03, 
                 f"{plateWidth*1000:.1f} mm", 'h', 0.015)
    draw_dimension(ax, -0.03, 0, -0.03, plateHeight, 
                 f"{plateHeight*1000:.1f} mm", 'v', 0.015)

# Konfiguracja wykresu
ax.set_xlim(-0.1, plateWidth + 0.1)
ax.set_ylim(plateHeight + 0.1, -0.1)
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
plt.show()