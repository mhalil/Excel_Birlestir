#!/usr/bin/env python
# coding: utf-8

# Aynı klasörde bulunan excel dosyalarını birleştiren python kodu.
# Tüm dosya içeriği birleştirildikten sonsa "TUMU_Baslikli.xlsx" adında yeni bir dosyaya kaydedilecek.
# Python Kodunun çalışması için bilgisayarınızda "Pandas", "openpyxl" ve "xlrd." kütüphanelerinin / modüllerinin yüklü olması gerekir.

import pandas as pd
import os

########## Gerekli Bilgileri  Düzenleyin ##########
sayfa_adi = "Sayfa1"			# kopyalanacak verilerin bulunduğu sayfa adı
baslik_satiri = 4				# başlık olarak kullanılacak satır numarası. tamsayı değeri olmalı
ilk_veri_satiri_orj = 5			# kopyalanacak ilk verinin bulunduğu satır numarası. tamsayı değeri olmalı
satir_kopyala_orj = 7			# kopyalanacak verilerin bulunduğu satır sayısı. tamsayı değeri olmalı
sutun_kopyala = "B:G"			# kopyalanacak verilerin bulunduğu sütun aralığı. Örneğin "A:K"
atlanacak_satir_sayisi_orj = 5 	# ilk veri grubu kopyalandıktan sonra ikinci veri grubuna erişmek için atlanacak satır sayısı.tamsayı değeri olmalı
dongu_orj = 20					# veri kopyalarken dosya içerisinde döngüyü kaç kez tekrarlamak istediğinizi belirtin. tamsayı değeri olmalı
####################################################################################
ilk_veri_satiri = ilk_veri_satiri_orj
satir_kopyala = satir_kopyala_orj
atlanacak_satir_sayisi = atlanacak_satir_sayisi_orj
dongu = dongu_orj
####################################################################################

dosyalar = os.listdir()     	# Python dosyasının bulunduğu dizindeki (klasördeki) TÜM DOSYA isimlerini, uzantıları ile birlikte al, "dosyalar" isimli listeye ekle / ata.
dosyalar.sort()           		# dosyalar listesindeki öğeleri (dosya isimlerini) alfabetik olarak sırala.

if "TUMU_Baslikli.xlsx" in dosyalar:         # Klasör içinde "TUMU_Baslikli.xlsx" dosyasının olup olmadığını kontrol et, varsa aşağıdaki kodları çalıştır.
    os.remove("TUMU_Baslikli.xlsx")          # Klasör içindeki "TUMU_Baslikli.xlsx" isimli dosyayı sil.
    dosyalar.remove("TUMU_Baslikli.xlsx")    # "TUMU_Baslikli.xlsx" isimli öğeyi "dosyalar" listesinden çıkar.

excel_dosyalari= []				# ".xlsx", ".xls" ya da ".ods" uzantılı dosyaların toplanacağı boş liste oluştur.

for i in dosyalar:          	# Dizindeki tüm dosya isimlerini kontrol et, ".xlsx", ".xls" ya da ".ods" uzantılı dosyaları "dosya_isimleri" isimli listeye ekle.
    if ((i[-5:] == ".xlsx") or (i[-4:] == ".xls") or (i[-4:] == ".ods") ):     # dosya uzantılarını kontrol et.
        excel_dosyalari.append(i)
# # print("\nExcel dosyalari:\n", excel_dosyalari)

def baslik(dosya_adi, say_adi=sayfa_adi, sat_atla=baslik_satiri, sat_sec=1, sut_sec=sutun_kopyala):	# Baslik belirlemek icin kullanilan fonksiyon.
	global sayfa_adi, ilk_veri_satiri, satir_kopyala, sutun_kopyala
	return pd.read_excel(dosya_adi, sheet_name=say_adi, header=None, skiprows=range(0,sat_atla-1), nrows=satir_kopyala, usecols=sut_sec)

df_baslik = baslik(excel_dosyalari[0])		# Basligi tespit etmek icin olusturulan df.
baslik = (list(df_baslik.iloc[0]))			# basligin liste biçimi
# # print("Baslik listesi:\n", baslik)

df = pd.DataFrame(columns = baslik)
# # print("Baslikli BOS df:\n", df)

def VeriCercevesi(dosya_adi, say_adi=sayfa_adi, sat_atla=ilk_veri_satiri, sat_sec=satir_kopyala-1, sut_sec=sutun_kopyala):      # Belirtilen dosya adına göre, dosya içeriğini Başlıksız DataFrame'e çeviren fonksiyon.
	global sayfa_adi, ilk_veri_satiri, satir_kopyala, sutun_kopyala, baslik
	g = pd.read_excel(dosya_adi, sheet_name=say_adi, names=baslik, skiprows=range(1,sat_atla-1), nrows=satir_kopyala, usecols=sut_sec)
	g["Dosya Adi"] = dosya_adi
	return g
# # print("VeriCercevesi Fonksiyonu calisti, Sonuc:\n", VeriCercevesi("D1.xlsx"))

def tum_veriler(dosya_adi):
	global sayfa_adi, ilk_veri_satiri, satir_kopyala, sutun_kopyala, atlanacak_satir_sayisi, baslik, dongu, df
	for _ in range(dongu):
		try:
			gecici_df = VeriCercevesi(dosya_adi, say_adi=sayfa_adi, sat_atla=ilk_veri_satiri, sat_sec=satir_kopyala, sut_sec=sutun_kopyala)
			df = pd.concat([df, gecici_df])
			# # print("\ndongu sonrası df:\n", df)
			satir_artir = satir_kopyala + atlanacak_satir_sayisi
			ilk_veri_satiri += satir_artir
			df.to_excel("TUMU_Baslikli.xlsx")    # Tüm dosyalar birleştirildikten sonra sonuç "TUMU_Baslikli.xlsx" ismi ile kaydedilir.
		except:
			print(f"Dongu tekrarlandı ancak {dosya_adi} dosyasında dongu sayısı kadar veri bulunmuyor")
			dongu -= 1

for dosya in excel_dosyalari:
	tum_veriler(dosya)
	ilk_veri_satiri = ilk_veri_satiri_orj					# Baslangic degerlerine geri don
	satir_kopyala = satir_kopyala_orj						# Baslangic degerlerine geri don
	atlanacak_satir_sayisi = atlanacak_satir_sayisi_orj 	# Baslangic degerlerine geri don
	dongu = dongu_orj

print("\n\nBİRLEŞİM SONRASI VERİ ÇERÇEVESİ:\n\n", df)
