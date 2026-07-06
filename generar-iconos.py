"""Genera los íconos PWA del Escáner de Documentos.
Ejecutar UNA sola vez con:  python generar-iconos.py
"""
from PIL import Image, ImageDraw
from pathlib import Path

OUT = Path(__file__).parent / "icons"
OUT.mkdir(exist_ok=True)

BG_DARK  = (10, 10, 10)     # fondo casi negro (marca)
DOC_COL  = (255, 255, 255)  # hoja blanca
LINE_COL = (60, 60, 68)     # texto simulado en la hoja
ACCENT   = (232, 33, 39)    # rojo NEXO (línea de escaneo)

def rounded_rect(draw, box, radius, fill):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=radius, fill=fill)

def draw_icon(size: int, maskable: bool = False) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Fondo: un cuadrado redondeado que ocupa toda el área (para "maskable" damos margen)
    if maskable:
        # zona segura: 80% central. El fondo ocupa todo, la ilustración va en el 80%.
        bg_box = (0, 0, size, size)
        rounded_rect(d, bg_box, radius=int(size * 0.22), fill=BG_DARK)
        inset = int(size * 0.10)
    else:
        rounded_rect(d, (0, 0, size, size), radius=int(size * 0.22), fill=BG_DARK)
        inset = int(size * 0.16)

    # Hoja de papel dentro
    doc_x1 = inset
    doc_y1 = int(size * 0.18 + inset * 0.5)
    doc_x2 = size - inset
    doc_y2 = size - inset - int(size * 0.02)
    doc_r  = int(size * 0.05)
    rounded_rect(d, (doc_x1, doc_y1, doc_x2, doc_y2), radius=doc_r, fill=DOC_COL)

    # "Doblez" de esquina (triángulo para que se vea como documento)
    fold = int(size * 0.09)
    d.polygon(
        [(doc_x2 - fold, doc_y1), (doc_x2, doc_y1 + fold), (doc_x2 - fold, doc_y1 + fold)],
        fill=(230, 230, 235)
    )

    # Líneas simulando texto dentro de la hoja
    line_h = max(2, int(size * 0.025))
    gap    = int(size * 0.06)
    for i, w_ratio in enumerate([0.62, 0.72, 0.48, 0.66, 0.55]):
        y = doc_y1 + int(size * 0.14) + i * gap
        x1 = doc_x1 + int(size * 0.10)
        x2 = x1 + int((doc_x2 - doc_x1) * w_ratio)
        rounded_rect(d, (x1, y, x2, y + line_h), radius=line_h // 2, fill=LINE_COL)

    # Línea de escaneo (rojo) — cruza la hoja de lado a lado
    scan_h = max(3, int(size * 0.038))
    scan_y = doc_y1 + int((doc_y2 - doc_y1) * 0.58)
    scan_x1 = doc_x1 - int(size * 0.05)
    scan_x2 = doc_x2 + int(size * 0.05)
    d.rectangle((scan_x1, scan_y, scan_x2, scan_y + scan_h), fill=ACCENT)

    return img

def main():
    # Íconos que exige la PWA + Apple touch icon
    for sz in [192, 512]:
        p = OUT / f"icon-{sz}.png"
        draw_icon(sz, maskable=False).save(p, "PNG", optimize=True)
        print(f"  {p.relative_to(OUT.parent)}")

    # Maskable (para Android adaptativo)
    for sz in [192, 512]:
        p = OUT / f"icon-{sz}-maskable.png"
        draw_icon(sz, maskable=True).save(p, "PNG", optimize=True)
        print(f"  {p.relative_to(OUT.parent)}")

    # Apple touch icon (iOS)
    p = OUT / "apple-touch-icon.png"
    draw_icon(180, maskable=False).save(p, "PNG", optimize=True)
    print(f"  {p.relative_to(OUT.parent)}")

    # Favicon
    p = OUT / "favicon-96.png"
    draw_icon(96, maskable=False).save(p, "PNG", optimize=True)
    print(f"  {p.relative_to(OUT.parent)}")

    print("\nListo.")

if __name__ == "__main__":
    main()
