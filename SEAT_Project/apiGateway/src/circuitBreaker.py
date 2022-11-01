from circuitbreaker import circuit


def onCircuitOpen(stubReservation, inputParam):

    suggestions = None
    print("[CB] CIRCUITO APERTO")
    msg = "funzionalità richiesta al momento non disponibile"
    return suggestions, msg


@circuit(failure_threshold=1, recovery_timeout=60, fallback_function=onCircuitOpen)
def getSuggestions(stubReservation, inputParam):

    print("[CB] sto chiamando il microservizio")
    response = stubReservation.getListOfProposal(inputParam)
    suggestions = []
    for offerta in response.offerta:
        proposta = [offerta.lido_id, offerta.city, round(int(offerta.distance), 2), offerta.price, round(int(offerta.averageReview),2), offerta.index]
        suggestions.insert(offerta.index, proposta)
    return suggestions, ""
