# Panorama FIX9 – Chatter-Bewegung, Bereiche und Twitch-Namensfarben

**17. November 2026 · Win10-Installation erfolgreich · Basis Streamen v1.3.1 RC2**

Dieser gezielte Hotfix korrigiert die Darstellung der Chat-Fahrer im gemeinsamen Panorama. Die sonstigen Game-, Wertungs-, Video- und Streamingfunktionen wurden nicht erweitert.

## Neu beziehungsweise korrigiert

- **Ohne Event:** Chatter können die gesamte Strecke nutzen.
- **Bei einem laufenden Event (Beitritt und Rennen):** Offizielle Event-Teilnehmer fahren **links**; Chat-Fahrer, die am Event nicht teilnehmen, fahren **rechts**.
- **Keine doppelten Figuren:** Ein Nutzer gehört immer nur einer Seite an. Bei einem Eventbeitritt oder Eventende fährt dieselbe Figur fließend zur neuen Position.
- **Chat gibt Schub:** Eine neue echte Twitch-Nachricht lässt den zugehörigen Fahrer zügig bis nach vorn in seinen erlaubten Bereich fahren. Anschließend fällt er wieder auf seine normale Position zurück. Laden und wiederholte Datenabfragen zählen nicht als neue Nachricht.
- **Namensfarben:** Normale Chat-Namen verwenden die übermittelte originale Twitch-Nutzerfarbe, unabhängig von der Trikotfarbe. Für offizielle Event-Namensschilder ist die kontrastreiche Schrift erlaubt.
- **Identität:** Der Streamer/Wattfahrer Leo wird weiterhin in einer gemeinsamen Figur geführt.

## Technik und Teststatus

Es wurden nur drei Programmdateien ausgetauscht. Vor der Installation liefen **13 automatisierte Tests erfolgreich**. Der neue Stand wurde über den freigegebenen Installer installiert; die Versionskennung bleibt aus Kompatibilitätsgründen unverändert. Die erste Live-API-Prüfung bestätigt die ganze Strecke ohne aktives Event sowie die Chatter-Namensfarben und die einzelne Leo-Figur.

**Noch von Jan im echten OBS-/Twitch-Betrieb zu prüfen:** Fahrt nach einer neuen Nachricht, Rückfall nach Abklingen, der Seitenwechsel bei aktivem Event, Namenskontrast und längerer Dauerbetrieb. Die bekannten Verbindungsabbrüche sind ein **eigenes, noch offenes Thema** und nicht Bestandteil von FIX9.

Die fortlaufende [Streamen-Testliste](https://github.com/burnhardbot/feedback/issues/16) bleibt offen; bisherige Prüfpunkte werden nicht als erledigt markiert.
