#!/usr/bin/env python3
"""Replace embedded PQR_StatusOverlayLib ... end block in Profiles/*_Abilities.xml"""

import re
from pathlib import Path

NEW_BLOCK = r'''if not PQR_StatusOverlayLib then
	PQR_StatusOverlayLib = true
	if PQR_OverlayBuffEnabled == nil then PQR_OverlayBuffEnabled = false end
	if PQR_RetPackAoE == nil then PQR_RetPackAoE = false end
	if PQR_RetDivinePleaLowMana == nil then PQR_RetDivinePleaLowMana = false end
	function PQR_CheckBtn(btn)
		return btn and btn:GetChecked()
	end
	function PQR_CreateStatusOverlay()
		if PQR_StatusOverlayFrame then return end
		local f = CreateFrame(&quot;Frame&quot;, &quot;PQR_StatusOverlayFrame&quot;, UIParent)
		PQR_StatusOverlayFrame = f
		f:SetWidth(300)
		f:SetHeight(178)
		f:SetPoint(&quot;TOP&quot;, UIParent, &quot;TOP&quot;, 0, -28)
		f:SetFrameStrata(&quot;MEDIUM&quot;)
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
		local cbR = CreateFrame(&quot;CheckButton&quot;, &quot;PQR_StatusOverlay_cbRot&quot;, f, &quot;UICheckButtonTemplate&quot;)
		cbR:SetPoint(&quot;TOPLEFT&quot;, f, &quot;TOPLEFT&quot;, 4, -68)
		cbR:SetScript(&quot;OnClick&quot;, function(self)
			StopRota = not PQR_CheckBtn(self)
		end)
		_G[cbR:GetName()..&quot;Text&quot;]:SetText(&quot;Rotation enabled&quot;)
		PQR_StatusOverlay_cbRot = cbR
		local cbA = CreateFrame(&quot;CheckButton&quot;, &quot;PQR_StatusOverlay_cbAoE&quot;, f, &quot;UICheckButtonTemplate&quot;)
		cbA:SetPoint(&quot;TOPLEFT&quot;, f, &quot;TOPLEFT&quot;, 4, -88)
		cbA:SetScript(&quot;OnClick&quot;, function(self)
			if AoE ~= nil then AoE = not not PQR_CheckBtn(self) end
		end)
		_G[cbA:GetName()..&quot;Text&quot;]:SetText(&quot;AoE mode (manual)&quot;)
		PQR_StatusOverlay_cbAoE = cbA
		local cbB = CreateFrame(&quot;CheckButton&quot;, &quot;PQR_StatusOverlay_cbBuff&quot;, f, &quot;UICheckButtonTemplate&quot;)
		cbB:SetPoint(&quot;TOPLEFT&quot;, f, &quot;TOPLEFT&quot;, 4, -108)
		cbB:SetScript(&quot;OnClick&quot;, function(self)
			PQR_OverlayBuffEnabled = not not PQR_CheckBtn(self)
		end)
		_G[cbB:GetName()..&quot;Text&quot;]:SetText(&quot;Extra toggle (profile hook)&quot;)
		PQR_StatusOverlay_cbBuff = cbB
		local cbP = CreateFrame(&quot;CheckButton&quot;, &quot;PQR_StatusOverlay_cbPack&quot;, f, &quot;UICheckButtonTemplate&quot;)
		cbP:SetPoint(&quot;TOPLEFT&quot;, f, &quot;TOPLEFT&quot;, 4, -128)
		cbP:SetScript(&quot;OnClick&quot;, function(self)
			PQR_RetPackAoE = not not PQR_CheckBtn(self)
		end)
		_G[cbP:GetName()..&quot;Text&quot;]:SetText(&quot;Ret: auto AoE (3+ melee enemies)&quot;)
		PQR_StatusOverlay_cbPack = cbP
		local cbD = CreateFrame(&quot;CheckButton&quot;, &quot;PQR_StatusOverlay_cbDPlea&quot;, f, &quot;UICheckButtonTemplate&quot;)
		cbD:SetPoint(&quot;TOPLEFT&quot;, f, &quot;TOPLEFT&quot;, 4, -148)
		cbD:SetScript(&quot;OnClick&quot;, function(self)
			PQR_RetDivinePleaLowMana = not not PQR_CheckBtn(self)
		end)
		_G[cbD:GetName()..&quot;Text&quot;]:SetText(&quot;Ret: Divine Plea below 30% mana&quot;)
		PQR_StatusOverlay_cbDPlea = cbD
		PQR_OverlayHUD_Accum = 0
		f:SetScript(&quot;OnUpdate&quot;, function(self, elapsed)
			PQR_OverlayHUD_Accum = PQR_OverlayHUD_Accum + elapsed
			if PQR_OverlayHUD_Accum &gt;= 0.15 then
				PQR_OverlayHUD_Accum = 0
				if PQR_UpdateStatusOverlay then PQR_UpdateStatusOverlay() end
			end
		end)
	end
	function PQR_UpdateStatusOverlay()
		if not PQR_StatusOverlayFrame then PQR_CreateStatusOverlay() end
		local _, classToken = UnitClass(&quot;player&quot;)
		PQR_StatusOverlayTitle:SetText(classToken or &quot;PQR&quot;)
		local sbad = StopRota and &quot;|cffff4444STOPPED|r&quot; or &quot;|cff44ff44RUNNING|r&quot;
		PQR_StatusOverlayLine1:SetText(&quot;Rotation: &quot;..sbad)
		local aoeStr = &quot;&quot;
		if AoE ~= nil then
			aoeStr = (AoE == true) and &quot;|cff44ff44Manual AoE ON|r&quot; or &quot;|cffff8888Manual AoE OFF|r&quot;
		elseif type(AOE) == &quot;function&quot; then
			aoeStr = AOE() and &quot;|cff44ff44AoE ON|r&quot; or &quot;|cffff8888AoE OFF|r&quot;
		else
			aoeStr = &quot;|cffaaaaaaAoE n/a|r&quot;
		end
		if classToken == &quot;PALADIN&quot; and PQR_CountMeleeEnemiesNearPlayer then
			local pc = PQR_CountMeleeEnemiesNearPlayer()
			if PQR_RetPackAoE == true and pc &gt;= 3 then
				aoeStr = aoeStr..&quot; | |cff44ff44Pack&quot;..pc..&quot; (auto)|r&quot;
			elseif PQR_RetPackAoE == true then
				aoeStr = aoeStr..&quot; | Pack:&quot;..pc
			end
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
		if PQR_StatusOverlay_cbRot then
			PQR_StatusOverlay_cbRot:SetChecked(StopRota ~= true)
		end
		if PQR_StatusOverlay_cbAoE then
			if AoE ~= nil then
				PQR_StatusOverlay_cbAoE:Show()
				PQR_StatusOverlay_cbAoE:SetChecked(AoE == true)
			else
				PQR_StatusOverlay_cbAoE:Hide()
			end
		end
		if PQR_StatusOverlay_cbBuff then
			PQR_StatusOverlay_cbBuff:SetChecked(not not PQR_OverlayBuffEnabled)
			if classToken == &quot;PALADIN&quot; then
				_G[PQR_StatusOverlay_cbBuff:GetName()..&quot;Text&quot;]:SetText(&quot;Sacred Shield (optional)&quot;)
				PQR_StatusOverlay_cbBuff:Show()
			else
				_G[PQR_StatusOverlay_cbBuff:GetName()..&quot;Text&quot;]:SetText(&quot;Extra toggle (profile hook)&quot;)
				PQR_StatusOverlay_cbBuff:Show()
			end
		end
		if PQR_StatusOverlay_cbPack then
			if classToken == &quot;PALADIN&quot; then
				PQR_StatusOverlay_cbPack:Show()
				PQR_StatusOverlay_cbPack:SetChecked(not not PQR_RetPackAoE)
			else
				PQR_StatusOverlay_cbPack:Hide()
			end
		end
		if PQR_StatusOverlay_cbDPlea then
			if classToken == &quot;PALADIN&quot; then
				PQR_StatusOverlay_cbDPlea:Show()
				PQR_StatusOverlay_cbDPlea:SetChecked(not not PQR_RetDivinePleaLowMana)
			else
				PQR_StatusOverlay_cbDPlea:Hide()
			end
		end
	end
end'''


def replace_one(path: Path, force: bool = False) -> bool:
    text = path.read_text(encoding="utf-8")
    pattern = r"if not PQR_StatusOverlayLib then[\s\S]*?\nend\n(?=end</Lua><RecastDelay>)"
    new_text, n = re.subn(pattern, NEW_BLOCK + "\n", text, count=1)
    if n != 1:
        print(f"SKIP pattern {path.name} (matches={n})")
        return False
    path.write_text(new_text, encoding="utf-8")
    print(f"OK {path.name}")
    return True


def main():
    root = Path("/workspace/Profiles")
    for p in sorted(root.glob("*_Abilities.xml")):
        replace_one(p, force=True)


if __name__ == "__main__":
    main()
