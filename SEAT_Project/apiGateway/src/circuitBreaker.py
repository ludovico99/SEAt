import circuitbreaker

# incrementa il numero di failure ogni volta che c'è un errore di connessione... si può settare con errori generici. Forse è meglio?

# By default, the circuit breaker stays open for 30 seconds to allow the integration point to recover. You can adjust this value with the recovery_timeout parameter.
@circuitbreaker.circuit(failure_threshold=3, recovery_timeout=60)
def getSuggestions(inputParam):
    response = self.stubReservation.getListOfProposal(inputParam)
    return response