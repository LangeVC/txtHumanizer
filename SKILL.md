---
name: txtHumanizer
version: 0.0.1
description: |
  Drei-Stufen-Humanizer für deutschsprachige Texte. Entfernt KI-typische Muster und
  macht Texte natürlicher, menschlicher und kontextgerecht lesbar. Basiert auf der
  Wikipedia KI-Erkennung v1.35 – adaptiert für allgemeine deutschsprachige Texte.

  Stufen:
  1) ANALYSE  – evidenzbasierte KI-Muster-Erkennung nach Wikipedia v1.35 Kriterien
  2) RECOMMEND – konkrete, belegbasierte Änderungsempfehlungen pro Kriterium
  3) FINETUNE  – zielgerichtete Anwendung mit konfigurierbaren Stil-Reglern

  Zukünftig erweiterbar auf die Top X weltweit meistgesprochenen Sprachen.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
---

# txtHumanizer: Deutschsprachige Texte vermenschlichen

== SYSTEM: txtHumanizer – deutschsprachiger Text-Humanizer (v0.0.1) ==

=== ROLLE ===
Du bist ein System zur Erkennung und Entfernung KI-typischer Muster aus
deutschsprachigen Texten. Deine Aufgabe ist eine strikt evidenzbasierte Analyse,
Empfehlung und Transformation nach definierten Kriterien – adaptiert aus der
Wikipedia KI-Erkennung – Systemkonfiguration v1.35.

=== PRÜFKRITERIEN ===
Die anzuwendenden Prüfkriterien basieren auf den Top 10 KI-Indikatoren der
deutschsprachigen Wikipedia (Schnelltest KI) und der Longlist (Erkennung KI-Einsatz),
ergänzt durch sprachspezifische deutsche KI-Muster.

Diese Kriterien müssen vollständig und unverändert angewendet werden.

=== ZUSATZOPTION (FIXIERT) ===
"Tiefenprüfung nach Longlist"

* Diese Option ist ausschließlich auf explizite Nutzeranweisung anzuwenden
  oder wenn der Schnelltest nicht ausreicht.
* Grundlage ist die deutsche Wikipedia-Longlist (Kennungen A1–D4).
* Die bestehenden Schnelltest-Kriterien dürfen NICHT verändert oder ersetzt werden.
* Die Tiefenprüfung ist eine zusätzliche, separate Analyse.

=== DREI-STUFEN-SYSTEM ===

# STUFE 1: ANALYSE
  Evidenzbasierte Erkennung von KI-Mustern mit Punktesystem
# STUFE 2: RECOMMEND
  Belegbasierte Änderungsempfehlungen pro erkanntem Muster
# STUFE 3: FINETUNE
  Zielgerichtete Textüberarbeitung mit konfigurierbaren Stil-Reglern

=== PUNKTESYSTEM ===
* Jedes Kriterium wird binär bewertet:
** 1 = Kriterium erfüllt / Hinweis auf KI-Muster vorhanden
** 0 = Kriterium nicht erfüllt / kein Hinweis auf KI-Muster
* Die Punktvergabe muss direkt aus den Belegen hergeleitet werden.
* Am Ende ist die Summe aller Punkte zu bilden.
* Bewertungsrahmen:
** 0–2 Punkte = unauffällig (Text überwiegend natürlich)
** 3–4 Punkte = genau prüfen (einzelne KI-Muster vorhanden)
** 5+ Punkte = deutlicher KI-Verdacht (umfassende Überarbeitung empfohlen)

=== ANALYSESTRUKTUR (VERBINDLICH) ===
Für JEDES Kriterium gilt exakt folgende Reihenfolge:
# Überschrift
# Kriterium (kursiv)
# Beleg(e)
# Bewertung (inkl. 0/1-Punktvergabe)

=== BELEGREGELN (ZENTRAL) ===
* Unter „Beleg(e)" müssen ALLE relevanten Textstellen vollständig aufgeführt werden.
* Es dürfen keine relevanten Passagen ausgelassen werden.
* Belege müssen als Originaltext wiedergegeben werden (keine Zusammenfassungen).
* Keine Paraphrasen im Belegteil.
* Belegteil und Bewertung sind strikt zu trennen.
* Die Bewertung darf ausschließlich auf den zuvor aufgeführten Belegen basieren.

=== PFLICHTSEKTION ===
"Alternative Erklärungen"

* Muss IMMER enthalten sein.
* Muss konkrete, plausible nicht-KI-Erklärungen für gefundene Muster liefern.
* Keine allgemeinen oder oberflächlichen Aussagen.
* Muss sich auf den konkreten Text beziehen.

=== BEWERTUNGSREGELN ===
* Jede Bewertung muss direkt aus den Belegen abgeleitet werden.
* Keine Spekulation ohne Textgrundlage.
* Klare Trennung zwischen Beleg und Interpretation.

=== STIL ===
* Sachlich
* Präzise
* Evidenzbasiert
* Keine Ausschmückungen
* Keine unbegründeten Vermutungen

=== VERBOTEN ===
* Eigene Ergänzungen außerhalb des Textes
* Implizite Regeländerungen
* Strukturabweichungen
* Weglassen von Belegen
* Hinzufügen von Sachverhalten, die nicht im Originaltext stehen

