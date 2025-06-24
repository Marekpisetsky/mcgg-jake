# 🤖 MCGG-JAKE – IA que aprende a jugar Magic Chess: Go Go

Bienvenido al repositorio oficial de **mcgg-jake**, un proyecto experimental de inteligencia artificial que aprende a jugar **Magic Chess: Go Go** como lo haría un humano: observando, interpretando y tomando decisiones sin reglas preprogramadas.

Antes de ejecutar cualquier script, instala todas las dependencias con:

```bash
pip install -r requirements.txt
```

En algunas plataformas `pyautogui` puede requerir paquetes del sistema (por ejemplo `scrot` y `xsel` en Linux).

---

## 🧠 ¿CÓMO FUNCIONARÁ LA IA DE MCGG-JAKE?

La IA sigue este ciclo general:

```
[Captura del estado del juego] → [Interpreta qué pasa en pantalla] → [Decide la mejor acción] → [Toma la acción] → [Observa el resultado] → [Aprende de la experiencia]
```

---

### 1. 📸 CAPTURA DEL ESTADO DEL JUEGO

**Entrada:** imágenes del juego (frames o capturas de pantalla).

**¿Qué detecta la IA en cada imagen?**

- Tu oro.
- Nivel actual del jugador.
- Cartas ofrecidas.
- Posiciones de héroes.
- Cofre del destino (cuando aparece).
- Ítems y sinergias.

**¿Cómo se usan estas imágenes?**

- Se guardan con su timestamp.
- Se emparejan con la acción que la IA tomó (o debió tomar).

---

### 2. 🧩 INTERPRETACIÓN DEL ESTADO (como un humano)

**NO usamos reglas preprogramadas.**

✅ En su lugar, usamos **visión computacional + aprendizaje automático**.

La IA aprende a identificar:

- Qué es una carta.
- Cuándo se gana oro.
- Cómo cambia la tienda.
- Qué decisiones llevan a la victoria.

---

### 3. 🕹️ DECISIÓN DE ACCIÓN

La IA debe aprender a decidir según el contexto:

| Momento             | Posibles Acciones                                 |
|---------------------|---------------------------------------------------|
| Tienda abierta      | Comprar carta A, B, C, o saltar                   |
| Fase de batalla     | No hacer nada                                     |
| Fase de tablero     | Colocar héroe, cambiar posición                   |
| Cofre del destino   | Elegir 1 de 3                                     |
| Entre rondas        | Actualizar tienda, subir de nivel, guardar oro   |

---

### 4. 📲 EJECUCIÓN DE LA ACCIÓN

Luego de decidir, la IA:

- Simula un toque en la pantalla (via `pyautogui` o `adb`).
- Espera y observa el siguiente estado.

---

### 5. 🧪 OBSERVACIÓN Y APRENDIZAJE

Se utiliza **aprendizaje por refuerzo**:

- Cada acción genera **recompensa** o **castigo**.

Ejemplos:

- ✅ Ganar una ronda tras una decisión → `+1`
- ❌ Perder oro innecesariamente → `-1`

Con el tiempo, la IA **maximiza su recompensa**.

---

### 6. 🔁 ENTRENAMIENTO CONTINUO

- Comienza con acciones aleatorias (exploración).
- Luego repite decisiones ganadoras (explotación).
- Se entrena con partidas almacenadas (frames + decisiones + resultados).

---

## 💡 EJEMPLO DE CICLO COMPLETO

```
🖼️ Frame 0341 del juego: la IA ve una tienda con Miya, Eudora y Layla.
🤔 Decide: “Compro Miya”.
🖱️ Simula clic en Miya.
⏱️ Espera y observa: ¿Ganó esa ronda? ¿Formó sinergia?
📈 Si fue buena decisión → la refuerza. Si no → la evita.
```

---

## 🔧 ¿QUÉ HAREMOS PRIMERO?

1. Grabar y dividir una partida en frames.
2. Etiquetar acciones por frame (opcional, al principio).
3. Crear dataset: imagen → acción → resultado.
4. Entrenar modelo con aprendizaje por refuerzo.
5. Ejecutar acciones reales más adelante.

---

## ✅ BENEFICIOS DEL ENFOQUE

- ❌ No depende de OCR ni reglas fijas.
- ✅ Aprende como un humano: viendo, probando y repitiendo.
- 🛠️ Se adapta incluso si el juego cambia ligeramente.

---

## 📁 ESTRUCTURA DEL REPO

- `leer_estado_juego.py` – Captura y análisis del estado actual.
- `motor_decisiones.py` – Modelo que decide acciones (en desarrollo).
- `oro_observador.py`, `leer_oro_automatico.py` – Sistema de detección de oro.
- `modelo_*.pth` – Pesos de los modelos entrenados.
- `mcgg_jake_runner.py` – Ciclo automatizado (por integrar).
- `detection.py` – Entrenamiento y uso del detector de objetos.

## 🎯 Entrenar el detector de objetos

1. Coloca tus capturas anotadas en `dataset/images` y las
   anotaciones en `dataset/annotations.json` (formato simple).
   Ahora se admiten clases adicionales para **cada héroe en tienda**,
   **las unidades del banco**, **el nivel del jugador** y objetos como
   cofres o ítems.
2. Ejecuta `python detection.py` con la función `train_detector` para
   generar `detector.pth` con todas estas clases.
3. Los módulos `leer_oro_automatico.py`, `leer_ronda_automatica.py`,
   `detectar_sinergias.py` y `leer_estado_juego.py` usarán ese modelo
   para localizar cada elemento sin depender de la resolución.
4. Para habilitar el aprendizaje continuo ejecuta `python autoentrenar_detector.py`.
   Este proceso captura nuevas imágenes etiquetadas durante las partidas y
   reentrena periódicamente, reemplazando `detector.pth` sin intervención manual.
5. Si deseas un ciclo totalmente autónomo (detector + agente DQN), ejecuta
   `python entrenamiento_autonomo.py`. Este script inicia el capturador y el
   bucle de entrenamiento para que el sistema juegue y aprenda sin supervisión.
6. Si los clics no coinciden con tu dispositivo, ajusta las constantes
   `SHOP_SLOT_COORDS` y `FIN_PARTIDA_REGION` en `config.py` según la resolución
   de pantalla.

---

## ⚙️ REQUISITOS

 - Python 3.10+
- `opencv-python`
- `pytesseract`
- `pyautogui`
- `Pillow`
- `torch` (en fase de entrenamiento)
- Instala todas estas dependencias con `pip install -r requirements.txt`

## Modo móvil

- Instala `scrcpy` o abre un emulador de Android.
- Ejecuta `adb start-server` y luego `adb devices` para verificar la conexión.
- Si se detecta tu dispositivo, ejecuta `scrcpy` para ver la pantalla en tiempo real.
- Si `adb devices` no muestra tu móvil, revisa los drivers USB y activa la depuración USB.

---

## 📜 LICENCIA

Distribuido bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

**Creado con visión, pasión y obsesión por automatizar Magic Chess.**
