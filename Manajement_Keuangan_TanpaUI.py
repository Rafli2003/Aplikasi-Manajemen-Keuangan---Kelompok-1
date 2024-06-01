# Input dari user
uang_saku = int(input("Masukkan uang saku bulanan: "))
target_tabungan = int(input("Masukkan target tabungan: "))
rentang_pengeluaran = {
    'makan_min': 50000,
    'makan_max': int(input("Masukkan rentang target pengeluaran uang makan(min. 50k): ")),
    'transportasi_min': 50000,
    'transportasi_max': int(input("Masukkan rentang target pengeluaran uang transportasi(min. 50k): ")),
    'kontrakan_min': 50000,
    'kontrakan_max': int(input("Masukkan rentang target pengeluaran uang kontrakan(min. 50k): ")),
    'jajan_min': 50000,
    'jajan_max': int(input("Masukkan rentang target pengeluaran uang jajan(min. 50k): ")),
}

def brute_force(uang_saku, target_tabungan, rentang_pengeluaran):
    # list kosong untuk menyimpan kombinasi yang memenuhi syarat
    semua_pembagian = []
    
    # Iterasi pembagian semua kombinasi dengan kelipatan 50k
    for makan in range(rentang_pengeluaran['makan_min'], rentang_pengeluaran['makan_max'] + 1, 50000): # range(start, stop, step) 
        for transportasi in range(rentang_pengeluaran['transportasi_min'], rentang_pengeluaran['transportasi_max'] + 1, 50000):
            for kontrakan in range(rentang_pengeluaran['kontrakan_min'], rentang_pengeluaran['kontrakan_max'] + 1, 50000):
                for jajan in range(rentang_pengeluaran['jajan_min'], rentang_pengeluaran['jajan_max'] + 1, 50000):
                    # menghitung total pengeluaran
                    total_pengeluaran = makan + transportasi + kontrakan + jajan
                    # Hitung tabungan
                    tabungan = uang_saku - total_pengeluaran
                    # Periksa apakah tabungan mencapai target
                    if tabungan == target_tabungan:
                        pembagian = {'makan': makan, 'transportasi': transportasi, 'kontrakan': kontrakan, 'jajan': jajan, 'tabungan': tabungan}
                        semua_pembagian.append(pembagian)
    
    return semua_pembagian

def backtracking(uang_saku, target_tabungan, rentang_pengeluaran):
    def is_valid_solution(assignment):
        # Cek apakah total pengeluaran lebih kecil dari atau sama dengan uang saku
        return sum(assignment.values()) <= uang_saku

    def process_solution(assignment):
        # Hitung tabungan
        tabungan = uang_saku - sum(assignment.values())
        # Cek apakah tabungan sesuai dengan target
        return tabungan == target_tabungan, tabungan, assignment

    def backtrack(assignment, category_idx):
        if category_idx >= len(categories):
            is_solution, tabungan, pembagian = process_solution(assignment)
            if is_solution:
                pembagian['tabungan'] = tabungan
                semua_pembagian.append(pembagian.copy())
        else:
            category = categories[category_idx]
            for amount in range(rentang_pengeluaran[f'{category}_min'], rentang_pengeluaran[f'{category}_max'] + 1, 50000):
                assignment[category] = amount
                if is_valid_solution(assignment):
                    backtrack(assignment, category_idx + 1)
                assignment[category] = 0

    categories = ['makan', 'transportasi', 'kontrakan', 'jajan']
    semua_pembagian = []
    assignment = {category: 0 for category in categories}
    backtrack(assignment, 0)

    return semua_pembagian

# Meminta pengguna memilih metode
metode = input("Pilih metode (brute force/backtracking): ").strip().lower()

# Menggunakan metode yang dipilih
if metode == "brute force":
    semua_pembagian = brute_force(uang_saku, target_tabungan, rentang_pengeluaran)
elif metode == "backtracking":
    semua_pembagian = backtracking(uang_saku, target_tabungan, rentang_pengeluaran)
else:
    print("Metode tidak valid. Pilih 'brute force' atau 'backtracking'.")
    semua_pembagian = []

# Output semua kombinasi pembagian
if semua_pembagian:
    print("===================================================\n")
    print("Semua kombinasi pembagian yang memenuhi syarat:")
    for idx, pembagian in enumerate(semua_pembagian, start=1):
        print(f"\nPilihan {idx}:")
        for key, value in pembagian.items():
            print(f"{key}: {value}")
        print("===================================================")
else:
    print("Maaf, tidak ada kombinasi apapun yang ditemukan.")

