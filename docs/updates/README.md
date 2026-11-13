# Öffentliche STREAMEN-Updates

Hier findet ihr die kurzen öffentlichen Changelogs je Version und **genau eine fortlaufende manuelle Testliste** über alle Versionen. Die eigentliche Streamen-Technik und private Entwicklungstickets bleiben im geschützten Projekt.

| Version | Changelog | Manuelle Testliste | Status |
| --- | --- | --- | --- |
<!-- STREAMEN_RELEASE_ROWS_BEGIN -->
| **v1.3** | [Änderungen](v1.3-changelog.md) | [Tests prüfen, kommentieren, Screenshots anhängen](https://github.com/burnhardbot/feedback/issues/16) | 🟡 Vorbereitung – kein veröffentlichtes v1.3-Release |
<!-- STREAMEN_RELEASE_ROWS_END -->

## Ablauf bei einem späteren Update

1. Der freigegebene Builder/Updater erzeugt für die **tatsächlich ausgelieferte Version** ein kurzes, öffentlich geeignetes Changelog.
2. **Neue manuelle Prüfungen werden an die immer gleiche [Testliste #16](https://github.com/burnhardbot/feedback/issues/16) angehängt.** Ungeprüfte Punkte und bestehende Häkchen bleiben auch nach beliebig vielen Updates erhalten; die Liste wird weder ersetzt noch pro Version dupliziert.
3. Jan und später Leo prüfen die reale Version, setzen mit ausreichender GitHub-Berechtigung Häkchen und ergänzen Kommentare oder bereinigte Screenshots.
4. Fehler werden über die vorhandene [öffentliche Bugvorlage](https://github.com/burnhardbot/feedback/issues/new?template=bug_report.yml) gemeldet und anhand der Testfall-ID zugeordnet.
5. Discord erhält **nur knappen Versions-/Serverstatus und genau zwei Links:** Changelog und Testliste.

**Noch nicht automatisiert:** Testergebnis-Synchronisierung ins private Code-Repo, ein separates Ein-Klick-Testdashboard ohne GitHub-Bearbeitungsoberfläche. Die neue GitHub-Action ermöglicht die Erstellung vorbereiteter Changelogs aus einem zuvor geprüften öffentlichen Manifest (nach Review und Aktivierung des Workflows); sie ist **kein** Server-Update und keine automatische Installation. GitHub-Kommentare/Screenshots sind bereits nutzbar, das automatische Spiegeln wird separat abgesichert. Niemand darf eine private Issue-Nummer oder vertrauliche Daten öffentlich kopieren.

**Öffentlich lesen; Änderungen nur nach GitHub-Anmeldung und passenden Rechten.** Testhäkchen sind keine Freigabe zum Programmieren oder Deployen.

## Vorlagen für weitere Versionen

- [Changelog-Vorlage](CHANGELOG-TEMPLATE.md) – für jeden tatsächlichen Release eine eigene öffentliche Versionsdatei erstellen.
- [Dauerhafte Testliste #16](https://github.com/burnhardbot/feedback/issues/16) – niemals eine neue Testlisten-Kopie pro Update anlegen. Neue Checks bekommen eine weltweit eindeutige `Txx`-ID; bei geänderter Funktion ist für einen erneuten Regressionstest eine neue ID anzulegen.
- [Hinweise zur automatischen Veröffentlichung](AUTOMATISIERUNG.md) – Ablauf und Sicherheitsgrenzen für geprüfte Release-Manifeste.

Die Manifeste und die GitHub-Action veröffentlichen nur als **vorbereitet** gekennzeichnete Informationen. Eine Releasefreigabe, Serverinstallation, private Issues-Synchronisierung oder ein manueller Test-PASS werden damit **nicht** erzeugt.
