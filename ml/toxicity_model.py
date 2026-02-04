from typing import List

# NOTE FOR REPORT / VIVA:
#
# This module implements a *lightweight, rule-based baseline model* for ingredient
# toxicity. In a full ML pipeline, the same interface
#     predict_toxicity(ingredient) -> float
# could be backed by a trained classifier (e.g. logistic regression) using features
# derived from datasets such as **Tox21** or other public toxicology benchmarks.
#
# Here we approximate that behaviour with:
# - simple text-derived "features": presence of toxic substrings in the ingredient name
# - a calibrated risk score in [0, 1]


HIGH_RISK_KEYWORDS: List[str] = [
    "paraben",
    "formaldehyde",
    "phthalate",
    "triclosan",
    "benzene",
    "oxybenzone",
    "coal tar",
    "n-(5-chlorobenzoxazol-2-yl)acetamide",
    "acetylcholine",
    "deanol aceglumate",
    "spironolactone",
    "tiratricol",
    "methotrexate",
    "aminocaproic acid",
    "cinchophen",
    "thyropropic acid",
    "trichloroacetic acid",
    "aconitum napellus",
    "aconitine",
    "adonis vernalis",
    "epinephrine",
    "rauwolfia serpentina",
    "alkyne alcohols",
    "isoprenaline",
    "allyl isothiocyanate",
    "alloclamide",
    "nalorphine",
    "sympathicomimetic amines",
    "aniline",
    "betoxycaine",
    "zoxazolamine",
    "procainamide",
    "benzidine",
    "tuaminoheptane",
    "octodrine",
    "2-amino-1,2-bis(4-methoxyphenyl)ethanol",
    "1,3-dimethylpentylamine",
    "4-aminosalicylic acid",
    "toluidines",
    "xylidines",
    "imperatorin",
    "ammi majus",
    "2,3-dichloro-2-methylbutane",
    "androgenic substances",
    "anthracene oil",
    "antibiotics",
    "antimony",
    "apocynum cannabinum",
    "apomorphine",
    "arsenic",
    "atropa belladonna",
    "atropine",
    "barium salts",
    "benzimidazol-2(3h)-one",
    "benzazepines",
    "benzodiazepines",
    "amylocaine",
    "eucaine",
    "isocarboxazid",
    "bendroflumethiazide",
    "beryllium",
    "bromine",
    "bretylium tosilate",
    "carbromal",
    "bromisoval",
    "brompheniramine",
    "benzilonium bromide",
    "tetrylammonium bromide",
    "brucine",
    "tetracaine",
    "mofebutazone",
    "tolbutamide",
    "carbutamide",
    "phenylbutazone",
    "cadmium",
    "cantharides",
    "cantharidine",
    "phenprobamate",
    "nitroderivatives of carbazole",
    "carbon disulphide",
    "catalase",
    "cephaeline",
    "chenopodium ambrosioides oil",
    "2,2,2-trichloroethane-1,1-diol",
    "chlorine",
    "chlorpropamide",
    "chrysoidine citrate hydrochloride",
    "chlorzoxazone",
    "crimidine",
    "chlorprothixene",
    "clofenamide",
    "n,n-bis(2-chloroethyl)methylamine n-oxide",
    "chlormethine",
    "cyclophosphamide",
    "mannomustine",
    "butanilicaine",
    "chlormezanone",
    "triparanol",
    "chlorophacinone",
    "chlorphenoxamine",
    "phenaglycodol",
    "chloroethane",
    "chromium",
    "claviceps purpurea",
    "conium maculatum",
    "glycyclamide",
    "cobalt benzenesulphonate",
]

MODERATE_RISK_KEYWORDS: List[str] = [
    "sodium benzoate",
    "sulfate",
]

# 🔑 Normalize keywords ONCE for case-insensitive matching
HIGH_RISK_KEYWORDS = [k.lower() for k in HIGH_RISK_KEYWORDS]
MODERATE_RISK_KEYWORDS = [k.lower() for k in MODERATE_RISK_KEYWORDS]


BASE_LOW_RISK_SCORE: float = 0.2
MODERATE_RISK_SCORE: float = 0.7
HIGH_RISK_SCORE: float = 0.9


def _normalize_ingredient(ingredient: str) -> str:
    """
    Normalize raw ingredient text before feature extraction.
    """
    return ingredient.lower().strip()


def _contains_any(substrings: List[str], text: str) -> bool:
    """Return True if any substring is found in text."""
    return any(sub in text for sub in substrings)


def predict_toxicity(ingredient: str) -> float:
    """
    Estimate a toxicity risk score for a single ingredient.

    Returns
    -------
    float
        Risk score in [0.0, 1.0]
    """

    normalized = _normalize_ingredient(ingredient)

    # Feature 1: high-risk substring detection
    if _contains_any(HIGH_RISK_KEYWORDS, normalized):
        return HIGH_RISK_SCORE

    # Feature 2: moderate-risk substring detection
    if _contains_any(MODERATE_RISK_KEYWORDS, normalized):
        return MODERATE_RISK_SCORE

    # Default: low baseline risk
    return BASE_LOW_RISK_SCORE