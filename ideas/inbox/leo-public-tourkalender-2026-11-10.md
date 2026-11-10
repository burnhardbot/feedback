# [OFFEN] [IDEE] GGP-Tourkalender und parallele kanalübergreifende Touren
**Dokument-/Archivstatus:** [OFFEN]

**Ideengeber:** Leo (`@leoburnhard`)  
**Bereich:** GGP / STREAMEN-Community  
**Stand:** **IN UMSETZUNG – PLANUNG AKTIV (10.11.2026)**. Eine fachliche Entscheidung ist verbindlich dokumentiert; Build, Produktfunktion und Liveabnahme sind dadurch noch nicht bestätigt.

Ein gemeinsamer GGP-Tourkalender könnte unterschiedliche Tourtypen, einzelne Etappen und saisonale Aktionen verständlich darstellen.

## Verbindliche Entscheidung B (10.11.2026)

**Eine GGP-Etappe darf mehreren Touren gleichzeitig zugeordnet werden. Jede Tour bekommt ihre eigene Wertung.** Ein offiziell bestätigtes Etappenergebnis wird dafür nicht doppelt erzeugt; stattdessen kann es je zugeordneter Tour genau einmal zu deren getrennter Wertung beitragen. Eine globale Mehrfachbuchung von km, Punkten oder Siegen ist nicht vorgesehen. Es werden keine zweiten, konkurrierenden Ergebnisdaten erzeugt.

## Verbindliche Entscheidung C (10.11.2026)

**Tour-Zuordnungen dürfen auch nach Etappenende rückwirkend korrigiert werden.** Berechtigte Verwaltungspersonen können eine bereits abgeschlossene Etappe einer weiteren Tour zuordnen oder eine alte Zuordnung entfernen. **Jede Änderung erhält ein nachvollziehbares Änderungsprotokoll und die betroffenen Tourwertungen werden neu berechnet.** Ursprüngliche offizielle Etappenergebnisse bleiben erhalten; keine doppelten globalen Punkte, Kilometer oder Siege. Das Archiv soll Änderungen sichtbar und nachvollziehbar halten.

**In Umsetzung heißt hier weiterhin: technische Planung aktiv; nicht gebaut, installiert oder live abgenommen.** Es wurden keine laufenden Tourwertungen geändert.

**Entschieden:** Touren und ihre offiziellen Fahrer-Ranglisten sind für alle Streamer gemeinsam; Etappen verschiedener Streamer gehören zur selben Tourwertung. **Noch offen:** gegebenenfalls unterschiedliche Tour-Wertungsregeln und Bearbeitungsrechte.

## Verbindliche Entscheidung: Touren sind für alle Streamer gleich (10.11.2026)

**Ein gemeinsamer GGP-Tourkalender und dieselben Touren für alle teilnehmenden Streamer.** Es gibt keine separate Jan-, Leo- oder Gast-Kopie derselben Tour. Etappen verschiedener Streamer können einer gemeinsamen Tour angehören, behalten aber ihre jeweilige veranstaltende Herkunft. Die zuvor beschlossenen Mehrfachzuordnungen (B) und rückwirkenden Korrekturen mit Protokoll und Neuberechnung (C) gelten weiterhin.

**Entschieden A (11.11.2026):** Eine gemeinsame kanalübergreifende Fahrer-Rangliste je Tour; keine eigenen Ranglisten pro Streamer. Nächste Frage: gleiche Wertungsregeln oder tourindividuelle Gewichtung? Weitere Detailregeln und Berechtigungen werden intern entschieden. Kein fertig getesteter Build.

## Bereits vorhandener technischer Kern – nachgeprüft (11.11.2026)

Die zentrale Tourverwaltung und **eine gemeinsame Tour-Rangliste für alle Streamer** sind im aktuell geprüften K8-Quellcode **bereits grundsätzlich vorhanden**. Es muss dafür keine zweite Tour-Wertung gebaut werden. Aktuell werden Beiträge zeitbasiert allen gleichzeitig aktiven Touren zugeordnet.

