from enum import Enum


class ChestPainType(str, Enum):
    TYPICAL_ANGINA = "typical angina"
    ATYPICAL_ANGINA = "atypical angina"
    ASYMPTOMATIC = "asymptomatic"
    NON_ANGINAL = "non-anginal"


class RestEcg(str, Enum):
    NORMAL = "normal"
    ST_ABNORMALITY = "st t-abnormality"
    LV_HYPERTROPHY = "lv_hypertrophy"


class SmokingStatus(str, Enum):
    NEVER = "nunca"
    FORMER = "ex-fumador"
    CURRENT = "fumador"


class Sex(str, Enum):
    MALE = "Masculino"
    FEMALE = "Femenino"

mean= {
    'age': 52.89,
    'systolic_blood_pressure': 132.89,
    'ldl_cholesterol': 241.26,
    'max_hr': 140.90,}

mode= {
    'chest_pain_type': 'asymptomatic',
    'rest_ecg': 'normal',
    'exang': False,
    'fasting_blood_sugar':False,  
}
