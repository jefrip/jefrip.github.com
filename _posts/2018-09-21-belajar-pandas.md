---
layout: post
title: 'Belajar Pandas'
date: 2018-09-21 10:10:15.000000000 +07:00
categories:
- python
tags:
- pandas
- python
status: publish
type: post
published: true
author: admin
excerpt_separator: <!--more-->
---


[![Pandas]({{ site.baseurl }}/assets/pandas.png)](https://pandas.pydata.org){:target="_blank"}

Beberapa waktu lalu berawal dari keingintahuan saya untuk mengolah data csv yang agak besar, rasanya agak lebih mudah menggunakan Python untuk mengolah data csv yang cukup besar. Saya memulai belajar menggunakan Python (Python 3) dan ternyata cukup mudah hampir mirip seperti PHP yang selama ini saya gunakan.

Jadi beberapa hal yang harus saya lakukan adalah generate data dummy, dan mengolahnya. Dikarenakan saya baru saja mencoba 'Python' mungkin beberapa percobaan akan jadi catatan saya di blog ini, terutama penggunaan Pandas yang saya rasa sangat powerful dan cepat sekali dalam pengolahan data csv untuk ukuran data yang lumayan besar.
<!--more-->
Pastikan Anda sudah menginstall Pandas dengan cara :
Install melalui Anaconda
```
conda install pandas
```
Atau install melalui pip
```
pip install --upgrade pandas
```
Pada blog saya kali ini akan menggunakan data yang berasal dari dataset dki jakarta pada laman http://data.jakarta.go.id/dataset/jumlahrtrwperkelurahandkijakarta. Bentuk data yang kita gunakan berbentuk csv [Data-Jumlah-RT-RW-per-Kelurahan_2013-2017.csv](https://gist.githubusercontent.com/jefrip/86276aeb5aa3bffa384124574dae3535/raw/7b17f82a5a02a9d87514f6c7415bc9a92e57bb30/Data-Jumlah-RT-RW-per-Kelurahan_2013-2017.csv).


#### Struktur data Pandas
- Series (Array 1 Dimensi)
- Dataframe (Array 2 Dimensi)

Untuk memulai/membaca file csv pada Pandas sangat mudah sekali 
```
import pandas as pd
df = pd.read_csv('Data-Jumlah-RT-RW-per-Kelurahan_2013-2017.csv')
print(df)
```
df akan berisi sebuah Dataframe / array 2 dimensi yang akan bisa kita olah/ubah ke series, contoh output seperti berikut :
```
      tahun         nama_provinsi    ...    jumlah_rt jumlah_rw
0      2013  PROVINSI DKI JAKARTA    ...           29         5
1      2013  PROVINSI DKI JAKARTA    ...           31         5
2      2013  PROVINSI DKI JAKARTA    ...           15         3
...
```
Kita akan melihat data unik(distict dalam SQL) kolom kabupaten_kota :
```
available_kabkota = df['nama_kabupaten_kota'].unique()
print(available_kabkota)
```
Maka output yang dihasilkan adalah :
```
['KAB.ADM.KEP.SERIBU' 'JAKARTA PUSAT' 'JAKARTA UTARA' 'JAKARTA BARAT' 'JAKARTA SELATAN' 'JAKARTA TIMUR']
```


#### Group By: split-apply-combine
Jika kita ingin menghitung record suatu kolom tertentu kita gunakan fungsi size()
```
count_kabkota = df.groupby(['nama_kabupaten_kota']).size().reset_index(name='counts')
print(count_kabkota)
```
Outputnya :
```
  nama_kabupaten_kota  counts
0       JAKARTA BARAT     280
1       JAKARTA PUSAT     220
2     JAKARTA SELATAN     325
3       JAKARTA TIMUR     325
4       JAKARTA UTARA     155
5  KAB.ADM.KEP.SERIBU      30
```

Untuk penjumlahan suatu kolom terhadap kolom tertentu, semisal kita ingin total pada kolom jumlah_rt terhadap kolom nama_kabupaten_kota, nama_kecamatan, nama_kelurahan
```
rt = df.groupby(['nama_kabupaten_kota','nama_kecamatan','nama_kelurahan'])['jumlah_rt'].sum().reset_index()
print(rt)
```
Outputnya sebagai berikut :
```
    nama_kabupaten_kota     nama_kecamatan         nama_kelurahan  jumlah_rt
0         JAKARTA BARAT         CENGKARENG       CENGKARENG BARAT        906
1         JAKARTA BARAT         CENGKARENG       CENGKARENG TIMUR       1132
2         JAKARTA BARAT         CENGKARENG           DURI KOSAMBI        843
3         JAKARTA BARAT         CENGKARENG                  KAPUK       1110
4         JAKARTA BARAT         CENGKARENG     KEDAUNG KALI ANGKE        494
5         JAKARTA BARAT         CENGKARENG             RAWA BUAYA        700
6         JAKARTA BARAT  GROGOL PETAMBURAN                 GROGOL        570
7         JAKARTA BARAT  GROGOL PETAMBURAN               JELAMBAR        695
8         JAKARTA BARAT  GROGOL PETAMBURAN          JELAMBAR BARU        674
9         JAKARTA BARAT  GROGOL PETAMBURAN  TANJUNG DUREN SELATAN        463
10        JAKARTA BARAT  GROGOL PETAMBURAN    TANJUNG DUREN UTARA        450
11        JAKARTA BARAT  GROGOL PETAMBURAN                 TOMANG        870
12        JAKARTA BARAT  GROGOL PETAMBURAN          WIJAYA KUSUMA        635
13        JAKARTA BARAT         KALI DERES              KALIDERES        908
14        JAKARTA BARAT         KALI DERES                  KAMAL        510
15        JAKARTA BARAT         KALI DERES             PEGADUNGAN        945
16        JAKARTA BARAT         KALI DERES                SEMANAN        583
17        JAKARTA BARAT         KALI DERES             TEGAL ALUR        822
18        JAKARTA BARAT        KEBON JERUK              DURI KEPA        685
19        JAKARTA BARAT        KEBON JERUK            KEBON JERUK        665
20        JAKARTA BARAT        KEBON JERUK         KEDOYA SELATAN        365
21        JAKARTA BARAT        KEBON JERUK           KEDOYA UTARA        660
22        JAKARTA BARAT        KEBON JERUK             KELAPA DUA        300
23        JAKARTA BARAT        KEBON JERUK       SUKABUMI SELATAN        390
24        JAKARTA BARAT        KEBON JERUK         SUKABUMI UTARA        515
25        JAKARTA BARAT          KEMBANGAN                  JOGLO        570
26        JAKARTA BARAT          KEMBANGAN      KEMBANGAN SELATAN        388
27        JAKARTA BARAT          KEMBANGAN        KEMBANGAN UTARA        590
28        JAKARTA BARAT          KEMBANGAN         MERUYA SELATAN        420
29        JAKARTA BARAT          KEMBANGAN           MERUYA UTARA        630
..                  ...                ...                    ...        ...
237       JAKARTA UTARA      KELAPA GADING    KELAPA GADING BARAT       1084
238       JAKARTA UTARA      KELAPA GADING    KELAPA GADING TIMUR       1211
239       JAKARTA UTARA      KELAPA GADING         PEGANGSAAN DUA       1262
240       JAKARTA UTARA               KOJA                   KOJA        735
241       JAKARTA UTARA               KOJA                  LAGOA       1110
242       JAKARTA UTARA               KOJA     RAWA BADAK SELATAN        545
243       JAKARTA UTARA               KOJA       RAWA BADAK UTARA        595
244       JAKARTA UTARA               KOJA           TUGU SELATAN        475
245       JAKARTA UTARA               KOJA             TUGU UTARA       1070
246       JAKARTA UTARA         PADEMANGAN                  ANCOL        346
247       JAKARTA UTARA         PADEMANGAN       PADEMANGAN BARAT       1073
248       JAKARTA UTARA         PADEMANGAN       PADEMANGAN TIMUR        767
249       JAKARTA UTARA        PENJARINGAN            KAMAL MUARA        224
250       JAKARTA UTARA        PENJARINGAN            KAPUK MUARA        500
251       JAKARTA UTARA        PENJARINGAN              PEJAGALAN       1125
252       JAKARTA UTARA        PENJARINGAN            PENJARINGAN       1210
253       JAKARTA UTARA        PENJARINGAN                  PLUIT       1251
254       JAKARTA UTARA      TANJUNG PRIOK           KEBON BAWANG        980
255       JAKARTA UTARA      TANJUNG PRIOK               PAPANGGO        635
256       JAKARTA UTARA      TANJUNG PRIOK           SUNGAI BAMBU        520
257       JAKARTA UTARA      TANJUNG PRIOK           SUNTER AGUNG       1400
258       JAKARTA UTARA      TANJUNG PRIOK            SUNTER JAYA       1116
259       JAKARTA UTARA      TANJUNG PRIOK          TANJUNG PRIOK        790
260       JAKARTA UTARA      TANJUNG PRIOK                WARAKAS        920
261  KAB.ADM.KEP.SERIBU    KEP. SERIBU SLT                P. PARI         70
262  KAB.ADM.KEP.SERIBU    KEP. SERIBU SLT              P. TIDUNG        145
263  KAB.ADM.KEP.SERIBU    KEP. SERIBU SLT         P. UNTUNG JAWA         45
264  KAB.ADM.KEP.SERIBU    KEP. SERIBU UTR             P. HARAPAN         75
265  KAB.ADM.KEP.SERIBU    KEP. SERIBU UTR              P. KELAPA        155
266  KAB.ADM.KEP.SERIBU    KEP. SERIBU UTR            P. PANGGANG        145
```

Sekian.