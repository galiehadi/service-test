========================================== Aplikasi Backend ==========================================

PENDAHULUAN :
sebelum saya memulai penjelasan tentang tutorial testing aplikasi ini, dst. saya akan menjelaskan sedikit tentang poin - poin yang saya pahami dari permintaan kebutuhan aplikasi ini terlebih dahulu sehingga harapannya jika ada pemahaman saya yang salah tentang kebutuhannya bisa dikomunikasikan terlebih lanjut. baik, kebutuhannya sebagai berikut :

1. API dapat menampilkan seluruh data menu. dengan ketentuan setiap menu mempunyai isian dan topping masing - masing. serta untuk ketentuan harga, setiap menu, topping dan isian mempunyai harga masing - masing.
2. API dapat calculate total harga dari total menu yang dipesan, dengan ketentuan menu bisa dipesan sebanyak mungkin.
3. API dapat menentukan supaya setiap menu yang dipesan hanya bisa request untuk satu jenis topping atau tidak memakai topping, dan satu jenis isian atau tidak memakai isian (tidak boleh lebih dari 1 topping ataupun lebih dari 1 isian)
4. Project API bebas mau pakai bahasa pemrograman apa dan database apa
5. Project di upload ke DockerHub dan github / gitlab

baik, dari pemahaman saya diatas semoga tidak ada pemahaman yang berbeda mengenai project yang saya buat. adapun pertanyaan yang mau disampaikan bisa ditanyakan kepada saya, untuk saat ini bisa melalui email galiehadisurya@gmail.com.


Poin 1,2,3, Penjelasan tentang API dan kebutuhan User :
Poin 1 :
    untuk menampilkan seluruh data menu ke user. kita menggunakan API dengan URL "localhost:8083/service/all/data". untuk contoh hasil JSON yang dikirm ke frontend, bisa dibuka di file "API.txt". step untuk mencoba di lokal:
    - pastikan aplikasi sudah berjalan lancar dan tidak ada error termasuk koneksi ke databasenya. jika melalui docker bisa pastikan menggunakan command "docker ps -a" dan pastikan container dalam status up, gunakan juga docker logs -f -n 50 {nama container} untuk melihat apakah ada pesan error. jika menjalankan program menggunakan VSCode, pastikan project sudah dibuka  di jendela VSCode dengan benar. lalu pastikan untuk aktif tab nya di file main.py, klik "Run" lalu "run Whitout Debugging". aplikasi akan berjalan di port 8083.
    - setelah dipastikan project berjalan normal lalu bisa dicoba akses API menggunakan aplikasi postman. untuk poin 1 ini kita menggunakan metode GET. jadi pilih get laulu masukkan URL "localhost:8083/service/all/data", lalu klik send. jika semua bberjalan lancar maka akan keluar feedback berupa hasil JSON, jika ada error maka akan muncul pesan error.
Poin 2,3 :
    - untuk poin 2 dan 3 saya jadikan di 1 API, jadi sebelum program melakukan calculasi untuk menghitung total harga, maka akan  dilakukan pengecekan terlebih dahulu apakah ada topping atau filling yang lebih dari 1 jenis. jika ada maka akan muncul pesan error, contoh seperti di dalam file "API.txt". untuk metode yang digunakan API menggunakan POST dengan data JSON yang dikirim dari frontend. URl yang dipakai "127.0.0.1:8083/service/count/price"
    - jika poin 2 terpenuhi maka akan dilanjutkan kalkulasi. proses kalkulasi karena asumsi saya frontend sudah memiliki data menuu dengan lengkap beserta harga, maka saya request untuk data JSON yang dikirim menyertakan harga juga. jadi untuk contoh format JSON yang dikirim ke API bisa dicek di file "API.txt". ubtuk hasil kalkulasi harga akan dikembalikan dengan JSON juga dengan tambahan masing - masing total price setiap menu dan juga total price dari keseluruhan menu, contoh feedback JSON bisa dilihat di "API.py".



Poin 4, Tools Project :
berikut tools yang dibutuhkan untuk membuat project ini.
- bahasa pemrograman menggunakan PYTHON v.3.7.x dengan library tambahan :
    - Pandas
    - mysql-connector
    - Flask
    - Flask Core
    - SQLAlchemy
    - urllib3
- untuk database menggunakan MYSQL v10.4.x dengan configurasi tambahan sebagai berikut:
    - username DB   : "toor"
    - password DB   : "P@ssw0rd"
    - port          : 3306
    - DB name       : "menu"
    - struktur table dan data bisa buka di sql.txt. disitu sudah terdapat query untuk create table" yg dibuutuhkan serta insert data yang dibutuhkan.
- untuk docker lokal yang saya pakai. menggunakan docker v.24.0.5. image akan di upload di dockerhub
- untuk github yang saya gunakan versi "git version 2.31.0.windows.1". project nantinya akan di upload di github