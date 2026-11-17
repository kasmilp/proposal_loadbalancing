"""Helper SVG untuk diagram ALQI-SAW. Warna sesuai ketentuan:
abu-abu existing, biru adaptasi, oranye pengembangan, merah gap, hijau kontribusi."""
from xml.sax.saxutils import escape

CAT = {
    "ex":  ("#ECEFF1", "#78909C"),   # existing
    "ad":  ("#E3F2FD", "#1E88E5"),   # adapted
    "dev": ("#FFF3E0", "#EF6C00"),   # developed
    "gap": ("#FFEBEE", "#E53935"),   # research gap
    "rc":  ("#E8F5E9", "#2E7D32"),   # contribution
    "plain": ("#FFFFFF", "#90A4AE"),
}
INK = "#1F2A33"
QUIET = "#55636E"
FONT = "DejaVu Sans, Arial, sans-serif"


class SVG:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.parts = []
        self.parts.append(
            f"<defs>"
            f"<marker id='ar' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'><path d='M0 0L10 5L0 10z' fill='#37474F'/></marker>"
            f"<marker id='arO' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'><path d='M0 0L10 5L0 10z' fill='#EF6C00'/></marker>"
            f"<marker id='arR' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'><path d='M0 0L10 5L0 10z' fill='#E53935'/></marker>"
            f"<marker id='arG' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'><path d='M0 0L10 5L0 10z' fill='#2E7D32'/></marker>"
            f"<marker id='arB' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'><path d='M0 0L10 5L0 10z' fill='#1E88E5'/></marker>"
            f"</defs>")
        self.rect(0, 0, w, h, fill="#FFFFFF", stroke="none", rx=0)

    def add(self, s):
        self.parts.append(s)

    def rect(self, x, y, w, h, fill="none", stroke="#90A4AE", sw=1.5, rx=10, dash=None, op=1):
        d = f" stroke-dasharray='{dash}'" if dash else ""
        self.add(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{rx}' fill='{fill}' fill-opacity='{op}' stroke='{stroke}' stroke-width='{sw}'{d}/>")

    def text(self, x, y, s, size=14, weight="normal", color=INK, anchor="start", italic=False):
        st = " font-style='italic'" if italic else ""
        self.add(f"<text x='{x}' y='{y}' font-family='{FONT}' font-size='{size}' font-weight='{weight}' fill='{color}' text-anchor='{anchor}'{st}>{escape(s)}</text>")

    def lines(self, x, y, arr, size=13, color=INK, anchor="start", lh=None, weight="normal"):
        lh = lh or size * 1.35
        for i, s in enumerate(arr):
            self.text(x, y + i * lh, s, size=size, color=color, anchor=anchor, weight=weight)

    def box(self, x, y, w, h, cat, title, body=(), tsize=14, bsize=12, center=False, dash=None, sw=1.8):
        fill, stroke = CAT[cat]
        self.rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, dash=dash)
        if center:
            self.text(x + w / 2, y + 22, title, size=tsize, weight="bold", anchor="middle")
            self.lines(x + w / 2, y + 22 + bsize * 1.6, body, size=bsize, color=QUIET, anchor="middle")
        else:
            self.text(x + 12, y + 22, title, size=tsize, weight="bold")
            self.lines(x + 12, y + 22 + bsize * 1.6, body, size=bsize, color=QUIET)

    def arrow(self, pts, color="#37474F", dash=None, sw=1.8, marker="ar", both=False):
        d = "M" + " L".join(f"{a} {b}" for a, b in pts)
        da = f" stroke-dasharray='{dash}'" if dash else ""
        ms = f" marker-start='url(#{marker})'" if both else ""
        self.add(f"<path d='{d}' fill='none' stroke='{color}' stroke-width='{sw}'{da} marker-end='url(#{marker})'{ms}/>")

    def line(self, pts, color="#37474F", dash=None, sw=1.8):
        d = "M" + " L".join(f"{a} {b}" for a, b in pts)
        da = f" stroke-dasharray='{dash}'" if dash else ""
        self.add(f"<path d='{d}' fill='none' stroke='{color}' stroke-width='{sw}'{da}/>")

    def tag(self, x, y, label, cat="gap"):
        fill, stroke = CAT[cat]
        w = 12 + 8.5 * len(label)
        self.add(f"<rect x='{x}' y='{y}' width='{w}' height='24' rx='12' fill='{stroke}' stroke='none'/>")
        self.text(x + w / 2, y + 17, label, size=13, weight="bold", color="#FFFFFF", anchor="middle")
        return w

    def band(self, x, y, w, h, label, fill="#F7F9FA"):
        self.rect(x, y, w, h, fill=fill, stroke="#CFD8DC", sw=1.2, rx=14, dash="6 4")
        self.add(f"<text x='{x + 14}' y='{y + h / 2}' font-family='{FONT}' font-size='13' font-weight='bold' fill='#78909C' text-anchor='middle' transform='rotate(-90 {x + 14} {y + h / 2})'>{escape(label)}</text>")

    def title(self, t, sub):
        self.text(30, 42, t, size=24, weight="bold")
        self.text(30, 68, sub, size=14, color=QUIET)

    def legend(self, x, y, items):
        cx = x
        for cat, lab in items:
            fill, stroke = CAT.get(cat, ("#fff", "#999"))
            if cat == "data":
                self.arrow([(cx, y + 10), (cx + 40, y + 10)])
                cx += 48
            elif cat == "ctrl":
                self.arrow([(cx, y + 10), (cx + 40, y + 10)], color="#EF6C00", dash="7 5", marker="arO")
                cx += 48
            elif cat == "mon":
                self.arrow([(cx, y + 10), (cx + 40, y + 10)], color="#1E88E5", dash="3 4", marker="arB")
                cx += 48
            else:
                self.rect(cx, y, 26, 20, fill=fill, stroke=stroke, sw=1.8, rx=5)
                cx += 34
            self.text(cx, y + 15, lab, size=13)
            cx += 9 * len(lab) * 0.85 + 26

    def note(self, x, y, arr):
        self.lines(x, y, arr, size=12.5, color=QUIET)

    def save(self, path):
        body = "\n".join(self.parts)
        svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{self.w}' height='{self.h}' "
               f"viewBox='0 0 {self.w} {self.h}'>\n{body}\n</svg>\n")
        open(path, "w", encoding="utf-8").write(svg)