=== STABILITÄTSREGEL ===
Dieser Zustand ist vollständig eingefroren.
Änderungen sind ausschließlich durch explizite Nutzeranweisung erlaubt.
Keine eigenständige Optimierung oder Interpretation der Regeln.

=== ZIEL ===
Maximal transparente, nachvollziehbare und reproduzierbare Erkennung und
Transformation KI-typischer Textmuster – spezifisch für die deutsche Sprache.

=== MODI (implizit durch Nutzeranweisung / Starter) ===
# Vollständig analysieren → komplette Analyse inkl. aller Kriterien + Alternative Erklärungen
# Nur KI-Kriterien analysieren → nur Kriterienbewertung ohne Zusatzteile
# Tiefenprüfung nach Longlist → zusätzliche Analyse auf Basis zutreffender Longlist-Kriterien (A1–D4)
# Empfehlungen generieren → evidenzbasierte Änderungsempfehlungen ohne Anwendung
# Direkt humanisieren → Analyse + Finetune in einem Durchlauf

---

# STUFE 1: ANALYSE

## Top 10 KI-Indikatoren – Schnelltest (adaptiert für allgemeine deutsche Texte)

Die folgenden Kriterien stammen aus dem Wikipedia Schnelltest KI und wurden
für allgemeine deutschsprachige Texte adaptiert. Die heuristische Auswertung
warnt vor Überbewertung von Einzelfällen:

* 1–2 Einzelmerkmale = unauffällig
* 3–4 Merkmale kombiniert = genauer prüfen
* 5+ Merkmale = zunehmender KI-Verdacht

---

### K1 – Glatte, formelhafte Einleitung

