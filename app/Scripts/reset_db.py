from sqlmodel import Session, SQLModel
from faker import Faker
from app.core.config import engine
from app.core.security import get_password_hash
from app.models import User
from app.models import MedicalHistory
from app.models import Patient

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
        hashed_password=get_password_hash('test3'),
        full_name= 'testefano testonio',
        email= 'testefano@testonio.com',
        is_active=True
    )

    # 2. Abrimos una sesión para interactuar con la BD
    with Session(engine) as session:
        # Añadimos los objetos a la sesión (todavía no están en la BD)
        session.add(user)
        session.add(user2)
        
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