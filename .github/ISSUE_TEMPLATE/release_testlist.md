---
name: "✅ Manuelle Release-Testliste"
about: "Neue öffentliche Testliste für eine konkrete Streamen-Version mit Häkchen, Kommentaren und Screenshot-Belegen"
title: "[TESTLISTE][VERSION] Manuelle Prüfungen"
---

> 🟡 **Neue Vorlage:** `VERSION`, `BUILD-ID`, Datum und die relevanten Prüfpunkte **vor Veröffentlichung** auf die tatsächlich freigegebene Version anpassen. Dieses Issue ist keine automatische Produktionsfreigabe.

**Version:** VERSION  
**Build-ID:** BUILD-ID  
**Installationsstatus:** NICHT BESTÄTIGT  
**Changelog:** LINK_ZUR_OEFFENTLICHEN_VERSION  
**Prüfer:** Jan / Leo (echten Prüfenden und GitHub-Konto dokumentieren)

## Nur manuell notwendige Tests

Ersetze diese Beispiele durch die **vom Checker für genau diese Version als manuell offen** gemeldeten Tests. Automatisch bestandene Tests hier nicht als manuell bestätigt ausgeben.

- [ ] **T01 – [Funktion]** – [Was ist am echten System zu prüfen?]
- [ ] **T02 – [Funktion]** – [Was ist am echten System zu prüfen?]
- [ ] **T03 – [Funktion]** – [Was ist am echten System zu prüfen?]

## Ergebnis melden

- **PASS:** Nach realer Prüfung Häkchen setzen (falls Bearbeitungsrecht), plus Kommentar `Txx PASS – VERSION – Nutzer – Datum – Gerät/OBS`.
- **FAIL:** Offen lassen, `Txx FAIL – Beschreibung` kommentieren, bereinigten Screenshot im Kommentar anhängen; bei Bedarf [Bug melden](https://github.com/burnhardbot/feedback/issues/new?template=bug_report.yml) und Testfall-ID angeben.
- **BLOCKIERT / NOT RUN:** Offen lassen und Grund kommentieren. Keine fiktiven Test-PASS.
- Ohne ausreichende GitHub-Editierrechte ist ein Kommentar möglich; der Haken muss dann von einem berechtigten Bearbeiter gesetzt werden. **Automatische Kommentar→Checkbox-Synchronisierung noch nicht implementiert.**

**Öffentlicher Datenschutz:** Keine Tokens, privaten URLs, IPs, internen Logs, privaten Tickets oder unbereinigten Screenshots veröffentlichen. Die öffentliche Liste autorisiert kein Coding oder Deployment.

## Abschluss

- [ ] Alle für diese Version verpflichtenden manuellen Tests sind nachvollziehbar PASS oder ein verbleibender Fehler ist verlinkt und bewertet.
- [ ] Tatsächlich ausgelieferte Build-ID und Changelog stimmen überein.
- [ ] Keine ungeklärten FAIL/BLOCKIERT/NOT RUN als erledigt ausgegeben.

**Freigabeentscheidung:** offen – eine Testliste allein gibt keine Produktivfreigabe.
