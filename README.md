# Multi-Platform Secret Refresher

Este proyecto es un servicio de infraestructura diseñado para automatizar la renovación de tokens de acceso y credenciales de diversas plataformas (Mercado Libre, Bitcran, etc.). El objetivo es evitar la expiración de servicios críticos mediante la actualización proactiva de secretos en **Google Cloud Secret Manager**.

## 🛠️ Sistemas Integrados

* **Mercado Libre (OAuth 2.0):** Gestión del flujo de `access_token` y `refresh_token`. Dado que estos tokens expiran cada **6 horas**, el servicio automatiza el intercambio de credenciales.
* **Bitcran (Auth API):** Renovación de tokens de sesión con una ventana de validez de una semana. El script verifica la antigüedad del secreto y lo renueva si tiene más de **5 días**.
* **Whapi (Notificaciones):** Sistema de alerta integrado que envía mensajes automáticos por WhatsApp en caso de que alguna renovación falle, garantizando una rápida intervención manual si es necesario.

## 📋 Requisitos de Configuración

### 1. Variables de Entorno (`.env`)

Configura las siguientes variables para habilitar la comunicación con las APIs y GCP:

| Categoría | Variable | Descripción |
| --- | --- | --- |
| **GCP** | `PROJECT_ID` | ID del proyecto en Google Cloud. |
| **Meli** | `CLIENT_ID`, `CLIENT_SECRET`, `REDIRECT_URI` | Credenciales de la aplicación en Mercado Libre. |
| **Bitcran** | `USER_BITCRAM`, `PASSWRD_BITCRAM` | Credenciales de acceso a la plataforma Bitcran. |
| **Alertas** | `TOKEN_WHAPI`, `PHONE` | Token de Whapi y número de destino para alertas. |

### 2. Google Cloud Secret Manager

Es necesario crear los contenedores de los secretos manualmente antes de la primera ejecución:

* `SECRET_MELI_ID`: Almacenará un objeto JSON con la estructura de tokens.
* `SECRET_BITCRAM_ID`: Almacenará el string del token de sesión.

---

## 🚀 Flujo de Puesta en Marcha (First Run)

### Caso Especial: Mercado Libre

La API de Mercado Libre requiere un paso de autorización manual por única vez para generar el código inicial.

1. **Generar el CODE:** Ingresa la siguiente URL en tu navegador (reemplazando con tus datos):
`https://auth.mercadolibre.com.ar/authorization?response_type=code&client_id=TU_CLIENT_ID&redirect_uri=TU_REDIRECT_URI`
2. **Capturar el Código:** Tras autorizar, serás redirigido a tu URI. Copia el valor del parámetro `?code=` que aparece en la barra de direcciones.
3. **Configurar `FIRST_CODE`:** Pega ese valor en la variable `FIRST_CODE` de tu archivo `.env`.
4. **Ejecutar el Job:** En la primera corrida, el sistema usará ese código para obtener el primer par de tokens y los guardará en Secret Manager. A partir de ahí, el proceso será 100% automático usando el `refresh_token`.

---

## ⏱️ Consideraciones de Tiempo

El sistema está diseñado para ejecutarse como un cronjob (Cloud Scheduler) con las siguientes frecuencias recomendadas:

* **Mercado Libre:** Los tokens duran **6 horas**. Se recomienda ejecutar el refresher cada 4 o 5 horas.
* **Bitcran:** Los tokens duran **7 días**. El script tiene una lógica interna que solo solicita un nuevo token si el actual tiene **5 días o más** de antigüedad.

## ⚠️ Manejo de Errores

Si una renovación falla (por ejemplo, si los servidores de Meli están caídos o el `refresh_token` se invalida), el sistema:

1. Registra el error detallado en los logs.
2. Envía una notificación de alta prioridad vía **WhatsApp** indicando el sistema afectado y el error capturado para una resolución inmediata.

---