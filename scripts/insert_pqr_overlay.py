#!/usr/bin/env python3
"""Insert PQR status overlay Lua into Profiles/*_Abilities.xml"""

import re
from pathlib import Path

OVERLAY_XML = r'''
if not PQR_StatusOverlayLib then
	PQR_StatusOverlayLib = true
	function PQR_CreateStatusOverlay()
		if PQR_StatusOverlayFrame then return end
		local f = CreateFrame(&quot;Frame&quot;, &quot;PQR_StatusOverlayFrame&quot;, UIParent)
		PQR_StatusOverlayFrame = f
		f:SetWidth(240)
		f:SetHeight(76)
		f:SetPoint(&quot;TOP&quot;, UIParent, &quot;TOP&quot;, 0, -28)
		local bg = f:CreateTexture(nil, &quot;BACKGROUND&quot;)
		bg:SetAllPoints()
		bg:SetTexture(0, 0, 0, 0.55)
		local t = f:CreateFontString(nil, &quot;OVERLAY&quot;, &quot;GameFontNormalSmall&quot;)
		t:SetPoint(&quot;TOPLEFT&quot;, f, &quot;TOPLEFT&quot;, 8, -6)
		t:SetJustifyH(&quot;LEFT&quot;)
		t:SetTextColor(1, 1, 1, 1)
		PQR_StatusOverlayTitle = t
		t:SetText(&quot;PQR&quot;)
		local l1 = f:CreateFontString(nil, &quot;OVERLAY&quot;, &quot;GameFontNormalSmall&quot;)
		l1:SetPoint(&quot;TOPLEFT&quot;, f, &quot;TOPLEFT&quot;, 8, -22)
		l1:SetJustifyH(&quot;LEFT&quot;)
		PQR_StatusOverlayLine1 = l1
		local l2 = f:CreateFontString(nil, &quot;OVERLAY&quot;, &quot;GameFontNormalSmall&quot;)
		l2:SetPoint(&quot;TOPLEFT&quot;, f, &quot;TOPLEFT&quot;, 8, -38)
		l2:SetJustifyH(&quot;LEFT&quot;)
		PQR_StatusOverlayLine2 = l2
		local l3 = f:CreateFontString(nil, &quot;OVERLAY&quot;, &quot;GameFontNormalSmall&quot;)
		l3:SetPoint(&quot;TOPLEFT&quot;, f, &quot;TOPLEFT&quot;, 8, -54)
		l3:SetJustifyH(&quot;LEFT&quot;)
		PQR_StatusOverlayLine3 = l3
	end
	function PQR_UpdateStatusOverlay()
		if not PQR_StatusOverlayFrame then PQR_CreateStatusOverlay() end
		local _, class = UnitClass(&quot;player&quot;)
		PQR_StatusOverlayTitle:SetText(class or &quot;PQR&quot;)
		local sbad = StopRota and &quot;|cffff4444STOPPED|r&quot; or &quot;|cff44ff44RUNNING|r&quot;
		PQR_StatusOverlayLine1:SetText(&quot;Rotation: &quot;..sbad)
		local aoeStr = &quot;&quot;
		if AoE ~= nil then
			aoeStr = (AoE == true) and &quot;|cff44ff44AoE ON|r&quot; or &quot;|cffff8888AoE OFF|r&quot;
		elseif type(AOE) == &quot;function&quot; then
			aoeStr = AOE() and &quot;|cff44ff44AoE ON|r&quot; or &quot;|cffff8888AoE OFF|r&quot;
		else
			aoeStr = &quot;|cffaaaaaaAoE n/a|r&quot;
		end
		PQR_StatusOverlayLine2:SetText(aoeStr)
		local parts = {}
		if MS ~= nil then
			table.insert(parts, (MS == true) and &quot;Mind Sear |cff44ff44ON|r&quot; or &quot;Mind Sear |cffff8888OFF|r&quot;)
		end
		if HN ~= nil then
			table.insert(parts, (HN == true) and &quot;Hurricane |cff44ff44ON|r&quot; or &quot;Hurricane |cffff8888OFF|r&quot;)
		end
		if VoL ~= nil then
			table.insert(parts, (VoL == true) and &quot;Volley |cff44ff44ON|r&quot; or &quot;Volley |cffff8888OFF|r&quot;)
		end
		if COL ~= nil then
			table.insert(parts, (COL == true) and &quot;Chain Lightning |cff44ff44ON|r&quot; or &quot;Chain Lightning |cffff8888OFF|r&quot;)
		end
		if Heal ~= nil then
			table.insert(parts, (Heal == true) and &quot;Chain Heal spam |cff44ff44ON|r&quot; or &quot;Chain Heal spam |cffff8888OFF|r&quot;)
		end
		if ELE ~= nil then
			table.insert(parts, (ELE == true) and &quot;Elem mode |cff44ff44ON|r&quot; or &quot;Elem mode |cffff8888OFF|r&quot;)
		end
		if SoC ~= nil or RoF ~= nil then
			local s = &quot;&quot;
			if SoC ~= nil then s = (SoC == true) and &quot;SoC |cff44ff44ON|r&quot; or &quot;SoC |cffff8888OFF|r&quot; end
			if RoF ~= nil then s = s..((s ~= &quot;&quot;) and &quot;  &quot; or &quot;&quot;)..((RoF == true) and &quot;RoF |cff44ff44ON|r&quot; or &quot;RoF |cffff8888OFF|r&quot;) end
			table.insert(parts, s)
		end
		if Opener ~= nil then
			table.insert(parts, Opener and &quot;Opener: Garrote&quot; or &quot;Opener: Ambush&quot;)
		end
		local extra = (#parts &gt; 0) and table.concat(parts, &quot;  |  &quot;) or &quot; &quot;
		PQR_StatusOverlayLine3:SetText(extra)
	end
end
'''.strip()

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
