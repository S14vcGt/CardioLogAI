from fastapi import HTTPException
from app.schemas.medical_history import MedicalHistoryCreate
from app.core.logger import get_logger
from app.core.const import mean, mode
import pandas as pd

logger = get_logger(__name__)

# Variables que el modelo espera recibir (en este orden)
MODEL_FEATURES = [
    "age",
    "sex",
    "chest_pain_type",
    "systolic_blood_pressure",
    "ldl_cholesterol",
    "fasting_blood_sugar",
    "rest_ecg",
    "max_hr",
    "exang",
]

# Features with multiple categories (Nominal)
categorical_cols = ['chest_pain_type', 'rest_ecg']

# Features with continuous or discrete numerical values
numeric_cols = ['age', 'systolic_blood_pressure', 'ldl_cholesterol', 'max_hr']


def predict_heart_disease(data: MedicalHistoryCreate, model) -> dict:
    """Pipeline completa: formatear datos → imputar → predecir."""
    try:
        input_df = format_data(data)
        prep_df = preprocessing(input_df)
        result = model_predict(prep_df, model)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error al utilizar modelo: {e}")
        raise HTTPException(status_code=500, detail="Error al usar el modelo de IA")


def format_data(data: MedicalHistoryCreate) -> pd.DataFrame:
    """
    Extrae del schema solo las variables que el modelo necesita (MODEL_FEATURES).
    No realiza ningún mapeo de tipos; el preprocesador del modelo se encarga de eso.
    """
    try:
        raw = data.model_dump()
        model_row = {feat: raw.get(feat) for feat in MODEL_FEATURES}

        df = pd.DataFrame([model_row])
        logger.info(f"Datos formateados para el modelo:\n{df.to_string()}")
        return df

    except Exception as e:
        logger.exception(f"Error al formatear datos: {e}")
        raise HTTPException(status_code=500, detail="Error al formatear datos")


def numerical_imputer(df: pd.DataFrame) -> pd.DataFrame:
    """
    Imputa valores faltantes en columnas numéricas usando la media
    calculada durante el entrenamiento.
    """
    try:
        for col, mean_value in mean.items():
            if col in df.columns and df[col].isnull().any():
                logger.info(f"Imputando '{col}' con media: {mean_value}")
                df[col] = df[col].fillna(mean_value)
        return df
    except Exception as e:
        logger.exception(f"Error al imputar variables numéricas: {e}")
        raise HTTPException(
            status_code=500, detail="Error al imputar variables numéricas"
        )


def categorical_imputer(df: pd.DataFrame) -> pd.DataFrame:
    """
    Imputa valores faltantes en columnas categóricas usando la moda
    calculada durante el entrenamiento.
    """
    try:
        for col, mode_value in mode.items():
            if col in df.columns and df[col].isnull().any():
                logger.info(f"Imputando '{col}' con moda: {mode_value}")
                df[col] = df[col].fillna(mode_value)
        return df
    except Exception as e:
        logger.exception(f"Error al imputar variables categóricas: {e}")
        raise HTTPException(
            status_code=500, detail="Error al imputar variables categóricas"
        )


def preprocessing(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica imputación numérica y categórica al DataFrame."""
    try:
        df = numerical_imputer(df)
        df = categorical_imputer(df)
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_cols),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
            ])

        X = preprocessor.fit_transform(df)
        return X
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error al preprocesar datos: {e}")
        raise HTTPException(status_code=500, detail="Error al preprocesar datos")


def model_predict(input_df: pd.DataFrame, model) -> dict:
    """Ejecuta la predicción y devuelve resultado con confianza."""
    try:
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]

        return {
            "prediction": int(prediction),
            "confidence": round(float(probability), 4),
            "risk_level": "Alto" if probability > 0.7 else "Moderado" if probability > 0.4 else "Bajo",
        }
    except Exception as e:
        logger.exception(f"Error al utilizar modelo: {e}")
        raise HTTPException(status_code=500, detail="Error al usar el modelo de IA")