# ---------------- ikon ----------------
def ic_starlink(s, x, y, c="#455A64"):
    # satelit kecil + piringan
    s.add(f"<g stroke='{c}' stroke-width='2' fill='none'>"
          f"<rect x='{x+22}' y='{y}' width='8' height='8' fill='{c}'/>"
          f"<rect x='{x+8}' y='{y+1}' width='12' height='6' fill='#90CAF9'/>"
          f"<rect x='{x+32}' y='{y+1}' width='12' height='6' fill='#90CAF9'/>"
          f"<path d='M{x+6} {y+30} Q{x+26} {y+52} {x+46} {y+30}' fill='#CFD8DC'/>"
          f"<path d='M{x+6} {y+30} L{x+46} {y+30}'/>"
          f"<path d='M{x+26} {y+41} L{x+26} {y+52} M{x+18} {y+52} L{x+34} {y+52}'/>"
          f"<path d='M{x+26} {y+30} L{x+26} {y+16}' stroke-dasharray='3 3'/></g>")


def ic_fiber(s, x, y, c="#455A64"):
    s.add(f"<g fill='none' stroke-width='3'>"
          f"<path d='M{x} {y+18} C{x+15} {y+4} {x+30} {y+32} {x+52} {y+16}' stroke='#FB8C00'/>"
          f"<path d='M{x} {y+26} C{x+15} {y+12} {x+30} {y+40} {x+52} {y+24}' stroke='#43A047'/>"
          f"<path d='M{x} {y+34} C{x+15} {y+20} {x+30} {y+48} {x+52} {y+32}' stroke='#1E88E5'/>"
          f"<circle cx='{x+52}' cy='{y+24}' r='5' fill='{c}' stroke='none'/></g>")


def ic_router(s, x, y, c="#37474F"):
    s.add(f"<g><rect x='{x}' y='{y+14}' width='56' height='26' rx='5' fill='{c}'/>"
          f"<circle cx='{x+12}' cy='{y+27}' r='3' fill='#80CBC4'/><circle cx='{x+22}' cy='{y+27}' r='3' fill='#80CBC4'/>"
          f"<circle cx='{x+32}' cy='{y+27}' r='3' fill='#FFCC80'/>"
          f"<path d='M{x+10} {y+14} L{x+6} {y} M{x+46} {y+14} L{x+50} {y}' stroke='{c}' stroke-width='3'/></g>")


