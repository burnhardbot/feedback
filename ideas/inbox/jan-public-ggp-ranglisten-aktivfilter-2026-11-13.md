# [OFFEN] [IDEE] GGP-Ranglisten: Sichtbar erst nach echten Wertungskilometern
**Dokument-/Archivstatus:** [OFFEN]

**Ideengeber:** Jan · **Stand:** Regel von Jan am 13.11.2026 bestätigt, mit Leo zu besprechen · **Keine Umsetzung beauftragt**

## Worum geht es?

In den GGP-Ranglisten stehen inzwischen viele reine Zuschauer und vermutlich auch Viewbots. Künftig sollen dort nur Spieler erscheinen, die **mindestens einmal wirklich aktiv mitgemacht und dadurch echte Wertungskilometer erhalten haben**.

Wir erfassen Wertungskilometer bereits getrennt von Zuschauer-Kilometern. Darauf kann ein kleiner zentraler Filter aufbauen.

## Einfaches Beispiel

| Tom | Gesammelte Zuschauer-km | Aktive Wertungs-km | Kilometerstand | Rangliste |
|---|---:|---:|---:|---|
| Vor der ersten Teilnahme | 850 | 0 | 850 | ❌ Unsichtbar |
| Nach seinem ersten Sprint | 850 | 2 | **852** | ✅ Sichtbar |

**Von Jan entschieden:** Nach der ersten gültigen aktiven Teilnahme zählen **alle zuvor und danach gesammelten Kilometer** in der normalen Wertung mit. Tom startet also nicht bei 2 km, sondern steht sofort mit **852 km** in der Rangliste.

Die alten Zuschauer-Kilometer werden **nicht** nachträglich in aktive Wertungskilometer umgebucht. Echte Wertungskilometer sind nur der **Nachweis für die Freischaltung**.

## Feste Regeln

- **Einmalig und dauerhaft:** Sobald mindestens einmal mehr als 0 echte Wertungskilometer gültig verbucht sind, ist das Spielerprofil freigeschaltet.
- **Gemeinsam:** Die Freischaltung gilt bei Jan, Leo, Twitch, YouTube und in gemeinsamen Touren für dasselbe verifizierte Spielerprofil.
- **Alle offiziellen Wertungen:** Tages-, Wochen-, Gesamt-, Kilometer-, Sprint-, Berg-, Etappen- und Tourwertungen. Die vorhandenen Formeln und Tour-Scores bleiben unverändert.
- **Keine Einschränkung beim Mitspielen:** Zuschauen, Chatten, Join und laufende Minigames funktionieren weiterhin wie bisher. Accounts werden weder gelöscht noch als Bot eingestuft.
- **Korrekte Buchungen:** Vollständig stornierte/ungültige Wertungskilometer dürfen keine unberechtigte Freischaltung erzeugen.

## Plan für die spätere Umsetzung im Code

1. **Vorhandene Daten verwenden:** Je stabiler Spieler-ID die gültigen, tatsächlich aktiv verdienten Wertungskilometer aus der bisherigen Historie ermitteln – keine Zuschauer-km als Nachweis und keine zweite Datenbank.
2. **Zentral filtern:** Aus den offiziellen Ranking-Kandidaten nur freigeschaltete Spieler übernehmen. **Erst danach** sortieren, Plätze vergeben und Top-5/Top-20 bilden. Bestehende Rankingfunktionen wiederverwenden.
3. **Überall dieselbe Liste:** API, Results-Webseite, Tourwertungen, OBS-Overlays und Chat müssen dieselben gefilterten Plätze anzeigen. Spielteilnehmer- und Zuschauerlisten bleiben unberührt.
4. **Automatisch aktualisieren:** Nach erster gültiger Teilnahme, Storno oder sicherer Profilzusammenführung Rankings/Caches erneuern. Bestehende Kilometer und Punkte **nicht neu buchen**.

**Codeprinzip (schematisch, keine echten Feldnamen):**

~~~js
const visible = rankingCandidates.filter(
  row => validActiveScoringKmLifetime(row.userId) > 0
);
return existingSortRankAndLimit(visible);
~~~

## Das muss vor Freigabe getestet werden

- [ ] Viewbot mit 900 Zuschauer-km und 0 Wertungskilometern: unsichtbar.
- [ ] Tom mit 850 bisherigen km + 2 aktiven Wertungskilometern: sofort sichtbar mit **852 km**.
- [ ] Join ohne Wertungskilometer: noch unsichtbar.
- [ ] Teilnahme bei Leo schaltet dasselbe verifizierte Profil auch für gemeinsame Wertungen bei Jan frei.
- [ ] Richtige Plätze/Top-5/Top-20 nach dem Filtern, keine Lücken oder doppelte Spieler.
- [ ] Daten, Formeln, Chat, Spielablauf und bestehende Kilometerbuchungen bleiben unverändert; Stornos und Jahreswechsel funktionieren.

## Status

**[OFFEN – JANS REGEL BESTÄTIGT, MIT LEO ZU BESPRECHEN]**

Nur Idee und Codeplan. **Kein Build, kein Server-/OBS-Eingriff und keine Änderung der Live-Wertungen.** Beim späteren Build zuerst den dann aktuellen Code und die tatsächliche Wertungskilometer-Speicherung prüfen.
