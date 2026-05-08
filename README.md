# txtHumanizer

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/LangeVC/txtHumanizer/releases/tag/v1.0.0)
[![Status](https://img.shields.io/badge/status-production%20ready-green)](https://github.com/LangeVC/txtHumanizer)
[![Capacium](https://img.shields.io/badge/Capacium-Install%20via%20cap-0B1020?style=flat-square&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNTAgNTAwIj48cGF0aCBmaWxsPSIjRjdGQUZDIiBkPSJNMzA4LjgzLDU5MC40N2wtMzYuMDItMzYuMjQtMjExLjMyLTQuNDQtMjExLjczLTMzLjExLTMzLjk3LDMzLjEtMzIuODMuMDYtMjE1Ljc0LDIxMy43NC4wNCwzMy40NC0zMi45OSwzMi43Mi0zMi45NSwyMTQuMDEuMDYuMDksMjE1LjYyLDMzLjg0LDMzLjc2LTMzLjk4LDMzLjExLjA3LDIxMi43NC0yMTAuNC4xMi0zNi4yMywzNi4yWk0zMDkuNjYsNTU0Ljh6NzUuNTktNzYuODQsMTM5LjgzLTE0MS4zMSwyNy43MS0yOC4xNiw5MC42NS05MC43Mi0xNTMuMjItMTUzLjE0LTEyMS41MiwxMjAuNTQtOTQuOTMsOTUuNDYtMjguMTIsMjguNDQsMTA0Ljc1LDEwNS41LDc2LjA4LDczLjY2LDY2LjQ3LDY2LjU3Wk0yMTcuMjYsMTg4LjQ0bDMyLjE0LTMyLjAyLTE2Mi41MS4wMy4wNCwxNjIuNDhMMjIxLjcyLDE4OC40NFpNNTIyOS44OSw4Ni4zNmwtMTYyLjY1LjA2LDE2Mi42MSwxNjIuNDguMDQtMTYyLjUzWk0yMTIuNTksNDk0Ljg0LTg0LjE1LTg0Ljg4LTQ1LjAyLTQ1LjcyLjA4LTE2Mi4wMiwxNTkuNDcuMDMtMzQuNzktMzQuNDJaTTM3NjguMzUsNTI4Ljk5aDE2MS41M3cwLjA1LTE2Mi4wNCwwLjUtMTU1LjEsNTU0Ljk5LTEwNi4zOCwxMDcuMDEtNTUuMjUsNTAuNjIsLTk5LjU4LDEwNS45LTc4LjUyLDk0Ljg2LTc1LjkyLTMzLjMxLTMyLjM0LDI3LjY5LTMyOC4wMiwtNDAuNTQsMzIuMDMsMzExLjQ0LDI1Mi41MiwyNTQuNDksMjUzLjU3Wk0xOTguOTQsODQwLjc3Yy0zMi4yNCwtMi4wMiAtMjIuMTQsLTIyLjEyIC0yNy4wMiwtMjUuOTUgLTQuOTUsLTMuOTEgLTEyNC45MiAtNS44NiAtMTI0LjkyLC01Ljg2IC04LjM4LC0wLjczIC0xNC44OSwtMi4yMyAtMTcuMDMsLTMuMzEgLTIuMjksLTEuMTggLTQuOTE2LC0wLjA0IC0xMS4zMTIsMC43NyAtMTMuNjQ4LDEuNzEgLTE3LjUyNCwzLjUzIC0yMC42MjQsNy4xNCAtMy4wNCwzLjUyIC0zLjcyOCw2LjM5IC00LjY4LDEyLjkzIC0wLjYyNCw0LjU3IC0wLjg2NCw3Ljg4IC0xLjA4NCwxMC43NCAtMC4wNCwwLjQ2IC0wLjA0LDAuOTUgMC4xMiwxLjI5IDAuMiwxLjI1IDAuMiwyLjkgMC4yLDMuNCAwLjA4LDEuMjkgMC4yLDIuMjQgMC4zMiwyLjk5IDAuMjMsMS4yOSAwLjUyLDEuODggMC45MiwyLjQ5IDAuNCwwLjYgMS40LDEuNjQgMi4wNCwyLjA4IDAuMjQsMC4yNCAyLjU2LDEuMzIgMi45MiwyLjA4IDEuMjQsMi40OCAxLjY4LDQuNzYgMi4zMiw4LjMyIDEuNTYsNy43NiAyLDguMjggMy41MiwxMS4zMiAxLjY0LDMuMjggMi41Miw0LjQ4IDMuNjgsNS4zMiAyLC41MiA1LjA4LDEuNTYgNy42OCwyLjE2IDEuMjgsLjI4IDUuMzIsMS45NiA2LjIsMy4xNiAuNzIsLjk1IDIuNDQsLjQ0IDcuMi0uMDQgNS43Ni0uMzYgOC43Mi0uNTYgMTAuMjgsLjI0ICAyLDEuNDggNy4wNCw3Ljk2IDguMzYsMTIuOCAxLjI4LDQuNTYgMS4yNCwxMC4wNCAyLjA0LDE5LjUyIC42NCw5LjY4IC44OCwyMC40OCAyLjQsMjcuNTYgMS4xMiw1LjYgMi4yNCwxMC42NCAzLjMyLDE0Ljk2IC44OCwzLjQ4IDIsNC40NiAzLjg4LDUuMzYgMi4wOCwuOTIgMy45NiwxLjI0IDcuNjgsMi42IDMuMjgsMS4wOCA2Ljg4LDIuNzIgOC4yNCw0LjQgLjUyLC41MiAuMzYsMS4xMiAyLjI4LDIuMzYgMS41MiwxLjIgMi42OCwxLjI4IDQuMjgsMi40IDQuODQsMi45NiA3LjMyLDUuNTYgMTEuNTIsOS4yNCAyLjg4LDIuNjggMy4yOCw0IDQuMTYsNC40OCAuNDQsLjEyIC42NCwuMzYgMS4zNiwxLjg4IDEuNjQsMy42OCAyLjY0LDUuMjQgNC4zNiw4Ljg0IC42OCwxLjQ0IC43MiwyLjY0IC44NCwzLjQ4IC4zMiwzLjIgLjc2LDUuMiAyLjI4LDExLjI0IC40OCwxLjc2IC42OCwyLjkyIC44OCw0IC4zMiwyLjUyIC44NCw0LjA0IC44NCw0LjA0IC4zNiwxLjUyIC41MiwyLjk2IDEuMTIsNC40NCAuODgsMi4xMi43MiwyLjg0IDAsNC44OC0xLjEyLDQuMzIgLS44OCw1LjUyIC0uMjQsNy42IC44OCwyLjggMS4wNCwzLjYgLjUyLDQuNC0uNTYsLjA4IC0xLjQ0LC42IC01LjA0LC44IC0zLjA4LC4wNCAwLC4xNiAwLC4xNlpoTTM5MTQuMjUsODkwLjY2Yy0xLjUyLC0uNTYgLTIuMjQsLTEuMDggLTMuMzYsLTIuMjggLTEuOTYsLTIuNjggLTMuOTYsLTMuNTYgLTQuMjgsLTQuMTIgLTEuMjgsLS44NCAtMi4yNCwtMi4yOCAtMy4yNCwtNC4zMiAtLjI0LC0uNjggLS4yNCwtMS4zMiAtLjI4LC0yLjA4IC0uMjgsLTIuMTYgLS40LC00LjkyIC0uNTYsLTYuMjQgLS4wNCwtMSAuMjgsLTIgLjA0LC0zLjY4IC0uMjgsLTEuMjggLS4yOCwtMi42IC0uNCwtNC4wOCAtMS4wOCwtMS44IC0uNTIsLTI4LjggLjI0LC0zNy45MiAuNCwtNC44NCAtLjI4LDEuMjggLjItNC4yOCAuMTYsLTEuMjggLjUyLC0yLjkyIDEuNiwtNC4yNCAuNTYsLS44OCAzLjQsLTMuODggNS42OCwtMy41Ni4xNiwwIC40NiAuMTYsLjcxIC4yOC0uMTIsLS42NiAuMDgsLTIuNTggLjE2LC0zLjA0IC4yLC0yIC43NiwtNC4zMiAyLC03IC40OC0xLjEyIC44OC0xLjg0IDEuNTYsLTIuNTYgLjkyLC0uNzIgMS42LC0xLjA4IDIuMjgsLTIuMjggLjI0LC0uNC40OC0uOTYgMS4xMiwtMS4wOC49Ni0uMjQgMS42OCwuMjggMi42OCwuMjggMS4zMiwuMDgsMS4zMi0uMTYsMi4xNi0uMjguNTItLjEyIC44LC0uMTYgMS4zMi0uNTYgLjQsLS4yNCAxLjEyLC0uMjggMS40NC0uNDggLjk2LC0uNTIgMi4yOCwtMS4xMiA0Ljc2LC0yLjQ0IC4yOC0uMTIgMi45Mi0xLjg0IDMuNTYsLTMuNTYgLjUyLC0xLjU2IDEuMzIsLTMuMjQgMS4yOCwtNS4xNiAwLC0uMzItLjEyLTEuMDQtLjEyLTIuNTYgLjA4LC0xIDAsLTIgLjI0LC0zLjU2IC4yOCwtMS4xMiAuMTYsLTIuNzIgMCwtNC4xMiAuNTYsMC0uMDQsMS42NC0uMjQsMi42NS0uMDgsLjUyIC0uMTYsMS4wNCAuMjQsMS40IC4yNCwuMjggMS4wOCwuNDggMS40NCwuNDggLjk2LCAwIDIuMzIsLTEuMTYgMi41MiwtMiAuMjQsLS45MiAuMjgsLTIuNzIgLjI4LC00LjQgLjA0LC0uMjggLjA0LC0uNjggLjI4LC0xLjIgMS40NCwtMi42NCAyLjI0LC00LjA4IDMuMjgsLTUuNTYgLjc2LC0xLjQ0IDEuMzIsLTMuNTYgMi4yNCwtNi44IC4zMi0xLjMzIC41Mi0yLjcgLjgtNC4wMiAuMjgtMS4zMiAuNTItMi42IDEuMDQsLTMuNjggLjk2LC0yLjIgMi4xMiwtNC4yNCAzLC03LjUyIC4yOC0xLjIxIC41Ni0yLjQzIC44NC0zLjc4IC4yNC0xLjM3IC40NC0yLjc4LTEuMiwtMy41IC0uNjQsLS4yNSAtMS4yOCwtLjUzIC0xLjc2LS43NyAtMS4wOCwtLjUyIC0yLjkyLC0yIC01LjYsLTEuNTYgLTEuMjgsLjI4IC0yLjYsLjIgLTMuNzYsLjQ0IC0uNjgsLjA4IC0yLjk2LDEuMiAtMy4wNCwxLjQgLTEuNjgsMi4wNCAtMi44OCw0LjkyIC00LjcyLDcuOTIgLTEuNjgsMi45MiAtMi40NCwzIC00LjYsNS40IC0xLjc2LDIuMTIgLTIuNzIsNC4zMiAtNS4xMiw3LjI4IC0zLjQsNCAtNS42LDYuNTYgLTEwLjIsMTAuNTIgLTIuOTIsMi44IC00LjQ0LDUuNjggLTYuNTYsOS4yOFoiLz48L3N2Zz4%3D&labelColor=0B1020&logoColor=F7FAFC)](https://github.com/Capacium/capacium)
[![CI](https://github.com/LangeVC/txtHumanizer/actions/workflows/ci.yml/badge.svg)](https://github.com/LangeVC/txtHumanizer/actions/workflows/ci.yml)
[![Capacium Validate](https://img.shields.io/badge/Capacium-Validate-blue)](https://github.com/Capacium/capacium-action-validate)
[![Capacium Publish](https://img.shields.io/badge/Capacium-Publish-blue)](https://github.com/Capacium/capacium-action-publish)

Drei-Stufen-Humanizer für deutschsprachige Texte. Erkennt und entfernt KI-typische
Muster auf Basis der **Wikipedia KI-Erkennung – Systemkonfiguration v1.35**.

```
ANALYSE → RECOMMEND → FINETUNE
```

## Quickstart

### Via Capacium (Recommended)

```bash
# Install Capacium
brew install capacium/tap/capacium

# Install txtHumanizer
cap install LangeVC/txtHumanizer
```

### Via Git (Alternative)

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/LangeVC/txtHumanizer.git ~/.claude/skills/txtHumanizer
```

### Via npx skills

```bash
npx skills add LangeVC/txtHumanizer
```

## Usage

```
/humanizer [Text einfügen]
```

Oder direkt:

```
Bitte humanize diesen Text: [dein Text]
```

## Die drei Stufen

| Stufe | Funktion | Beschreibung |
|---|---|---|
| **1. ANALYSE** | Erkennung | Evidenzbasierte KI-Muster-Erkennung mit Punktesystem (0–10) + Longlist (A1–D4) |
| **2. RECOMMEND** | Empfehlung | Belegbasierte Änderungsempfehlungen pro Kriterium mit vorher/nachher |
| **3. FINETUNE** | Überarbeitung | Zielgerichtete Anwendung mit 7 konfigurierbaren Stil-Reglern |

## Stil-Regler

| Regler | Optionen |
|---|---|
| **Domäne** | alltag, business, akademisch, journalistisch, literarisch, technisch |
| **Formalität** | formell, neutral, informell |
| **Persönlichkeit** | nüchtern, moderat, ausdrucksstark |
| **Texttreue** | konservativ, ausgewogen, mutig |
| **Satzbau** | minimal, moderat, maximal |
| **Kreativität** | standard, kreativ, experimentell |
| **Seele** | keine, leicht, stark |

## Kriterienkatalog

### Schnelltest (10 Kriterien)

| # | Kriterium | Beschreibung |
|---|---|---|
| K1 | Glatte Einleitung | Formelhafte Eröffnung ohne spezifische Fakten |
| K2 | Metafloskeln | „Es ist wichtig zu betonen …" |
| K3 | Konnektoren-Inflation | „darüber hinaus", „zudem", „folglich" gehäuft |
| K4 | Gleichförmiger Satzrhythmus | Gleiche Satzlängen und Strukturen |
| K5 | Dreierlisten | „X, Y und Z" als Standardmuster |
| K6 | „Nicht nur … sondern auch" | Schema­tische Verstärkungsstruktur |
| K7 | Vage Zuschreibungen | „Experten sagen", „Studien zeigen" ohne Quelle |
| K8 | Standard-Abschnitte | „Herausforderungen", „Zukunftsperspektiven" |
| K9 | Gleichförmige Absätze | 3–5 Sätze pro Absatz, identisch aufgebaut |
| K10 | Zu perfekte Übergänge | Didaktisch geglättete Absatzverknüpfungen |

### Deutsche Spezifika (4 Zusatzkriterien)

| # | Kriterium | Beschreibung |
|---|---|---|
| K11 | Anglizismen/Denglisch | „Sinn machen", „in 2024", übermäßige -ieren-Verben |
| K12 | Nominalstil | Extrem verdichtete Nominalphrasen |
| K13 | Partizipialkonstruktionen | Gehäufte „-end"-Formen |
| K14 | KI-Vokabular (DE) | „entscheidend", „vielschichtig", „tiefgreifend" |

### Longlist (optional, 29 Kriterien A1–D4)

Tiefenprüfung nach der deutschen Wikipedia-Longlist — Qualitätsprobleme (A),
stilistische Merkmale (B–C), Hinweise auf menschliche Erstellung (D).

## Beispiel

**Vorher (KI-generiert):**
> Künstliche Intelligenz ist ein bedeutendes und vielschichtiges Themenfeld,
> das in den letzten Jahren zunehmend an Bedeutung gewonnen hat. Es ist wichtig
> zu betonen, dass KI nicht nur die Art und Weise, wie Unternehmen arbeiten,
> grundlegend verändert, sondern auch tiefgreifende Auswirkungen auf die
> Gesellschaft als Ganzes hat. Darüber hinaus zeigen Studien, dass der Einsatz
> von KI-Technologien zu einer signifikanten Steigerung der Effizienz,
> Produktivität und Innovationskraft führen kann.

**Nachher (humanisiert, Modus: business):**
> KI verändert Unternehmensabläufe spürbar. Ein Werkzeugbauer aus Baden-
> Württemberg hat 2024 seine Fertigungsplanung auf ein KI-System umgestellt
> und die Durchlaufzeit um 23 Prozent gesenkt. Ähnliches berichten Logistiker:
> KI-gestützte Routenplanung spart im Schnitt 15 Prozent Kraftstoff.

## Referenzen

- [Wikipedia:WikiProjekt KI und Wikipedia/Schnelltest KI (v1.35)](https://de.wikipedia.org/wiki/Wikipedia:WikiProjekt_KI_und_Wikipedia/Schnelltest_KI)
- [Wikipedia:WikiProjekt KI und Wikipedia/Erkennung KI-Einsatz (Longlist)](https://de.wikipedia.org/wiki/Wikipedia:WikiProjekt_KI_und_Wikipedia/Erkennung_KI-Einsatz)
- [Wikipedia:Signs of AI writing (en)](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Humanizer Skill by @blader](https://github.com/davila7/claude-code-templates)
- [Capacium – Capability Packaging System](https://github.com/Capacium/capacium)

## Lizenz

MIT
