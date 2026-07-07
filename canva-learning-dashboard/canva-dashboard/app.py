import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from collections import Counter
import re

st.set_page_config(
    page_title="Canva Learning Dashboard",
    page_icon="🎨",
    layout="wide",
)

DATA_DIR = Path(__file__).parent / "data"
LOOKER_EMBED_URL = "https://datastudio.google.com/embed/reporting/8af08094-4164-44b2-b1bc-33064c86bb37"

INDICATOR_GROUPS = {
    "Kemudahan Penggunaan": {
        "q_praktis_cepat": "Praktis & cepat digunakan",
        "q_fitur_mudah": "Fitur mudah dipahami",
        "q_navigasi_sederhana": "Navigasi sederhana",
        "q_mudah_temukan_fitur": "Mudah menemukan fitur",
        "q_cepat_belajar": "Cepat dipelajari",
    },
    "Manfaat yang Dirasakan": {
        "q_fitur_premium_gratis": "Fitur premium terasa gratis/terjangkau",
        "q_kualitas_visual": "Kualitas visual hasil desain",
        "q_mempermudah_tugas": "Mempermudah tugas kuliah",
        "q_terlihat_profesional": "Hasil terlihat profesional",
        "q_interaktif_kreatif": "Interaktif & mendorong kreativitas",
    },
    "Kepercayaan Platform": {
        "q_rasa_aman": "Rasa aman menggunakan aplikasi",
        "q_platform_andal": "Platform andal/stabil",
        "q_privasi_data": "Privasi data terjaga",
        "q_jarang_error": "Jarang mengalami error",
        "q_reputasi_populer": "Reputasi & popularitas",
    },
    "Loyalitas Pengguna": {
        "q_pakai_berulang": "Pakai berulang kali",
        "q_rekomendasikan": "Merekomendasikan ke orang lain",
        "q_pilih_canva": "Memilih Canva dibanding aplikasi lain",
        "q_eksplorasi_fitur": "Aktif eksplorasi fitur baru",
        "q_jadikan_utama": "Menjadikan Canva aplikasi utama",
    },
}
ALL_Q_LABELS = {k: v for grp in INDICATOR_GROUPS.values() for k, v in grp.items()}

STOPWORDS_ID = set("""
yang di ke dari dan atau untuk pada dengan ini itu adalah tidak juga saya aku kamu kita
akan sudah belum masih bisa ada ya nya nya. lah kok deh sih banget bgt gak ga tapi karena
jadi kalau kalo lebih paling sangat sekali dong si dr yg utk pd dgn krn tdk jd blm udh udah
buat dalam saat oleh atas bawah antara sebagai secara maka namun sementara begitu jika apa
aja aja. saja hanya cuma dia mereka kami kalian nih tuh kan deh wkwk wkwkwk
""".split())


@st.cache_data
def load_survey():
    df = pd.read_csv(DATA_DIR / "survey.csv")
    return df


@st.cache_data
def load_reviews():
    df = pd.read_csv(DATA_DIR / "reviews.csv", parse_dates=["tanggal"])
    return df


def top_words(texts, n=15):
    words = []
    for t in texts.dropna():
        tokens = re.findall(r"[a-zA-Z]+", str(t).lower())
        words.extend([w for w in tokens if w not in STOPWORDS_ID and len(w) > 2])
    return Counter(words).most_common(n)


survey = load_survey()
reviews = load_reviews()

st.title("🎨 Canva Learning Dashboard")
st.caption(
    "Dashboard interaktif — Analisis survei penerimaan pengguna & ulasan Google Play aplikasi Canva. "
    "Project akademik Manajemen Sistem Informasi."
)

tab1, tab2, tab3 = st.tabs(
    ["📋 Survei Pengguna", "⭐ Ulasan Google Play", "📊 Laporan Looker Studio"]
)

