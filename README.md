# CardioLogAI

Sistema de información médica basado en machine learning para la detección temprana de enfermedades cardiovasculares.

## 🚀 Características

- **Autenticación segura**: Registro e inicio de sesión con JWT.
- **Gestión de pacientes**: CRUD completo con validación de datos.
- **Historial médico**: Registro y seguimiento de condiciones médicas.
- **Integración con IA**: Modelos de machine learning para diagnóstico temprano.
- **Base de datos PostgreSQL**: Persistencia segura y escalable.

## 🛠️ Instalación

1. **Clonar el repositorio**

```bash
git clone <url-del-repositorio>
cd backend
```

2. **Instalar dependencias**

```bash
uv sync
```

3. **Configurar variables de entorno**

Crea un archivo `.env` en la raíz del proyecto:

```bash
# PostgreSQL
DATABASE_URL="postgresql://user:password@host:port/database"

# JWT
SECRET_KEY="tu-clave-secreta"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Firebase
FIREBASE_CREDENTIALS_PATH="/path/to/serviceAccountKey.json"
```

4. **Crear la base de datos**

```bash
uv run python -m app.db.init_db
```

## 🏃 Ejecución

```bash
uv run uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`.

## 🧪 Tests

```bash
uv test
```

## 📂 Estructura del Proyecto

```
backend/
├── app/
│   ├── api/             # Endpoints de la API
│   ├── core/            # Configuración y seguridad
│   ├── db/              # Conexión y modelos de base de datos
│   ├── models/          # Modelos de datos
│   ├── schemas/         # Esquemas Pydantic
│   ├── services/        # Lógica de negocio
│   └── main.py          # Punto de entrada de la aplicación
├── tests/               # Tests de integración
├── .env                 # Variables de entorno
└── pyproject.toml       # Dependencias del proyecto
```

## 🤝 Contribuciones

1. Crear una rama para tu feature:

```bash
git checkout -b feature/nueva-funcionalidad
```

2. Desarrollar la funcionalidad y agregar tests.

3. Ejecutar tests:

```bash
uv test
```

4. Hacer commit y push:

```bash
git add .
git commit -m "feat: nueva funcionalidad"
git push origin feature/nueva-funcionalidad
```

5. Crear un Pull Request en GitHub.

## 📝 Licencia

Este proyecto es de código cerrado y pertenece a sus autores.