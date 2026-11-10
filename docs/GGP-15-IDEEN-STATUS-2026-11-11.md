# [OFFEN] GGP – Prüfbares Statusregister für alle 15 Leo-Ideen (11.11.2026)
**Dokument-/Archivstatus:** [OFFEN] – Register aktiv, einzelne Ideen haben eigenen Status.

**Prüfstand:** 11.11.2026 · Unverändertes, SHA-verifiziertes Original `Streamen-Server-Win10-v1.2.44-TEST-K8.zip` (SHA-256 `746dabacd5e6a1cb8746c557c30901cf43c2b7d3aa81a06d87da77f197160ef4`). **Quellprüfung ist keine browser-/OBS-/Win10-/Live-Abnahme.** Keine Server-/Installer-/Scoreänderung. Bestehende Funktionen nicht noch einmal entwickeln.

**Ergebnis:** **1 archiviert/verworfen · 2 in Umsetzung (Planung aktiv) · 3 teilweise vorhanden mit offenen Restpunkten · 7 offene Konzepte · 2 Zukunft/Parkplatz = 15 Ideen.** **0** Ideen als Gesamtfunktion vollständig implementiert **und** abgenommen. Keine offenen/teilweise umgesetzten Ideen allein auf Basis eines Codebausteins schließen.