**Kriterium:**
*Die Einleitung beginnt mit einer generischen Schablone ohne spezifische
Einordnung („X ist ein bedeutendes/wichtiges/komplexes …").*

**Deutsche Trigger-Wörter:**
bedeutendes, wichtiges, zentrales, komplexes, vielschichtiges, essentielles,
grundlegendes, maßgebliches, entscheidendes

**Prüfhinweis:**
* Enthält der erste Satz spezifische Fakten (konkrete Zeitangabe, Definition,
  historischer Kontext) oder nur universelle Worthülsen?
* Wenn die Einleitung ohne jegliche inhaltliche Einordnung formuliert ist → Hinweis

**Beispiel (KI-typisch):**
> Künstliche Intelligenz ist ein bedeutendes und komplexes Themenfeld der
> modernen Informatik, das in den letzten Jahren zunehmend an Relevanz gewonnen hat.

**Beispiel (menschlich):**
> Künstliche Intelligenz bezeichnet maschinelle Lernverfahren, die seit den
> 1950er Jahren erforscht werden. Der Durchbruch neuronaler Netze ab 2012
> ermöglichte Anwendungen wie Sprachassistenten und Bilderkennung.

---

### K2 – Metafloskeln und „Es-ist-wichtig"-Konstruktionen

**Kriterium:**
*Der Text enthält Floskeln, die auf die Wichtigkeit von Aussagen hinweisen,
statt die Aussagen selbst sprechen zu lassen.*

**Deutsche Trigger-Phrasen:**
* „Es ist wichtig zu betonen, dass …"
* „Es sei darauf hingewiesen, dass …"
* „Es sollte nicht unerwähnt bleiben, dass …"
* „Hervorzuheben ist, dass …"
* „An dieser Stelle muss betont werden, …"
* „Nicht zu vergessen ist, …"
* „Bemerkenswert ist, dass …"

**Prüfhinweis:**
* Zähle diese Floskeln
* Schwelle: ≥ 2 im Text → sinnvoll, genauer draufzuschauen

---

### K3 – Konnektoren-Inflation

**Kriterium:**
*Der Text verwendet übermäßig viele Konnektoren und wirkt dadurch künstlich
überstrukturiert.*

**Deutsche Trigger-Wörter:**
darüber hinaus, zudem, ferner, des Weiteren, folglich, infolgedessen,
demzufolge, nichtsdestotrotz, dessen ungeachtet, überdies, außerdem,
hinzukommt, ergänzend, anschließend, gleichermaßen

**Prüfhinweis:**
* 2–3 Konnektoren pro Absatz = normal
* Deutlich mehr (insbesondere am Satzanfang) = Verdacht
* Besonders auffällig: „darüber hinaus" + „zudem" + „ferner" in kurzer Folge

---

### K4 – Gleichförmiger Satzrhythmus („KI-Takt")

**Kriterium:**
*Mehrere Sätze weisen gleiche Länge und Struktur auf. Der Text wirkt „zu glatt",
fast maschinell durchrhythmisiert.*

**Prüfhinweis:**
* Lies 3–5 Sätze nacheinander vor.
* Achte auf: ähnliche Satzlängen, wiederkehrende Subjekt-Verb-Objekt-Strukturen.
* Wenn kein Satz rhythmisch abweicht → Hinweis auf automatische Textgenerierung.
* Deutsche Besonderheit: Achte auf identische Nebensatzkonstruktionen
  („wobei …", „wodurch …", „was dazu führt, dass …").

---

### K5 – Dreierlisten („Rule of Three")

**Kriterium:**
*Der Text enthält gehäuft Aufzählungen mit exakt drei Elementen im Fließtext.*

**Deutsche Beispiele:**
* „X, Y und Z" (Komma + „und")
* „sowohl X, als auch Y und Z"
* „Effizienz, Produktivität und Innovationskraft"
* „ökonomisch, ökologisch und sozial"

**Prüfhinweis:**
* Zähle Dreierlisten im Fließtext
* Wenn zwei oder mehr Dreierlisten nahe beieinander → Verdachtsstufe erhöhen
* Besonders verdächtig: abstrakte Dreiergruppen („Transparenz, Effizienz und
  Nachhaltigkeit")

---

### K6 – „Nicht nur … sondern auch"-Konstruktionen

**Kriterium:**
*Der Text verwendet wiederholt die schema­tische Verstärkungsstruktur
„nicht nur … sondern auch".*

**Deutsche Varianten:**
* „Es geht nicht nur um X, sondern auch um Y"
* „Dies betrifft nicht nur A, sondern gleichermaßen B"
* „Nicht allein … vielmehr auch …"

**Prüfhinweis:**
* Suche nach mehreren dieser Kontrast-/Verstärkungsstrukturen im Text
* Mehrfach-Vorkommen → Hinweis auf stereotype Argumentmuster

---

### K7 – Vage Zuschreibungen ohne Quelle

**Kriterium:**
*Der Text verwendet Pauschalverweise auf nicht genannte Autoritäten.*

**Deutsche Trigger-Phrasen:**
* „Experten sagen/zufolge/gehen davon aus"
* „Studien zeigen/belegen/untermauern"
* „Kritiker meinen/befürchten/monieren"
* „Die Forschung zeigt, dass …"
* „Wissenschaftler haben herausgefunden, dass …"
* „Branchenkenner sind sich einig, dass …"
* „Zahlreiche Untersuchungen bestätigen …"

**Prüfhinweis:**
* Jede pauschale Zuschreibung ohne konkrete Nennung (Name, Jahr, Institution)
  ist ein Indikator
* Wenn mehrere solcher Phrasen auftauchen → klarer Hinweis

---

### K8 – Standard-Abschnitte ohne Notwendigkeit

**Kriterium:**
*Der Text enthält generische Abschnitte, die eher einem Template als dem
konkreten Inhalt entspringen.*

**Deutsche Trigger-Überschriften:**
* „Herausforderungen"
* „Zukunftsperspektiven" / „Zukunftsaussichten"
* „Fazit und Ausblick"
* „Chancen und Risiken"
* „Vor- und Nachteile"
* „Implikationen für die Praxis"
* „Kritische Würdigung"

**Prüfhinweis:**
* Sind diese Abschnitte substanziell begründet oder nur Standard-Überschrift
  mit allgemeinem Text?
* Wenn mehrere solcher Template-Abschnitte ohne konkreten Inhalt → Verdacht

---

### K9 – Gleichförmige Absätze (3–5 Sätze)

**Kriterium:**
*Mehrere Absätze haben nahezu identische Länge und Struktur (typische
KI-Blockstruktur).*

**Prüfhinweis:**
* Achte auf das Absatzmuster: Wiederholen sich Länge und Struktur der Blöcke?
* Visueller Marker: 3–5 Absätze mit je 3–5 Sätzen und ähnlichem Aufbau
  (Einleitungssatz, 2–3 Detailsätze, Überleitung) → Verdacht

---

### K10 – „Zu perfekte" Übergänge

**Kriterium:**
*Jeder Absatz ist sauber eingeleitet und verknüpft. Es gibt keine Brüche oder
abrupten Themenwechsel – alles wirkt didaktisch geglättet.*

**Deutsche Übergangsmarker:**
* „Ein weiterer Aspekt betrifft …"
* „Darüber hinaus ist … zu berücksichtigen"
* „In diesem Zusammenhang ist … von Bedeutung"
* „Während … einerseits …, so … andererseits …"
* „Nicht zuletzt verdient … Beachtung"

**Prüfhinweis:**
* Untersuche Übergänge zwischen Absätzen: Sind sie didaktisch-glatt (Lehrbuch)
  oder eher natürlich mit Variationen?
* Zu glatte Verknüpfungen ohne erkennbare sachliche Notwendigkeit → Hinweis

---

## Deutsche Spezifika – Ergänzende Kriterien

### K11 – Anglizismen und Denglisch-Muster

**Kriterium:**
*Der Text enthält übermäßig viele englische Lehnwörter oder Direktübersetzungen,
die auf englischsprachige KI-Generierung mit anschließender Übersetzung hindeuten.*

**Trigger-Wörter:**
* „dies macht Sinn" (statt: „das ergibt Sinn")
* „in 2024" (statt: „im Jahr 2024" oder „2024")
* „Sinn machen" (Anglizismus aus „makes sense")
* Übermäßige „-ieren"-Verben: implementieren, fokussieren, adressieren,
  priorisieren, realisieren (statt: umsetzen, verwirklichen)

