from enum import Enum


class ChestPainType(str, Enum):
    TYPICAL_ANGINA = "typical angina"
    ATYPICAL_ANGINA = "atypical angina"
    ASYMPTOMATIC = "asymptomatic"
    NON_ANGINAL = "non-anginal"


class RestEcg(str, Enum):
    NORMAL = "normal"
    ST_ABNORMALITY = "st-abnormality"
    LV_HYPERTROPHY = "lv_hypertrophy"


class SmokingStatus(str, Enum):
    NEVER = "never"
    FORMER = "former"
    CURRENT = "current"


class Sex(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