| # | Idee | Sachstatus | Nachgewiesener Code-Bestand | Noch offen / zuständiger Owner |
|---:|---|---|---|---|
| [1](https://github.com/burnhardbot/feedback/discussions/1) | Adventskalender | **OFFEN · Konzept** | Tour-/Ranking-Basis vorhanden; keine Türchen-/Gewinnengine | Freigaben, Ziehung, Gewinn-/Einlöse-Audit |
| [2](https://github.com/burnhardbot/feedback/discussions/2) | Zufällige Ambient-Lurker | **ARCHIVIERT · VERWORFEN** | Echtes `!lurk` existiert separat | 5–8 zufällige Füllfiguren ausdrücklich NICHT bauen |
| [3](https://github.com/burnhardbot/feedback/discussions/3) | Discord-Nachrichten & Regelwerk | **OFFEN · Konzept** | Results/API vorhanden; Discord-Tourfunk = Voice, nicht Ergebnisbot | Ergebnisbenachrichtigung, Einlösung, Regelwerk 3 Längen |
| [4](https://github.com/burnhardbot/feedback/discussions/4) | Handelbare Community-Ökonomie | **ZUKUNFT · Parken** | Scores/Kanalpunkte vorhanden, keine Handel-/Inventarengine | Shop, Trades, Autorität, Transaktionsjournal |
| [5](https://github.com/burnhardbot/feedback/discussions/5) | GGP Medien-/Brandingpaket | **OFFEN · Medienprojekt** | Styles/Assets/Design-Prompts vorhanden | Vollständiges freigegebenes Paket/Trailer/Emotes nicht verifiziert |
| [6](https://github.com/burnhardbot/feedback/discussions/6) | Twitch-/Zwift-Mitfahrer & Bonuspunkte | **TEILWEISE · Rest offen** | Watt-Friends/Streamer-ID/Visualisierung vorhanden | Mixed-Pickles-Group-Ride-Bonus nicht belegt |
| [7](https://github.com/burnhardbot/feedback/discussions/7) | Overlay: Timer, Join, Straße | **TEILWEISE · UX-/OBS-Check** | Overlay, Countdown, Phasen, Panorama vorhanden | Timer/Join/Geometrie bei Ereignislast visuell nicht abgenommen |
| [8](https://github.com/burnhardbot/feedback/discussions/8) | Tourpreise, Wunsch-Tickets, Challenges | **OFFEN · Konzept** | Ergebnis-/Wertungskategorien vorhanden | Konfigurierbarer Preis-/Challenge-Katalog und Einlösungen fehlen |
| [9](https://github.com/burnhardbot/feedback/discussions/9) | 3 Seasons, Archiv und Reset | **OFFEN · Konzept** | Jahr/Woche/Tour/Stage-/Reset-Scopes vorhanden | Drei-Saisons-Lifecycle und Archivabschluss nicht belegt |
| [10](https://github.com/burnhardbot/feedback/discussions/10) | Eigenständiger burnhard_bot-Streamdirector | **ZUKUNFT · Parken** | OBS-Szenen-Director vorhanden | Eigenständiger Bot-Stream/Jan–Leo-Auto-Regie nicht belegt |
| [11](https://github.com/burnhardbot/feedback/discussions/11) | Tourkalender & Etappen-Zuordnung | **IN UMSETZUNG · Planung aktiv** | Globaler Kalender, gemeinsame Tour-Rangliste, Parallel-Touren, Backfill vorhanden | Stage↔Tour-Auswahl, rückwirkende Stage-Korrektur/Audit; internes Umsetzungsticket |
| [12](https://github.com/burnhardbot/feedback/discussions/12) | Verbrauchbares Trikot-Inventar | **OFFEN · Jan-Pilot-Konzept** | Wertungstrikots/Kanalpunkte existieren, aber sind NICHT Inventar | `!trikots`/`!verleihe`, Bestände, Verbrauch/Einlösung fehlen |
| [13](https://github.com/burnhardbot/feedback/discussions/13) | Raids, Subs, Rollen-Streak-Effekte | **TEILWEISE · Rest offen** | Raid-Ereignis/Role-Badges vorhanden | Vollständige Grafiken/Animationen nicht abgenommen; keine Zufallsfahrer |
| [14](https://github.com/burnhardbot/feedback/discussions/14) | Vortagssieger im Peloton | **IN UMSETZUNG · Planung aktiv** | Sieger-Badges/Stage-Snapshots vorhanden | Wiedereinblendung nach Sprint, langsames Zurückfallen; internes Umsetzungsticket |
| [15](https://github.com/burnhardbot/feedback/discussions/15) | Winter-Specials & Kanalpunkte | **OFFEN · Konzept** | Kanalpunkt-/Effektbasis vorhanden | `!snowman`, `!snowball`, Superrakete nicht belegt |

## Status- und Archivregeln

- **ARCHIVIERT / VERWORFEN** nur nach ausdrücklichem Nutzerbeschluss. Für die 5–8 Zufalls-Lurker ist die historische Vollfassung unter `ideas/archive/` gesichert; der alte Inboxpfad bleibt ausschließlich als Weiterleitung erhalten, damit GitHub-Links nicht brechen. Die echte `!lurk`-Funktion bleibt unberührt.
- **IN UMSETZUNG – PLANUNG AKTIV** bedeutet bestehendes Umsetzungsticket, bestätigte Fachziele, aber noch **keine** Fertigstellung oder Livefreigabe. Tourkalender und Vortagssieger haben interne Umsetzungstickets.
- **TEILWEISE** bedeutet nachgewiesene Teilfunktionen im Originalcode. Vor einem Build nur die noch fehlende Funktion und ihre Tests planen; keine zweite Engine oder parallelen Wertungsspeicher bauen.
- **OFFEN** und **ZUKUNFT** bleiben Ideen/Planungen, **nicht automatisch** Bauaufträge oder umzusetzende Issues.
- **VORHANDEN** ist nur eine Bezeichnung für konkrete, überprüfte Codebausteine, **nicht** für eine komplett funktionierende Produktidee. Erst nach passender Source-/Browser-/OBS-/Win10-/Live-Abnahme gegebenenfalls als umgesetzt schließen.
- Neue Fragen sind nur erlaubt, wenn aktueller Originalcode, bestehende Beschlüsse und dokumentierte Regeln keine eindeutige Antwort liefern. Keine wiederholten Grundsatzfragen über gemeinsame Touren, Ranking, feste Kategorie-Punkte, vorhandene Backfill-/Adminmechanik.

## Nachweise / Abgrenzungen

Das K8-Paket enthält bereits gemeinsame Tour-/Ranking-/Overlay-/Twitch-Bausteine; interne Quellpfade und Zugangsinformationen bleiben ausschließlich im privaten Projekt. Etappenergebnisse behalten ihre Herkunft; Tourwertungen sind gemeinsam. Das aktuelle Datumsschema bucht bei allen aktiven Touren; die einzelne Stage↔Tour-Zuordnung mit rückwirkendem Audit ist ein eigener, bereits entschiedener Restpunkt.

**Änderungsdisziplin:** Nur Dokumentation / vorhandene GitHub-Discussions / abgeschlossene Ideen archivieren. Keine Produktivdateien, keine API-Tokens, keine Installation. Bei späterem Build Differenz aus dem dann aktuellen Source-SHA erneut prüfen.

**Öffentlicher Ideenpool:** [Ideas](https://github.com/burnhardbot/feedback/discussions/categories/ideas). Technische Detailtickets und interne Quellen werden nicht öffentlich dupliziert.
