# Streamen Test Center – GitHub Pages

Die öffentliche Streamen-Weboberfläche wird direkt aus dem GitHub-Repository `burnhardbot/feedback` als **GitHub Pages** veröffentlicht. Sie ist bewusst eine statische Web-App und **greift nicht auf den Win10-Server zu**.

## Aktuelle Funktionen

- Mobilfreundliche Übersicht der **einen fortlaufenden GitHub-Issue-Testliste #16**.
- Offene, bestandene, fehlgeschlagene und blockierte Prüfungen; Suche nach ID, Beschreibung und Bereich.
- Bestehende Häkchen, neue Test-IDs und datierte Ergebnisse werden **live und nur lesend über GitHub** geladen; fehlgeschlagener GitHub-Aufruf zeigt eine klare Fehlermeldung statt erfundener Prüfergebnisse.
- Changelog-Übersicht nach tatsächlich vorhandenen öffentlichen Dateien, mit aufklappbaren Details und ausdrücklich **ohne Behauptung einer Installation**.
- Öffentliche GitHub-Issues sowie Links zur Bug-Meldung; sensible private Issues und Serverinformationen erscheinen nicht.
- Bei einem Test kann der Benutzer einen `/test Txx PASS/FAIL/BLOCKIERT vX.Y.Z`-Kommentar vorbereiten. **Die Webseite selbst setzt keine Häkchen, sendet nichts im Hintergrund und hat keinen Schreibtoken.** GitHub-Anmeldung und Kommentar bleiben erforderlich; Bilder werden über GitHubs Kommentar-Uploader angehängt.

## Veröffentlichungsweg

1. GitHub-Branch mit `docs/index.html`, `docs/dashboard/` und `.github/workflows/deploy-test-dashboard.yml` von Jan prüfen und nach `main` mergen.
2. Der `actions/configure-pages@v5`-Schritt versucht mit `enablement: true`, Pages direkt beim ersten Lauf einzurichten. Falls GitHub die nötigen Repositoryrechte dafür nicht freigibt, im öffentlichen Repository **Settings → Pages → Build and deployment → GitHub Actions** als Quelle auswählen.
3. Den Workflow **Deploy Streamen Test Center to GitHub Pages** nach Aktivierung einmal ausführen und den tatsächlich ausgegebenen URL kontrollieren. **Vor erfolgreichem Lauf keinen erfundenen Pages-Link als live ausgeben.**
4. Bei Frontend-Updates wird bei relevantem `main`-Commit automatisch neu veröffentlicht. Neue GitHub-Tests und Kommentare erscheinen ohne neue Server-/Webseiten-Version beim nächsten Abruf (manuelles Refresh oder alle fünf Minuten im offenen Tab).

## Testablauf über GitHub-Kommentare

- Berechtigte GitHub-Nutzer kommentieren auf der [dauerhaften Liste #16](https://github.com/burnhardbot/feedback/issues/16) z. B. `/test T03 PASS v1.3.1 – Jan, 13.11.2026, OBS, echte Kamera geprüft`.
- Der Action-Workflow `.github/workflows/accept-test-comments.yml` akzeptiert **nur** echte Kommentare auf Issue #16 und **nur** ausdrücklich freigegebene GitHub-Logins aus [`docs/updates/tester-roles.json`](../updates/tester-roles.json). Zunächst ausschließlich `laberfeuer`. **Leos GitHub-Login muss Jan später verifizieren und ergänzen**; eine E-Mail-Adresse oder ChatGPT-Mitgliedschaft ersetzt keine GitHub-Identität.
- **PASS** setzt nur den angefragten Haken; **FAIL/BLOCKIERT** lässt ihn offen oder öffnet ihn wieder. Bereits bestehende andere Tests bleiben unverändert. Ein älterer Kommentar darf einen neueren Befund nicht überschreiben.
- Die Kommentare samt öffentlichen GitHub-Bildanhängen bilden das Protokoll. Nur tatsächlich manuell geprüfte Resultate zählen; die Action macht weder aus einem Kommentar einen Server-Readback noch eine Releasefreigabe.
- Bei Fehlern weiterhin das öffentliche [Bugformular](https://github.com/burnhardbot/feedback/issues/new?template=bug_report.yml) nutzen und die Test-ID nennen. Die technische Synchronisierung in **private** Issues ist ein getrenntes, bislang nicht eingerichtetes Arbeitspaket.

## Sicherheit und Grenzen

- Kein OAuth-Client-Secret, GitHub-PAT, Discord-Webhook oder privater Link im Browsercode.
- Kein neues öffentliches Schreib-API, kein Win10-Zugriff; GitHub Actions arbeitet ausschließlich mit dem auf das öffentliche Repo beschränkten `GITHUB_TOKEN` und seinen minimalen Berechtigungen.
- Die GitHub-API hat Abruflimits; wenn sie nicht erreichbar ist, gibt es **keinen** erfundenen grünen Status. Nur autorisierte Kommentare beeinflussen die Anzeige von FAIL/BLOCKIERT.
- Der Dashboard-„Funktioniert“-Knopf bereitet **nur den Kommentar** vor. Echte Ein-Klick-Schreibzugriffe und Screenshot-Uploads direkt innerhalb der Webseite würden eine separat zu prüfende GitHub-App-/OAuth-Backend-Komponente benötigen. Keine Secrets in statischem HTML/JavaScript hinterlegen.
- Die manuelle Testliste ist **fortlaufend**: Auch nach 100 neuen Updates bleiben alle früheren noch offenen Tests sichtbar. Bei einer neuen Regression wird ein neuer Testfall angehängt, der alte historische PASS bleibt unverändert.

**Tests:** `node --test test_dashboard.js` und `python -m unittest discover -s tools/updates -p 'test_*.py' -v` aus dem Repository-Root.
