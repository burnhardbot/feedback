# [OFFEN] [IDEE] Season-Specials: !snowman, !snowball und Superrakete
**Dokument-/Archivstatus:** [OFFEN]

**Ideengeber:** Leo (`@leoburnhard`)  
**Bereich:** GGP / STREAMEN-Community  
**Stand:** OFFEN – KONZEPT / PLATTFORM VORHANDEN · KANNALPUNKTE-BASIS VORHANDEN – WINTER-COMMANDS FEHLEN · K8-Quelle geprüft, keine Build-/Livefreigabe.

Winter- und Saisonaktionen sollen den GGP mit zeitlich begrenzten Chatbefehlen und Spezialeffekten abwechslungsreicher machen.

## K8-Statusinventur · 11.11.2026

**Fachstatus:** OFFEN – KONZEPT / PLATTFORM VORHANDEN. **Codeprüfung:** KANNALPUNKTE-BASIS VORHANDEN – WINTER-COMMANDS FEHLEN. **Gesamtidee vollständig implementiert/abgenommen:** NEIN.

**Vorhandener Ist-Code:** K8 hat Twitch-Kanalpunkte, Redemptions, Effekt- und Event-Pipelines (`minigame/channel-points.js` und zugehörige Routen).

**Noch nicht nachgewiesener Funktionsumfang:** Spezielle `!snowman`-, `!snowball`- und Superraketen-Effekte sind in den geprüften aktiven Game-/Panorama-Pfaden nicht als vollständiges Feature nachgewiesen. 1000 Kanalpunkte ist ein historischer Vorschlagswert, keine freigegebene Einstellung.

**Abgrenzung/Referenzen:** Vorhandene Kanalpunkt-/Panorama-Engine und [#53](https://github.com/burnhardbot/stream/issues/53) statt eigener Event-Engine verwenden. [Private Discussion #71](https://github.com/burnhardbot/stream/discussions/71) · [öffentliche Discussion #15](https://github.com/burnhardbot/feedback/discussions/15). Kein neuer Build, keine neue Ausgabe oder autom. Migration. Original `v1.2.44 TEST-K8`, SHA-256 `746dabacd5e6a1cb8746c557c30901cf43c2b7d3aa81a06d87da77f197160ef4`. **Quellprüfung ≠ Live-/Win10-/OBS-Abnahme.**

---
## Vorschlag
- Saisonbefehle wie `!snowman` oder `!snowball`.
- Alternativ oder zusätzlich Einlösungen über Twitch-Kanalpunkte.
- Eine besondere „Superrakete“ als Community-Effekt; eine mögliche Punktzahl ist noch nicht beschlossen.
- Thematische Grafiken, Power-ups und kleine Überraschungen.

## Offene Fragen
Welche Effekte sind nur kosmetisch? Welche beeinflussen gegebenenfalls das Rennen? Wie funktionieren Cooldowns, Rückerstattungen und Fairness?

**Wichtig:** Noch kein verbindliches Balancing und keine Aktivierung von Chatbefehlen.

---
**Hinweis:** Diese öffentliche Beschreibung enthält bewusst keine privaten Entwicklungsunterlagen oder Google-Drive-Links. Interne Planung findet ausschließlich im privaten Projekt statt. Eine Idee ist keine Zusage zur Umsetzung.
