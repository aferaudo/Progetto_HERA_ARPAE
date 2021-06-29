# Monitoraggio Stato Pozzi
N.B. Questo algoritmo dovrà essere chiamato ogni volta che nuovi dati vengono caricati nella cartella FTP in modo da mantenere la visualizzazione degli stati sulla mappa coerente.

L'algoritmo implementato in **status_monitor.py** consente di cambiare il colore di un ambito sulla base dello stato dei pozzi appartenenti a quell'ambito.

Per prima cosa l'algoritmo **calcola lo stato del pozzo**. Il calcolo viene effettuato usando il percentile 25 ordinando i valori in maniera ascendente(dal minore al maggiore). In particolare: 

* al di sopra del percentile 25 se l'ultimo valore registrato non corrisponde con il minimo di sempre lo stato del pozzo è giallo (1)

* se l'ultimo valore registrato è al di sotto del percentile 25 lo stato del pozzo è verde (2)

* se l'ultimo valore registrato corrisponde con il minimo di sempre lo stato del pozzo è rosso (0)

Una volta che lo stato del pozzo è stato aggiornato, viene effettuato il **calcolo dei pesi**. Quest'ultimo tiene conto del volume dei dati emunto da quel pozzo e della data dell'ultimo valore registrato. Il *volume* è calcolato come il rapporto tra numero di giorni per cui si hanno dei dati per un pozzo e il numero massimo di giorni per quell'ambito; si considerano i giorni perchè i pozzi ARPAE registrano solitamente il livello medio giornaliero, mentre i pozzi HERA registrano il livello medio ogni 15 minuti. La *data* dell'ultimo dato registrato è importante per comprendere quanto il dato fornito per quel pozzo sia valido. Se un dato supera l'anno di età il peso da attribuire a tale pozzo è 0.

I pesi vengono successivamente utilizzati per **selezionare il colore da attribuire all'ambito**. Per ogni stato (rosso, giallo, verde) viene effettuata la somma dei pesi. Queste somme vengono usate per selezionare lo stato che potrebbe essere attribuito all'intero ambito: ad esempio se esistono 3 pozzi nello stato verde ognuno con peso 0,3, quindi con somma 0,9, e un pozzo lo stato giallo con peso 0,8 lo stato che verrà selezionato sarà lo stato verde. Una volta che un possibile stato è stato selezionato viene calcolato quanto questo pesi sul totale (somma per quello stato/ somma dei pesi). Tornando al caso precedente si ha 0,9 (somma pesi stato verde) / 1,7 (somma totale dei pesi per quell'ambito). Se il valore ottenuto supera 0.5 all'ambito verrà assegnato il colore corrispondente a quello stato(nell'esempio precendente verde), altrimenti il colore assegnato sarà il giallo.