# [OFFEN] [IDEE] GGP-Liveoverlay verbessern: Timer, Join-Anzeige und Lesbarkeit
**Dokument-/Archivstatus:** [OFFEN]

**Ideengeber:** Leo (`@leoburnhard`)  
**Bereich:** GGP / STREAMEN-Community  
**Stand:** TEILWEISE UMGESETZT – UX-/OBS-REST OFFEN · TEILWEISE CODE VORHANDEN – VISUELLE ABNAHME OFFEN · K8-Quelle geprüft, keine Build-/Livefreigabe.

Die GGP-Overlays sollen gerade während vieler Chat- und Eventaktionen besser lesbar bleiben.

## K8-Statusinventur · 11.11.2026

**Fachstatus:** TEILWEISE UMGESETZT – UX-/OBS-REST OFFEN. **Codeprüfung:** TEILWEISE CODE VORHANDEN – VISUELLE ABNAHME OFFEN. **Gesamtidee vollständig implementiert/abgenommen:** NEIN.

**Was der Code bereits enthält:** K8 hat bestehende Panorama-/Overlay-Renderer, Zeit- und Rundenphasen, Live-Peloton, Chat-/Join-/Szenendarstellungen (`minigame/overlays.js`, `minigame/panorama/live.js`, `display.js`). Diese Komponenten werden wiederverwendet.

**Was gegenüber dem Vorschlag fehlt:** Kein gesicherter aktueller 10+-Ereignis-/OBS-Nachweis, dass der Timer nie überdeckt wird und Join-/Rennphase, Straßenbreite, Fahrerhöhe und Leo-Alpha-Schnitt überall den Anforderungen entsprechen. Das sind Abnahme- und gegebenenfalls gezielte Layoutkorrekturen, kein neues Overlay-System.

**Abgrenzung/Referenzen:** Bestehende Panorama- und Namensbadge-Aufgaben [#53](https://github.com/burnhardbot/stream/issues/53), [#79](https://github.com/burnhardbot/stream/issues/79) und [#31](https://github.com/burnhardbot/stream/issues/31) als Abhängigkeiten. [Private Discussion #66](https://github.com/burnhardbot/stream/discussions/66) · [öffentliche Discussion #7](https://github.com/burnhardbot/feedback/discussions/7). Kein eigenständiges neues Implementierungs-Issue oder Bauauftrag aufgrund dieser Dokumentation. Original-ZIP `v1.2.44 TEST-K8`, SHA-256 `746dabacd5e6a1cb8746c557c30901cf43c2b7d3aa81a06d87da77f197160ef4`. **Quellprüfung ≠ vollständige Live-/OBS-/Win10-Abnahme.**

---
## Vorschlag
- Den Countdown dauerhaft sichtbar halten, auch wenn zahlreiche Einlösungsmeldungen erscheinen.
- Die offene Beitrittsphase, das laufende Rennen und die Ergebnisphase klar voneinander unterscheiden.
- Die Rennstrecke und Fahrer so anordnen, dass sie besser erkennbar sind.
- Overlay-Ausschnitte und transparente Einblendungen für unterschiedliche Streamansichten prüfen.

## Testideen
Lange Namen, viele gleichzeitig eintreffende Meldungen, verschiedene Bildschirmgrößen und transparente Hintergründe.

**Status:** Gemeldete UX-Idee. Ob einzelne Punkte in der aktuell laufenden Version noch fehlerhaft sind, muss gesondert geprüft werden.

---
**Hinweis:** Diese öffentliche Beschreibung enthält bewusst keine privaten Entwicklungsunterlagen oder Google-Drive-Links. Interne Planung findet ausschließlich im privaten Projekt statt. Eine Idee ist keine Zusage zur Umsetzung.
