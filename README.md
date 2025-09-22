# TEL231_Tarea1_OteizaPascual_ZaragozaJose

## Códigos Parte 3 y Parte 4

Este repositorio contiene los scripts en Python utilizados en la Tarea 1 del curso **TEL231 - Sistemas de Telecomunicaciones**.
Los códigos corresponden a la **Parte 3 (señal sintética y DFT)** y la **Parte 4 (procesamiento de audio con FFT y filtros)**.

---

## Estructura

```
src/
├── Parte1.py   # Código de la Parte 3
└── Parte2.py   # Código de la Parte 4
```

Las imágenes y audios generados se guardan automáticamente en carpetas separadas:

```
imagenes/       # Figuras generadas por los scripts
audios/
├── audio_original/   # Audio de entrada
└── audios_filtrados/ # Audios filtrados (salida)
```

---

##  Ejecución

### Parte 3 – Señal sintética y DFT

Genera la señal periódica, su DFT y la visualización 3D.

```bash
cd src
python Parte1.py
```

* Las figuras se guardarán en la carpeta `../imagenes/`.

### Parte 4 – Procesamiento de audio

Carga un archivo `.wav`, aplica filtros en frecuencia (pasa bajos, pasa banda y pasa altos) y reconstruye con IFFT.

```bash
cd src
python Parte2.py 
```

* Los audios resultantes se guardarán en `../audios/audios_filtrados/`.
* Las gráficas comparativas se guardarán en `../imagenes/`.

---

## Dependencias

Instala los paquetes necesarios con:

```bash
pip install numpy scipy matplotlib plotly librosa soundfile pydub
```

---

## Requerimientos adicionales

* Para que **pydub** funcione correctamente, necesitas tener **FFmpeg** instalado y accesible en tu sistema.

  * En Windows puedes instalarlo con:

    ```powershell
    winget install Gyan.FFmpeg
    ```
  * En Linux/macOS:

    ```bash
    sudo apt install ffmpeg
    # o
    brew install ffmpeg
    ```

---

## Autores

* José Zaragoza — 202230539-8 — jose.zaragoza@usm.cl
* Pascual Oteiza — 202230554-1 — pascual.oteiza@usm.cl
