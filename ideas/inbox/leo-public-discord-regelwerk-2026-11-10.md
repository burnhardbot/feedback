# [OFFEN] [IDEE] Discord-Benachrichtigungen und verständliches GGP-Regelwerk
**Dokument-/Archivstatus:** [OFFEN]

**Ideengeber:** Leo (`@leoburnhard`)  
**Bereich:** GGP / STREAMEN-Community  
**Stand:** OFFEN – KONZEPT · OFFEN – FUNKTION NICHT IMPLEMENTIERT · K8-Quelle geprüft, keine Build-/Livefreigabe.

GGP-Ereignisse sollen nachvollziehbar in Discord angekündigt werden. Gleichzeitig soll eine verständliche Spielanleitung für neue und erfahrene Teilnehmer entstehen.

## K8-Statusinventur · 11.11.2026

**Fachstatus:** OFFEN – KONZEPT. **Codeprüfung:** OFFEN – FUNKTION NICHT IMPLEMENTIERT. **Gesamtidee vollständig implementiert/abgenommen:** NEIN.

**Was der Code bereits enthält:** K8 bietet bereits Result- und Ranking-APIs; `telemetry/server.js` hat einen Discord↔Tourfunk-**Audio-/Voice-Bridge**-Statusadapter. Dieser Adapter ist **kein** Discord-Ergebnisbot oder Regelwerk-Publisher.

**Was gegenüber dem Vorschlag fehlt:** Automatische bestätigte Gewinner-/Trikot-/Einlösungsnachrichten nach Discord und Regelwerk in drei Längen sind nicht nachgewiesen. Vorhandene Spielregeln/Results wiederverwenden, keine zweite Wertungsquelle.

**Abgrenzung/Referenzen:** Bestehendes Results-Issue [#77](https://github.com/burnhardbot/stream/issues/77) nur als Daten-/Darstellungsabhängigkeit. [Öffentliche Discussion #3](https://github.com/burnhardbot/feedback/discussions/3). Keine neue Ausgabe, Installation oder Daten-/Score-Migration durch diese Dokumentation. Prüfung anhand des unveränderten Originalpakets `v1.2.44 TEST-K8`, SHA-256 `746dabacd5e6a1cb8746c557c30901cf43c2b7d3aa81a06d87da77f197160ef4`. **Quellprüfung ≠ vollständige Live-/OBS-/Win10-Abnahme.**

---
## Vorschlag
- Discord-Meldungen bei bestätigten Trikotverleihungen, Einlösungen und Tour-/Etappensiegen.
- Regelwerk in drei Fassungen: kurz für den Einstieg, mittel für Kommandos und Einlösungen, ausführlich für Website und Discord.
- Klar erläutern: Beitreten, Wertungen, Saisonregeln, Sonderbefehle, Preise und Inventar.

## Offene Fragen
Welche Ereignisse sind tatsächlich relevant? Wie verhindert man Spam oder doppelte Meldungen? Welche Texte müssen vor einer Veröffentlichung freigegeben werden?

**Wichtig:** Keine geheimen Webhooks, Tokens oder internen Berechtigungsdetails veröffentlichen.

---
**Hinweis:** Diese öffentliche Beschreibung enthält bewusst keine privaten Entwicklungsunterlagen oder Google-Drive-Links. Interne Planung findet ausschließlich im privaten Projekt statt. Eine Idee ist keine Zusage zur Umsetzung.
