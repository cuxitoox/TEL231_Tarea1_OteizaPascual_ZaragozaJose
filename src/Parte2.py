import numpy as np
import librosa
import soundfile as sf
from pydub import AudioSegment
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Rutas manuales
in_path = "../audios/audio_original/audio1.wav"  
out_lp = "../audios/audios_filtrados/PB_leq_1000Hz.wav"
out_bp = "../audios/audios_filtrados/PBanda_300-3400Hz.wav"
out_hp = "../audios/audios_filtrados/PA_geq_1000Hz.wav"
graf_lp = "../graficos/Parte2/comparativa_PB.html"
graf_bp = "../graficos/Parte2/comparativa_PBanda.html"
graf_hp = "../graficos/Parte2/comparativa_PA.html"

def load_audio(path, sr=16000):
    """
    Carga un archivo de audio y lo remuestrea a la frecuencia 'sr' si es necesario.
    Devuelve el audio como vector numpy y la frecuencia de muestreo usada.
    """
    x, in_sr = librosa.load(path, sr=None, mono=True)
    if in_sr != sr:
        x = librosa.resample(x, orig_sr=in_sr, target_sr=sr)
    if np.max(np.abs(x)) > 1.0:
        x = x / np.max(np.abs(x))
    return x.astype(np.float32), sr

def save_wav(path, x, sr):
    """
    Guarda un vector de audio 'x' en un archivo WAV en la ruta 'path' con frecuencia 'sr'.
    Normaliza la señal para evitar saturación.
    """
    x_out = x / (np.max(np.abs(x)) + 1e-12)
    sf.write(path, x_out, sr)

def rfft_mag(x, sr):
    """
    Calcula la FFT de un solo lado (rfft) de la señal 'x' y devuelve:
    - X: FFT compleja
    - freqs: frecuencias correspondientes
    - mag: magnitud escalada para señales reales
    """
    N = len(x)
    X = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(N, d=1.0/sr)
    mag = np.abs(X) * (2.0 / N)
    mag[0] /= 2.0
    if N % 2 == 0:
        mag[-1] /= 2.0
    return X, freqs, mag

def apply_mask_and_irfft(X, mask, target_len):
    """
    Aplica una máscara frecuencial 'mask' a la FFT 'X' y reconstruye la señal temporal
    usando la IFFT. Devuelve la señal filtrada.
    """
    Xf = X * mask
    y = np.fft.irfft(Xf, n=target_len)
    mx = np.max(np.abs(y)) + 1e-12
    if mx > 1.0:
        y = y / mx
    return y

def design_masks(freqs, sr,f_lp=1000.0,f_bp=(300.0, 3400.0),f_hp=1000.0):
    """
    Crea máscaras ideales para filtros pasa bajos, pasa banda y pasa altos
    según las frecuencias de corte especificadas.
    """
    lp_mask = (freqs <= f_lp).astype(float)
    bp_mask = ((freqs >= f_bp[0]) & (freqs <= f_bp[1])).astype(float)
    hp_mask = (freqs >= f_hp).astype(float)
    return lp_mask, bp_mask, hp_mask

def plot_time_and_spectrum(x, y, sr, title_signal, title_spectrum, out_html):
    """
    Genera un gráfico comparativo (Plotly) entre la señal original 'x' y la filtrada 'y':
    - Arriba: dominio temporal
    - Abajo: espectro de magnitud
    Guarda el gráfico como archivo HTML.
    """
    t = np.arange(len(x)) / sr
    X, f, MagX = rfft_mag(x, sr)
    Y, _, MagY = rfft_mag(y, sr)
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=(title_signal, title_spectrum),
        vertical_spacing=0.12
    )
    fig.add_trace(go.Scatter(x=t, y=x, name="Original"), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=y, name="Filtrada"), row=1, col=1)
    fig.update_xaxes(title_text="Tiempo (s)", row=1, col=1)
    fig.update_yaxes(title_text="Amplitud", row=1, col=1)
    fig.add_trace(go.Scatter(x=f, y=MagX, name="Original"), row=2, col=1)
    fig.add_trace(go.Scatter(x=f, y=MagY, name="Filtrada"), row=2, col=1)
    fig.update_xaxes(title_text="Frecuencia (Hz)", row=2, col=1)
    fig.update_yaxes(title_text="|X(f)| (esc. 1-lado)", row=2, col=1)
    fig.update_layout(height=800, width=1100, title="Comparaciones")
    fig.write_html(out_html)
    print(f"[OK] Gráfico guardado: {out_html}")

# --- Pipeline principal ---
sr = 16000
x, sr = load_audio(in_path, sr=sr)
N = len(x)
X, freqs, _ = rfft_mag(x, sr)
lp_mask, bp_mask, hp_mask = design_masks(freqs, sr)
y_lp = apply_mask_and_irfft(X, lp_mask, N)
y_bp = apply_mask_and_irfft(X, bp_mask, N)
y_hp = apply_mask_and_irfft(X, hp_mask, N)
save_wav(out_lp, y_lp, sr)
save_wav(out_bp, y_bp, sr)
save_wav(out_hp, y_hp, sr)
plot_time_and_spectrum(
    x, y_lp, sr,
    title_signal="Temporal: Original vs Pasa-Bajos (<=1000 Hz)",
    title_spectrum="Espectro: Original vs Pasa-Bajos",
    out_html=graf_lp
)
plot_time_and_spectrum(
    x, y_bp, sr,
    title_signal="Temporal: Original vs Pasa-Banda (300–3400 Hz)",
    title_spectrum="Espectro: Original vs Pasa-Banda",
    out_html=graf_bp
)
plot_time_and_spectrum(
    x, y_hp, sr,
    title_signal="Temporal: Original vs Pasa-Altos (>=1000 Hz)",
    title_spectrum="Espectro: Original vs Pasa-Altos",
    out_html=graf_hp
)
print("[FIN] Listo.")