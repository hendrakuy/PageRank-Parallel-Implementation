from mpi4py import MPI
import json

# Fungsi untuk memuat graph dari file JSON yang telah disimpan oleh crawler
def load_graph_from_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Fungsi untuk menghitung PageRank secara paralel menggunakan MPI
def parallel_pagerank(graph, num_iterations=100, d=0.85):
    # Inisialisasi MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank() 
    size = comm.Get_size() 

    num_pages = len(graph)  
    pages = list(graph.keys()) 
    # Inisialisasi nilai awal PageRank yang sama untuk setiap halaman
    pagerank = {page: 1 / num_pages for page in pages}
    
    # Melakukan iterasi untuk menghitung PageRank
    for _ in range(num_iterations):
        new_pagerank = {page: (1 - d) / num_pages for page in pages}
        local_pages = pages[rank::size]
        
        # Menghitung kontribusi lokal dari setiap halaman
        local_contributions = {page: 0 for page in pages}
        for page in local_pages:
            for link in graph.get(page, []):
                if link in pagerank:
                    local_contributions[link] += pagerank[page] / len(graph[page])

        # Menggabungkan kontribusi dari semua proses dengan operasi penjumlahan (reduce)
        total_contributions = comm.allreduce(list(local_contributions.values()), op=MPI.SUM)
        
        # Update nilai PageRank berdasarkan kontribusi yang diterima
        for idx, page in enumerate(pages):
            new_pagerank[page] += d * total_contributions[idx]
                
        # Memperbarui nilai PageRank untuk iterasi berikutnya
        pagerank = new_pagerank

    return pagerank

# Blok utama untuk memuat graph, menghitung PageRank secara paralel, dan menyimpan hasil
if __name__ == "__main__":
    filename = 'crawled_site_data.json' 
    graph = load_graph_from_json(filename) 
    pagerank = parallel_pagerank(graph) 

    # Urutkan hasil PageRank dari yang tertinggi ke yang terendah
    sorted_pagerank = dict(sorted(pagerank.items(), key=lambda item: item[1], reverse=True))

    # Proses dengan rank 0 akan menyimpan hasil PageRank ke dalam file JSON
    if MPI.COMM_WORLD.Get_rank() == 0:
        result_filename = 'sorted_pagerank.json'
        with open(result_filename, 'w') as f:
            json.dump(sorted_pagerank, f, indent=4)
        print(f"Hasil PageRank yang telah diurutkan telah disimpan di {result_filename}")