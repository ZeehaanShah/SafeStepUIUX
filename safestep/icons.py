"""SVG icons (same set as the SafeStep website)."""
IC = {
 "shield": "<path d=\"M12 3l7 3v5c0 4.5-3 8.3-7 10-4-1.7-7-5.5-7-10V6l7-3z\"/><path d=\"M9 12l2 2 4-4\"/>",
 "search": "<circle cx=\"11\" cy=\"11\" r=\"6.5\"/><path d=\"M16 16l4.5 4.5\"/><path d=\"M8.5 11l2 2 3-3.5\"/>",
 "play": "<path d=\"M12 3l7 3v5c0 4.5-3 8.3-7 10-4-1.7-7-5.5-7-10V6l7-3z\"/><path d=\"M10.5 9.5v5l4-2.5z\"/>",
 "badge": "<circle cx=\"12\" cy=\"9\" r=\"5.5\"/><path d=\"M8.5 13.5L7 21l5-2.5L17 21l-1.5-7.5\"/>",
 "book": "<path d=\"M3 5h6a3 3 0 013 3v12a2.5 2.5 0 00-2.5-2.5H3z\"/><path d=\"M21 5h-6a3 3 0 00-3 3v12a2.5 2.5 0 012.5-2.5H21z\"/>",
 "cal": "<rect x=\"3.5\" y=\"5\" width=\"17\" height=\"15.5\" rx=\"2.5\"/><path d=\"M3.5 10h17M8 3v4M16 3v4M9 15l2 2 4-4\"/>",
 "chat": "<path d=\"M4 5.5h16v11H10l-4.5 3.5v-3.5H4z\"/><path d=\"M8.5 11h.01M12 11h.01M15.5 11h.01\"/>",
 "help": "<circle cx=\"12\" cy=\"12\" r=\"8.5\"/><circle cx=\"12\" cy=\"12\" r=\"3.5\"/><path d=\"M6 6l3.5 3.5M18 6l-3.5 3.5M6 18l3.5-3.5M18 18l-3.5-3.5\"/>",
 "warn": "<path d=\"M12 4l9 15.5H3z\"/><path d=\"M12 10v4.5M12 17v.3\"/>",
 "back": "<path d=\"M19 12H5M11 6l-6 6 6 6\"/>",
 "next": "<path d=\"M5 12h14M13 6l6 6-6 6\"/>",
 "globe": "<circle cx=\"12\" cy=\"12\" r=\"8.5\"/><path d=\"M3.5 12h17M12 3.5c3 3 3 14 0 17M12 3.5c-3 3-3 14 0 17\"/>",
 "mic": "<rect x=\"9\" y=\"3.5\" width=\"6\" height=\"10.5\" rx=\"3\"/><path d=\"M5.5 11.5a6.5 6.5 0 0013 0M12 18v3\"/>",
 "share": "<circle cx=\"6\" cy=\"12\" r=\"2.5\"/><circle cx=\"18\" cy=\"6\" r=\"2.5\"/><circle cx=\"18\" cy=\"18\" r=\"2.5\"/><path d=\"M8.2 10.9l7.5-3.8M8.2 13.1l7.5 3.8\"/>",
 "check": "<circle cx=\"12\" cy=\"12\" r=\"8.5\"/><path d=\"M8 12.5l2.8 2.8L16 9.5\"/>",
 "phone": "<path d=\"M6 3.5h3l1.5 4.5-2 1.5a12 12 0 006 6l1.5-2 4.5 1.5v3a2 2 0 01-2 2A16.5 16.5 0 014 5.5a2 2 0 012-2z\"/>",
 "home": "<path d=\"M4 11l8-6.5 8 6.5\"/><path d=\"M6 9.5V19h12V9.5\"/><path d=\"M10 19v-5h4v5\"/>",
 "user": "<circle cx=\"12\" cy=\"8.5\" r=\"3.8\"/><path d=\"M4.5 20c1.2-3.8 4-5.5 7.5-5.5s6.3 1.7 7.5 5.5\"/>",
 "close": "<path d=\"M6 6l12 12M18 6L6 18\"/>",
 "bulb": "<path d=\"M9 18h6M10 21h4\"/><path d=\"M12 3a6 6 0 00-3.6 10.8c.7.5 1.1 1.3 1.1 2.2h5c0-.9.4-1.7 1.1-2.2A6 6 0 0012 3z\"/>",
 "lock": "<rect x=\"5\" y=\"10.5\" width=\"14\" height=\"10\" rx=\"2.5\"/><path d=\"M8.5 10.5V8a3.5 3.5 0 017 0v2.5\"/>",
 "msg": "<rect x=\"3.5\" y=\"5\" width=\"17\" height=\"13\" rx=\"2.5\"/><path d=\"M4 6.5l8 6 8-6\"/>",
 "qr": "<rect x=\"4\" y=\"4\" width=\"6\" height=\"6\" rx=\"1\"/><rect x=\"14\" y=\"4\" width=\"6\" height=\"6\" rx=\"1\"/><rect x=\"4\" y=\"14\" width=\"6\" height=\"6\" rx=\"1\"/><path d=\"M14 14h2v2h-2zM18 14h2M14 18h2M18 18h2v2\"/>",
 "card": "<rect x=\"3\" y=\"6\" width=\"18\" height=\"12\" rx=\"2.5\"/><path d=\"M3 10h18M7 15h4\"/>",
 "video": "<rect x=\"3\" y=\"6.5\" width=\"12.5\" height=\"11\" rx=\"2.5\"/><path d=\"M15.5 10.5l5-3v9l-5-3\"/>",
 "sms": "<rect x=\"6\" y=\"2.5\" width=\"12\" height=\"19\" rx=\"2.5\"/><path d=\"M10.5 18.5h3\"/>",
 "spark": "<path d=\"M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M18 6l-2.5 2.5M8.5 15.5L6 18\"/>",
 "bell": "<path d=\"M6 16.5V11a6 6 0 0112 0v5.5l1.5 1.5h-15z\"/><path d=\"M10 20.5h4\"/>",
 "text": "<path d=\"M5 6h14M12 6v13M8.5 19h7\"/>",
 "family": "<circle cx=\"8\" cy=\"8\" r=\"3\"/><circle cx=\"16.5\" cy=\"9.5\" r=\"2.5\"/><path d=\"M2.5 19c.8-3.4 3-5 5.5-5s4.7 1.6 5.5 5M13.5 15.5c.9-1 2-1.5 3-1.5 2 0 3.6 1.3 4.2 4\"/>",
 "logout": "<path d=\"M14 4h4.5A1.5 1.5 0 0120 5.5v13a1.5 1.5 0 01-1.5 1.5H14\"/><path d=\"M10 16l-4-4 4-4M6 12h10\"/>",
 "coin": "<circle cx=\"12\" cy=\"12\" r=\"8.5\"/><path d=\"M9 9.5h5M9 12.5h5M11 9.5c2 0 2 3 0 3l3 3\"/>",
 "menu": "<path d=\"M4 7h16M4 12h16M4 17h16\"/>",
 "copy": "<rect x=\"8\" y=\"8\" width=\"12\" height=\"12\" rx=\"2.5\"/><path d=\"M16 8V5.5A1.5 1.5 0 0014.5 4h-9A1.5 1.5 0 004 5.5v9A1.5 1.5 0 005.5 16H8\"/>",
 "send": "<path d=\"M4 12l16-8-6 16-2.5-6.5z\"/>",
 "speaker": "<path d=\"M4 9.5h3.5L12 5.5v13l-4.5-4H4z\"/><path d=\"M15.5 9a4 4 0 010 6M18 6.5a7.5 7.5 0 010 11\"/>"
}


def ic(name: str, size: str = "1.35em", color: str = "currentColor") -> str:
    return (f'<svg class="ico" style="width:{size};height:{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{IC.get(name, "")}</svg>')
