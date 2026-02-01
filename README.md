# ArXiv HTML to EPUB Converter

Uno script Python completo per scaricare paper scientifici da arXiv in formato HTML e convertirli in file EPUB perfettamente formattati e validati. Lo script gestisce automaticamente il download delle immagini, la pulizia del contenuto, l'estrazione dei metadati e la generazione di un ebook pronto per la lettura su qualsiasi dispositivo.

## Installazione

### Prerequisiti

Python 3.7 o superiore.

### Setup

Clona o scarica il repository, quindi installa le dipendenze necessarie:

```bash
pip install -r requirements.txt
```

Le dipendenze includono:
- `requests` per il download delle pagine web
- `beautifulsoup4` per il parsing e la pulizia dell'HTML
- `ebooklib` per la creazione dei file EPUB
- `lxml` per un parsing veloce ed efficiente

## Utilizzo Base

### Conversione Semplice

La forma più semplice di utilizzo richiede solo l'URL del paper in formato HTML:

```bash
python arxiv_to_epub.py "https://ar5iv.labs.arxiv.org/html/2412.20331"
```

Lo script scarica il paper, lo processa e crea un file EPUB con un nome generato automaticamente dal titolo del documento.

### Specificare il Nome del File

Se preferisci scegliere il nome del file di output:

```bash
python arxiv_to_epub.py "https://ar5iv.labs.arxiv.org/html/2412.20331" -o mio_paper.epub
```

### Conversione Silenziosa

Per script automatici o batch processing, puoi disabilitare tutti i messaggi informativi:

```bash
python arxiv_to_epub.py "URL" --quiet
```

In modalità silenziosa vengono mostrati solo gli errori critici.

## Opzioni Avanzate

### Rimozione dell'Abstract

Se stai convertendo paper molto lunghi o preferisci un documento più compatto, puoi rimuovere la sezione dell'abstract:

```bash
python arxiv_to_epub.py "URL" --no-abstract
```

Questo rimuove automaticamente le sezioni identificate come abstract dal documento finale.

### Rimozione delle Figure

Per creare una versione solo testo del paper, utile per la lettura veloce o per ridurre la dimensione del file:

```bash
python arxiv_to_epub.py "URL" --remove-figures
```

Tutte le figure vengono rimosse, mantenendo solo il contenuto testuale.

### Gestione delle Immagini

Le immagini vengono automaticamente scaricate e incluse nel file EPUB. Puoi controllare la loro dimensione massima:

```bash
python arxiv_to_epub.py "URL" --max-image-width 1200
```

Il valore predefinito è 800 pixel. Impostare un valore più alto mantiene immagini di qualità superiore ma aumenta la dimensione del file. Un valore più basso riduce le dimensioni ma può compromettere la leggibilità di grafici dettagliati.

### Limitazione degli Autori

Paper scientifici possono avere decine o centinaia di autori. Per evitare metadata eccessivamente lunghi:

```bash
python arxiv_to_epub.py "URL" --max-authors 3
```

Il valore predefinito è 4. Solo i primi N autori vengono inclusi nei metadata del file EPUB.

### Timeout Personalizzato

Se hai una connessione lenta o stai scaricando paper con molte immagini, puoi aumentare il timeout:

```bash
python arxiv_to_epub.py "URL" --timeout 60
```

Il valore predefinito è 30 secondi. Un timeout più lungo può essere necessario per paper di grandi dimensioni.

### Combinazione di Opzioni

Puoi combinare liberamente le opzioni per personalizzare la conversione:

```bash
python arxiv_to_epub.py "URL" \
  -o scientific_paper.epub \
  --no-abstract \
  --remove-figures \
  --max-authors 2 \
  --max-image-width 1000 \
  --timeout 45 \
  --quiet
```

## Caratteristiche Principali

### Pulizia Intelligente del Contenuto

Rimuove automaticamente tutti gli elementi non pertinenti al contenuto del paper:
- Barre di navigazione e menu
- Header e footer delle pagine
- Script e stili inline
- Elementi pubblicitari
- Controlli dell'interfaccia web
- Social sharing buttons

Il risultato è un documento pulito che contiene solo il paper scientifico.

### Gestione Completa delle Immagini

