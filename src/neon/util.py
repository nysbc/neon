memc_access_affiliations = {
    "wads",
    "nyu",
    "colu",
    "mskcc",
    "mssm",
    "cuny",
    "aecom",
    "weil",
    "ru",
}


def access_for_affiliation(affiliation: str) -> str:
    affiliation = affiliation.lower().strip()
    if affiliation in memc_access_affiliations:
        return "memc"
    return affiliation
