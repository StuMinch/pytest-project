# Device Check Service

This repository contains a small service that polls Sauce Labs private devices and runs pytest scripts when a device becomes available.

---

## English

### Prerequisites

- Python 3 (virtual environment recommended)
- `requests` and `pytest` installed in the environment
- Appium/test dependencies for your tests (for example `appium-python-client`)
- Your Sauce Labs credentials available as environment variables

Set credentials in your shell:

```bash
export SAUCE_USERNAME=your-username
export SAUCE_ACCESS_KEY=your-access-key
```

Activate the project's virtual environment (if used):

```bash
source venv/bin/activate
```

### Running the service

Run once (single run):

```bash
python device_check_service.py --max-runs 1 --test-script test_features.py
```

Run continuously (poll devices and run tests each time one becomes available):

```bash
python device_check_service.py
```

Override devices or poll interval:

```bash
python device_check_service.py --devices iPhone_SE_2020_POC132 iPhone_SE_2020_POC124 --poll-interval 15
```

Background (simple):

```bash
nohup python device_check_service.py > device_check.log 2>&1 &
```

### How tests receive device info

When a device becomes available the service sets the environment variable `SELECTED_DEVICE_ID` for the pytest process. In your tests read it with:

```python
import os
device_id = os.environ.get("SELECTED_DEVICE_ID")
```

### Troubleshooting

- Ensure `SAUCE_USERNAME` and `SAUCE_ACCESS_KEY` are correct.
- Verify network connectivity to Sauce Labs.
- Ensure the Python environment has `requests`, `pytest`, and any Appium/test dependencies installed.

---

## Español

### Requisitos previos

- Python 3 (se recomienda entorno virtual)
- `requests` y `pytest` instalados en el entorno
- Dependencias de Appium/tests necesarias (por ejemplo `appium-python-client`)
- Credenciales de Sauce Labs disponibles en variables de entorno

Configura las credenciales en tu shell:

```bash
export SAUCE_USERNAME=tu-usuario
export SAUCE_ACCESS_KEY=tu-access-key
```

Activa el entorno virtual del proyecto (si lo usas):

```bash
source venv/bin/activate
```

### Ejecutar el servicio

Ejecutar una vez (un solo run):

```bash
python device_check_service.py --max-runs 1 --test-script test_features.py
```

Ejecutar continuamente (hace polling y lanza pruebas cada vez que hay un dispositivo disponible):

```bash
python device_check_service.py
```

Sobrescribir dispositivos o intervalo de sondeo:

```bash
python device_check_service.py --devices iPhone_SE_2020_POC132 iPhone_SE_2020_POC124 --poll-interval 15
```

Ejecución en segundo plano (simple):

```bash
nohup python device_check_service.py > device_check.log 2>&1 &
```

### Cómo reciben las pruebas el dispositivo seleccionado

El servicio establece la variable de entorno `SELECTED_DEVICE_ID` para el proceso pytest cuando un dispositivo está disponible. En tus pruebas puedes leerla con:

```python
import os
device_id = os.environ.get("SELECTED_DEVICE_ID")
```

### Resolución de problemas

- Verifica que `SAUCE_USERNAME` y `SAUCE_ACCESS_KEY` sean correctos.
- Asegura la conectividad de red hacia Sauce Labs.
- Confirma que el entorno Python tenga `requests`, `pytest` y las dependencias de Appium/las pruebas instaladas.

---

If you want, I can also add a `requirements.txt` entry for `requests` and `appium-python-client`, or commit these changes to the repo.