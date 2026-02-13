import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from app.services.patient import create, get_all_by_doctor, get_by_id
from app.models.patient import Patient
from app.schemas.patient import PatientCreate


@pytest.fixture
def mock_session():
    return MagicMock()


def test_create_patient_success(mock_session):
    patient = PatientCreate(
        name="Carlos",
        lastname="Pérez",
        birth_date="1990-05-15",  # String según tu modelo
        address="Av. Bolivar 123",
        cedula=20123456,
        phone="0414-1234567",
        email="carlos@test.com",
        sex="M",
        family_history=True,
        doctor_id="doc_uuid_888",
    )

    result = create(mock_session, patient)

    # Assert (Verificar)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

    # Verificamos que los datos críticos se pasaron correctamente
    # Al ser un unit test con mock, 'result' será el objeto que construyó tu función
    assert result.cedula == 20123456
    assert result.email == "carlos@test.com"
    assert result.doctor_id == "doc_uuid_888"


def test_create_patient_integrity_error(mock_session):
    # Arrange
    patient = PatientCreate(
        name="Carlos",
        lastname="Pérez",
        birth_date="1990-05-15",  # String según tu modelo
        address="Av. Bolivar 123",
        cedula=20123456,
        phone="0414-1234567",
        email="carlos@test.com",
        sex="M",
        family_history=True,
        doctor_id="doc_uuid_888",
    )
    # Simulamos que al hacer commit, la BD grita "Duplicado!"
    mock_session.commit.side_effect = IntegrityError(None, None, "Duplicate entry")

    with pytest.raises(HTTPException) as exc_info:
        create(mock_session, patient)

    assert exc_info.value.status_code == 400
    assert "Cedula ya registrada" in exc_info.value.detail
    mock_session.rollback.assert_called_once()  # Verificar que se hizo rollback


def test_create_patient_unexpected_error(mock_session):
    # Arrange
    patient_data = PatientCreate(
        name="Carlos",
        lastname="Pérez",
        birth_date="1990-05-15",  # String según tu modelo
        address="Av. Bolivar 123",
        cedula=20123456,
        phone="0414-1234567",
        email="carlos@test.com",
        sex="M",
        family_history=True,
        doctor_id="doc_uuid_888",
    )
    mock_session.commit.side_effect = Exception("DB Down")

    with pytest.raises(HTTPException) as exc_info:
        create(mock_session, patient_data)

    assert exc_info.value.status_code == 500
    assert "Error inesperado" in exc_info.value.detail
    mock_session.rollback.assert_called_once()


# --- TESTS PARA: get_all_by_doctor ---


def test_get_all_by_doctor_success(mock_session):
    # Arrange
    doctor_id = "doc_1"
    lista_pacientes = [{"id": "1"}, {"id": "2"}]

    # Simulamos la cadena: session.exec(stmt).all()
    mock_exec = mock_session.exec.return_value
    mock_exec.all.return_value = lista_pacientes

    result = get_all_by_doctor(mock_session, doctor_id)

    # Assert
    assert len(result) == 2
    assert result == lista_pacientes
    mock_session.exec.assert_called_once()


def test_get_all_by_doctor_error(mock_session):
    # Arrange
    mock_session.exec.side_effect = Exception("Fallo de conexión")

    with pytest.raises(HTTPException) as exc_info:
        get_all_by_doctor(mock_session, "doc_1")

    assert exc_info.value.status_code == 500


# --- TESTS PARA: get_by_id ---


def test_get_by_id_success(mock_session):
    mock_patient_db = Patient(
        id="patient_uuid_999",
        name="Carlos",
        lastname="Pérez",
        birth_date="1990-05-15",  # String según tu modelo
        address="Av. Bolivar 123",
        cedula=20123456,
        phone="0414-1234567",
        email="carlos@test.com",
        sex="M",
        family_history=True,
        doctor_id="doc_uuid_888",
    )
    mock_session.exec.return_value.first.return_value = mock_patient_db

    # Act
    result = get_by_id(mock_session, "patient_uuid_999")

    # Assert
    assert result.id == "patient_uuid_999"
    assert result.name == "Carlos"
    assert result.family_history is True  # Verificamos un campo booleano específico


def test_get_by_id_not_found(mock_session):

    mock_exec = mock_session.exec.return_value
    mock_exec.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        get_by_id(mock_session, "p_999")

    assert exc_info.value.status_code == 404
    assert "Paciente no encontrado" in exc_info.value.detail


def test_get_by_id_internal_error(mock_session):

    mock_session.exec.side_effect = Exception("Error crítico")

    with pytest.raises(HTTPException) as exc_info:
        get_by_id(mock_session, "p_1")

    assert exc_info.value.status_code == 500
    assert "Error inesperado" in exc_info.value.detail
    assert "Error crítico" in exc_info.value.detail
