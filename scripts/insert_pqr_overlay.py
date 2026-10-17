#!/usr/bin/env python3
"""Insert PQR status overlay Lua into Profiles/*_Abilities.xml"""

import re
import sys
from pathlib import Path

_scripts = Path(__file__).resolve().parent
sys.path.insert(0, str(_scripts))
from replace_pqr_overlay_block import NEW_BLOCK as OVERLAY_XML

OVERLAY_XML = OVERLAY_XML.strip()

CALL_UPDATE = "\nif PQR_UpdateStatusOverlay then PQR_UpdateStatusOverlay() end\n"


def patch_functionsloaded(text: str) -> str:
    """Insert overlay library immediately before `end</Lua>` that closes -- Function -- block."""
    m = re.search(r"(functionsloaded\s*=\s*true\s*\n)(end</Lua>)", text)
    if not m:
        return text
    return text.replace(m.group(1) + m.group(2), m.group(1) + OVERLAY_XML + "\n" + m.group(2), 1)


def patch_funcloaded_druid(text: str) -> str:
    """Insert overlay once after first `FuncLoaded = true` before GotClearCast (druid)."""
    return re.sub(
        r"(FuncLoaded\s*=\s*true\s*\n)(\s*GotClearCast\s*=\s*0)",
        r"\1" + OVERLAY_XML + "\n\2",
        text,
        count=1,
    )


def patch_all_abilities(text: str) -> str:
    parts = text.split("<Ability>")
    out = [parts[0]]
    for part in parts[1:]:
        out.append(patch_one_ability("<Ability>" + part))
    return "".join(out)


def patch_one_ability(segment: str):
    """Append PQR_UpdateStatusOverlay to Hotkeys and Stuff Lua bodies."""
    name_m = re.match(r"<Ability><Name>([^<]*)</Name>", segment)
    if not name_m:
        return segment
    name = name_m.group(1)
    lua_open = segment.find("<Lua>")
    if lua_open < 0:
        return segment
    lua_inner_start = lua_open + len("<Lua>")
    lua_close = segment.find("</Lua><RecastDelay>", lua_inner_start)
    if lua_close < 0:
        return segment
    body = segment[lua_inner_start:lua_close]

    changed = False
    if "Stuff --" in name and name.strip().startswith("--") and name.strip().endswith("Stuff --"):
        if "PQR_UpdateStatusOverlay()" not in body:
            body = body.rstrip() + CALL_UPDATE
            changed = True
    elif "Hotkeys" in name:
        if "PQR_UpdateStatusOverlay()" not in body:
            body = body.rstrip() + CALL_UPDATE
            changed = True

    if not changed:
        return segment
    return segment[:lua_inner_start] + body + segment[lua_close:]


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text

    if "PQR_StatusOverlayLib" in text:
        print(f"SKIP (already patched): {path.name}")
        return False

    text = patch_functionsloaded(text)
    if text == orig:
        text = patch_funcloaded_druid(text)

    if "PQR_StatusOverlayLib" not in text:
        print(f"SKIP (no functionsloaded / FuncLoaded anchor): {path.name}")
        return False

    text2 = patch_all_abilities(text)

    if text2 == orig:
        print(f"WARN no hotkey/stuff changes: {path.name}")

    path.write_text(text2, encoding="utf-8")
    print(f"OK {path.name}")
    return True


def main():
    root = Path("/workspace/Profiles")
    for p in sorted(root.glob("*_Abilities.xml")):
        patch_file(p)


if __name__ == "__main__":
    main()
