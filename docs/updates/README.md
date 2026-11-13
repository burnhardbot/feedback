# Öffentliche STREAMEN-Updates

Hier findet ihr die knappen öffentlichen Änderungslisten und die zugehörigen manuellen Testlisten. Die eigentliche Streamen-Technik und private Entwicklungstickets bleiben im geschützten Projekt.

| Version | Changelog | Manuelle Testliste | Status |
| --- | --- | --- | --- |
| **v1.3** | [Änderungen](v1.3-changelog.md) | [Tests prüfen, kommentieren, Screenshots anhängen](https://github.com/burnhardbot/feedback/issues/16) | 🟡 Vorbereitung – kein veröffentlichtes v1.3-Release |

## Ablauf bei einem späteren Update

1. Der freigegebene Builder/Updater erzeugt für die **tatsächlich ausgelieferte Version** ein kurzes, öffentlich geeignetes Changelog.
2. Die **noch nötigen manuellen Prüfungen** werden als eigene versionierte GitHub-Testliste mit stabilen Testfallkennungen veröffentlicht.
3. Jan und später Leo prüfen die reale Version, setzen mit ausreichender GitHub-Berechtigung Häkchen und ergänzen Kommentare oder bereinigte Screenshots.
4. Fehler werden über die vorhandene [öffentliche Bugvorlage](https://github.com/burnhardbot/feedback/issues/new?template=bug_report.yml) gemeldet und anhand der Testfall-ID zugeordnet.
5. Discord erhält **nur knappen Versions-/Serverstatus und genau zwei Links:** Changelog und Testliste.

**Noch nicht automatisiert:** Testergebnis-Synchronisierung ins private Code-Repo, automatische Erstellung des Changelogs aus Releases, ein separates Ein-Klick-Testdashboard ohne GitHub-Bearbeitungsoberfläche. GitHub-Kommentare/Screenshots sind bereits nutzbar, das automatische Spiegeln wird separat abgesichert. Niemand darf eine private Issue-Nummer oder vertrauliche Daten öffentlich kopieren.

**Öffentlich lesen; Änderungen nur nach GitHub-Anmeldung und passenden Rechten.** Testhäkchen sind keine Freigabe zum Programmieren oder Deployen.
