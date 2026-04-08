from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.schemas.medical_history import MedicalHistoryCreate, MedicalHistoryRead
from app.schemas.medication import MedicationEntryRead
from app.models.medical_history import MedicalHistory
from app.models.medication import Medication, MedicalHistoryMedication
from app.models.patient import Patient
from app.models.user import User
from app.core.config import SessionDep
from app.core.logger import get_logger
from app.Scripts.medical_history_helpers import calcular_edad, calcular_bsa_mosteller

logger = get_logger(__name__)


def _get_or_create_medication(session: Session, name: str, rxcui: str | None) -> Medication:
    """Busca un medicamento por nombre (case-insensitive). Si no existe, lo crea."""
    statement = select(Medication).where(Medication.name == name.strip())
    medication = session.exec(statement).first()
    if medication:
        # Actualizar rxcui si viene y no estaba
        if rxcui and not medication.rxcui:
            medication.rxcui = rxcui
            session.add(medication)
        return medication

    medication = Medication(name=name.strip(), rxcui=rxcui)
    session.add(medication)
    session.flush()  # Para obtener el ID sin hacer commit
    return medication


def _build_medication_reads(history: MedicalHistory) -> list[MedicationEntryRead]:
    """Convierte los links de medicamentos de una historia en MedicationEntryRead."""
    result = []
    for link in history.medication_links:
        med = link.medication
        result.append(MedicationEntryRead(
            id=med.id,
            name=med.name,
            rxcui=med.rxcui,
            dose=link.dose,
            unit=link.unit,
            frequency=link.frequency,
        ))
    return result


def create_medical_history(
    session: SessionDep,
    patient_id: str,
    history: MedicalHistoryCreate,
    current_user: User,
):
    try:
        statement = select(Patient).where(
            Patient.id == patient_id, Patient.doctor_id == current_user.id
        )
        patient = session.exec(statement).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")

        history_dict = history.model_dump()
        history_dict["patient_id"] = patient_id
        history_dict["age"] = calcular_edad(patient.birth_date)  # yyyy-mm-dd

        # sex es solo para el modelo, no es columna de MedicalHistory
        history_dict.pop("sex", None)

        # Extraer medications antes de crear el modelo
        medications_data = history_dict.pop("medications", [])

        db_history = MedicalHistory(**history_dict)
        session.add(db_history)
        session.flush()  # Para tener el ID disponible

        # Crear los links de medicamentos
        for med_data in medications_data:
            medication = _get_or_create_medication(
                session, med_data["name"], med_data.get("rxcui")
            )
            link = MedicalHistoryMedication(
                medical_history_id=db_history.id,
                medication_id=medication.id,
                dose=med_data.get("dose"),
                unit=med_data.get("unit"),
                frequency=med_data.get("frequency"),
            )
            session.add(link)

        session.commit()
        session.refresh(db_history)

        # Construir respuesta con medicamentos
        result = MedicalHistoryRead.model_validate(db_history)
        result.medications = _build_medication_reads(db_history)
        return result
    except HTTPException as e:
        session.rollback()
        raise e
    except Exception as e:
        session.rollback()
        logger.exception(
            f"Error al crear historia medica para paciente '{patient_id}': {e}"
        )
        raise HTTPException(status_code=500, detail="Error interno del servidor")


def get_medical_histories_by_patient(
    session: SessionDep, patient_id: str, current_user: User
):
    try:
        statement = select(Patient).where(
            Patient.id == patient_id, Patient.doctor_id == current_user.id
        )
        patient: Patient = session.exec(statement).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")

        statement = select(MedicalHistory).where(
            MedicalHistory.patient_id == patient_id
        )
        histories = session.exec(statement).all()

        # Construir respuesta con medicamentos para cada historia
        results = []
        for h in histories:
            read = MedicalHistoryRead.model_validate(h)
            read.medications = _build_medication_reads(h)
            results.append(read)
        return results
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(f"Error al obtener historias del paciente '{patient_id}': {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
