# Device Check Service

This repository contains a small service that polls Sauce Labs private devices and runs pytest scripts when a device becomes available.

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

### Comportamiento por script respecto a disponibilidad de dispositivos

Si pasas varios scripts con `--test-script`, el servicio comprobará la disponibilidad de dispositivos antes de ejecutar cada script. Flujo de ejemplo al ejecutar dos scripts:

1. El servicio espera a que cualquier dispositivo configurado esté AVAILABLE
2. Ejecuta `test_features.py`
3. Tras completar `test_features.py`, el servicio vuelve a comprobar la disponibilidad
4. Ejecuta `test_foodtruck.py` cuando un dispositivo esté AVAILABLE

Ejemplo de comando:

```bash
python device_check_service.py --max-runs 1 --test-script test_features.py test_foodtruck.py
```

Esto asegura que cada prueba comience sólo cuando haya un dispositivo realmente disponible (útil cuando varios dispositivos están compartidos).

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

### Per-script device availability behavior

When you pass multiple scripts with `--test-script`, the service will check for an available device before each script is executed. Example flow when running two scripts:

1. Service waits for any configured device to become AVAILABLE
2. Runs `test_features.py`
3. After `test_features.py` completes, the service re-checks device availability
4. Runs `test_foodtruck.py` when a device is AVAILABLE

Example command:

```bash
python device_check_service.py --max-runs 1 --test-script test_features.py test_foodtruck.py
```

This ensures each test starts only when a device is actually available (useful when multiple devices are shared).

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