Per evitare di lasciare riferimenti esterni che non permetterebbero la visualizzazione delle immagini:
- Scarica ogni immagine presente nel paper
- La include direttamente nel file EPUB
- Converte URL relativi in riferimenti locali
- Gestisce correttamente diversi formati (PNG, JPEG, GIF, SVG, WebP)

Il file EPUB risultante funziona completamente offline, senza dipendere dalla disponibilità del server arXiv.

### Estrazione Automatica dei Metadati

Identifica e estrae automaticamente:
- Il titolo del paper
- Gli autori (con pulizia dei nomi da simboli o note)
- Data di creazione del file EPUB

I metadati vengono inclusi correttamente nel file EPUB per una gestione ottimale nelle librerie digitali (testato con Calibre).

### Supporto Formule Matematiche

Le formule matematiche in formato MathML vengono:
- Riconosciute automaticamente
- Processate per garantire namespace corretti
- Dichiarate nel manifest EPUB per compatibilità
- Pulite da attributi non standard

Questo garantisce che le formule vengano visualizzate correttamente nei reader che supportano MathML.

### Formattazione Ottimizzata per la Lettura

Il file EPUB include stili CSS professionali che ottimizzano:
- Leggibilità del testo (font Georgia, interlinea 1.6)
- Formattazione delle tabelle scientifiche
- Visualizzazione di codice e blocchi preformattati
- Layout responsive per diversi dispositivi
- Gerarchia visiva dei titoli

### Validazione EPUB Completa

I file generati passano la validazione epubcheck senza errori o warning. Questo garantisce:
- Compatibilità con tutti i lettori EPUB standard
- Nessun problema durante l'import nelle librerie
- Rispetto delle specifiche EPUB 3.2
- Funzionamento affidabile su tutti i dispositivi

## Flusso di Lavoro Tipico

### Conversione di un Singolo Paper

```bash
# 1. Trova il paper su arXiv
# 2. Seleziona "HTML (experimental)" e copia il link
# 3. Esegui la conversione
python arxiv_to_epub.py "https://arxiv.org/html/2512.24880v2" -o paper.epub

# 4. Verifica il risultato
ls -lh paper.epub

# Output esempio:
# -rw-r--r-- 1 user user 3.2M Feb  2 00:20 paper.epub
```

### Conversione per Lettura Veloce

Per una lettura rapida del contenuto principale senza distrazioni:

```bash
python arxiv_to_epub.py "URL" \
  --no-abstract \
  --remove-figures \
  --max-image-width 600 \
  -o lettura_veloce.epub
```

Questo crea un file più leggero, perfetto per una prima passata sul contenuto.

### Conversione Alta Qualità per Archiviazione

Per mantenere la massima qualità per referenza futura:

```bash
python arxiv_to_epub.py "URL" \
  --max-image-width 1600 \
  --timeout 60 \
  -o archivio.epub
```

Questo preserva immagini ad alta risoluzione e gestisce meglio download lenti.

### Batch Processing

Per convertire multipli paper in sequenza:

```bash
# Crea uno script batch
cat > convert_papers.sh << 'EOF'
#!/bin/bash
while IFS= read -r url; do
  python arxiv_to_epub.py "$url" --quiet
done < paper_urls.txt
EOF

chmod +x convert_papers.sh

# Crea la lista di URL
cat > paper_urls.txt << 'EOF'
https://arxiv.org/html/2412.20331
https://arxiv.org/html/2401.12345
https://arxiv.org/html/2403.67890
EOF

# Esegui la conversione
./convert_papers.sh
```

## Risoluzione Problemi

### Timeout Durante il Download

Se la conversione si interrompe con un errore di timeout:

```bash
# Aumenta il timeout a 60 secondi
python arxiv_to_epub.py "URL" --timeout 60
```

Questo è particolarmente utile per risolvere problemi legati a:
- Paper con molte immagini di grandi dimensioni
- Connessioni internet lente o instabili
- Server arXiv sotto carico

### Immagini Mancanti nel File Finale

Se alcune immagini non appaiono nel file EPUB:
- Verifica i messaggi di warning durante la conversione
- Le immagini non scaricabili vengono automaticamente rimosse
- Controlla che il server arXiv sia accessibile
- Alcune immagini potrebbero richiedere autenticazione

