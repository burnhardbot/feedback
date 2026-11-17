# [ERFASST] STREAMEN Panorama FIX8 – 17.11.2026

**Status:** Auf dem freigegebenen Windows-Testsystem installiert; technische Erstprüfung bestanden. Die manuelle OBS- und Langzeitabnahme ist noch offen.

## Änderungen

- Echte aktive Twitch-Chatter erscheinen wieder im gemeinsamen Panorama-Peloton, auch wenn gerade kein Minigame läuft. Ein `!join` ist für die reine Anzeige nicht nötig.
- Jan- und Leo-Chats werden aus bereits bestätigten Ereignissen angezeigt; reine Chataktivität verleiht keine Spielpunkte.
- Leos verifizierte Twitch-Live-Rolle und seine Watt-Fahrer-Rolle werden als **eine Figur** dargestellt. Es wird nicht anhand bloß ähnlicher Namen zusammengeführt.
- Ein Chat-Eintrag bleibt höchstens zehn Minuten ohne neue Nachricht aktiv. Die Anzeige nutzt weiterhin die bestehende Teilnehmerbegrenzung und ist für OBS sowie Browser vorgesehen.
- Der bestehende FIX7-Speicher-/Ledger-Code sowie Spielstände, Einstellungen und Zugänge wurden nicht als Teil dieses Fixes geändert.

## Prüfstand

- Isolierte Tests: **5/5 bestanden**.
- Windows-Paketprüfung, Vorabprüfung, Installer und erneute Quell-Hashprüfung: **bestanden**.
- Erste Live-API-Prüfung: Chatter in der gemeinsamen Welt sichtbar, Leo nur einmal mit beiden Rollen.
- **Offen:** echter OBS-Sichttest, Reload-/Chat-TTL-Test, Spielstandsabgleich und längere RAM-/Stabilitätsbeobachtung.
- Beim Update war der sanfte Game-Drain nach 120 Sekunden nicht bestätigt. Der Installer verwendete danach seinen identitätsgesicherten Stopppfad; dies bleibt ein Warnhinweis, kein bestandener Drain-Test.

## Testliste

Die dauerhaften [Streamen-Testfälle T11–T15](https://github.com/burnhardbot/feedback/issues/16) bleiben bis zur tatsächlichen manuellen Prüfung offen. Frühere offene Tests werden dadurch nicht ersetzt.
