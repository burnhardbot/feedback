# [OFFEN] [IDEE] GGP-Ranglisten: Sichtbar erst nach echten Wertungskilometern
**Dokument-/Archivstatus:** [OFFEN]

**Ideengeber:** Jan · **Abstimmung:** mit Leo ausstehend  
**Bereich:** STREAMEN / GGP / offizielle Wertungen  
**Stand:** Idee mit technischem Umsetzungsvorschlag vom 13.11.2026 · **Kein Build- oder Liveauftrag**

## Kurz erklärt – worum geht es?

In den offiziellen GGP-Ranglisten erscheinen inzwischen viele reine Zuschauer-Accounts bzw. vermutete Viewbots, obwohl sie nie aktiv bei einem Spiel mitgefahren sind. Das macht die Wertungen unübersichtlich.

**Vorschlag:** Für offizielle Ranglisten wird ein Spieler erst dann berücksichtigt, wenn auf seinem Profil **mindestens einmal mehr als 0 echte Wertungskilometer aus einer gültigen aktiven Spielteilnahme verbucht** wurden. Diese Kilometer werden im System bereits getrennt von passiven Zuschauer-Kilometern erfasst.

Die Freischaltung gilt **einmalig, dauerhaft, spielerbezogen und über alle Streamer/Plattformen hinweg**. Danach darf der Spieler in den jeweiligen Wertungen erscheinen, sofern er dort überhaupt einen Wertungsstand hat. Es wird **keine Mindestmenge außer `> 0`** eingeführt.

| Beispiel | Passive Zuschauer-km | Echte Wertungs-km (historisch) | Offizielle Ranglisten |
|---|---:|---:|---|
| Reiner Viewbot | 900 | 0 | Nicht anzeigen |
| Bisher passiver Zuschauer | 150 | 0 | Noch nicht anzeigen |
| Einmal bei einem Sprint mitgefahren | 150 | 1,2 | Anzeigen |
| Langjähriger aktiver Spieler | 600 | 20 | Anzeigen |

**Was bedeutet das für Zuschauer?** Jeder kann weiter zuschauen, chatten und erstmals bei `!sprint`, `!berg` oder `!gruppe` mitmachen. Die Sperre betrifft nur die **Darstellung/Platzierung in offiziellen Ranglisten**, nicht die Teilnahme, Punktebuchung oder Speicherung. Niemand wird gelöscht oder als Bot markiert.

## Umfang und beschlossene Grundidee

- **Globales Teilnahme-Kriterium:** Eine historisch gültige, wirklich verbuchte positive Zahl an **aktiven Wertungskilometern** reicht. Passive Zuschauer-km, Chataktivität, ein bloßer Join, Anzeigename oder Anwesenheit reichen nicht.
- **Dauerhaft und kanalübergreifend:** Eine echte Teilnahme bei Jan oder Leo sowie über Twitch oder YouTube schaltet dasselbe eindeutig identifizierte Spielerprofil frei; keine weitere Teilnahme pro Woche/Etappe/Tour nötig. Bestehende Identitätsverknüpfung nutzen, nicht nach ähnlichen Nicknames zusammenführen.
- **Betroffene offiziellen Listen:** Tages-, Wochen-, Gesamt-/Jahres-, Kilometer-, Etappen-, Sprint-, Berg- und Tourwertungen (einschließlich Tour-Kilometer, grüne/rote Punkte und Etappensiege/Regenbogen), soweit der jeweilige Wertungsmodus diese darstellt. **Das Kriterium ist global**, die Punkte/Ergebnisse pro Scope bleiben getrennt.
- **Nicht betroffen:** JOIN/LIVE-Teilnehmerlisten, einzelne tatsächliche Rennergebnisse, Chat- und Zuschauerstatistiken, `!lurk`, Spielablauf, Wertungsformeln, offizielle Buchungen und historische Rohdaten.
- **Korrekturen respektieren:** Stornierte oder nachträglich zurückgenommene Wertungskilometer dürfen keinen falschen dauerhaften Nachweis hinterlassen. „Dauerhaft“ meint: keine erneute Aktivitätsprüfung pro Zeitraum; eine vollständig annullierte, nie gültige Teilnahme zählt nicht.