Il processo di creazione epub tenta sempre di scaricare le immagini ma procede anche se alcune non sono disponibili.

### Contenuto Incompleto

Se il file EPUB non contiene tutto il paper:
- Verifica di usare l'URL corretto (arxiv.org/html/, non arxiv.org)
- Alcuni paper potrebbero non essere disponibili in formato HTML
- Usa l'URL "html" e non "pdf"

Formato URL corretto:
```
Corretto:   https://arxiv.org/html/2412.20331
Sbagliato:  https://arxiv.org/abs/2412.20331
Sbagliato:  https://arxiv.org/pdf/2412.20331.pdf
```

### Formule Matematiche Non Visualizzate

Se le formule matematiche non vengono renderizzate:
- Il problema potrebbe dipendere dal lettore EPUB utilizzato
- Non tutti i lettori supportano MathML
- Prova con Calibre (ottimo supporto MathML)
- Apple Books su iOS/macOS supporta MathML
- Alcuni lettori potrebbero mostrare il codice invece della formula

### File EPUB Troppo Grande

Se il file risultante è troppo grande:

```bash
# Riduci la dimensione delle immagini
python arxiv_to_epub.py "URL" --max-image-width 600

# O rimuovi completamente le figure
python arxiv_to_epub.py "URL" --remove-figures
```

Dimensioni tipiche:
- Solo testo: 50-200 KB
- Con immagini 800px: 2-5 MB
- Con immagini 1600px: 5-15 MB

### Validazione del File Generato

Per verificare che il file EPUB sia correttamente formato:

```bash
# Scarica epubcheck (una tantum)
wget https://github.com/w3c/epubcheck/releases/download/v5.1.0/epubcheck-5.1.0.zip
unzip epubcheck-5.1.0.zip

# Valida il file
java -jar epubcheck-5.1.0/epubcheck.jar tuo_file.epub

# Output atteso:
# Validating using EPUB version 3.2 rules.
# No errors or warnings detected.
# EPUBCheck completed
```

Oppure vai su https://draft2digital.com/book/epubcheck/upload e carica l'epub per un controllo approfondito

## Compatibilità Lettori EPUB

### Lettori Testati e Compatibili

- **Calibre** (Windows, macOS, Linux): Compatibilità completa, eccellente supporto MathML
- **Apple Books** (iOS, macOS): Compatibilità completa, supporto MathML nativo
- **Google Play Books** (Android, Web): Compatibilità completa, supporto base MathML
- **Adobe Digital Editions**: Compatibilità completa
- **Thorium Reader** (Windows, macOS, Linux): Compatibilità completa, ottimo per accessibilità
- **FBReader** (Multi-piattaforma): Compatibilità buona, supporto limitato MathML

### Conversione per Kindle

I file EPUB possono essere convertiti per Kindle usando Calibre:

```bash
ebook-convert paper.epub paper.mobi
```

Nota: Amazon Kindle ha supporto limitato per formule matematiche complesse.

## Struttura del File EPUB Generato

I file EPUB creati contengono:

```
paper.epub
├── META-INF/
│   └── container.xml           (Metadata container)
├── OEBPS/
│   ├── content.xhtml           (Contenuto principale del paper)
│   ├── toc.ncx                 (Indice navigazione)
│   ├── nav.xhtml               (Navigazione HTML5)
│   ├── style/
│   │   └── nav.css             (Stili CSS)
│   └── images/
│       ├── img_1_abc123.png    (Immagini scaricate)
│       ├── img_2_def456.jpg
│       └── ...
└── mimetype                     (Identificatore EPUB)
```

## Note Tecniche

### Formato URL Supportato

Lo script è ottimizzato per paper arXiv convertiti in HTML dal servizio ar5iv:
- arxiv.org/html fornisce versioni HTML dei paper arXiv
- Il formato HTML permette estrazione più accurata del contenuto
- Le immagini in formato PDF vengono automaticamente convertite

### Gestione della Memoria

Durante la conversione, lo script:
- Mantiene il contenuto HTML in memoria
- Scarica le immagini progressivamente
- Libera memoria dopo ogni immagine processata

