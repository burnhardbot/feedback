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

## Streamen Test Center – GitHub Pages

- [Weboberfläche, Bedienung und Sicherheitsmodell](../dashboard/README.md) – im [DRAFT-PR #17](https://github.com/burnhardbot/feedback/pull/17) vorbereitet; **GitHub Pages erst nach erfolgreichem Deployment öffentlich erreichbar**.
- Die Webseite liest dieselbe fortlaufende [Testliste #16](https://github.com/burnhardbot/feedback/issues/16). Filter nach offen, bestanden, Fehlern, Blockiert und Bereich; Changelogs werden getrennt angezeigt.
- **Status-Meldung nach Aktivierung:** Jan kann im GitHub-Issue einen echten Test z. B. mit `/test T03 PASS v1.3.1 – Jan, 13.11.2026, OBS, geprüft` kommentieren. Der abgesicherte `issue_comment`-Workflow setzt dann genau diesen Haken. FAIL/BLOCKIERT lässt den Test offen. Screenshots werden im GitHub-Kommentar hochgeladen. Zunächst nur GitHub-Login `laberfeuer` berechtigt; Leos echter GitHub-Username ist noch nachzutragen.
- Es gibt **keine anonymen Schreibrechte** und keine gespeicherten GitHub-Tokens im Browser. Eigene Ein-Klick-Schreibaktionen ohne GitHub-Kommentar benötigen später eine eigenständige, gesichert zu authentifizierende Backend-Anbindung.
