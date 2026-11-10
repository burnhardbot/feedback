# [OFFEN] [IDEE] Drei GGP-Seasons mit Themen, Archiv und sicherem Saisonwechsel
**Dokument-/Archivstatus:** [OFFEN]

**Ideengeber:** Leo (`@leoburnhard`)  
**Bereich:** GGP / STREAMEN-Community  
**Stand:** OFFEN – KONZEPT / BESTANDSGRUNDLAGEN VORHANDEN · JAHRES-/WOCHEN-/TOUR-SCOPES VORHANDEN – DREI-SEASONS-LIFECYCLE NICHT · K8-Quelle geprüft, keine Build-/Livefreigabe.

Der GGP könnte über das Jahr verschiedene thematische Seasons erhalten, jeweils mit eigener Gestaltung und Auswertung.

## K8-Statusinventur · 11.11.2026

**Fachstatus:** OFFEN – KONZEPT / BESTANDSGRUNDLAGEN VORHANDEN. **Codeprüfung:** JAHRES-/WOCHEN-/TOUR-SCOPES VORHANDEN – DREI-SEASONS-LIFECYCLE NICHT. **Gesamtidee vollständig implementiert/abgenommen:** NEIN.

**Vorhandener Ist-Code:** K8 hat Jahr-/Wochen-/Tour-/Etappen-Wertungen und Resetgrenzen (z. B. `scoreResetAt`, Tour-Historie). Das ersetzt kein eigenständiges Dreiseason-Modell mit sicheren Grenzen.

**Noch nicht nachgewiesener Funktionsumfang:** Winter/Frühjahr/Sommer als drei automatisch wechselnde Season-Scopes samt Abschluss-Snapshot, spezifischem Archiv, Motto-Publikation und garantierter nicht-destruktiver Saisonwechsel nicht nachgewiesen. Saisonstarts aus Monatsnotizen sind keine bestätigten Kalendertage.

**Abgrenzung/Referenzen:** Bestehende Wertungs- und Results-Engine [#77](https://github.com/burnhardbot/stream/issues/77) behalten; kein automatischer Reset/Löschung. [Private Discussion #68](https://github.com/burnhardbot/stream/discussions/68) · [öffentliche Discussion #9](https://github.com/burnhardbot/feedback/discussions/9). Kein neuer Build, keine neue Ausgabe oder autom. Migration. Original `v1.2.44 TEST-K8`, SHA-256 `746dabacd5e6a1cb8746c557c30901cf43c2b7d3aa81a06d87da77f197160ef4`. **Quellprüfung ≠ Live-/Win10-/OBS-Abnahme.**

---
## Vorschlag
- Winter-/Hauptsaison, Frühlingssaison und Sommersaison mit eigenen Motiven und Aktionen.
- Saisonbezogene Ergebnisse, Trailer und Sonderaktionen.
- Am Saisonende eine nachvollziehbare Archivansicht; frühere Ergebnisse bleiben erhalten.
- Neue Saisonwertungen beginnen in einem klar definierten Zeitraum, ohne historische Daten zu löschen.

## Offene Fragen
Exakte Saisontermine, Kanal- oder Tourbezug, Jahreswechsel, Gleichstände und eventuelle Offseason. Die bisherigen Monatsgrenzen sind nur Ideen.

**Wichtig:** Kein automatischer Datenreset und keine neue konkurrierende Wertungslogik.

---
**Hinweis:** Diese öffentliche Beschreibung enthält bewusst keine privaten Entwicklungsunterlagen oder Google-Drive-Links. Interne Planung findet ausschließlich im privaten Projekt statt. Eine Idee ist keine Zusage zur Umsetzung.
