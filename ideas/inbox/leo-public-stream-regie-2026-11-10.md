# [OFFEN] [IDEE] Zukunftsidee: GGP-Regie mit kontrollierten Streamerwechseln
**Dokument-/Archivstatus:** [OFFEN]

**Ideengeber:** Leo (`@leoburnhard`)  
**Bereich:** GGP / STREAMEN-Community  
**Stand:** ZUKUNFT – GEPLANT, NICHT IN UMSETZUNG · ZUKUNFT – TEILFUNKTIONEN VORHANDEN, EIGENER BOT-STREAM NICHT · K8-Quelle geprüft, keine Build-/Livefreigabe.

Langfristige Idee: Eine GGP-Regie könnte zwischen bereits verfügbaren Streameransichten wechseln und Zuschauern eine abwechslungsreiche gemeinsame Übertragung bieten.

## K8-Statusinventur · 11.11.2026

**Fachstatus:** ZUKUNFT – GEPLANT, NICHT IN UMSETZUNG. **Codeprüfung:** ZUKUNFT – TEILFUNKTIONEN VORHANDEN, EIGENER BOT-STREAM NICHT. **Gesamtidee vollständig implementiert/abgenommen:** NEIN.

**Was der Code bereits enthält:** In K8 ist bereits ein OBS-/Szenen-Director (`telemetry/obs-director.js`: Szenen NORMAL, BURNHARD, PELOTON, BERG, EVENT, RACE; Kandidatenauswahl und Szenenwechsel) vorhanden. Das ist keine Bestätigung eines eigenständigen burnhard_bot-Livestreams.

**Was gegenüber dem Vorschlag fehlt:** Separater Bot-Stream, sichere Jan/Leo-Regieumschaltung, eigene Ausspielrechte und Abnahme sind nicht belegt. Bestehenden Director nicht erneut bauen oder automatisch aktivieren.

**Abgrenzung/Referenzen:** Vorhandene OBS-/Regie-Owner berücksichtigen, kein zusätzlicher Issue- oder Bauauftrag. [Öffentliche Discussion #10](https://github.com/burnhardbot/feedback/discussions/10). Keine neue Ausgabe, Installation oder Daten-/Score-Migration durch diese Dokumentation. Prüfung anhand des unveränderten Originalpakets `v1.2.44 TEST-K8`, SHA-256 `746dabacd5e6a1cb8746c557c30901cf43c2b7d3aa81a06d87da77f197160ef4`. **Quellprüfung ≠ vollständige Live-/OBS-/Win10-Abnahme.**

---
## Vorschlag
- Wechsel zwischen freigegebenen Jan-/Leo-Ansichten oder einem separat geplanten Regie-Stream.
- Manuelle Steuerung und jederzeitige Rückkehr zu einer sicheren Standardansicht.
- Gut sichtbare Anzeige, welcher Stream beziehungsweise welche Kamera gerade live ist.

## Offene Fragen
Welche Szenen sind verfügbar und dürfen verwendet werden? Wer übernimmt die Regie? Ist ein eigenständiger Bot-Stream sinnvoll?

**Status:** Unverbindliche Zukunftsidee. Keine automatische OBS-, Twitch- oder Livesteuerung wird hiermit freigegeben.

---
**Hinweis:** Diese öffentliche Beschreibung enthält bewusst keine privaten Entwicklungsunterlagen oder Google-Drive-Links. Interne Planung findet ausschließlich im privaten Projekt statt. Eine Idee ist keine Zusage zur Umsetzung.