## Konkreter Umsetzungsplan für einen späteren Codeauftrag

1. **Ist-Code und Datenquelle feststellen.** Im *dann aktuellen* freigegebenen Source-Stand exakt ermitteln, wo aktiv verdiente Wertungskilometer separat gespeichert/bestätigt und gegebenenfalls korrigiert werden. Nicht einfach das Gesamtfeld `km` oder passive Zuschauer-km prüfen. Existierende Scopes, Ledger, Identitäts-/Merge-Regeln und Saison-/Resetarchiv beachten; keinen neuen Wertungsspeicher anlegen.
2. **Zentralen Berechtigungsnachweis ableiten.** Für jede stabile `userId` aus gültigen offiziellen Buchungen den **historisch verbleibenden Netto-Wert an aktiven Wertungskilometern** ermitteln. `eligibleForRankings(userId) = (confirmedActiveScoringKmLifetime > 0)`. Wenn die Historie ausreichend ist, nur abgeleitet und ggf. versionsgebunden zwischengespeichert; kein zusätzlicher permanenter Schalter nötig. Falls Archiv/Reset den Nachweis nicht liefert, erst eine sichere Migrations-/Persistenzstrategie gesondert planen.
3. **Genau einmal zentral filtern.** Den bestehenden Weg für offizielle Ranglisten verwenden. Aus den Kandidaten **zuerst** alle `userId`s ohne positiven Nachweis entfernen, **danach** nach existierenden Kategorien sortieren, Gleichstände/Rangnummern berechnen und Top-N/Paginierung anwenden. Nicht erst fünf Viewbots aus einer fertigen Top-5 entfernen. Keine zweite Ranking-Engine aufbauen.
4. **Alle Ausgaben konsistent halten.** Dieselbe gefilterte offizielle Rangfolge in Ergebnis-API, Results-Webseite, Touransicht, OBS-/Panorama-Wertung und zugehörigen Chat-Ausgaben verwenden. Nur die betroffenen *offiziellen Ranglisten* ändern, nicht automatisch jede beliebige Spielerliste. Bestehende Tour- und Stage-Scope-Logik bleibt maßgeblich.
5. **Änderungen sofort wirksam machen.** Bei erster gültiger aktiver Kilometerbuchung und bei offiziellen Stornos/Korrekturen/Profilzusammenführungen ggf. vorhandene Ranking-Caches invalidieren. Bestandsdaten beim Start bzw. vor Freigabe lesend gegenrechnen; keine Löschung oder rückwirkende Neubuchung.

**Schematisches JavaScript – keine Behauptung über vorhandene Feldnamen:**

```js
// validActiveKmByUser wird aus dem vorhandenen offiziellen Buchungsnachweis
// NETTO und über die gesamte gültige Historie ermittelt.
const eligible = userId => (validActiveKmByUser.get(userId) ?? 0) > 0;

const visible = rankingCandidates.filter(row => eligible(row.userId));
return existingSortRankAndLimit(visible); // existierende Logik weiterverwenden
```

**Bezug zum bekannten Stand:** In einer früher geprüften K8-Codebasis waren bereits zentrale Tour-/Rankingpfade wie `scopeLeaderboard`, `displayRankings` sowie gemeinsame `userId`-Scopes dokumentiert. Ihre **tatsächlichen aktuellen Implementierungen** sind vor einem Build erneut zu prüfen; diese Idee ist **kein** Source-Audit des aktuellen Win10-Servers. Bestehende Tour-/Etappen-Planung nicht mit diesem Filter verwechseln.

