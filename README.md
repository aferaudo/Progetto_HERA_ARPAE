# Progetto_HERA_ARPAE
Questo repository contiene tutti i dati e gli script usati per la realizzazione della dashboard.


## Dati attualmente nel DB
### Dati di contesto
**N.B.** Per dettagli riguardo pozzi, idrometri e pluviometri leggere README files delle rispettive cartelle.
* Coordinate Pozzi

* Livello e portata Pozzi

* Coordinate di tutti i Pluviometri

* Coordinate delle reti di pluviometri (calcolate come media delle coordinate dei pluviometri appartenenti ad una rete) **TEMPORANEO**

* Coordinate degli idrometri selezionati aventi dati almeno fino a fine 2018 (fonte dexter)

### Dati aggiuntivi
* Tabella StatoPozzi contenente lo stato di ogni singolo pozzo (questo dovrebbe variare in base al calcolo del percentile)

* Tabella link_geo_maps usata per rendere la home dashboard cliccabile


## TODO
* Inserire dati di Portata media giornaliera degli idrometri

* Inserire dati Pluviometri (media mensile o settimanale?)
*  Inserirei i nivometri di Doccia di Fiumalbo e Monteacuto delle Alpi insieme ai pluviometri
* Script per il calcolo del percentile (potrebbe essere unificato con il successivo)
* Script monitoraggio dello stato di una rete (attualmente lo script cambia il colore basandosi sul dato letto nella tabella stato pozzi)
