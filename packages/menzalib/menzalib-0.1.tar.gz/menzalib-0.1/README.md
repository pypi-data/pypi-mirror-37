Come installare:

Aprire terminale dentro menzalib e scrivere "pip install ."

Funzioni:
Nota: Tutte le funzioni accettano sia numeri che array,
nel caso di array computano l'errore per ogni elemento dell'array

dRdig(R) computa l'errore sulla misura di resistenza del multimetro digitale
supponendo di utilizzare la scala appropriata per la misura

dVdig(V) computa l'errore sulla misura di ddp del multimetro digitale
supponendo di utilizzare la scala appropriata per la misura

dCdig(C) computa l'errore sulla misura di capacità del multimetro digitale
supponendo di utilizzare la scala appropriata per la misura

dVosc(V) computa l'errore sulla misura di voltaggio dell'oscilloscopio,
si suppone di utilizzare la scala "coarse" migliore per fare la misura,
ovvero la scala più piccola in cui il segnale non esce dal display.

dTosc(t) computa l'errore sulla misura del tempo dell'oscilloscoppio (WIP)
