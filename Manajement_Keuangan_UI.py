import streamlit as st
import timeit

# Fungsi Brute Force
def brute_force(uang_saku, target_tabungan, rentang_pengeluaran):
    semua_pembagian = []
    for makan in range(rentang_pengeluaran['makan_min'], rentang_pengeluaran['makan_max'] + 1, 50000):
        for transportasi in range(rentang_pengeluaran['transportasi_min'], rentang_pengeluaran['transportasi_max'] + 1, 50000):
            for kontrakan in range(rentang_pengeluaran['kontrakan_min'], rentang_pengeluaran['kontrakan_max'] + 1, 50000):
                for jajan in range(rentang_pengeluaran['jajan_min'], rentang_pengeluaran['jajan_max'] + 1, 50000):
                    total_pengeluaran = makan + transportasi + kontrakan + jajan
                    tabungan = uang_saku - total_pengeluaran
                    if tabungan == target_tabungan:
                        pembagian = {'makan': makan, 'transportasi': transportasi, 'kontrakan': kontrakan, 'jajan': jajan, 'tabungan': tabungan}
                        semua_pembagian.append(pembagian)
    return semua_pembagian

# fungsi Backtracking
def backtracking(uang_saku, target_tabungan, rentang_pengeluaran):
    def backtrack(assignment, idx, total_pengeluaran):
        nonlocal semua_pembagian
        if idx == len(categories):
            tabungan = uang_saku - total_pengeluaran
            if tabungan == target_tabungan:
                semua_pembagian.append(assignment.copy())
        else:
            category = categories[idx]
            for amount in range(rentang_pengeluaran[f'{category}_min'], rentang_pengeluaran[f'{category}_max'] + 1, 50000):
                new_total = total_pengeluaran + amount
                if new_total <= uang_saku: 
                    assignment[category] = amount
                    backtrack(assignment, idx + 1, new_total)
                    assignment[category] = 0

    categories = ['makan', 'transportasi', 'kontrakan', 'jajan']
    semua_pembagian = []
    assignment = {category: 0 for category in categories}
    backtrack(assignment, 0, 0)

    return semua_pembagian


# UI Streamlit
st.title("Aplikasi Pembagian Uang Saku")

# Input dari pengguna
uang_saku = st.number_input("Masukkan uang saku bulanan:", min_value=0, step=50000)
target_tabungan = st.number_input("Masukkan target tabungan:", min_value=0, step=50000)

rentang_pengeluaran = {
    'makan_min': 50000,
    'makan_max': st.number_input("Masukkan rentang target pengeluaran uang makan (min. 50k):", min_value=50000, step=50000),
    'transportasi_min': 50000,
    'transportasi_max': st.number_input("Masukkan rentang target pengeluaran uang transportasi (min. 50k):", min_value=50000, step=50000),
    'kontrakan_min': 50000,
    'kontrakan_max': st.number_input("Masukkan rentang target pengeluaran uang kontrakan (min. 50k):", min_value=50000, step=50000),
    'jajan_min': 50000,
    'jajan_max': st.number_input("Masukkan rentang target pengeluaran uang jajan (min. 50k):", min_value=50000, step=50000),
}

metode = st.selectbox("Pilih metode:", ["Brute Force", "Backtracking"])

# Menjalankan algoritma berdasarkan metode yang dipilih
if st.button("Hitung"):
    # Hitung waktu eksekusi metode terpilih
    if metode == "Brute Force":
        durasi_metode_terpilih = timeit.timeit(lambda: brute_force(uang_saku, target_tabungan, rentang_pengeluaran), number=1)
        pembagian_semua = brute_force(uang_saku, target_tabungan, rentang_pengeluaran)
    else:
        durasi_metode_terpilih = timeit.timeit(lambda: backtracking(uang_saku, target_tabungan, rentang_pengeluaran), number=1)
        pembagian_semua = backtracking(uang_saku, target_tabungan, rentang_pengeluaran)

    # Hitung waktu eksekusi metode lain untuk perbandingan
    if metode == "Brute Force":
        durasi_metode_lainnya = timeit.timeit(lambda: backtracking(uang_saku, target_tabungan, rentang_pengeluaran), number=1)
        nama_metode_lainnya = "Backtracking"
    else:
        durasi_metode_lainnya = timeit.timeit(lambda: brute_force(uang_saku, target_tabungan, rentang_pengeluaran), number=1)
        nama_metode_lainnya = "Brute Force"

   

    # Tampilkan kombinasi yang memenuhi syarat
    if pembagian_semua:
         # Tampilkan hasil dan perbandingan durasi eksekusi
        st.write(f"Durasi waktu eksekusi metode {metode}: {durasi_metode_terpilih:.10f} detik")
        st.write(f"Durasi waktu eksekusi metode {nama_metode_lainnya}: {durasi_metode_lainnya:.10f} detik")
    
        if durasi_metode_terpilih < durasi_metode_lainnya:
            st.write(f"Metode {metode} lebih cepat daripada metode {nama_metode_lainnya}.")
        else:
            st.write(f"Metode {metode} lebih lambat daripada metode {nama_metode_lainnya}.")
        st.write("Semua kombinasi pembagian yang memenuhi syarat:")
        for idx, pembagian in enumerate(pembagian_semua, start=1):
            st.write(f"\nPilihan {idx}:")
            st.write(pembagian)
    else:
        if uang_saku == (target_tabungan + rentang_pengeluaran['makan_max'] + rentang_pengeluaran['transportasi_max'] + rentang_pengeluaran['kontrakan_max'] + rentang_pengeluaran['jajan_max']):
            st.write("Maaf, tidak ada kombinasi apapun yang ditemukan.")
        elif uang_saku > (target_tabungan + rentang_pengeluaran['makan_max'] + rentang_pengeluaran['transportasi_max'] + rentang_pengeluaran['kontrakan_max'] + rentang_pengeluaran['jajan_max']):
            st.write("Maaf, tidak ada kombinasi apapun yang ditemukan.")
            st.warning("Pastikan total tabungan dan rentang pengeluaran anda tidak kurang dari uang saku anda")
