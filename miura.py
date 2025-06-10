import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import math

# Parametri
a = 25               
b = 25               
alpha_deg = 60       
alpha = np.radians(alpha_deg)

# Oblika in velikost dodatka
addon_shape = 'heart'    # 'square' ali 'circle' ali 'heart'
addon_size = 8           # mm — za 'square': stranica, za 'circle': premer, za 'heart': širina
addon_angle = 90         # stopinj

# Izračun zamika v x- in y-smeri zaradi kota alpha
dx = b * np.cos(alpha)
dy = b * np.sin(alpha)

# Velikost slike v mm
W_mm = 297
H_mm = 390
W_in = W_mm / 25.4
H_in = H_mm / 25.4

# Izračun števila stolpcev in vrstic
n = math.floor((W_mm - dx) / (2 * a))  # Stolpci
m = math.floor(H_mm / (2 * dy))        # Vrstice

# Izhodna mapa (RELATIVNO do lokacije .py datoteke)
output_dir = os.path.join(os.path.dirname(__file__), 'output_svgs')
os.makedirs(output_dir, exist_ok=True)

# Osnova imena datoteke
filename_base = (
    f'miura_a{a:.1f}_b{b:.1f}_n{n}_m{m}'
    f'_alpha{alpha_deg:.0f}'
    f'_{addon_shape}{addon_size}mm'
)
full_path_base = os.path.join(output_dir, filename_base)

# Ustvari figuro
fig = plt.figure(figsize=(W_in, H_in))
ax = fig.add_subplot(111)
ax.set_xticks([]); ax.set_yticks([])
ax.set_xticklabels([]); ax.set_yticklabels([])

# Funkcija za kvadrat
def draw_centered_square(ax, cx, cy, size=addon_size, **kwargs):
    half = size / 2
    rect = patches.Rectangle(
        (cx - half, cy - half),
        size, size,
        fill=False,
        **kwargs
    )
    ax.add_patch(rect)

# Funkcija za krog
def draw_centered_circle(ax, cx, cy, diameter=addon_size, **kwargs):
    radius = diameter / 2
    circ = patches.Circle(
        (cx, cy),
        radius,
        fill=False,
        **kwargs
    )
    ax.add_patch(circ)

# Funkcija za srček z rotacijo
def draw_centered_heart(ax, cx, cy, size=addon_size, angle_deg=0, **kwargs):
    t = np.linspace(0, 2 * np.pi, 200)
    x = 16 * np.sin(t)**3
    y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)

    x /= 32
    y /= 26

    x *= size
    y *= size

    angle_rad = np.radians(angle_deg)
    x_rot = x * np.cos(angle_rad) - y * np.sin(angle_rad)
    y_rot = x * np.sin(angle_rad) + y * np.cos(angle_rad)

    x_rot += cx
    y_rot += cy

    heart = patches.Polygon(
        np.column_stack([x_rot, y_rot]),
        closed=True,
        fill=False,
        **kwargs
    )
    ax.add_patch(heart)

# Nariši mrežo in dodatke
for i in range(n):
    for j in range(m):
        x_off = i * 2 * a
        y_off = j * 2 * dy

        cells = [
            [(0, dy), (a, dy), (a+dx, 0), (dx, 0)],
            [(0, dy), (dx, 2*dy), (a+dx, 2*dy), (a, dy)],
            [(a, dy), (2*a, dy), (2*a+dx, 0), (a+dx, 0)],
            [(a, dy), (a+dx, 2*dy), (2*a+dx, 2*dy), (2*a, dy)],
        ]
        for poly in cells:
            poly_mm = [ (x + x_off, y + y_off) for x, y in poly ]
            xs, ys = zip(*(poly_mm + [poly_mm[0]]))
            ax.plot(xs, ys, '-', linewidth=0.3, color='black')

            # Center
            cx = sum(x for x, _ in poly_mm) / 4
            cy = sum(y for _, y in poly_mm) / 4

            # Dodatek
            if addon_shape == 'square':
                draw_centered_square(ax, cx, cy, size=addon_size, edgecolor='black', linewidth=0.3)
            elif addon_shape == 'circle':
                draw_centered_circle(ax, cx, cy, diameter=addon_size, edgecolor='black', linewidth=0.3)
            elif addon_shape == 'heart':
                draw_centered_heart(ax, cx, cy, size=addon_size, angle_deg=addon_angle, edgecolor='black', linewidth=0.3)
            else:
                raise ValueError(f"Nepodprta oblika dodatka: {addon_shape}")

# Obreži na papir
ax.set_xlim(0, W_mm)
ax.set_ylim(0, H_mm)
ax.set_aspect('equal')

# Shrani
for ext in ['svg', 'png']:
    full_path = f"{full_path_base}.{ext}"
    plt.savefig(full_path, dpi=300, bbox_inches=None)
    print(f"Slika shranjena kot: {full_path}")

plt.show()
