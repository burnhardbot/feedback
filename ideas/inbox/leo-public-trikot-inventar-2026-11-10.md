# [OFFEN] [IDEE] Trikot-Inventar und Zuschauer-Redeems
**Dokument-/Archivstatus:** [OFFEN]

**Ideengeber:** Leo (`@leoburnhard`)  
**Bereich:** GGP / STREAMEN-Community  
**Stand:** OFFEN – KONZEPT / JAN-PILOT NICHT GESTARTET · OFFEN – EIGENTLICHE INVENTARFUNKTION NICHT IMPLEMENTIERT · K8-Quelle geprüft, keine Build-/Livefreigabe.

Virtuelle Sieger- und Spezialtrikots sollen für Zuschauer als sammelbare und gegebenenfalls einlösbare Gegenstände funktionieren.

## K8-Statusinventur · 11.11.2026

**Fachstatus:** OFFEN – KONZEPT / JAN-PILOT NICHT GESTARTET. **Codeprüfung:** OFFEN – EIGENTLICHE INVENTARFUNKTION NICHT IMPLEMENTIERT. **Gesamtidee vollständig implementiert/abgenommen:** NEIN.

**Was der Code bereits enthält:** K8 hat offizielle Etappensieger-Trikots und Outfit-/Snapshot-Regeln (`minigame/stage-jersey-visuals.js`, `burnhard.js`) sowie Twitch-Kanalpunkte und Redemptions (`minigame/channel-points.js`). Das ist **nicht** das geplante Verbrauchstrikot-Inventar.

**Was gegenüber dem Vorschlag fehlt:** Persönliche Trikotbestände, `!trikots`, `!verleihe`, atomare Trikoteinlösung, Jan-only-Pilot, Mix-It-Up-Owner und Restore/Audit nicht nachgewiesen.

**Abgrenzung/Referenzen:** Klar getrennt von [#33 Wertungstrikots](https://github.com/burnhardbot/stream/issues/33) und [#10 Siegerehrung](https://github.com/burnhardbot/stream/issues/10). [Private Discussion #63](https://github.com/burnhardbot/stream/discussions/63) · [öffentliche Discussion #12](https://github.com/burnhardbot/feedback/discussions/12). Kein eigenständiges neues Implementierungs-Issue oder Bauauftrag aufgrund dieser Dokumentation. Original-ZIP `v1.2.44 TEST-K8`, SHA-256 `746dabacd5e6a1cb8746c557c30901cf43c2b7d3aa81a06d87da77f197160ef4`. **Quellprüfung ≠ vollständige Live-/OBS-/Win10-Abnahme.**

---
## Vorschlag
- Inventar für `polkadot` (Berg), `the green` (Sprint) und `rainbow` (Regenbogen).
- Moderatoren beziehungsweise Streamer können Trikots vergeben; Zuschauer können ihren Bestand etwa mit `!trikots` abrufen.
- Einlösung für besondere Stream-Effekte, mit verständlichen Berechtigungen, Cooldowns und Limits.
- Leo prüft zunächst eine Umsetzung mit Mix It Up; ein zusätzlicher Server-Pilot für Jan wäre getrennt zu bewerten.

## Offene Fragen
Wie lauten die finalen Befehle? Welche Wirkung hat jede Einlösung? Wer verwaltet den maßgeblichen Inventarbestand? Wie werden Fehler und doppelte Einlösungen verhindert?

**Wichtig:** Gemeint ist ein einlösbares Zuschauerinventar, nicht ein automatischer Outfitwechsel mitten in einer Etappe. Noch keine Aktivierung beschlossen.

---
**Hinweis:** Diese öffentliche Beschreibung enthält bewusst keine privaten Entwicklungsunterlagen oder Google-Drive-Links. Interne Planung findet ausschließlich im privaten Projekt statt. Eine Idee ist keine Zusage zur Umsetzung.
