# **Hash Generator v3.0 - Manual del Usuario**
================================================================

## 📋 TABLA DE CONTENIDOS
================================================================
1.  DESCRIPCIÓN GENERAL
2.  REQUISITOS DEL SISTEMA
3.  INSTALACIÓN
4.  PRIMER USO
5.  GUÍA DE FUNCIONES
6.  SOLUCIÓN DE PROBLEMAS
7.  PREGUNTAS FRECUENTES
8.  INFORMACIÓN TÉCNICA
9.  SEGURIDAD Y PRIVACIDAD
10. REPORTES Y CONTRIBUCIONES

================================================================
## 🚀 1. DESCRIPCIÓN GENERAL
================================================================

**Hash Generator v3.0** es una aplicación profesional para generar,
comparar y verificar hashes criptográficos de archivos.

**USOS PRINCIPALES:**
• Verificar integridad de archivos descargados
• Comparar archivos duplicados
• Crear manifiestos de seguridad
• Auditoría de integridad de directorios

**CARACTERÍSTICAS PRINCIPALES:**
✅ Soporta 11 algoritmos diferentes (MD5, SHA256, SHA512, etc.)
✅ Interfaz gráfica moderna y fácil de usar
✅ Procesamiento por lotes
✅ Comparador inteligente de archivos
✅ Sistema de verificación de integridad
✅ Exportación a múltiples formatos (TXT, CSV, JSON)
✅ Registro de auditoría automático
✅ Totalmente portable (no requiere instalación)

================================================================
## 💻 REQUISITOS DEL SISTEMA
================================================================

**MÍNIMOS:**
• Windows 7, 8, 10 u 11
• 500 MB de espacio libre
• 1 GB de RAM
• Procesador de 1 GHz

**RECOMENDADO:**
• Windows 10/11 (64-bit)
• 4 GB de RAM
• 100 MB de espacio libre
• Procesador Dual-core

**NOTAS IMPORTANTES:**
• NO requiere Python instalado
• NO requiere .NET Framework
• NO requiere Java
• Totalmente portable - ejecuta desde USB

**ARCHIVOS MUY GRANDES (>4GB):**
Recomendado 4 GB RAM para procesamiento óptimo.

================================================================
## 📥 3. INSTALACIÓN
================================================================

**VERSIÓN PORTABLE**

1. DESCARGAR EL ARCHIVO:
   Obtén `HashGenerator_v3.0` desde el repositorio oficial GitHub

2. PREPARAR PARA PRIMER USO:
   Si Windows bloquea la aplicación:
   1. Haz clic derecho en HashGenerator_v3.0
   2. Selecciona "Propiedades"
   3. En la pestaña "General", marca "Desbloquear"
   4. Haz clic en "Aplicar" y "Aceptar"

3. AGREGAR EXCEPCIÓN EN WINDOWS DEFENDER (OPCIONAL):
   • Ejecuta `WindowsDefender_Manager.bat` como **Administrador**
   • Selecciona la opción **1** para agregar excepción automática

================================================================
## 🎯 4. PRIMER USO
================================================================

**EJECUCIÓN INICIAL:**
1. Doble clic en `HashGenerator_v3.0`
2. Si aparece advertencia de Windows:
   • Haz clic en "Más información"
   • Selecciona "Ejecutar de todas formas"
3. La aplicación se abre con interfaz en español

**CONFIGURACIÓN INICIAL RECOMENDADA:**
1. Ve a la pestaña "Configuración"
2. Selecciona tu tema preferido (Claro/Oscuro)
3. Configura formato de exportación predeterminado

================================================================
## 📚 5. GUÍA DE FUNCIONES
================================================================

### 5.1 📄 HASH INDIVIDUAL
Genera hash de un solo archivo.

**PASOS:**
1. Pestaña "Hash Individual"
2. Click en "Seleccionar archivo"
3. Elegir algoritmo (SHA256 ejemplo)
4. Click en "Calcular Hash"

**CARACTERÍSTICAS:**
• Barra de progreso en tiempo real
• Copia al portapapeles con un clic
• Tiempo de procesamiento mostrado
• Registro automático en logs

### 5.2 📦 HASH EN LOTE
Procesa múltiples archivos simultáneamente.

**PASOS:**
1. Pestaña "Hash en Lote"
2. "Agregar archivos" (Ctrl+A para múltiples)
3. Seleccionar algoritmo
4. "Calcular Lote"

**EXPORTACIÓN DE RESULTADOS:**
• TXT: Formato legible humano
• CSV: Para Excel/Google Sheets
• JSON: Para integración con otras apps

### 5.3 🔄 COMPARADOR
Compara dos archivos o un archivo con un hash.

**MODOS DE COMPARACIÓN:**
Modo 1: Archivo vs Archivo
   A: Seleccionar primer archivo
   B: Seleccionar segundo archivo