def ic_switch(s, x, y, c="#37474F"):
    ports = "".join(f"<rect x='{x+6+i*9}' y='{y+20}' width='6' height='6' fill='#B0BEC5'/>" for i in range(5))
    s.add(f"<g><rect x='{x}' y='{y+12}' width='56' height='22' rx='4' fill='{c}'/>{ports}"
          f"<path d='M{x+8} {y+6} L{x+24} {y+6} M{x+20} {y+2} L{x+24} {y+6} L{x+20} {y+10} M{x+48} {y+6} L{x+32} {y+6} M{x+36} {y+2} L{x+32} {y+6} L{x+36} {y+10}' stroke='{c}' stroke-width='2' fill='none'/></g>")


def ic_ap(s, x, y, c="#37474F"):
    s.add(f"<g fill='none' stroke='{c}' stroke-width='2.5'>"
          f"<path d='M{x+8} {y+44} Q{x+28} {y+26} {x+48} {y+44} Z' fill='#ECEFF1'/>"
          f"<path d='M{x+18} {y+20} Q{x+28} {y+12} {x+38} {y+20}'/>"
          f"<path d='M{x+12} {y+13} Q{x+28} {y} {x+44} {y+13}'/>"
          f"<circle cx='{x+28}' cy='{y+27}' r='2.5' fill='{c}'/></g>")


def ic_client(s, x, y, c="#37474F"):
    s.add(f"<g><rect x='{x+4}' y='{y+8}' width='34' height='22' rx='2' fill='#90CAF9' stroke='{c}' stroke-width='2'/>"
          f"<path d='M{x} {y+33} L{x+42} {y+33}' stroke='{c}' stroke-width='4'/>"
          f"<rect x='{x+46}' y='{y+10}' width='14' height='24' rx='3' fill='#B3E5FC' stroke='{c}' stroke-width='2'/></g>")


def ic_db(s, x, y, c="#37474F"):
    s.add(f"<g stroke='{c}' stroke-width='2' fill='#ECEFF1'>"
          f"<path d='M{x} {y+8} L{x} {y+38} A20 7 0 0 0 {x+40} {y+38} L{x+40} {y+8}'/>"
          f"<ellipse cx='{x+20}' cy='{y+8}' rx='20' ry='7' fill='#CFD8DC'/>"
          f"<path d='M{x} {y+20} A20 7 0 0 0 {x+40} {y+20} M{x} {y+30} A20 7 0 0 0 {x+40} {y+30}' fill='none'/></g>")


def ic_monitor(s, x, y, c="#37474F"):
    s.add(f"<g fill='none' stroke='{c}' stroke-width='2'>"
          f"<rect x='{x}' y='{y+4}' width='44' height='30' rx='3' fill='#FFFFFF'/>"
          f"<path d='M{x+4} {y+22} L{x+12} {y+22} L{x+17} {y+12} L{x+23} {y+30} L{x+29} {y+16} L{x+34} {y+22} L{x+40} {y+22}' stroke='#E53935'/>"
          f"<path d='M{x+16} {y+40} L{x+28} {y+40} M{x+22} {y+34} L{x+22} {y+40}'/></g>")


def ic_gear(s, x, y, c="#EF6C00"):
    import math
    cx, cy, r1, r2 = x + 22, y + 22, 20, 14
    pts = []
    for i in range(16):
        a = i * math.pi / 8
        r = r1 if i % 2 == 0 else r2 + 2
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    s.add(f"<g><polygon points='{' '.join(pts)}' fill='{c}'/><circle cx='{cx}' cy='{cy}' r='7' fill='#FFFFFF'/></g>")


def ic_saw(s, x, y, c="#1E88E5"):
    bars = "".join(f"<rect x='{x+4+i*11}' y='{y+38-h}' width='8' height='{h}' fill='{c}'/>" for i, h in enumerate([14, 26, 20, 32]))
    s.add(f"<g>{bars}<path d='M{x} {y+40} L{x+50} {y+40}' stroke='#37474F' stroke-width='2'/>"
          f"<text x='{x+40}' y='{y+12}' font-family='{FONT}' font-size='16' font-weight='bold' fill='#37474F'>Σ</text></g>")


def ic_route(s, x, y, c="#37474F"):
    s.add(f"<g fill='none' stroke='{c}' stroke-width='3'>"
          f"<path d='M{x} {y+22} L{x+20} {y+22} L{x+40} {y+6}'/><path d='M{x+20} {y+22} L{x+40} {y+22}'/><path d='M{x+20} {y+22} L{x+40} {y+38}'/>"
          f"<path d='M{x+34} {y+3} L{x+42} {y+5} L{x+38} {y+12}'/><path d='M{x+36} {y+17} L{x+43} {y+22} L{x+36} {y+27}'/><path d='M{x+38} {y+32} L{x+42} {y+39} L{x+34} {y+41}'/></g>")
