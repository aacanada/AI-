"""Inline SVG icon set (24x24, stroke). No emoji fonts are guaranteed in the renderer."""

_P = {
    "lake": '<path d="M2 15c2 0 2-1.5 4-1.5S8 15 10 15s2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5"/><path d="M2 19c2 0 2-1.5 4-1.5S8 19 10 19s2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5"/><path d="M4 11l5-7 4 5 3-3 5 6"/>',
    "skate": '<path d="M3 13h18"/><path d="M4 13c0 2 1 3 3 3h10c2 0 3-1 3-3"/><circle cx="7" cy="19" r="1.6"/><circle cx="17" cy="19" r="1.6"/><path d="M7 9l3-4 4 2"/>',
    "bus": '<rect x="4" y="3" width="16" height="15" rx="3"/><path d="M4 11h16"/><path d="M8 3v8M16 3v8"/><circle cx="8" cy="15" r="1"/><circle cx="16" cy="15" r="1"/><path d="M6 18v3M18 18v3"/>',
    "bag": '<path d="M5 8h14l-1 13H6L5 8z"/><path d="M9 8V6a3 3 0 016 0v2"/>',
    "food": '<path d="M7 3v8M5 3v5a2 2 0 004 0V3"/><path d="M7 11v10"/><path d="M17 3c-2 0-3 3-3 6s1 4 3 4v8"/>',
    "beach": '<path d="M12 4a8 8 0 018 8H4a8 8 0 018-8z"/><path d="M12 12l3 9"/><path d="M3 21h18"/>',
    "leaf": '<path d="M5 19c0-9 6-14 15-15-1 9-6 15-15 15z"/><path d="M5 19l8-8"/>',
    "ball": '<circle cx="12" cy="12" r="9"/><path d="M12 3c-2 4-2 9 0 18"/><path d="M3.5 9c5 1 12 1 17 0"/><path d="M4 16c5-2 11-2 16 0"/>',
    "pool": '<circle cx="15" cy="6" r="2"/><path d="M6 12l4-3 4 3 3-2"/><path d="M2 16c2 0 2-1.5 4-1.5s2 1.5 4 1.5 2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5"/><path d="M2 20c2 0 2-1.5 4-1.5s2 1.5 4 1.5 2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5"/>',
    "ice": '<path d="M12 2v20M3 7l18 10M21 7L3 17"/><path d="M9 4l3 2 3-2M9 20l3-2 3 2"/>',
    "tree": '<path d="M12 2l6 8h-3l4 6h-5v6h-4v-6H5l4-6H6l6-8z"/>',
    "cap": '<path d="M2 9l10-5 10 5-10 5L2 9z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/><path d="M22 9v6"/>',
    "mask": '<path d="M4 4h16v6a8 8 0 01-16 0V4z"/><path d="M8 9h2M14 9h2"/><path d="M9 13c2 2 4 2 6 0"/>',
    "note": '<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>',
    "users": '<circle cx="9" cy="7" r="3.2"/><path d="M3 20c0-3.5 2.7-6 6-6s6 2.5 6 6"/><circle cx="17" cy="8" r="2.6"/><path d="M15.5 14c3 0 5.5 2 5.5 5"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "home": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "school": '<path d="M3 21h18"/><path d="M5 21V10l7-5 7 5v11"/><path d="M10 21v-5h4v5"/><path d="M12 5V2h3"/>',
    "star": '<path d="M12 3l2.8 5.8 6.2.9-4.5 4.4 1 6.2L12 17.4 6.5 20.3l1-6.2L3 9.7l6.2-.9L12 3z"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    "book": '<path d="M4 4h6a3 3 0 013 3v13a2 2 0 00-2-2H4V4z"/><path d="M20 4h-6a3 3 0 00-3 3"/><path d="M20 4v14h-7"/>',
    "wrench": '<path d="M14 6a4 4 0 005 5l-9 9a2 2 0 01-3-3l9-9a4 4 0 00-2-2z"/>',
    "climb": '<path d="M6 21l3-6 3 2 2-5 4-2"/><circle cx="9" cy="5" r="1.2"/><circle cx="15" cy="9" r="1.2"/><circle cx="7" cy="11" r="1.2"/><circle cx="17" cy="15" r="1.2"/>',
    "robot": '<rect x="5" y="8" width="14" height="11" rx="2"/><path d="M12 4v4"/><circle cx="12" cy="3.5" r="1"/><circle cx="9" cy="13" r="1.2"/><circle cx="15" cy="13" r="1.2"/><path d="M2 13h3M19 13h3"/>',
    "code": '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/>',
    "mountain": '<path d="M2 20l7-12 4 6 3-4 6 10H2z"/>',
    "pin": '<path d="M12 21s7-6.2 7-11.5A7 7 0 005 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
}


def icon(name, size=64, color="#ffffff", width=2.2):
    return (f'<svg class="ic" viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round">{_P[name]}</svg>')
