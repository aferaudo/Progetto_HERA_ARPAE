# Progetto_HERA_ARPAE
Questo repository contiene tutti i dati e gli script usati per la realizzazione della dashboard.


## Dati attualmente nel DB
### Dati di contesto
**N.B.** Per dettagli riguardo pozzi, idrometri e pluviometri leggere README files delle rispettive cartelle.
* Coordinate Pozzi

* Livello e portata Pozzi

* Coordinate dei Pluviometri selezionati

* Coordinate delle reti di pluviometri (calcolate come media delle coordinate dei pluviometri appartenenti ad una rete) **Non più visulizzati**

* Coordinate degli idrometri selezionati aventi dati almeno fino a fine 2018 (fonte dexter)

* Portata media giornaliera degli idrometri selezionati

* Precipitazione cumulata giornaliera dei pluviometri selezionati

### Dati aggiuntivi
* Tabella StatoPozzi contenente lo stato di ogni singolo pozzo (questo dovrebbe variare in base al calcolo del percentile)

* Tabella link_geo_maps usata per rendere la home dashboard cliccabile




## TODO

* Aggiornare tabella stato pozzi con i nuovi pozzi di Bologna inseriti: da fare dopo aver ricevuto i dati di livello

* Aggiornare DATI di RIMINI (HERA) e rimuovere quelli attuali

* Aggiungere territorio nella tabella coord (?)

* Aggiornare tabella coord con ON DELETE CASCADE

* Inserire i nivometri di Doccia di Fiumalbo e Monteacuto delle Alpi insieme ai pluviometri

* Script per il calcolo del percentile (potrebbe essere unificato con il successivo)

* Script monitoraggio dello stato di una rete (attualmente lo script cambia il colore basandosi sul dato letto nella tabella stato pozzi)

* Script che automatizza il processo di inserimento dati nel db

* Divisione pozzi per appartenenza: Visualizzazione dei semafori relativi ai pozzi ARPAE ed HERA separata

****
#### Note varie
* I dati del pozzo MANZOLINO 7 (HERA) sono stati completamente rimossi per un problema sulla sonda