Per paper con centinaia di immagini, potrebbero essere necessari 200-500 MB di RAM.

### Sicurezza e Privacy

Lo script:
- Non invia dati a server terzi
- Non traccia le conversioni
- Non richiede autenticazione
- Funziona completamente in locale dopo il download

I file EPUB generati non contengono tracker o analytics.

## Sviluppo e Contributi

### Struttura del Progetto

```
arxiv-to-epub/
├── arxiv_to_epub.py              # Script principale
├── requirements.txt              # Dipendenze Python
├── README.md                     # Questa guida
├── .gitignore                    # File da escludere da Git
└── docs/                         # Documentazione tecnica
    ├── IMPLEMENTATION_DOCS.md    # Dettagli implementazione
    ├── VALIDATION_FIXES.md       # Correzioni validazione EPUB
    ├── CODE_COMPARISON.md        # Evoluzione del codice
    └── PROJECT_STRUCTURE.md      # Struttura progetto
```

### Testing Locale

Per testare modifiche allo script:

```bash
# Crea una cartella per i test (già nel .gitignore)
mkdir test_output

# Testa con diversi paper
python arxiv_to_epub.py "URL1" -o test_output/test1.epub
python arxiv_to_epub.py "URL2" -o test_output/test2.epub --no-abstract
python arxiv_to_epub.py "URL3" -o test_output/test3.epub --remove-figures

# Valida i risultati
for f in test_output/*.epub; do
  echo "Validating $f"
  java -jar epubcheck.jar "$f"
done
```

### Report Bug e Suggerimenti

Se incontri problemi o hai suggerimenti:
1. Verifica che il problema non sia già documentato nella sezione Risoluzione Problemi
2. Prova con l'ultima versione dello script
3. Includi l'URL del paper che causa il problema
4. Includi il messaggio di errore completo
5. Specifica il sistema operativo e la versione Python

## Domande Frequenti

**Q: Posso convertire paper da altri siti oltre ad arXiv?**
A: Lo script è ottimizzato per arXiv tramite ar5iv. Per altri siti potrebbero essere necessarie modifiche alla logica di estrazione del contenuto.

**Q: Il file EPUB funzionerà offline?**
A: Sì, completamente. Tutte le immagini vengono scaricate e incluse nel file.

**Q: Quanto tempo richiede una conversione tipica?**
A: Per un paper standard: 15-30 secondi. Paper con molte immagini possono richiedere 1-2 minuti.

**Q: Posso automatizzare la conversione di molti paper?**
A: Sì, vedi la sezione "Batch Processing" per esempi di script.

**Q: Le formule matematiche vengono preservate?**
A: Sì, se il paper HTML originale usa MathML. Il supporto dipende dal lettore EPUB.

**Q: Posso modificare gli stili CSS?**
A: Sì, il CSS è incluso nello script e può essere personalizzato modificando la variabile `style` nel metodo `create_epub()`.

**Q: Il file EPUB può essere venduto o distribuito?**
A: Dipende dalla licenza del paper originale su arXiv. Lo script non aggiunge restrizioni DRM.

## Licenza

Questo script è fornito come strumento per uso personale ed educativo. Rispetta sempre le licenze e i termini d'uso dei paper che converti.

## Changelog

### Versione Corrente
- Download e embedding automatico di tutte le immagini
- Supporto completo per formule MathML
- Validazione EPUB 3.2 completa
- Opzioni avanzate per personalizzazione output
- Pulizia intelligente del contenuto
- Gestione robusta degli errori
- Logging configurabile
- Supporto timeout personalizzabile

### Miglioramenti Futuri Possibili
- Conversione automatica LaTeX → MathML
- Resize intelligente delle immagini
- Supporto per paper multi-capitolo
- Cache locale per riconversioni
- Interfaccia grafica opzionale
- Estrazione automatica indice dei contenuti

## Riconoscimenti

Questo progetto utilizza:
- Il servizio arXiv/html per versioni HTML dei paper arXiv
- La libreria ebooklib per la generazione EPUB
- BeautifulSoup per il parsing HTML
- Requests per il download delle risorse

Grazie alla comunità open source per gli strumenti che rendono possibile questo progetto.