# GitHub-only: Changelogs und **eine fortlaufende** manuelle Testliste

**Stand 13.11.2026 – Vorschlag zur Aktivierung nach Review.** Dieser Prozess verändert **keine** Serverdateien, startet keine Dienste und bestätigt **keine** Installation. Die Win10-Version v1.2.45 und deren laufender separater Fix bleiben unberührt.

## Dauerhafte Testliste – verbindliche Datenregel

- **Genau eine URL für alle Updates:** [Öffentliche manuelle Prüfliste #16](https://github.com/burnhardbot/feedback/issues/16). **Nie** pro Release eine neue Kopie erzeugen.
- Neue, wirklich manuell erforderliche Prüfungen bekommen weltweit eindeutige Kennungen (`T11`, `T12`, …). Die Automatik **hängt sie an**.
- Eine *nicht* abgehakte Prüfung bleibt über jedes weitere Update hinweg sichtbar und offen, bis sie tatsächlich geprüft wird. Offene Punkte aus v1.3 bestehen also auch bei v1.3.1, v1.4 oder v2.0 weiter.
- Bereits abgehakte Punkte, Kommentare und Screenshots bleiben erhalten. Bei geänderter Funktion oder nötigem neuen Regressionstest wird **eine neue ID** vergeben. Ein alter PASS ist **kein** Nachweis für die neue Version.
- **PASS** nur nach echtem Live-Test, mit datiertem Kommentar einschließlich tatsächlich getesteter Build-ID. **FAIL/BLOCKIERT/NOT RUN** bleibt ohne Häkchen und bekommt bei Bedarf öffentliche Bugverknüpfung.
- GitHub-Zugang zum Abhaken/Kommentieren erfordert passende Rechte. Ein öffentlich lesbares Issue ist keine unauthentifizierte Schreiboberfläche.

## So erzeugt Codex die öffentlichen Release-Informationen

1. **Nach einem echten Build- und Testbericht** erstellt der autorisierte Builder ein **öffentlich bereinigtes** JSON-Manifest in `docs/updates/manifests/vX.Y.Z.json`. Den Dateinamen an die echte vorbereitete Versionsnummer anpassen. Ohne reale Daten **kein** Manifest mit ausgedachten Features anlegen.
2. Manifest auf einem GitHub-Branch reviewen; erst nach Jans Zustimmung in `main` übernehmen. Diese Prüfung betrifft den Inhalt, **nicht** eine Live-Installation.
3. Jan startet in GitHub unter **Actions → Publish prepared release notes and permanent test backlog → Run workflow** für genau diese `version` auf `main` die Veröffentlichung. Nur GitHub-Akteur `laberfeuer` kann diesen Lauf ausführen.
4. Die Action prüft den Inhalt, erzeugt eine **eigene Changelog-Datei für diese Version**, ergänzt in der **bestehenden Issue #16** ausschließlich neue T-IDs und fügt der [Updateübersicht](README.md) eine Versionszeile hinzu.
5. Der Workflow darf jederzeit wiederholt werden: gleiche Version, gleiche Testfälle ergeben **keine Duplikate**. Ein bereits veröffentlichter Changelog wird nicht mit geändertem Inhalt überschrieben. Konflikte führen zu **FAIL** statt stiller Änderung.
6. Der spätere echte Codex-Updater veröffentlicht den Installationsstatus **erst nach nachgewiesenem Win10-Readback** in einem separat geregelten Schritt. Die hier eingerichtete Action schreibt bewusst immer nur **VORBEREITET**.

### Manifestformat (Schema-Beispiel, **kein** reales Release)

```json
{
  "version": "v1.3.1",
  "build_id": "BEISPIEL-NICHT-INSTALLIERT",
  "status": "prepared",
  "changes": [
    "Öffentlich formulierter Punkt, der tatsächlich im geprüften Release enthalten ist."
  ],
  "manual_tests": [
    {
      "id": "T11",
      "title": "Beispielprüfung",
      "description": "Erwartetes Verhalten am realen Gerät oder in OBS prüfen."
    }
  ]
}
```

Die Version und Test-IDs im Beispiel sind **Platzhalter**, nicht als existierende Updates oder Tests zu verstehen. Keine internen IPs, privaten Repository-Verweise, Secrets, personenbezogenen Daten, Zugangstokens, vollständigen Logzeilen oder unbereinigten Screenshots veröffentlichen.

## Rückverfolgbarkeit und Grenzen

| Gegenstand | GitHub-Ziel | Derzeitiger Status |
| --- | --- | --- |
| Versioniertes Kurz-Changelog | `docs/updates/vX.Y.Z-changelog.md` | Manuell für v1.3 vorhanden; automatische Erzeugung im hier vorgeschlagenen Workflow |
| **Fortlaufende** manuelle Prüfungen | [Immer Issue #16](https://github.com/burnhardbot/feedback/issues/16) | Öffentlich nutzbar; automatische Ergänzung im vorgeschlagenen Workflow |
| Reale Testbefunde | Häkchen und Kommentare in Issue #16 | Manuell, mit GitHub-Identität; Bilder als Kommentar-Anhang |
| Öffentliche Bugs | [Bugmeldeformular](https://github.com/burnhardbot/feedback/issues/new?template=bug_report.yml) | Verlinkung der T-ID im Bug und Testkommentar zunächst manuell |
| Automatische öffentliche→private Issue-Synchronisierung | Separat zu bauen | **Nicht vorhanden / nicht behaupten** |
| Eigenes komfortables Handy-Webdashboard | Separat zu bauen mit sicherem Login | **Nicht vorhanden / GitHub Issue ist derzeit die Weboberfläche** |
| Discord-Status | Zwei Links: Changelog der Version + **immer** Issue #16 | Webhook später nur auf Jans Server, dann Leo; noch **nicht aktiv** |

Die bestehende Ideas-Discussion-Spiegelung ist **keine** allgemeine Bugs-/Test-Ergebnis-Synchronisierung. Für die spätere private Zuordnung zuerst Berechtigungen, Deduplizierung und Geheimnisschutz umsetzen. Leos Testerrolle berechtigt **nicht** zum Programmieren oder zu Updates.

## Technische Sicherheitsgrenzen

- Die Action ist **manuell** (`workflow_dispatch`), nur auf `main`, nur für `laberfeuer`; minimale benötigte GitHub-Rechte `contents: write` und `issues: write`, kein Remotezugriff oder Drive-/Discord-Token.
- Ein exklusiver GitHub-Actions-Concurrency-Key verhindert parallele Veröffentlichungen. Vor dem Anhängen liest die Action die Testliste frisch ein. Bereits bestehende ID mit abweichender Bedeutung/Version oder doppelte ID → Fehler.
- Innerhalb des Workflows laufen vor jedem Publizieren die Python-Unittests. Bei Fehler keine serverseitige Aktion. Eine Changelog-Kollision wird vor Änderungen erkannt; ein unterbrochener Publikationslauf kann mit denselben Daten erneut gestartet werden.
- Für die zeitgleiche manuelle Bearbeitung der Issue #16 während der sehr kurzen Publikation gibt es ohne transaktionelles GitHub-Issue-API **keine absolute Konkurrenzsperre**. Deshalb vor dem Ausführen kurz sicherstellen, dass gerade niemand Checkboxen bearbeitet, und danach die Häkchen prüfen. Datiertes Kommentarprotokoll bleibt als Nachweis bestehen.
- Die Builder-/Updater-Phasenregel im privaten Repo bleibt bis zur **gesonderten Bestätigung** nur Entwurf; diese öffentliche Dokumentationsautomatik autorisiert keinen produktiven Servereingriff.
