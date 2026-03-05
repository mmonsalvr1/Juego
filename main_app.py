import streamlit as st
import random

# -------------------------------------------------
# Configuración de la app
# -------------------------------------------------
st.set_page_config(
    page_title="Operación: Descubre a tu Padrino",
    page_icon="🕵️‍♂️",
    layout="centered",
)

# -------------------------------------------------
# Parámetros del juego
# -------------------------------------------------
NOMBRE_REVEAL = "MATIAS"
RESPUESTA_CORRECTA = "Matias Monsalve"  # Debe coincidir EXACTO con la opción en SUSPECTOS
MIN_ACIERTOS = 3

SUSPECTOS = [
    "Samuel Restrepo",
    "Sara Valencia",
    "Alejandro Galeano",
    "Matias Monsalve",
]

PISTAS = [
    {
        "title": "Pista #1 💪 Energía",
        "text": (
            "Este padrino cree firmemente que el día mejora después de sudar un poco. "
            "No es raro verlo entrenando en el gym."
        ),
        "question": "¿Quién crees que encaja con esta pista?",
        "correct": RESPUESTA_CORRECTA,
    },
    {
        "title": "Pista #2 🥏 Deporte",
        "text": (
            "Mientras muchos juegan fútbol o baloncesto… "
            "este padrino corre detrás de un frisbee."
        ),
        "question": "¿Quién sería el padrino que juega ultimate?",
        "correct": RESPUESTA_CORRECTA,
    },
    {
        "title": "Pista #3 😌 Plan ideal",
        "text": (
            "Si hay dos opciones: fiesta gigante o un parche tranqui… "
            "este padrino prefiere el parche tranqui."
        ),
        "question": "¿Qué sospechoso crees que elige este plan?",
        "correct": RESPUESTA_CORRECTA,
    },
    {
        "title": "Pista #4 🍦 Debilidad",
        "text": (
            "Hay algo que puede mejorar cualquier día de este padrino: "
            "una bola (o mejor dos) de helado."
        ),
        "question": "¿Quién pediría helado sin pensarlo dos veces?",
        "correct": RESPUESTA_CORRECTA,
    },
    {
        "title": "Pista #5 🍫 La final",
        "text": (
            "Última pista: la fruta favorita de este padrino es… "
            "**el chocolate** 🍫 (no pregunten, solo disfruten)."
        ),
        "question": "¿Quién considera el chocolate como una fruta?",
        "correct": RESPUESTA_CORRECTA,
    },
]

# -------------------------------------------------
# Estado de sesión
# -------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 0  # 0 intro, 1 pistas, 2 mini-reto, 3 resultado

if "answers" not in st.session_state:
    st.session_state.answers = {}  # guarda pista_0..pista_4 y final_pick

# Guardamos un orden barajado por pista para que NO cambie con reruns
if "shuffled_options" not in st.session_state:
    st.session_state.shuffled_options = {}  # {idx: [opciones mezcladas]}

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def go(next_step: int):
    st.session_state.step = next_step
    st.rerun()

def reset_game():
    st.session_state.step = 0
    st.session_state.answers = {}
    st.session_state.shuffled_options = {}
    st.rerun()