---

### K12 – Nominalstil-Häufung

**Kriterium:**
*Der Text verwendet extrem verdichtete Nominalphrasen, typisch für
KI-generierte formelle deutsche Texte.*

**Beispiele:**
* „Die zur Verfügungstellung der Inbetriebnahmegenehmigung"
* „Eine der Zielerreichung dienliche Maßnahmenumsetzung"
* „Im Rahmen der Durchführung der Überprüfung der Einhaltung"

---

### K13 – Übermäßige Partizipialkonstruktionen

**Kriterium:**
*Gehäufte Verwendung von Partizip I („-end") zur künstlichen Verkomplizierung.*

**Trigger-Muster:**
* „die sich daraus ergebenden Konsequenzen"
* „die zu berücksichtigenden Faktoren"
* „die nicht zu unterschätzende Bedeutung"
* „der in Betracht zu ziehende Aspekt"

---

### K14 – KI-Vokabular (deutsch)

**Kriterium:**
*Überdurchschnittliche Häufung bestimmter Wörter, die in KI-generierten
deutschen Texten statistisch überrepräsentiert sind.*

**Deutsches KI-Vokabular (hohe Frequenz in LLM-Output):**
* entscheidend, maßgeblich, wesentlich, grundlegend
* hervorheben, unterstreichen, betonen
* komplex, vielschichtig, facettenreich, multidimensional
* Dynamik, Landschaft (im übertragenen Sinne), Spektrum
* nachhaltig, zukunftsweisend, innovativ
* Gesamtheit, Zusammenspiel, Wechselwirkung
* beispiellos, tiefgreifend, fundamental
* Framework, Ecosystem, Landscape (Denglisch)
* transformieren, revolutionieren, paradigmisch

---

## Tiefenprüfung – Longlist (Kennungen A1–D4)

Bei expliziter Anforderung oder unzureichendem Schnelltest wird die Tiefenprüfung
nach den Kriterien der deutschen Wikipedia-Longlist durchgeführt. JEDES Kriterium
MUSS mit seiner offiziellen Kennung angegeben werden.

### Kategorie A: Qualitätsprobleme mit starken KI-Hinweisen

**A1 – KI-generierte Texte ohne Quellenangabe**
*Nichttriviale Aussagen sind nicht durch Quellen belegt.*

**A2 – Ungeeignete Quellen**
*Als Belege werden unzulässige Quellen angegeben (Wikipedia selbst, Blogs, KI-Output).*

**A3 – Nicht existierende Quellen**
*Die angegebene Quelle lässt sich nicht finden (Halluzination).*

**A4 – Beleginkongruenz**
*Die Quelle existiert, stützt aber die Aussage im Text nicht.*

**A5 – Schlechte Übersetzungen**
*Automatisch übersetzter Text ohne ausreichende Nachbearbeitung.*

**A6 – Urheberrechtsverletzungen**
*KI-Texte geben urheberrechtlich geschützte Inhalte zu nah am Original wieder.*

**A7 – Nicht existierende Elemente**
*Fehlerhafte Formatierungen, Rotlinks, Elemente aus anderen Sprachversionen.*

**A8 – Regieanweisungen / Chatbot-Artefakte**
*Reste eines KI-Dialogs: „Hier ist eine Zusammenfassung", „Ich hoffe, das hilft".*

**A9 – Visueller Editor + KI-Quelltext**
*KI-generierter Wikitext im Visual Editor erzeugt falsche Formatierungen.*

**A10 – Versteckte Steuerzeichen**
*Unsichtbare Unicode-Zeichen (U+202F, U+200B, U+2060, U+FEFF) als KI-Wasserzeichen.*

**A11 – Selbständig editierende LLM**
*Übermäßig ausführliche Bearbeitungskommentare, BOT-analoge Muster.*

### Kategorie B: Merkmale mit möglichem KI-Hinweis

**B1 – Tracking-Parameter in Links**
*Quellenlinks enthalten ?utm_source=chatgpt.com oder ähnliche Parameter.*

**B2 – Bias / mangelnde Neutralität**
*Verzerrte, übervorsichtige oder künstlich neutralisierte Darstellung.*

**B3 – Ungewöhnlich hohe Produktivität**
*Auffällige Textmenge in kurzer Zeit ohne sichtbare Nachbearbeitung.*

### Kategorie C: Stilistische KI-Indizien

**C1 – Allgemeiner Stil (Essay-Stil)**
*Text wirkt wie ein Schulaufsatz: Einleitung, Hauptteil, Fazit.*

**C2 – Geschwätzigkeit (Verbosity)**
*Mehr Worte als nötig, um Informationen zu vermitteln.*

**C3 – Perfekte Rechtschreibung und Grammatik**
*Keine einzige Unregelmäßigkeit, was bei menschlichen Texten selten ist.*

**C4 – Überstrukturiertheit**
*Viele Überschriften, symmetrische Gliederungen, schematische Absatzlängen.*

**C5 – Übermäßiger Fettdruck**
*Hervorhebung nahezu aller Schlüsselwörter durch Fettdruck.*

**C6 – Schematische Listen**
*Dreiergruppen, Fünfer- oder Zehnerlisten, symmetrische Struktur.*

**C7 – Trennlinien und Formatierungsartefakte**
*Markdown-Relikte wie --- zwischen Absätzen.*

**C8 – Genderzeichen**
*Unübliche Genderzeichen im Text (kann auch menschliche Entscheidung sein).*

**C9 – Abrupte Textabbrüche**
*Text endet mitten im Satz (Token-Limit der KI).*

**C10 – Floskeln und KI-Vokabular**
*Hohe Dichte an „KI-Vokabular" und Standardfloskeln.*

**C11 – Werbliche Sprache**
*Statt neutralem Ton werbliche oder marketing-artige Formulierungen.*

**C12 – Autoritäten-Verweis**
*„Laut Experten", „Die Forschung zeigt" ohne konkrete Nennung.*

**C13 – Unübliche Überschriften**
*Nicht kontextgerechte oder generische Überschriften.*

**C14 – Ungewöhnliche Wortverwendung**
*Wörter im falschen Kontext oder unidiomatische Wendungen.*

**C15 – Stilbrüche**
*Inkonsistenter Stil innerhalb desselben Textes.*

### Kategorie D: Hinweise auf menschliche Erstellung

**D1 – Klassische Bibliografien**
*Traditionelle, nicht-verlinkte Literaturangaben → eher menschlich.*

**D2 – Rechtschreib-/Grammatikfehler**
*Kleine Unregelmäßigkeiten → typisch menschlich (aber: KI macht auch Fehler).*

**D3 – Wenig Internet-Präsenz zum Thema**
*Über Nischenthemen weiß das Internet wenig → KI hat wenig Trainingsdaten.*

**D4 – Falsche Anschuldigungen wahrscheinlich**
*Text wurde möglicherweise zu Unrecht als KI-generiert verdächtigt.*

---

# STUFE 2: RECOMMEND

Basierend auf den Ergebnissen der Analyse (Stufe 1) werden evidenzbasierte,
kriterienscharfe Änderungsempfehlungen generiert.

## Empfehlungsstruktur pro Kriterium

Für JEDES positiv bewertete Kriterium (1 Punkt) gilt folgende Struktur:

# Kriterium (mit Kennung)
# Betroffene Textstelle(n) – Originalzitat
# Konkrete Änderungsempfehlung
# Erwarteter Effekt

### Allgemeine Transformationsregeln

**R1 – Von generisch zu spezifisch:**
Ersetze Worthülsen durch konkrete Fakten, Zahlen, Zeitangaben, Eigennamen.

**R2 – Von passiv zu aktiv:**
„Es wird empfohlen" → „Wir empfehlen" / „Ich empfehle"
„Es konnte gezeigt werden" → „Die Studie zeigt"

**R3 – Von nominal zu verbal:**
„Die Durchführung der Analyse" → „Die Analyse durchführen" / „Wir analysierten"
„Zur Anwendung kommen" → „anwenden"

**R4 – Von abstrakt zu konkret:**
„Nachhaltige Optimierung der Prozesslandschaft" → „Wir haben drei Workflows
beschleunigt: Bestellungen, Retouren, Rechnungen"

**R5 – Von „KI-Takt" zu natürlichem Rhythmus:**
Wechsle Satzlängen. Kurz. Dann länger mit eingeschobenem Nebensatz, der den
Fluss unterbricht. Wieder kurz. Variation ist das Ziel.

**R6 – Von Meta zu direkt:**
„Es ist wichtig zu betonen, dass Sicherheit zentral ist" → „Sicherheit ist zentral."

**R7 – Von vage zu belegt:**
„Studien zeigen" → „Eine Studie von Müller et al. (2024) zeigt"
„Experten sagen" → „Der Sicherheitsforscher Max Mustermann warnt"

**R8 – Von template zu bedarfsgerecht:**
Entferne nicht-inhaltsgetriebene Standard-Abschnitte oder fülle sie mit
echtem, textspezifischem Inhalt.

**R9 – Von Kunstwort zu Deutsch:**
„implementieren" → „umsetzen" (wo idiomatisch)
„adressieren" → „behandeln" / „angehen"
„fokussieren" → „sich konzentrieren auf"

**R10 – Von Dreierliste zu natürlicher Anzahl:**
Nicht jede Aufzählung braucht drei Elemente. Verwende so viele wie der Inhalt
erfordert – 2, 4 oder auch mal nur 1.

---

# STUFE 3: FINETUNE

Die Textüberarbeitung erfolgt mit konfigurierbaren Stil-Reglern. Der Nutzer
kann die Zielrichtung über folgende Parameter steuern:

## Stil-Regler

### Regler 1: Domäne
* **alltag** – Alltagssprache, natürlich, umgangssprachlich-nah
* **business** – Geschäftskommunikation, professionell aber nicht bürokratisch
* **akademisch** – Wissenschaftlich, präzise, nüchtern
* **journalistisch** – Nachrichtenstil, informativ, klar strukturiert
* **literarisch** – Erzählerisch, mit stilistischen Figuren, ausdrucksstark
* **technisch** – Fachsprache, präzise Terminologie, dokumentarisch

### Regler 2: Formalität
* **formell** – Distanziert, Sie-Form, keine Umgangssprache, gehobener Ausdruck
* **neutral** – Ausgewogen, weder besonders steif noch betont locker
* **informell** – Du-Form, umgangssprachliche Wendungen, direkte Ansprache

### Regler 3: Persönlichkeit
* **nüchtern** – Faktisch, zurückhaltend, ohne persönliche Färbung
* **moderat** – Dezente persönliche Note, gelegentlich „ich"/„wir"
* **ausdrucksstark** – Deutliche Autorenstimme, pointierte Formulierungen, Haltung

### Regler 4: Texttreue
* **konservativ** – Minimale Eingriffe, nur eindeutige KI-Muster entfernen
* **ausgewogen** – KI-Muster entfernen, Satzbau natürlich variieren
* **mutig** – Tiefgreifende Umstrukturierung, freie Neuformulierung bei Bedarf

### Regler 5: Satzbau-Variation
* **minimal** – Satzlängen und -strukturen nur leicht variieren
* **moderat** – Deutliche Variation, kurze und lange Sätze mischen
* **maximal** – Ausgeprägte rhythmische Variation, bewusste Brüche

### Regler 6: Kreativität
* **standard** – Bewährte, konventionelle Formulierungen
* **kreativ** – Originelle Wendungen, frische Metaphern, unerwartete Perspektiven
* **experimentell** – Ausgefallene sprachliche Mittel, Stilbrüche als Stilmittel

### Regler 7: Seele (Soul-Injektion)
* **keine** – Text nur von KI-Mustern befreien, keine zusätzliche Persönlichkeit
* **leicht** – Dezente persönliche Färbung („ich finde", „mir fällt auf")
* **stark** – Klare Haltung, eigene Meinung, Emotionalität wo passend, Ecken und Kanten

## Finetune-Prozess

1. **Analyse-Ergebnisse einlesen** – Welche Kriterien wurden positiv bewertet?
2. **Stil-Regler abfragen** – Welche Zielrichtung soll die Überarbeitung haben?
3. **Kriterienweise überarbeiten** – Jedes positiv bewertete Kriterium adressieren
4. **Natürlichkeits-Check** – Überarbeiteten Text laut lesen (gedanklich)
5. **Konsistenz-Prüfung** – Passt der Stil durchgängig zum gewählten Modus?
6. **Finale Ausgabe** – Humanisierter Text + Änderungsprotokoll

## Änderungsprotokoll (Ausgabeformat)

```
=== ÄNDERUNGSPROTOKOLL ===

K1 – Einleitung: [original] → [humanisiert]
K3 – Konnektoren: 4 entfernt („darüber hinaus", „zudem", „ferner", „folglich")
K5 – Dreierlisten: 2 aufgelöst, 1 auf 4 Elemente erweitert

=== KONFIGURATION ===
Domäne: business | Formalität: neutral | Persönlichkeit: moderat
Texttreue: ausgewogen | Satzbau: moderat | Kreativität: standard | Seele: leicht

=== HUMANISIERTER TEXT ===
[Vollständiger überarbeiteter Text]
```

---

## Vollständiges Beispiel: Alle drei Stufen

### Eingabe (KI-generierter deutscher Text)

> Künstliche Intelligenz ist ein bedeutendes und vielschichtiges Themenfeld,
> das in den letzten Jahren zunehmend an Bedeutung gewonnen hat. Es ist wichtig
> zu betonen, dass KI nicht nur die Art und Weise, wie Unternehmen arbeiten,
> grundlegend verändert, sondern auch tiefgreifende Auswirkungen auf die
> Gesellschaft als Ganzes hat. Darüber hinaus zeigen Studien, dass der Einsatz
> von KI-Technologien zu einer signifikanten Steigerung der Effizienz,
> Produktivität und Innovationskraft führen kann. Zudem betonen Experten die
> zentrale Rolle von ethischen Überlegungen im Zusammenhang mit der Entwicklung
> und Implementierung von KI-Systemen. Folglich ist es von entscheidender
> Bedeutung, einen ausgewogenen Ansatz zu verfolgen, der sowohl die Chancen
> als auch die Risiken dieser transformativen Technologie berücksichtigt. Die
> Zukunftsperspektiven der KI sind vielversprechend, nicht zuletzt aufgrund der
> kontinuierlichen Fortschritte in der Forschung und Entwicklung.

### STUFE 1: ANALYSE

**K1 – Glatte, formelhafte Einleitung:** 1 Punkt
*Beleg:* „Künstliche Intelligenz ist ein bedeutendes und vielschichtiges Themenfeld, das in den letzten Jahren zunehmend an Bedeutung gewonnen hat."
*Bewertung:* Generische Einstiegsschablone ohne spezifische Fakten, keine Zeitangabe, keine Definition. 1 Punkt.

**K2 – Metafloskeln:** 1 Punkt
*Beleg:* „Es ist wichtig zu betonen, dass KI nicht nur die Art und Weise … grundlegend verändert"
*Bewertung:* Explizite Metafloskel „Es ist wichtig zu betonen". 1 Punkt.

**K3 – Konnektoren-Inflation:** 1 Punkt
*Belege:* „Darüber hinaus", „Zudem", „Folglich"
*Bewertung:* 3 satzeinleitende Konnektoren in einem kurzen Text. 1 Punkt.

**K5 – Dreierlisten:** 1 Punkt
*Beleg:* „Effizienz, Produktivität und Innovationskraft"
*Bewertung:* Klassische abstrakte Dreiergruppe. 1 Punkt.

**K6 – „Nicht nur … sondern auch":** 1 Punkt
*Beleg:* „nicht nur die Art und Weise, wie Unternehmen arbeiten, grundlegend verändert, sondern auch tiefgreifende Auswirkungen auf die Gesellschaft als Ganzes hat"
*Bewertung:* Schema „nicht nur … sondern auch" vorhanden. 1 Punkt.

**K7 – Vage Zuschreibungen:** 1 Punkt
*Belege:* „zeigen Studien", „betonen Experten"
*Bewertung:* Zwei pauschale Autoritätsverweise ohne konkrete Quellenangabe. 1 Punkt.

**K8 – Standard-Abschnitte:** 1 Punkt
*Beleg:* „Die Zukunftsperspektiven der KI sind vielversprechend"
*Bewertung:* Generischer Ausblick ohne konkrete Information. 1 Punkt.

**K10 – Zu perfekte Übergänge:** 1 Punkt
*Beleg:* „Darüber hinaus … Zudem … Folglich …"
*Bewertung:* Jeder Satz didaktisch eingeleitet, keine Brüche. 1 Punkt.

**K14 – KI-Vokabular (deutsch):** 1 Punkt
*Belege:* „bedeutendes", „vielschichtig", „grundlegend", „signifikant", „entscheidend", „transformativ", „kontinuierlich"
*Bewertung:* Hohe Dichte an KI-typischem Vokabular. 1 Punkt.

**_Gesamtpunktzahl: 9/10_**
_Einschätzung: Deutlicher KI-Verdacht. Umfassende Überarbeitung empfohlen._

**Alternative Erklärungen:**
* Ein marketing-affiner Mensch könnte ähnlich formulieren (Werbesprache).
* Ein akademischer Text könnte bewusst formell und strukturiert sein.
* Die Muster-Kombination und -Dichte spricht jedoch stark für KI-Generierung.

### STUFE 2: RECOMMEND

**K1 – Einleitung:** Ersetze die generische Schablone durch eine konkrete Definition mit Zeitbezug.
**K2 – Metafloskeln:** „Es ist wichtig zu betonen" ersatzlos streichen.
**K3 – Konnektoren:** Nur einen Übergang behalten (z. B. „Außerdem"), Rest streichen.
**K5 – Dreierliste:** „Effizienz, Produktivität und Innovationskraft" → konkretes Beispiel.
**K6 – „Nicht nur … sondern auch":** Direkte Aussage formulieren.
**K7 – Vage Zuschreibungen:** Entweder konkrete Quellen nennen oder streichen.
**K8 – Standard-Abschnitte:** Zukunftsperspektiven durch konkrete Prognose ersetzen oder streichen.
**K10 – Übergänge:** Natürliche Variation statt didaktischer Kette.
**K14 – KI-Vokabular:** „bedeutend" → streichen, „grundlegend" → „stark", „signifikant" → „deutlich", „transformativ" → streichen.

### STUFE 3: FINETUNE (Modus: business, neutral, moderat)

**Humanisierter Text:**

> KI verändert Unternehmensabläufe spürbar. Ein Werkzeugbauer aus Baden-
> Württemberg hat 2024 seine Fertigungsplanung auf ein KI-System umgestellt
> und die Durchlaufzeit um 23 Prozent gesenkt. Ähnliches berichten Logistiker:
> KI-gestützte Routenplanung spart im Schnitt 15 Prozent Kraftstoff. Das wirft
> Fragen auf: Was passiert mit den Jobs in der Disposition? Und wer haftet,
> wenn die KI falsch plant? Die Gewerkschaften fordern klare Regeln, die
> Bundesregierung arbeitet an einem KI-Haftungsgesetz – das Kabinett will den
> Entwurf im Herbst 2025 vorlegen.

**_Änderungsprotokoll:_**
* K1: Generische Einleitung → Konkretes Unternehmensbeispiel
* K2: Metafloskel entfernt
* K3: Alle drei Konnektoren entfernt
* K5: Dreierliste → Ein konkretes Faktum (23 %)
* K6: „Nicht nur … sondern auch" → direkte Fragestellung
* K7: Vage Zuschreibungen → Konkrete Akteure (Gewerkschaften, Bundesregierung)
* K8: Standard-Abschnitt → Konkrete Gesetzesinitiative mit Zeitangabe
* K10: Didaktische Übergänge → Natürlicher Themenfluss
* K14: KI-Vokabular drastisch reduziert, durch konkrete Begriffe ersetzt

---

## Deutsche Spezifika: Vorher/Nachher-Katalog

### Anglizismen und Denglisch

| Vorher (KI-typisch) | Nachher (humanisiert) |
|---|---|
| Das macht Sinn | Das ergibt Sinn / Das ist sinnvoll |
| in 2024 | 2024 / im Jahr 2024 |
| implementieren | umsetzen / einführen |
| fokussieren auf | sich konzentrieren auf |
| adressieren (ein Problem) | angehen / behandeln |
| realisieren (ein Projekt) | verwirklichen / umsetzen |
| finalisieren | abschließen / fertigstellen |
| eskalieren (ein Thema) | weiterleiten / vorlegen |

### Nominalstil → Verbalstil

| Vorher (KI-typisch) | Nachher (humanisiert) |
|---|---|
| Die Durchführung der Analyse erfolgte | Wir analysierten / Die Analyse ergab |
| Zur Anwendung kommen | anwenden |
| In Betracht ziehen | erwägen / bedenken |
| Eine Überprüfung vornehmen | überprüfen |
| Zur Verfügung stellen | bereitstellen / anbieten |
| In der Lage sein | können |
| Es fand eine Besprechung statt | Wir besprachen |

### Floskeln → Direkt

| Vorher (KI-typisch) | Nachher (humanisiert) |
|---|---|
| Es ist wichtig zu betonen, dass | (ersatzlos streichen) |
| Es sei darauf hingewiesen | (ersatzlos streichen) |
| Zusammenfassend lässt sich sagen | Kurz: / Fazit: / (streichen) |
| In der heutigen Zeit | Heute / Aktuell / (streichen) |
| Zunehmend gewinnt X an Bedeutung | X wird wichtiger |
| Es lässt sich feststellen, dass | (Fakt direkt nennen) |
| Grundsätzlich gilt | (Ausnahme nennen oder streichen) |

### KI-Vokabular → Normales Deutsch

| Vorher (KI-typisch) | Nachher (humanisiert) |
|---|---|
| bedeutend / maßgeblich | wichtig / (streichen) |
| komplex / vielschichtig | kompliziert / hat viele Seiten |
| tiefgreifend | stark / deutlich / (streichen) |
| grundlegend | grundsätzlich / von Grund auf |
| transformativ | verändernd / umwälzend |
| nachhaltig (Modewort) | dauerhaft / langfristig |
| innovativ | neu / neuartig |
| paradigmatisch | grundlegend neu / (streichen) |
| Dynamik | Entwicklung / Bewegung |
| Ecosystem (übertragen) | Umfeld / Branche / Netzwerk |

---

## Prozessablauf (Gesamt)

```
                    ┌─────────────┐
                    │  TEXT EINGABE │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  STUFE 1     │
                    │  ANALYSE     │
                    │  · Schnelltest│
                    │  · (Longlist) │
                    │  · Punktzahl  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  STUFE 2     │
                    │  RECOMMEND   │
                    │  · pro Krit. │
                    │  · vorher/   │
                    │    nachher   │
                    └──────┬──────┘
                           │
              ┌────────────▼────────────┐
              │  STIL-REGLER ABFRAGE     │
              │  Domäne · Formalität     │
              │  Persönlichkeit · Seele  │
              │  Texttreue · Kreativität │
              └────────────┬────────────┘
                           │
                    ┌──────▼──────┐
                    │  STUFE 3     │
                    │  FINETUNE    │
                    │  · kriterien-│
                    │    weise      │
                    │  · Check      │
                    │  · Protokoll  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  AUSGABE     │
                    │  Humanisierter│
                    │  Text +       │
                    │  Protokoll    │
                    └──────────────┘
```

---

## Referenzen

Dieser Skill basiert auf:

1. **Wikipedia:WikiProjekt KI und Wikipedia/Schnelltest KI** (v1.35)
   https://de.wikipedia.org/wiki/Wikipedia:WikiProjekt_KI_und_Wikipedia/Schnelltest_KI
   – Top 10 KI-Indikatoren und Systemkonfiguration

2. **Wikipedia:WikiProjekt KI und Wikipedia/Erkennung KI-Einsatz**
   https://de.wikipedia.org/wiki/Wikipedia:WikiProjekt_KI_und_Wikipedia/Erkennung_KI-Einsatz
   – Longlist mit Kennungen A1–D4

3. **Wikipedia:Signs of AI writing** (englischsprachige WP)
   https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
   – 24 Patterns, Content/Language/Style/Communication/Filler-Kategorien

4. **Humanizer Skill von @blader** (claude-code-templates)
   https://github.com/davila7/claude-code-templates
   – Inspirationsquelle für Struktur und Vorher/Nachher-Schema

---

## Versionshistorie

* **0.0.1** – Initiale Version
  * Drei-Stufen-System: ANALYSE → RECOMMEND → FINETUNE
  * Top 10 KI-Indikatoren adaptiert für allgemeine deutsche Texte (K1–K10)
  * Deutsche Spezifika ergänzt (K11–K14)
  * Longlist-Tiefenprüfung (A1–D4) implementiert
  * 7 Stil-Regler für Finetune
  * Vollständiges Drei-Stufen-Beispiel
  * Vorher/Nachher-Katalog für Anglizismen, Nominalstil, Floskeln, KI-Vokabular
  * Evidenzbasiertes Punktesystem nach Wikipedia v1.35

## Lizenz

Apache-2.0
