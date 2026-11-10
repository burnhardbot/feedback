# [OFFEN] [IDEE] Interaktive GGP-Events: Raid-Gruppen, Subs, Streaks und Rollen-Skins
**Dokument-/Archivstatus:** [OFFEN]

**Ideengeber:** Leo (`@leoburnhard`)  
**Bereich:** GGP / STREAMEN-Community  
**Stand:** TEILWEISE UMGESETZT – VISUELLE IDEEN OFFEN · TWITCH-/RAID-QUELLEN VORHANDEN – GEWÜNSCHTE EVENTS VISUELL UNVOLLSTÄNDIG · K8-Quelle geprüft, keine Build-/Livefreigabe.

Besondere Twitch-Ereignisse könnten in der GGP-Rennszene sichtbar werden.

## K8-Statusinventur · 11.11.2026

**Fachstatus:** TEILWEISE UMGESETZT – VISUELLE IDEEN OFFEN. **Codeprüfung:** TWITCH-/RAID-QUELLEN VORHANDEN – GEWÜNSCHTE EVENTS VISUELL UNVOLLSTÄNDIG. **Gesamtidee vollständig implementiert/abgenommen:** NEIN.

**Vorhandener Ist-Code:** K8 verarbeitet Twitch-Raid-Events (unter anderem `channel.raid`/Gruppenevent in `minigame/burnhard.js`) und hat Rollen-/Badge-Projektion im Panorama. Das belegt Eventbasis, nicht die vollständigen geplanten Render-Effekte.

**Noch nicht nachgewiesener Funktionsumfang:** Große sichtbare Raid-Animation, Streak-Flammenspur, Sub- und VIP-/Mod-Skins sind als komplette, OBS-abgenommene Funktion nicht verifiziert. WICHTIG: Nutzerbeschluss gegen zufällige/erfundene Füllfahrer gilt auch hier: Raid-Meldungen erzeugen keine willkürlichen mitwertenden oder als echte Fahrer getarnten Avatare.

**Abgrenzung/Referenzen:** Rollenbadges [#79](https://github.com/burnhardbot/stream/issues/79), Sprite-/Animationsowner [#18](https://github.com/burnhardbot/stream/issues/18) und Panorama [#53](https://github.com/burnhardbot/stream/issues/53); keine doppelten Teilnehmer. [Private Discussion #70](https://github.com/burnhardbot/stream/discussions/70) · [öffentliche Discussion #13](https://github.com/burnhardbot/feedback/discussions/13). Kein neuer Build, keine neue Ausgabe oder autom. Migration. Original `v1.2.44 TEST-K8`, SHA-256 `746dabacd5e6a1cb8746c557c30901cf43c2b7d3aa81a06d87da77f197160ef4`. **Quellprüfung ≠ Live-/Win10-/OBS-Abnahme.**

---
## Vorschlag
- Bei einem Raid erscheinen dekorative Begleitfiguren.
- Sub- oder Streak-Ereignisse lösen passende, kurzzeitige Effekte aus.
- Moderatoren oder VIPs können klar erkennbare Spezial-Looks bekommen.
- Zuschauer und Emotes erhalten passende visuelle Auftritte am Straßenrand.

## Offene Fragen
Welche Events sollen welche Effekte auslösen? Wie werden Mehrfachmeldungen, Cooldowns und Grafikperformance behandelt? Welche Rollenfarben und Designs passen?

**Wichtig:** Dekorative Figuren sind keine realen Rennteilnehmer; ihre Anzahl beeinflusst keine Spielwertung.

---
**Hinweis:** Diese öffentliche Beschreibung enthält bewusst keine privaten Entwicklungsunterlagen oder Google-Drive-Links. Interne Planung findet ausschließlich im privaten Projekt statt. Eine Idee ist keine Zusage zur Umsetzung.
