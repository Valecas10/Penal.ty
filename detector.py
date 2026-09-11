def is_shootout(summary):
    """Devuelve True si el partido está o estuvo en una tanda."""

    if summary.get("shootout"):
        return True

    for play in summary.get("plays", []):
        if play.get("shootout") is True:
            return True

    return False


def get_shootout_data(summary):
    """Devuelve los datos de la tanda."""

    return summary.get("shootout", [])