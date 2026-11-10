# [OFFEN] [IDEE] Twitch-/Zwift-Mitfahrer und Bonuspunkte für gemeinsame Fahrten
**Dokument-/Archivstatus:** [OFFEN]

**Ideengeber:** Leo (`@leoburnhard`)  
**Bereich:** GGP / STREAMEN-Community  
**Stand:** TEILWEISE UMGESETZT – REST OFFEN · TEILWEISE CODE VORHANDEN – GROUP-RIDE-BONUS FEHLT · K8-Quelle geprüft, keine Build-/Livefreigabe.

Die Teilnahme an gemeinsamen GGP- beziehungsweise Mixed-Pickles-Fahrten könnte besser sichtbar und optional belohnt werden.

## K8-Statusinventur · 11.11.2026

**Fachstatus:** TEILWEISE UMGESETZT – REST OFFEN. **Codeprüfung:** TEILWEISE CODE VORHANDEN – GROUP-RIDE-BONUS FEHLT. **Gesamtidee vollständig implementiert/abgenommen:** NEIN.

**Was der Code bereits enthält:** Die Panorama- und Fahrerprojektion führt Chat, sichtbare Watt-Friends und registrierte Streamer zusammen (`minigame/panorama/live.js`, insbesondere `wattsFriends`, `liveStreamers`, Identity Merge). Zwift-/Watt-Quellen bestehen.

**Was gegenüber dem Vorschlag fehlt:** Ein bestätigter GGP-Punktebonus allein für tatsächliches Mixed-Pickles-Group-Ride-Mitfahren ist nicht belegt. `minigame/burnhard.js` blockiert bestimmte Legacy-Telemetrie-Buchungen; keine ungeprüfte Zwift-Strecke als GGP-Punkt buchen. Echte aktive Fahrerpräsenz und Bonus-Scoring getrennt behandeln.

**Abgrenzung/Referenzen:** Vorhandene Friends-/Watt-/Group-Ride-Daten verwenden; automatischer realer Peloton-Besatz im [#79](https://github.com/burnhardbot/stream/issues/79) beschrieben. [Private Discussion #64](https://github.com/burnhardbot/stream/discussions/64) · [öffentliche Discussion #6](https://github.com/burnhardbot/feedback/discussions/6). Kein eigenständiges neues Implementierungs-Issue oder Bauauftrag aufgrund dieser Dokumentation. Original-ZIP `v1.2.44 TEST-K8`, SHA-256 `746dabacd5e6a1cb8746c557c30901cf43c2b7d3aa81a06d87da77f197160ef4`. **Quellprüfung ≠ vollständige Live-/OBS-/Win10-Abnahme.**

---
## Vorschlag
- Streamer mit bestätigtem Live-Status können als Teilnehmer dargestellt werden.
- Weitere Zwift-Fahrer erscheinen, sofern ihre Zuordnung und tatsächliche Teilnahme gesichert sind.
- Für nachweisliches Mitfahren bei Group Rides könnte es einen gesondert definierten Bonus geben.

## Offene Fragen
Ab wann zählt jemand als aktiv? Wie werden verschiedene Identitäten zuverlässig zugeordnet? Was geschieht bei Datenpausen? Wie verhindert man doppelte Punkte?

**Wichtig:** Keine erfundenen Fahrer, Kilometer oder Wertungsereignisse. Bonusregeln und Gewichtungen sind noch offen.

---
**Hinweis:** Diese öffentliche Beschreibung enthält bewusst keine privaten Entwicklungsunterlagen oder Google-Drive-Links. Interne Planung findet ausschließlich im privaten Projekt statt. Eine Idee ist keine Zusage zur Umsetzung.