def header():
    st.markdown(
        """
        <div style="text-align:center;">
            <h1 style="margin-bottom:0.2rem;">🕵️‍♂️ Operación: Descubre a tu Padrino</h1>
            <p style="margin-top:0; opacity:0.85;">Jueguito express: 5 pistas + mini reto final. Si aciertas, revelamos el padrino.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def contar_aciertos():
    aciertos = 0
    for i in range(len(PISTAS)):
        if st.session_state.answers.get(f"pista_{i}") == RESPUESTA_CORRECTA:
            aciertos += 1
    return aciertos

# -------------------------------------------------
# UI
# -------------------------------------------------
header()

# ---------------- STEP 0: Intro ----------------
if st.session_state.step == 0:
    st.divider()
    st.markdown("### 🚨 Caso abierto")
    st.write(
        "Tienes **5 pistas**. En cada una, elige el sospechoso que crees que es tu padrino. "
        "Al final, harás un mini-reto con tu **sospechoso final**."
    )
    st.info(
        f"Para resolver el caso debes acertar **mínimo {MIN_ACIERTOS}/5** pistas "
        "y también escoger bien el **sospechoso final**. Si no… tendrás que volver a intentarlo 😈"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎮 Empezar", use_container_width=True):
            st.session_state.answers = {}
            st.session_state.shuffled_options = {}
            go(1)
    with col2:
        st.write("📌 Tip: responde rápido, no lo pienses tanto 😄")

# ---------------- STEP 1: Pistas ----------------
elif st.session_state.step == 1:
    st.divider()

    idx = len([k for k in st.session_state.answers.keys() if k.startswith("pista_")])
    total = len(PISTAS)

    st.progress(min(idx, total) / total)
    st.caption(f"Pista {min(idx+1, total)}/{total}")

    if idx >= total:
        go(2)

    pista = PISTAS[idx]
    st.markdown(f"### {pista['title']}")
    st.write(pista["text"])

    # ✅ Opciones mezcladas por pista (se guardan para que no cambien en reruns)
    if idx not in st.session_state.shuffled_options:
        opciones = SUSPECTOS.copy()
        random.shuffle(opciones)
        st.session_state.shuffled_options[idx] = opciones
    else:
        opciones = st.session_state.shuffled_options[idx]

    choice = st.radio(
        pista["question"],
        options=opciones,
        index=None,
        key=f"choice_{idx}",
    )

    colA, colB = st.columns(2)
    with colA:
        if st.button("✅ Confirmar", use_container_width=True, disabled=(choice is None)):
            st.session_state.answers[f"pista_{idx}"] = choice
            st.success("Sospechoso anotado 👀")
            st.rerun()

    with colB:
        if st.button("🔁 Reiniciar", use_container_width=True):
            reset_game()

# ---------------- STEP 2: Mini-reto final ----------------
elif st.session_state.step == 2:
    st.divider()
    st.markdown("### 🧩 Mini-reto final")
    st.write("Ya tienes las 5 pistas. Ahora elige tu **sospechoso final** para resolver el caso.")

    aciertos = contar_aciertos()
    st.metric("Aciertos (por ahora)", f"{aciertos}/5")

    final_pick = st.selectbox("Tu sospechoso final es:", SUSPECTOS, index=0)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📩 Ver resultado", use_container_width=True):
            st.session_state.answers["final_pick"] = final_pick
            go(3)

    with col2:
        if st.button("⬅️ Volver a pistas", use_container_width=True):
            go(1)

# ---------------- STEP 3: Resultado (gated 3/5 + final correcto) ----------------
elif st.session_state.step == 3:
    st.divider()
    st.markdown("### 🧾 Resultado del caso")

    aciertos = contar_aciertos()
    final_pick = st.session_state.answers.get("final_pick", "—")

    st.write(f"Tu sospechoso final fue: **{final_pick}**")
    st.write(f"Aciertos: **{aciertos}/5** (mínimo **{MIN_ACIERTOS}**)")

    gano = (aciertos >= MIN_ACIERTOS) and (final_pick == RESPUESTA_CORRECTA)

    if gano:
        st.success("✅ ¡Caso resuelto! Reuniste suficientes pistas y elegiste el sospechoso final correcto.")
        st.balloons()
        st.markdown(f"## 🚨 Descubriste a: **{NOMBRE_REVEAL}** 😎💛")
        st.image("foto_matias.jpg", caption="Tu padrino 😎", width=300)
        st.info(
            "👉 Cuando me descubras, envía un mensaje por el grupo con una palabra que empiece por **M**. "
            "Y si eres la primera persona en enviarlo te ganas un premio 🏆"
        )
    else:
        st.error("❌ Te equivocaste… vuelve a intentarlo 😈")
        st.write("Tip: necesitas mínimo 3/5 y además escoger bien el sospechoso final.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Volver a intentar", use_container_width=True):
            reset_game()
    with col2:
        if st.button("⬅️ Volver a pistas", use_container_width=True):
            go(1)
