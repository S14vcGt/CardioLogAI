from sqlmodel import Session, SQLModel
from faker import Faker
from app.core.config import engine
from app.core.security import get_password_hash
from app.models import User
from app.models import MedicalHistory
from app.models import Patient
from app.core.const import Sex, ChestPainType, RestEcg, SmokingStatus

fake = Faker('es_ES') # Configurado en español

def create_tables():
    print("🗑️  Borrando tablas antiguas...")
    SQLModel.metadata.drop_all(engine)
    
    print("✨ Creando tablas nuevas...")
    SQLModel.metadata.create_all(engine)

def seed_data():
    print("🌱 Insertando datos de prueba (semilla)...")
    
    # 1. Definimos los objetos que queremos crear
    user = User(
        id='71bab27e-51aa-43da-a5ec-dd4e0c999afe', 
        is_admin=True, 
        username='test4',
        hashed_password=get_password_hash('test'), 
        full_name= 'testaferro testini', 
        email= 'testaferro@testini.com', 
        is_active=True
    )

    user2 = User(
        id='bbe29c00-8811-4321-9c66-e984d2495261', 
        is_admin=False,
        username='test3',
        hashed_password=get_password_hash('test'),
        full_name= 'testefano testonio',
        email= 'testefano@testonio.com',
        is_active=True
    )

    patient1 = Patient(
        id='3ad28c40-08ec-451e-81fa-22f3e8b0a9bd',
        name='Paciente',
        lastname='Prueba 1',
        birth_date='1980-05-15',
        address='Calle Falsa 123',
        cedula=12345678,
        phone='+584141234567',
        email='paciente1@prueba.com',
        sex=Sex.MALE,
        family_history=True,
        personal_history=False,
        doctor_id=user.id
    )

    history1 = MedicalHistory(
        id='a1e2f3g4-5678-90ab-cdef-123456789012',
        age=45,
        smoking_status=SmokingStatus.NEVER,
        sedentary_lifestyle=False,
        systolic_blood_pressure=120.0,
        diastolic_blood_pressure=80.0,
        ldl_cholesterol=100.0,
        max_hr=160.0,
        chest_pain_type=ChestPainType.ASYMPTOMATIC,
        exang=False,
        fasting_blood_sugar=90.0,
        body_mass_index=24.5,
        rest_ecg=RestEcg.NORMAL,
        weight=75.0,
        height=175.0,
        body_surface_area=1.9,
        heart_disease=False,
        model_prediction=0.15,
        model_confidence=0.90,
        model_used='Random Forest',
        description='Control de rutina, todo normal. Sin riesgo aparente.',
        patient_id=patient1.id
    )

    patient2 = Patient(
        id='9cf8ea11-66af-4386-8a50-681b9e863118',
        name='Paciente',
        lastname='Prueba 2',
        birth_date='1965-10-20',
        address='Avenida Principal 456',
        cedula=87654321,
        phone='+584129876543',
        email='paciente2@prueba.com',
        sex=Sex.FEMALE,
        family_history=False,
        personal_history=True,
        doctor_id=user2.id
    )

    history2 = MedicalHistory(
        id='b2c3d4e5-6789-01bc-defg-234567890123',
        age=60,
        smoking_status=SmokingStatus.CURRENT,
        sedentary_lifestyle=True,
        systolic_blood_pressure=140.0,
        diastolic_blood_pressure=90.0,
        ldl_cholesterol=150.0,
        max_hr=140.0,
        chest_pain_type=ChestPainType.TYPICAL_ANGINA,
        exang=True,
        fasting_blood_sugar=110.0,
        body_mass_index=28.0,
        rest_ecg=RestEcg.ST_ABNORMALITY,
        weight=85.0,
        height=165.0,
        body_surface_area=2.0,
        heart_disease=True,
        model_prediction=0.85,
        model_confidence=0.88,
        model_used='XGBoost',
        description='Paciente con riesgo cardiovascular elevado, requiere seguimiento.',
        patient_id=patient2.id
    )

    # 2. Abrimos una sesión para interactuar con la BD
    with Session(engine) as session:
        # Añadimos los objetos a la sesión (todavía no están en la BD)
        session.add(user)
        session.add(user2)
        session.add(patient1)
        session.add(history1)
        session.add(patient2)
        session.add(history2)
        
        # 3. Confirmamos los cambios (aquí se guardan en PostgreSQL)
        session.commit()
    
    print("✅ ¡Datos insertados con éxito!")

def seed_heavy_data():
    j=50
    usuarios_fake = []
    
    # Crear 50 usuarios falsos
    for _ in range(j):
        user = User(
            id=fake.uuid4(), 
            is_admin=False,
            username=fake.user_name(),
            hashed_password=fake.password(length=4),
            full_name= fake.name_nonbinary(),
            email= fake.email(),
            is_active=True
        )
        usuarios_fake.append(user)

    with Session(engine) as session:
        # add_all es más rápido para listas grandes
        session.add_all(usuarios_fake) 
        session.commit()
        
    print(f"🚀 ¡{j} usuarios falsos creados!")

if __name__ == "__main__":
    # Ejecutamos en orden: primero estructura, luego datos
    create_tables()
    seed_data()
    #seed_heavy_data()