# ============================================================
# TAB 1 — SURVEY
# ============================================================
with tab1:
    st.sidebar.header("🔎 Filter Survei")
    gender_opt = st.sidebar.multiselect(
        "Jenis kelamin", sorted(survey["jenis_kelamin"].dropna().unique()),
        default=sorted(survey["jenis_kelamin"].dropna().unique())
    )
    freq_opt = st.sidebar.multiselect(
        "Frekuensi penggunaan", sorted(survey["frekuensi_penggunaan"].dropna().unique()),
        default=sorted(survey["frekuensi_penggunaan"].dropna().unique())
    )
    prodi_opt = st.sidebar.multiselect(
        "Program studi", sorted(survey["program_studi"].dropna().unique()),
        default=sorted(survey["program_studi"].dropna().unique())
    )

    f_survey = survey[
        survey["jenis_kelamin"].isin(gender_opt)
        & survey["frekuensi_penggunaan"].isin(freq_opt)
        & survey["program_studi"].isin(prodi_opt)
    ]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Responden", f"{len(f_survey)}")
    overall_mean = f_survey[list(ALL_Q_LABELS.keys())].mean().mean()
    c2.metric("Rata-rata Skor Keseluruhan", f"{overall_mean:.2f} / 5")
    pct_sering = (f_survey["frekuensi_penggunaan"].isin(["Sering", "Sangat Sering"])).mean() * 100
    c3.metric("% Pengguna Aktif (Sering+)", f"{pct_sering:.0f}%")
    c4.metric("Jumlah Program Studi", f_survey["program_studi"].nunique())

    st.divider()

    colA, colB = st.columns([1, 1])

    with colA:
        st.subheader("Radar Skor per Indikator")
        group_means = {
            grp: f_survey[list(cols.keys())].mean().mean()
            for grp, cols in INDICATOR_GROUPS.items()
        }
        radar_fig = go.Figure()
        radar_fig.add_trace(go.Scatterpolar(
            r=list(group_means.values()) + [list(group_means.values())[0]],
            theta=list(group_means.keys()) + [list(group_means.keys())[0]],
            fill="toself",
            name="Rata-rata"
        ))
        radar_fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=False, height=420,
            margin=dict(t=30, b=30)
        )
        st.plotly_chart(radar_fig, use_container_width=True)
        st.caption(
            "Catatan: pengelompokan 20 pertanyaan ke 4 indikator (Kemudahan, Manfaat, "
            "Kepercayaan, Loyalitas) merupakan interpretasi berdasarkan nama kolom kuesioner."
        )

    with colB:
        st.subheader("Skor Rata-rata per Pertanyaan")
        q_means = f_survey[list(ALL_Q_LABELS.keys())].mean().sort_values(ascending=True)
        bar_df = pd.DataFrame({
            "Pertanyaan": [ALL_Q_LABELS[k] for k in q_means.index],
            "Skor": q_means.values
        })
        fig_bar = px.bar(bar_df, x="Skor", y="Pertanyaan", orientation="h", range_x=[0, 5])
        fig_bar.update_layout(height=420, margin=dict(t=30, b=30))
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()
    st.subheader("Demografi Responden")
    d1, d2, d3 = st.columns(3)
    with d1:
        fig_g = px.pie(f_survey, names="jenis_kelamin", title="Jenis Kelamin", hole=0.4)
        st.plotly_chart(fig_g, use_container_width=True)
    with d2:
        fig_f = px.pie(f_survey, names="frekuensi_penggunaan", title="Frekuensi Penggunaan", hole=0.4)
        st.plotly_chart(fig_f, use_container_width=True)
    with d3:
        usia_counts = f_survey["usia"].dropna().value_counts().sort_index()
        fig_u = px.bar(x=usia_counts.index.astype(str), y=usia_counts.values,
                        labels={"x": "Usia", "y": "Jumlah"}, title="Distribusi Usia")
        st.plotly_chart(fig_u, use_container_width=True)

    st.subheader("Top 10 Program Studi Responden")
    prodi_counts = f_survey["program_studi"].value_counts().head(10)
    fig_p = px.bar(x=prodi_counts.values, y=prodi_counts.index, orientation="h",
                    labels={"x": "Jumlah Responden", "y": "Program Studi"})
    fig_p.update_layout(height=400)
    st.plotly_chart(fig_p, use_container_width=True)

    with st.expander("📄 Lihat data mentah survei"):
        st.dataframe(f_survey, use_container_width=True)

