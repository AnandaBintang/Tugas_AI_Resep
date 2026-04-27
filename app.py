import streamlit as st
import os
import urllib.parse
from dotenv import load_dotenv
from groq import Groq

# ==========================================
# BAGIAN 1: PENGATURAN KEAMANAN & API
# ==========================================
# Mengambil kunci rahasia dari file .env (Sesuai instruksi dosen)
load_dotenv()
API_KEY_GROQ = os.getenv("GROQ_API_KEY")

# ==========================================
# BAGIAN 2: MEMBUAT TAMPILAN ANTARMUKA (UI)
# ==========================================
st.title("AI Chef: Resep Sisa Kulkas")
st.write("Punya bahan sisa di kulkas tapi bingung mau dimasak apa? Tinggal masukin aja bahan-bahannya, nanti dicariin resep yang pas sekalian sama gambar masakannya.")

# Membuat kotak isian untuk pengguna
bahan_input = st.text_input("Bahan yang ada (pisahkan dengan koma):", placeholder="Contoh: Telur, Nasi, Sosis")

# Membuat tombol
if st.button("Buat Resep!"):
    # Mengecek apakah pengguna sudah mengisi bahan
    if bahan_input == "":
        st.warning("Isi dulu dong bahannya, jangan dikosongin.")
    else:
        # Menampilkan pesan loading
        pesan_tunggu = st.info("Lagi mikirin resep sama bikin gambarnya, tunggu bentar ya...")
        
        try:
            # ==========================================
            # BAGIAN 3: MODALITAS 1 - TEKS KE TEKS (GROQ)
            # ==========================================
            # Menghubungkan ke otak AI Groq
            client = Groq(api_key=API_KEY_GROQ)
            
            # Membuat instruksi (prompt) untuk AI
            prompt_koki = f"Lo itu koki rumahan yang jago masak. Gue cuma punya bahan ini: {bahan_input}. Bikinin 1 resep masakan yang gampang dibuat. Tulis nama masakannya di baris pertama, terus bahan-bahannya, sama cara bikinnya. Pake bahasa Indonesia yang santai dan natural, jangan pake emoji, jangan pake tanda strip panjang, dan jangan keliatan kayak ditulis robot."
            
            # Meminta AI menjawab
            respon_ai = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt_koki}],
                model="llama-3.1-8b-instant", # Ini adalah model AI gratis yang sangat cepat
            )
            
            # Menyimpan teks jawaban AI
            teks_resep = respon_ai.choices[0].message.content

            # ==========================================
            # BAGIAN 4: MODALITAS 2 - TEKS KE GAMBAR (POLLINATIONS)
            # ==========================================
            # Membuat instruksi gambar (dalam bahasa Inggris agar hasilnya lebih bagus)
            prompt_gambar = f"Delicious cooked food made with {bahan_input}, aesthetic food photography, high resolution"
            
            # Mengubah spasi menjadi format yang aman untuk Link/URL (misal spasi jadi %20)
            prompt_aman = urllib.parse.quote(prompt_gambar)
            
            # Menggabungkan ke link API Pollinations
            url_gambar = f"https://image.pollinations.ai/prompt/{prompt_aman}?width=720&height=480&nologo=true"

            # ==========================================
            # BAGIAN 5: MENAMPILKAN HASIL KE LAYAR
            # ==========================================
            pesan_tunggu.empty() # Menghapus pesan loading
            st.success("Nih resepnya udah jadi, cek di bawah ya.")
            
            # Menampilkan gambar dari URL Pollinations
            st.image(url_gambar, caption=f"Kira-kira tampilannya kayak gini kalau dimasak dari: {bahan_input}")
            
            # Menampilkan teks resep
            st.write(teks_resep)

        except Exception as e:
            st.error(f"Ada yang error nih, coba lagi nanti ya. Detail: {e}")