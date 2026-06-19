# SGC Backend MongoDB

Sistema de Gestión de Contenidos (SGC) con backend basado en MongoDB

## 📋 Descripción

**SGC Backend MongoDB** es una aplicación backend completa diseñada para gestionar contenidos utilizando MongoDB como base de datos. Este proyecto implementa una arquitectura moderna que combina JavaScript/Node.js con Python para proporcionar una solución robusta y escalable.

## 🛠️ Stack Tecnológico

- **JavaScript** (46.1%) - Lógica principal del backend
- **Python** (37.8%) - Procesamiento y utilidades adicionales
- **CSS** (15.3%) - Estilos (si incluye frontend)
- **HTML** (0.8%) - Plantillas

### Tecnologías Principales
- **Base de Datos:** MongoDB
- **Runtime:** Node.js
- **Lenguajes:** JavaScript, Python

## 📁 Estructura del Proyecto

```
sgc-backend-mongodb/
├── README.md
├── package.json
├── src/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   ├── middleware/
│   └── utils/
├── python/
│   └── [scripts y utilidades Python]
├── tests/
└── .env.example
```

## 🚀 Características

- ✅ API RESTful completa
- ✅ Integración con MongoDB
- ✅ Autenticación y autorización
- ✅ Validación de datos
- ✅ Manejo de errores robusto
- ✅ Scripts de utilidad en Python

## 📦 Instalación

### Requisitos Previos
- Node.js (v14 o superior)
- MongoDB (v4.0 o superior)
- Python (v3.8 o superior)
- npm o yarn

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Josue337/sgc-backend-mongodb.git
   cd sgc-backend-mongodb
   ```

2. **Instalar dependencias de Node.js**
   ```bash
   npm install
   ```

3. **Instalar dependencias de Python (si aplica)**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   ```
   Edita el archivo `.env` con tus configuraciones:
   ```
   MONGODB_URI=mongodb://localhost:27017/sgc
   PORT=3000
   NODE_ENV=development
   ```

5. **Iniciar la aplicación**
   ```bash
   npm start
   ```

## 🔧 Configuración

### MongoDB
Asegúrate de que MongoDB está ejecutándose en tu máquina local o configura la URI de conexión remota en el archivo `.env`:

```bash
MONGODB_URI=mongodb+srv://usuario:contraseña@cluster.mongodb.net/sgc
```

### Variables de Entorno
Consulta el archivo `.env.example` para ver todas las variables disponibles.

## 📚 Uso

### Iniciar el servidor
```bash
npm start
```

### Modo desarrollo con reinicio automático
```bash
npm run dev
```

### Ejecutar tests
```bash
npm test
```

## 🔌 API Endpoints

La API ofrece múltiples endpoints para gestionar contenidos. Consulta la documentación específica o los comentarios en el código fuente para más detalles.

Ejemplo básico:
```bash
GET /api/contenidos
POST /api/contenidos
GET /api/contenidos/:id
PUT /api/contenidos/:id
DELETE /api/contenidos/:id
```

## 🐍 Scripts Python

Los scripts Python ubicados en la carpeta `python/` pueden ejecutarse para:
- Procesar datos
- Realizar migraciones
- Tareas de mantenimiento

```bash
python python/script_name.py
```

## 🧪 Testing

Ejecuta los tests con:
```bash
npm test
```

Para cobertura de código:
```bash
npm run test:coverage
```

## 📝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo una licencia abierta. Consulta el archivo LICENSE para más detalles.

## 👤 Autor

- **GitHub:** [@Josue337](https://github.com/Josue337)

## 📞 Soporte

Si encuentras problemas o tienes preguntas, por favor:
- Abre un [Issue](https://github.com/Josue337/sgc-backend-mongodb/issues)
- Consulta la [Wiki](https://github.com/Josue337/sgc-backend-mongodb/wiki)

## 🔄 Cambios Recientes

- Proyecto creado el 2026-06-19
- Rama principal: `main`

---

**Última actualización:** Junio 19, 2026