# ============================================================
# TAB 2 — GOOGLE PLAY REVIEWS
# ============================================================
with tab2:
    st.sidebar.header("🔎 Filter Ulasan")
    sent_opt = st.sidebar.multiselect(
        "Sentimen", sorted(reviews["sentimen"].dropna().unique()),
        default=sorted(reviews["sentimen"].dropna().unique())
    )
    rating_opt = st.sidebar.multiselect(
        "Rating", sorted(reviews["rating"].dropna().unique()),
        default=sorted(reviews["rating"].dropna().unique())
    )
    date_min, date_max = reviews["tanggal"].min(), reviews["tanggal"].max()
    date_range = st.sidebar.date_input(
        "Rentang tanggal", (date_min.date(), date_max.date()),
        min_value=date_min.date(), max_value=date_max.date()
    )

    f_rev = reviews[
        reviews["sentimen"].isin(sent_opt) & reviews["rating"].isin(rating_opt)
    ]
    if isinstance(date_range, tuple) and len(date_range) == 2:
        f_rev = f_rev[
            (f_rev["tanggal"].dt.date >= date_range[0])
            & (f_rev["tanggal"].dt.date <= date_range[1])
        ]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Ulasan", f"{len(f_rev)}")
    c2.metric("Rata-rata Rating", f"{f_rev['rating'].mean():.2f} ⭐" if len(f_rev) else "-")
    pct_pos = (f_rev["sentimen"] == "Positif").mean() * 100 if len(f_rev) else 0
    c3.metric("% Sentimen Positif", f"{pct_pos:.0f}%")
    pct_neg = (f_rev["sentimen"] == "Negatif").mean() * 100 if len(f_rev) else 0
    c4.metric("% Sentimen Negatif", f"{pct_neg:.0f}%")

    st.divider()
    e1, e2 = st.columns(2)
    with e1:
        st.subheader("Distribusi Rating")
        rc = f_rev["rating"].value_counts().sort_index()
        fig_r = px.bar(x=rc.index.astype(str), y=rc.values,
                        labels={"x": "Rating (bintang)", "y": "Jumlah Ulasan"})
        st.plotly_chart(fig_r, use_container_width=True)
    with e2:
        st.subheader("Proporsi Sentimen")
        fig_s = px.pie(f_rev, names="sentimen", hole=0.4,
                        color="sentimen",
                        color_discrete_map={"Positif": "#2ecc71", "Netral": "#f1c40f", "Negatif": "#e74c3c"})
        st.plotly_chart(fig_s, use_container_width=True)

    st.subheader("Tren Ulasan per Tanggal")
    trend = f_rev.groupby([f_rev["tanggal"].dt.date, "sentimen"]).size().reset_index(name="jumlah")
    fig_t = px.bar(trend, x="tanggal", y="jumlah", color="sentimen", barmode="stack",
                    color_discrete_map={"Positif": "#2ecc71", "Netral": "#f1c40f", "Negatif": "#e74c3c"})
    st.plotly_chart(fig_t, use_container_width=True)

    st.subheader("Kata yang Paling Sering Muncul dalam Ulasan")
    words = top_words(f_rev["review_asli"])
    if words:
        wdf = pd.DataFrame(words, columns=["Kata", "Frekuensi"])
        fig_w = px.bar(wdf.sort_values("Frekuensi"), x="Frekuensi", y="Kata", orientation="h")
        fig_w.update_layout(height=450)
        st.plotly_chart(fig_w, use_container_width=True)
    else:
        st.info("Tidak ada data untuk ditampilkan pada filter saat ini.")

    with st.expander("📄 Lihat data ulasan"):
        search = st.text_input("Cari kata kunci dalam ulasan")
        table = f_rev[["username", "rating", "review_asli", "versi_aplikasi", "tanggal", "sentimen"]]
        if search:
            table = table[table["review_asli"].str.contains(search, case=False, na=False)]
        st.dataframe(table, use_container_width=True)

# ============================================================
# TAB 3 — LOOKER STUDIO
# ============================================================
with tab3:
    st.subheader("📊 Laporan Looker Studio — Canva Learning Dashboard")
    st.caption(
        "Laporan ini bersumber langsung dari Looker Studio. Jika tampilan kosong, pastikan "
        "opsi 'Enable embedding' sudah diaktifkan pada pengaturan sharing report tersebut."
    )
    st.components.v1.iframe(LOOKER_EMBED_URL, height=700, scrolling=True)
    st.link_button("Buka laporan di tab baru", "https://datastudio.google.com/reporting/8af08094-4164-44b2-b1bc-33064c86bb37")

st.divider()
st.caption("Dibuat untuk keperluan akademik — Canva Learning Dashboard © 2026")
