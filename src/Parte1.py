import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

### Parte 3a
# --- Parámetros ---
Fs = 1000          # Hz
T = 2.0            # s
t = np.arange(0, T, 1/Fs)

# --- Señal compuesta ---
x = (
    np.sin(2*np.pi*3*t)
    + (1/5)*np.sin(2*np.pi*7*t)
    + (3/10)*np.sin(2*np.pi*11*t)
    + (1/5)*np.sin(2*np.pi*17*t)
)


# --- Gráfico tiempo ---
plt.figure(figsize=(10,3.2))
plt.plot(t, x, linewidth=1.2)
plt.title("Señal x(t) en 0–2 s")
plt.xlabel("Tiempo t [s]")
plt.ylabel("Amplitud")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("../graficos/Parte1/parte3a_x_t.png", dpi=200)
plt.close()
print("Guardado: graficos/parte3a_x_t.png")

# Utilidades de señal/DFT

def generate_time_vector(T=2.0, fs=1000):
    """
    Genera vector de tiempo 0 <= t < T con paso 1/fs.
    """
    N = int(T * fs)
    t = np.arange(N) / fs
    return t, fs, N

def synth_signal(t, components):
    """
    components: lista de tuplas (A, f) para A*sin(2π f t)
    """
    x = np.zeros_like(t, dtype=float)
    for A, f in components:
        x += A * np.sin(2*np.pi*f*t)
    return x

def dft_single_sided(x, fs):
    """
    DFT de un solo lado y espectro de amplitud escalado para senoidales:
    Amp[k] = (2/N)*|X[k]|, sin duplicar DC ni Nyquist si existe.
    Retorna freqs (Hz) y Amp.
    """
    N = len(x)
    X = np.fft.rfft(x)                 # positivo + DC (+ Nyquist si N par)
    freqs = np.fft.rfftfreq(N, d=1/fs)
    Amp = (2.0 / N) * np.abs(X)

    # Ajuste de DC (k=0) y Nyquist (si corresponde) para no duplicar
    Amp[0] = Amp[0] / 2.0
    if N % 2 == 0:
        Amp[-1] = Amp[-1] / 2.0
    return freqs, Amp


# Visualización 3D (Plotly)

def plot_3d_time_spectrum_components(
    t, x, fs, components, title="Sección 3: Señal base, espectro y componentes (3D)",
    fmax_plot=40.0, use_stems=True, spectrum_x="end", spectrum_margin=0.10
):
    # --- DFT y recorte de rango ---
    freqs_full, Amp_full = dft_single_sided(x, fs)
    mask = freqs_full <= fmax_plot
    freqs, Amp = freqs_full[mask], Amp_full[mask]

    import plotly.graph_objects as go
    fig = go.Figure()

    # --- Señal temporal en banda Y=0 (X = t, Y = 0, Z = x(t)) ---
    fig.add_trace(go.Scatter3d(
        x=t, y=np.zeros_like(t), z=x,
        mode='lines', name='x(t) (Y=0)',
        hovertemplate="t=%{x:.3f}s<br>f=0 Hz<br>amp=%{z:.3f}"
    ))

    # --- Posición X para el espectro ---
    T = float(t.max()) if t.size else 0.0
    if spectrum_x == "end":
        x_spec_pos = T * (1.0 + spectrum_margin)  
    elif isinstance(spectrum_x, (int, float)):
        x_spec_pos = float(spectrum_x)
    else:
        x_spec_pos = 0.0  # fallback

    # --- Espectro en plano X = x_spec_pos (Y = f, Z = Amp) ---
    if use_stems:
        for fy, ay in zip(freqs, Amp):
            fig.add_trace(go.Scatter3d(
                x=[x_spec_pos, x_spec_pos], y=[fy, fy], z=[0, ay],
                mode='lines', name=None, showlegend=False
            ))
        fig.add_trace(go.Scatter3d(  # línea base
            x=np.full_like(freqs, x_spec_pos), y=freqs, z=np.zeros_like(freqs),
            mode='lines', name='Espectro', hoverinfo='skip'
        ))
    else:
        fig.add_trace(go.Scatter3d(
            x=np.full_like(freqs, x_spec_pos), y=freqs, z=Amp,
            mode='lines+markers', name='Espectro',
            hovertemplate="t≈%{x:.3f}s<br>f=%{y:.3f} Hz<br>Amp=%{z:.3f}"
        ))

    # --- Componentes senoidales cada una en su banda Y=f_i (X = t, Y=f_i, Z=A·sin(...)) ---
    for A, f in components:
        fig.add_trace(go.Scatter3d(
            x=t, y=np.full_like(t, f, dtype=float), z=A*np.sin(2*np.pi*f*t),
            mode='lines', name=f'Comp: A={A}, f={f} Hz'
        ))

    # --- Rango de ejes y título ---
    x_max_plot = x_spec_pos if x_spec_pos > T else T
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="Tiempo (s)",
            yaxis_title="Frecuencia (Hz)",
            zaxis_title="Amplitud",
            xaxis=dict(range=[0, x_max_plot*1.05]),
            yaxis=dict(range=[0, fmax_plot])
        ),
        legend=dict(x=0.02, y=0.98)
    )
    fig.show(renderer="browser")



if __name__ == "__main__":
    # (a) Señal base del enunciado
    base_components = [
        (1.0, 3.0),
        (0.2, 7.0),
        (0.3, 11.0),
        (0.2, 17.0),
    ]
    t, fs, N = generate_time_vector(T=2.0, fs=1000)  # fs alto para gráficos suaves
    x = synth_signal(t, base_components)

    # (b) DFT + justificación
    freqs, Amp = dft_single_sided(x, fs)

    # (c) Gráfico 3D para la señal base
    plot_3d_time_spectrum_components(t, x, fs, base_components,
        title="Sección 3: Señal base, espectro y componentes (3D)")

    # (d) Tres variantes para observar cambios en el espectro (edita a gusto)
    variants = [
        # Variante 1: más energía en baja frecuencia
        [(1.2, 3.0), (0.15, 7.0), (0.10, 11.0), (0.05, 17.0)],
        # Variante 2: desplazar frecuencias
        [(1.0, 4.0), (0.2, 8.0), (0.3, 12.0), (0.2, 18.0)],
        # Variante 3: menos componentes y amplitudes diferentes
        [(0.8, 3.0), (0.5, 11.0)]
    ]
    for i, comps in enumerate(variants, start=1):
        xi = synth_signal(t, comps)
        plot_3d_time_spectrum_components(
            t, xi, fs, comps,
            title=f"Sección 3(d): Variante {i} (3D)"
        )