**Context7-Bedarf:** NEIN für diesen Vorschlag – reine interne Bewertungs-/Anzeigelogik ohne neue oder geänderte externe Bibliotheks-/SDK-APIs. Bei späterer andersartiger Implementierung erneut prüfen.

## Wichtiger Punkt für die Besprechung Jan ↔ Leo

**Empfohlener Minimal-Eingriff:** Wir filtern nur die Anzeige und Platzierung; bisherige Zuschauer-Kilometer und Punkte werden **nicht rückwirkend umgerechnet**. Folge: Wer nach langer passiver Zeit erstmals echte Wertungskilometer bekommt, kann danach mit seinem bisherigen regulären Wertungsstand auftauchen. Das ist bewusst die einfachste und rückbaubare Variante. Falls das nicht gewünscht ist, wäre eine zusätzliche Regel „passive Punkte vor erster Aktivteilnahme zählen nicht“ ein **separater, deutlich größerer Eingriff** in die Wertungsberechnung und braucht einen eigenen Beschluss.

**Grenze:** Das ist ein **Teilnahme- und Sichtbarkeitsfilter, keine garantierte Bot-Erkennung**. Ein Account, der tatsächlich eine gültige aktive Teilnahme samt Wertungskilometern erlangt, erfüllt das Kriterium. Dafür wären gegebenenfalls getrennte Anti-Missbrauchsregeln nötig.

## Abnahmekriterien und Testfälle (alle NOT RUN)

- [ ] Account mit 1.000 passiven km, **0 aktiven Wertungs-km**: in keiner offiziellen Rangliste, Rohdaten unverändert.
- [ ] Nach erstem gültigen Wertungs-km-Eintrag `> 0`: automatisch sichtbar, ohne Neustart/manuelle Freigabe.
- [ ] Echte Teilnahme mit **0** gutgeschriebenen aktiven km: noch nicht freigeschaltet.
- [ ] Einmalige Teilnahme bei Leo → dasselbe verifizierte Profil bei Jan und in gemeinsamen Tour-Rankings berechtigt; keine doppelte Person.
- [ ] Tages-/Wochenwechsel, neues Jahr/Season, parallele Touren und historische Archive: globale Berechtigung bleibt, die **pro Liste** gültigen Scores bleiben korrekt getrennt.
- [ ] Korrektur/Storno aller ehemals verbuchten aktiven km → keine ungültige Ranglistenfreigabe; spätere neue Teilnahme aktiviert wieder.
- [ ] Sortierung, Gleichstand, Rangnummer und Top-5/Top-20 korrekt **nach** Filterung; Platz 1 ist bester tatsächlich zugelassener Spieler.
- [ ] API, Browser/Results, OBS/Panorama und Chat zeigen pro Wertung dieselben Reihenfolgen/Plätze; JOIN und laufende Minigames bleiben unverändert.
- [ ] Alle bisherigen Kilometer, Punkte, Historien und Ledger unverändert; kein Spielstandreset, keine neue Doppelbuchung und keine Datenlöschung.
- [ ] Vor Umsetzung aktuelle Source-Version/Hashes, echte Konten-/Profilverknüpfung und Testdaten bestätigen; Tests in geeigneter Testumgebung, Produktivabnahme getrennt.

## Status und Schutzgrenzen

**[OFFEN – ZUR DISKUSSION MIT LEO]**. Dieser Vorschlag erlaubt **keinen automatischen Build, Commit in Serverquellen, Release, Win10-/OBS-/Twitch-Eingriff, Reset oder Produktiv-Neuberechnung**. Umsetzung erst nach Jans ausdrücklichem Auftrag und geltenden Projektprüfungen.

Öffentliche Beschreibung ohne geheime Zugangsdaten, private Dateien oder Produktivdetails. Diese Idee wird erst nach echter Umsetzung und überprüfter Abnahme als erledigt behandelt.