Modo 2: Archivo vs Hash
   A: Seleccionar archivo
   B: Pegar hash manualmente

**RESULTADOS:**
✅ COINCIDENCIA: Archivos idénticos
❌ DISTINTO: Archivos diferentes
⚠ ERROR: Problema en cálculo

### 5.4 🔍 VERIFICACIÓN DE INTEGRIDAD
Verifica archivos contra un manifiesto existente.

**CREAR MANIFIESTO:**
1. Seleccionar carpeta
2. Elegir algoritmo
3. "Crear manifest desde carpeta"
4. Guardar como JSON/CSV/TXT

**VERIFICAR INTEGRIDAD:**
1. "Cargar manifest" (archivo .json/.csv/.txt)
2. Seleccionar carpeta actual
3. Click en "Verificar contra manifest"

**RESULTADOS DETALLADOS:**
✓ archivo1.txt - OK
✗ archivo2.txt - MISMATCH (esperado: abc123, obtenido: def456)
✗ archivo3.txt - MISSING

### 5.5 ⚙ CONFIGURACIÓN

**OPCIONES DISPONIBLES:**
• Apariencia: Claro / Oscuro
• Exportación: Formato predeterminado
• Logs: Directorio de registros

================================================================
## 🔧 6. SOLUCIÓN DE PROBLEMAS
================================================================

### PROBLEMA 1: Windows bloquea la aplicación
SÍNTOMA: "Windows protegió tu PC"
SOLUCIÓN:
  1. Click derecho → Propiedades → Desbloquear
  2. Ejecutar WindowsDefender_Manager.bat como Admin
  3. Seleccionar opción 1

### PROBLEMA 2: Error "Falta MSVCR100.dll"
SOLUCIÓN:
  1. Descargar Visual C++ Redistributable:
     https://aka.ms/vs/17/release/vc_redist.x64.exe
  2. Instalar y reiniciar

### PROBLEMA 3: La aplicación se cierra inesperadamente
POSIBLES CAUSAS:
  • Archivo corrupto
  • Permisos insuficientes
  • Conflicto con antivirus

SOLUCIONES:
  1. Ejecutar como Administrador
  2. Desactivar temporalmente antivirus
  3. Descargar versión nueva

### PROBLEMA 4: No puede acceder a archivos de red
SOLUCIÓN:
  1. Verificar permisos de red
  2. Mapear unidad de red
  3. Copiar archivos localmente

### PROBLEMA 5: Lento con archivos muy grandes (>4GB)
OPTIMIZACIONES:
  • Usar algoritmos rápidos (xxHash64)
  • Cerrar otras aplicaciones
  • Procesar en lote separado

================================================================
## ❓ 7. PREGUNTAS FRECUENTES
================================================================

### Q1: ¿Qué algoritmo debo usar?
• Seguridad: SHA256 o SHA512
• Velocidad: xxHash64 o CRC32
• Compatibilidad: MD5 o SHA1
• Recomendado general: SHA256

### Q2: ¿Puedo usarlo en red corporativa?
✅ Sí, completamente seguro:
• No requiere conexión a internet
• No envía datos externos
• Solo lectura de archivos locales/red local

### Q3: ¿Cómo verificar archivos descargados?
1. Obtener hash oficial del sitio Web o del archivo a verificar.
2. Calcular hash con esta herramienta
3. Comparar en pestaña "Comparador"
4. Si coinciden: archivo íntegro

### Q4: ¿Dónde se guardan los logs?
• Por defecto: carpeta "logs" junto al ejecutable
• Contiene: audit_log.csv con todos los cálculos
• Formato: CSV compatible con Excel

### Q5: ¿Puedo cambiar el idioma?
• Actualmente solo español
• Próximas versiones incluirán inglés

### Q6: ¿Es seguro para datos confidenciales?
✅ Totalmente seguro:
• Procesamiento 100% local
• No hay telemetría
• No requiere internet
• Código abierto disponible

================================================================
## 🔬 8. INFORMACIÓN TÉCNICA
================================================================

### ALGORITMOS SOPORTADOS:
• MD5 (128-bit)
• SHA1 (160-bit)
• SHA256 (256-bit)
• SHA512 (512-bit)
• BLAKE2b (512-bit)
• BLAKE2s (256-bit)
• SHA3-256 (256-bit)
• SHA3-512 (512-bit)
• Whirlpool (512-bit)(Proximamente...)
• xxHash64 (64-bit)
• CRC32 (32-bit)
• Adler32 (32-bit)

### FORMATOS DE EXPORTACIÓN:
• TXT: Legible humano, ideal para reportes
• CSV: Compatible Excel/Google Sheets
• JSON: Para integración con otras apps
• Manifest: Especial para verificación

