# ArXiv HTML to EPUB Converter

Arxiv2Epub è uno strumento da riga di comando per scaricare paper scientifici da arXiv e convertirli in ebook EPUB. Il programma supporta ora il **download batch**, il **riconoscimento automatico degli ID arXiv** e la gestione mista di URL e identificativi.

## Installazione

### Prerequisiti

Python 3.10 o superiore.

### Setup

Clona il repository e installa le dipendenze:

```bash
pip install -r requirements.txt
```

## Utilizzo

Il programma è flessibile e accetta sia URL completi che semplici ID dei paper.

### 1. Conversione Singola (ID o URL)

Non è più necessario cercare l'URL HTML specifico, basta l'ID del paper:

```bash
# Tramite ID (consigliato)
python arxiv_to_epub.py 2412.20331

# Tramite ID con versione
python arxiv_to_epub.py 2412.20331v2

# Tramite URL completo
python arxiv_to_epub.py "https://arxiv.org/html/2412.20331"
```

### 2. Conversione Multipla (Batch)

Puoi scaricare e convertire più paper in una sola volta. Il programma li processerà sequenzialmente:

```bash
python arxiv_to_epub.py 2412.20331 2501.00006v1 2310.12345
```

### 3. Input Misti

Puoi mescolare URL e ID nello stesso comando:

```bash
python arxiv_to_epub.py 2412.20331 "https://arxiv.org/html/2501.00006" arXiv:2305.09876
```

## Opzioni e Flag

### Output Personalizzato

Specifica il nome del file (funziona **solo** con un singolo input):

```bash
python arxiv_to_epub.py 2412.20331 -o mio_paper.epub
```

*Nota: Se inserisci più paper, l'opzione `-o` verrà ignorata e i file verranno nominati automaticamente basandosi sul titolo.*

### Personalizzazione Contenuto

```bash
# Rimuovi l'abstract e le figure per un file più leggero
python arxiv_to_epub.py 2412.20331 --no-abstract --remove-figures

# Limita il numero di autori nei metadati (default: 4)
python arxiv_to_epub.py 2412.20331 --max-authors 2
```

### Gestione Immagini

```bash
# Imposta larghezza massima immagini (default: 800px)
python arxiv_to_epub.py 2412.20331 --max-image-width 1200
```

### Opzioni di Sistema

```bash
# Modalità silenziosa (mostra solo errori e riepilogo finale)
python arxiv_to_epub.py 2412.20331 --quiet

# Aumenta timeout per connessioni lente (default: 30s)
python arxiv_to_epub.py 2412.20331 --timeout 60

# Salta la validazione preventiva dell'URL (più veloce, meno sicuro)
python arxiv_to_epub.py 2412.20331 --no-validate
```

## Esempio di Workflow Completo

Immagina di voler leggere tre paper nel weekend. Non serve creare script complessi:

```bash
python arxiv_to_epub.py \
  2602.02639 \
  2501.00006 \
  https://arxiv.org/html/2412.20331 \
  --max-image-width 1000 \
  --quiet
```

**Output:**
Il programma scaricherà i tre documenti, mostrerà eventuali errori per i singoli file e stamperà un riepilogo finale:

```text
Riepilogo:
  Successi: 3
  Fallimenti: 0
  Totale: 3
```

## Risoluzione Problemi Comuni

* **Errore "Impossibile interpretare input":** Verifica che l'ID sia corretto (es. `2602.02639`) o che l'URL sia raggiungibile.
* **Timeout:** Usa `--timeout 60` se scarichi paper con immagini molto pesanti o se arXiv risponde lentamente.
* **Formule Matematiche:** Il supporto dipende dal lettore EPUB. Consigliati: **Calibre**, **Apple Books**, **Thorium Reader**.

## Domande Frequenti (FAQ)

**Q: Posso convertire paper da altri siti oltre ad arXiv?**
A: Per il momento no. Lo script è pensato esclusivamente per arXiv. Per altri siti potrebbero essere necessarie modifiche alla logica di estrazione del contenuto. Se riesci a farlo funzionare non esitare ad aprire una pull request

**Q: Il file EPUB funzionerà offline?**
A: Sì, completamente. Tutte le immagini vengono scaricate e incluse nel file.

**Q: Quanto tempo richiede una conversione tipica?**
A: Per un paper standard: 15 secondi. Paper con molte immagini, invece, possono richiedere 1-2 minuti.

**Q: Le formule matematiche vengono preservate?**
A: Sì, se il paper HTML originale usa MathML dovrebbero rimanere perfettamente leggibili. Il supporto però dipende dal lettore EPUB utilizzato.

## Nota Tecnica

Il programma tenta automaticamente di convertire qualsiasi ID o URL nel formato HTML di arXiv (`/html/`).

Se un paper non ha una versione HTML disponibile su arXiv, la conversione fallirà. Questo significa che solo alcuni paper (solitamente tutti quelli dal 2022 in poi) possono essere scaricati in formato epub.

## Report Bug e Suggerimenti

Se incontri problemi o hai suggerimenti:

1. Verifica che il problema non sia già documentato nella sezione Risoluzione Problemi
2. Includi l'URL del paper che causa il problema.
3. Includi il messaggio di errore completo.
4. Specifica il sistema operativo, la versione Python e qualsiasi altra informazione che reputi importante

## Licenza

Questo script è fornito come strumento per uso personale ed educativo. Rispetta sempre le licenze e i termini d'uso dei paper che converti.

## Riconoscimenti

Questo progetto utilizza:

* Il servizio arXiv/html per versioni HTML dei paper arXiv
* La libreria ebooklib per la generazione EPUB
* BeautifulSoup per il parsing HTML
* Requests per il download delle risorse

Grazie alla comunità open source per gli strumenti che rendono possibile questo progetto!
