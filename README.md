# Progetto_HERA_ARPAE
Questo repository contiene tutti i dati e gli script usati per la realizzazione della dashboard.


## Dati attualmente nel DB
### Dati di contesto
**N.B.** Per dettagli riguardo pozzi, idrometri e pluviometri leggere README files delle rispettive cartelle.

* Coordinate Pozzi (anche nuovi pozzi HERA)

* Livello e portata Pozzi (anche nuovi pozzi HERA)

* Coordinate dei Pluviometri selezionati

* Coordinate delle reti di pluviometri (calcolate come media delle coordinate dei pluviometri appartenenti ad una rete) **Non più visulizzati**

* Coordinate degli idrometri selezionati aventi dati almeno fino a fine 2018 (fonte dexter)

* Portata media giornaliera degli idrometri selezionati

* Precipitazione cumulata giornaliera dei pluviometri selezionati

### Dati aggiuntivi
* Tabella StatoPozzi contenente lo stato di ogni singolo pozzo (questo dovrebbe variare in base al calcolo del percentile)

* Tabella link_geo_maps usata per rendere la home dashboard cliccabile




## TODO

* Aggiungere grafici nel mid-layer con unica dashboard

* Aggiornare tabella coord con ON DELETE CASCADE

* Inserire i nivometri di Doccia di Fiumalbo e Monteacuto delle Alpi insieme ai pluviometri

* Script che automatizza il processo di inserimento dati nel db

* Divisione pozzi per appartenenza: Visualizzazione dei semafori relativi ai pozzi ARPAE ed HERA separata

* Diminuire numero di richieste di geojson files (grafana-map-panel)

****
#### Note varie
* I dati del pozzo MANZOLINO 7 (HERA) sono stati completamente rimossi per un problema sulla sonda

* Pozzi Campiano e Pianacci di Rimini pochi dati validi (*aggiornati*)

* Script per il calcolo del percentile considera solo i livelli con portata <= 0.3: deve essere chiamato manualmente per ora, in futuro dovrà essere chiamato da chi va ad effettuare l'update settimanale/mensile dei dati, in modo da ottenere il seguente comportamento: *ogni volta che nuovi dati vengono inseriti il percentile cambia e di conseguenza cambia anche la soglia che provoca una modifica dello stato dei singoli pozzi*