# [OFFEN] [IDEE] Interaktiver GGP-Adventskalender mit Preisen, Türchen und Wintergrafiken
**Dokument-/Archivstatus:** [OFFEN]

**Ideengeber:** Leo (`@leoburnhard`)  
**Bereich:** GGP / STREAMEN-Community  
**Stand:** OFFEN – KONZEPT · OFFEN – NEUE FUNKTION NICHT IMPLEMENTIERT · K8-Quelle geprüft, keine Build-/Livefreigabe.

Ein Adventskalender als eigene GGP-Winteraktion mit täglich freischaltbaren Türchen, passenden Wintergrafiken, Gewinnerdarstellung und transparenten Teilnahmebedingungen.

## K8-Statusinventur · 11.11.2026

**Fachstatus:** OFFEN – KONZEPT. **Codeprüfung:** OFFEN – NEUE FUNKTION NICHT IMPLEMENTIERT. **Gesamtidee vollständig implementiert/abgenommen:** NEIN.

**Was der Code bereits enthält:** Vorhanden sind Tourkalender, Wertungs- und Eventdaten als mögliche Grundlage. Im geprüften K8-Code kein eigenständiges GGP-Adventstürchen-/Gewinn-/Freigabesystem nachgewiesen.

**Was gegenüber dem Vorschlag fehlt:** Türchen, Tagesfreigabe, Gewinnrechte, Ziehung/Einlösung, Kalender-/OBS-Ansicht und Audit sind ein neues Feature, nicht Teil der bestehenden Tourverwaltung.

**Abgrenzung/Referenzen:** Keine eigenständige Implementierungs-Issue-Zusage; Tourkalender [#88](https://github.com/burnhardbot/stream/issues/88) nur als Abhängigkeit. [Öffentliche Discussion #1](https://github.com/burnhardbot/feedback/discussions/1). Keine neue Ausgabe, Installation oder Daten-/Score-Migration durch diese Dokumentation. Prüfung anhand des unveränderten Originalpakets `v1.2.44 TEST-K8`, SHA-256 `746dabacd5e6a1cb8746c557c30901cf43c2b7d3aa81a06d87da77f197160ef4`. **Quellprüfung ≠ vollständige Live-/OBS-/Win10-Abnahme.**

---
## Vorschlag
- Tagesaktionen beziehungsweise Türchen sichtbar im Stream freischalten.
- Preise und Teilnahmebedingungen vorab festlegen; Gewinne nachvollziehbar zuordnen.
- Kalender, Gewinner und vergangene Türchen in einer Übersicht darstellen.

## Offene Fragen
Wie lang soll die Aktion dauern? Wer darf teilnehmen? Wie gehen wir mit Mehrfachgewinnen, verpassten Tagen und eventuellen Auslosungen um? Termine und Gewinnmechanik sind noch nicht beschlossen.

---
**Hinweis:** Diese öffentliche Beschreibung enthält bewusst keine privaten Entwicklungsunterlagen oder Google-Drive-Links. Interne Planung findet ausschließlich im privaten Projekt statt. Eine Idee ist keine Zusage zur Umsetzung.