Die verbleibende geplante Erweiterung ist vor allem die **bewusst auswählbare Zuordnung einer bestimmten Etappe zu bestimmten Touren** sowie eine **rückwirkende Korrektur mit Änderungsprotokoll und Neuberechnung**. Quellcodeprüfung ersetzt keine bestandene Live-/Win10-Abnahme. **Status: bestehende Grundlagen implementiert, verbleibende Änderungen IN UMSETZUNG – PLANUNG AKTIV.**

## Verbindliche Entscheidung A – eine gemeinsame Tourwertung (11.11.2026)

**Alle Streamer verwenden eine einzige gemeinsame Fahrer-Rangliste für jede GGP-Tour.** Bestätigte Fahrerbeiträge aus den zugehörigen Jan-, Leo- und weiteren Streamer-Etappen erscheinen im selben Tour-Ranking; es gibt **keine getrennten Jan-/Leo-Tabellen für dieselbe Tour**. Eine verifiziert identische Person erscheint dabei nur einmal, auch wenn sie bei verschiedenen Streamern teilnimmt. Unbestätigt gleichlautende Nutzernamen werden nicht automatisch zusammengelegt.

Die vorigen Beschlüsse bleiben gültig: **B** – eine Etappe darf für mehrere Touren zählen; **C** – auch nach Etappenende darf die Tourzuordnung mit Änderungsprotokoll und Neuberechnung der betroffenen Tourwertungen korrigiert werden; **gemeinsamer Tourkatalog** für alle Streamer. Etappenresultate werden nicht mehrfach erzeugt und globale Punkte/km nicht doppelt gebucht.

**Keine erneute Fachfrage zu Tour-Gewichtungen:** Der Server hat bereits einheitliche Wertungskategorien; diese bleiben bestehen. Die gezielte Etappenzuordnung samt rückwirkender Korrektur ist in Planung. **Status: IN UMSETZUNG – PLANUNG AKTIV**, ohne Build/Live-Abnahme.

## Bestehende Regeln im Server verifiziert (11.11.2026)

Die gemeinsamen GGP-Touren, kanalübergreifenden Fahrer-Ranglisten und zeitgleich aktiven Touren sind **bereits im aktuellen K8-Quellcode vorhanden**. Die bestehenden Wertungskategorien gelten für alle Touren einheitlich: Kilometer als Hauptwertung, vorhandene Sprint-/Bergpunkte und Etappensiege. **Keine neuen Tour-Gewichtungen oder separaten Streamer-Ranglisten erforderlich.** Der Server besitzt außerdem bereits einen geschützten historischen Rückrechnungsmechanismus für die nachträgliche Anlage einer gesamten Tour.

Noch zu ergänzen ist die **gezielte Auswahl, welche Etappe zu welcher Tour gehört**, einschließlich autorisierter Korrektur nach Etappenende mit Änderungsprotokoll und Aktualisierung der betroffenen Tourwertungen. Vorhandene Regeln und Resultate bleiben erhalten; kein neuer Produkt-Build, Live-Test oder Datenwechsel durch diesen Beschluss.

## Ursprünglicher Vorschlag
- Tourtypen wie Klassiker, Streamer-Events, IRL-Fahrten oder Zwift-Touren.
- Kanalübergreifende Touren mit jeweils klar zugeordneten Etappen.
- Ein Ablauf vom Entwurf über die Prüfung bis zur Veröffentlichung.
- Zu jeder Tour optionale Informationen zu Teilnahme, Geschichte, Medien und Preisen.
- Kalenderansicht für aktive und geplante Touren, einschließlich bewusster Pausen.

## Offene Fragen
**Entschieden B + C:** Parallel laufende Touren und Mehrfachzuordnung sind erlaubt; Zuordnungen dürfen rückwirkend mit Audit und Tourwertungs-Neuberechnung berichtigt werden. **Weiter offen:** tourindividuelle Wertungsregeln, Absagen und Terminänderungen.

**Wichtig:** Vorgeschlagene Termine gelten erst nach gesonderter Bestätigung.

---
**Hinweis:** Diese öffentliche Beschreibung enthält bewusst keine privaten Entwicklungsunterlagen oder Google-Drive-Links. Interne Planung findet ausschließlich im privaten Projekt statt. Eine Idee ist keine Zusage zur Umsetzung.