### ESPECIFICACIONES TÉCNICAS:
• Lenguaje: Python 3.11+
• GUI: CustomTkinter
• Tamaño ejecutable: ~15-50 MB
• Arquitectura: 64-bit
• Dependencias: Incluidas en el ejecutable

### LÍMITES CONOCIDOS:
• Tamaño máximo archivo: Limitado por RAM
• Caracteres especiales: Soporta UTF-8
• Rutas: Máximo 260 caracteres (limitación Windows)

================================================================
## 🔒 9. SEGURIDAD Y PRIVACIDAD
================================================================

### GARANTÍAS DE SEGURIDAD:
✅ No recopila información personal
✅ No requiere conexión a internet
✅ Código disponible para revisión

### POLÍTICA DE PRIVACIDAD:
1. CERO recolección de datos
2. CERO telemetría
3. CERO conexiones externas
4. CERO registro de uso
5. Solo logs locales opcionales

================================================================
## 10. REPORTES Y CONTRIBUCIONES
================================================================

### REPORTAR PROBLEMAS:
Incluir en el reporte:
1. Versión de Hash Generator
2. Sistema operativo y versión
3. Pasos para reproducir el error
4. Captura de pantalla si es posible
5. Archivo de log (logs/audit_log.csv)

### ACTUALIZACIONES:
• Versión actual: 3.0.0
• Fecha lanzamiento: 12/12/2025
• Próxima versión: 3.1 
• Actualizaciones: Manuales desde sitio web

### CONTRIBUCIONES:
¿Quieres contribuir?
• Reportar bugs en GitHub
• Sugerir características
• Traducir a otros idiomas
• Mejorar documentación

================================================================
## 📄 LICENCIA
================================================================

**LICENCIA MIT - Software Libre y de Código Abierto**

**PUEDES:**
✅ Usarlo para cualquier propósito (personal/comercial)
✅ Modificar y adaptar el código
✅ Distribuir copias (gratis o de pago)
✅ Incluirlo en otros proyectos

**DEBES:**
📋 Incluir el aviso de copyright original
📋 Mantener el texto de la licencia MIT

**EL AUTOR NO GARANTIZA:**
⚠ Funcionamiento en todos los sistemas
⚠ Corrección de errores
⚠ Soporte técnico obligatorio

**ATRIBUCIÓN:**
© 2025 Smith Lozano - Licencia MIT
Versión 3.0.0 - Código fuente disponible

================================================================
## 🌟 CONSEJOS AVANZADOS
================================================================

### PARA ADMINISTRADORES DE SISTEMAS:
• Usar manifiestos para auditorías regulares
• Programar verificaciones automáticas con scripts
• Integrar con sistemas de monitoreo vía exportación JSON
• Establecer políticas de hash corporativas (ej: solo SHA256)

### PARA DESARROLLADORES:
• Los manifiestos JSON pueden integrarse con APIs
• Los logs CSV son fáciles de analizar con PowerBI
• Puede usarse en pipelines de CI/CD para verificación

### PARA USUARIOS AVANZADOS:
• Combinar con robocopy para sincronización segura
• Usar en scripts PowerShell para automatización
• Integrar con sistemas de backup para verificación

================================================================
## 📖 GLOSARIO
================================================================

### TÉRMINOS TÉCNICOS:
• Hash: Huella digital única de un archivo
• Checksum: Sinónimo de hash para verificación
• Algoritmo: Método matemático para calcular hash
• Integridad: Garantía de que un archivo no ha cambiado
• Manifest: Lista de archivos con sus hashes
• Colisión: Cuando dos archivos diferentes tienen mismo hash

### COMPARATIVA DE ALGORITMOS:
┌─────────────────┬────────────┬──────────┬────────────┐
│ Algoritmo       │ Seguridad  │ Velocidad│ Tamaño hash│
├─────────────────┼────────────┼──────────┼────────────┤
│ MD5             │ Baja       │ Alta     │ 32 chars   │
│ SHA1            │ Media      │ Media    │ 40 chars   │
│ SHA256          │ Alta       │ Media    │ 64 chars   │
│ SHA512          │ Muy Alta   │ Baja     │ 128 chars  │
│ xxHash64        │ Baja       │ Muy Alta │ 16 chars   │
└─────────────────┴────────────┴──────────┴────────────┘

================================================================
## 🎉 AGRADECIMIENTOS
================================================================

Gracias por elegir **Hash Generator v3.0**.

**CRÉDITOS:**
• Desarrollador principal: Smith Lozano
• Librerías utilizadas: CustomTkinter, PyInstaller
• Comunidad: Agradecimientos a usuarios por feedback

**VERSIONES ANTERIORES:**
• v1.0 (2024): Versión inicial consola
• v2.0 (2025): Interfaz gráfica básica
• v3.0 (12/12/2025): Interfaz moderna, todas las funciones
================================================================
*Hash de verificación de este documento: Hash_Verificacion_HashGenerator_v3.0.txt*
================================================================
