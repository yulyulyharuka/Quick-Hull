#QuickHull
import matplotlib.pyplot as plt
import numpy as np
import math
import os
import random

list_titik = []

#Fungsi untuk mencari jarak antar titik
def JarakTitik(titik1, titik2) :
    selisih = ((titik1[0]-titik2[0])**2) + ((titik1[1]-titik2[1])**2)
    jarak = selisih**(1/2)

    return jarak

#Memghitung persamaan garis
def PersamaanGaris(titik1, titik2) :
    persamaan = []
    x = titik1[1] - titik2[1]
    persamaan.append(x)
    y = titik2[0] - titik1[0]
    persamaan.append(y)
    c = (titik2[1]*titik1[0]) - (titik1[1]*titik2[0])
    persamaan.append(c)

    return persamaan

#Mencari jarak titik ke sebuah garis
def JarakTitikGaris (titik, persamaan_garis) :
    pembilang = abs((persamaan_garis[0]*titik[0]) + (persamaan_garis[1]*titik[1]) + (persamaan_garis[2]))
    penyebut = (persamaan_garis[0]**2 + persamaan_garis[1]**2)**(1/2)
    jarak = pembilang/penyebut

    return jarak

#Mencari titik terjauh dari sebuah titik acuan
def TitikTerjauh(titik1, titik2, titik_list) :
    p = PersamaanGaris(titik1, titik2)
    jarak_max = JarakTitikGaris(titik_list[0], p)
    point_max = titik_list[0]
    i = 1
    count = len(titik_list)
    while (i < count):
        if (JarakTitikGaris(titik_list[i], p) > jarak_max) :
            jarak_max = JarakTitikGaris(titik_list[i], p)
            point_max = titik_list[i]
        i = i + 1
    return point_max

#Determinan untuk mencari apakah titik berada di sisi atas atau bawah garis acuan
def Determinan(titik1, titik2, titik3) :
    det = (titik1[0]*titik2[1]) + (titik3[0]*titik1[1]) + (titik2[0]*titik3[1]) - (titik3[0]*titik2[1]) - (titik2[0]*titik1[1]) - (titik1[0]*titik3[1])
    return det

def HapusTitik(titik_kiri, titik_kanan, PointJauh, points) :
    list_kiri = []
    list_kanan = []
    for point in points :
        if (Determinan(titik_kiri, PointJauh, point) > 0) :
            list_kiri.append(point)

    for point in points :
        if (Determinan(PointJauh, titik_kanan, point) > 0) :
            list_kanan.append(point)

    i = 0
    while (len(points) != 0 and (i < len(points))) :
        if (len(list_kiri) != 0 and len(list_kanan)!=0) :
            if (not (points[i] in list_kanan)  and not (points[i] in list_kiri)) :
                points.pop(i)
            else :
                i = i+1
        elif (len(list_kiri) == 0 and len(list_kanan) != 0) :
            if (not (points[i] in list_kanan)) :
                points.pop(i)
            else :
                i = i+1
        elif (len(list_kanan) == 0 and len(list_kiri) != 0) :
            if (not points[i] in list_kiri) :
                points.pop(i)
            else :
                i = i + 1
        else :
            points.pop(i)

#Fungsi strategi QuickHull
def QuickHull(titik_kiri, titik_max, titik_kanan, titik_list) :
    hull = []
    titik_list.sort()
    if (len(titik_list) == 0) :
        hull.append(titik_max)
        return hull
    elif (len(titik_list) == 1) :
        hull.append(titik_max)
        hull.append(titik_list[0])
        titik_list.pop(0)
        return hull
    elif (len(titik_list) > 1) :
        hull.append(titik_max)

        inner_point = []     #list untuk titik yang berada di bawah garis
        outer_point = []     #list untuk titik yang berada di atas garis
        for titik in (titik_list) :
            if (Determinan(titik_kiri, titik_max, titik) > 0) :
                outer_point.append(titik)
            elif (Determinan(titik_kiri, titik_max, titik) < 0)  :
                inner_point.append(titik)

        HullKiri = []
        HullKanan = []
        if (len(outer_point) > 0 ):
            PointJauhKiri = TitikTerjauh(titik_kiri, titik_max, outer_point)
            HapusTitik(titik_kiri, titik_max,PointJauhKiri, outer_point)
            HullKiri = QuickHull(titik_kiri, PointJauhKiri,titik_max, outer_point)
        if (len(inner_point) > 0 ) :
            PointJauhKanan = TitikTerjauh(titik_max, titik_kanan, inner_point)
            HapusTitik(titik_max, titik_kanan, PointJauhKanan,inner_point)
            HullKanan = QuickHull(titik_max, PointJauhKanan, titik_kanan,inner_point)

        hull = hull + HullKiri + HullKanan

        return hull

def SortHull(list_hull) :
    hull_urut = []
    point_kiri = list_hull[0]
    point_kanan= list_hull[1]
    list_hull.remove(point_kiri)
    hull_urut.append(point_kanan)
    hull_bawah = []

    for titik in list_hull :
        if (Determinan(point_kiri, point_kanan, titik) > 0) :
            hull_urut = [titik] + hull_urut
        elif (Determinan(point_kiri, point_kanan, titik) < 0) :
            hull_bawah.append(titik)

    hull_bawah.sort()
    hull_urut.sort()

    hull_bawah = list(reversed(hull_bawah))

    hull_urut = [point_kiri] + hull_urut + hull_bawah + [point_kiri]

    return (hull_urut)


############################################# MAIN PROGRAM #############################################
print ("Masukan jumlah titik :")
jumlah_titik = int(input("> "))
print(" ")

#Menginisiasi titik random
for i in range(jumlah_titik) :
    x = random.randint(0,100)
    y = random.randint(0,100)
    titik = x,y
    list_titik.append(titik)

print ("Hasil random titik :")
print (list_titik)

list_titik.sort()
point_kiri = list_titik[0]
list_titik.pop(0)
point_kanan = list_titik[len(list_titik)-1]
list_titik.pop(len(list_titik)-1)

hull = []
if (len(list_titik) == 0) :
    hull.append(point_kiri)
    hull.append(point_kanan)
elif (len(list_titik) == 1) :
    hull.append(point_kiri)
    hull.append(point_kanan)
    hull.append(list_titik[0])
elif (len(list_titik) > 1) :
    hull.append(point_kiri)
    hull.append(point_kanan)

    #Membagi menjadi 2 daerah yaitu daerah atas(left_point) dan daerah bawah (right_point)

    left_point = []     #list untuk titik yang berada di atas garis
    right_point = []    #list untuk titik yang berada di bawah garis
    for titik in list_titik :
        if (Determinan(point_kiri, point_kanan, titik) > 0) :
            left_point.append(titik)
        elif (Determinan(point_kiri, point_kanan, titik) < 0) :
            right_point.append(titik)

    LeftHull = []
    RightHull = []

    #Mencari Convex Hull bagian atas
    if (len(left_point) > 0) :
        TitikJauhKiri = TitikTerjauh(point_kiri, point_kanan, left_point)
        HapusTitik(point_kiri, point_kanan, TitikJauhKiri, left_point)
        LeftHull = QuickHull(point_kiri, TitikJauhKiri, point_kanan, left_point)

    #Mencari Convex Hull bagian bawah
    if (len(right_point) > 0) :
        TitikJauhKanan = TitikTerjauh(point_kiri, point_kanan, right_point)
        HapusTitik(point_kanan, point_kiri, TitikJauhKanan, right_point)
        RightHull = QuickHull( point_kanan, TitikJauhKanan,point_kiri, right_point)

    hull = hull + LeftHull + RightHull

hull_urut = []
hull_urut = SortHull(hull)
print()
print("Titik-titik hasil QuickHull : ", hull_urut)
x_hull = []
y_hull = []
for i in range(len(hull_urut)) :
    x_hull.append(hull_urut[i][0])
    y_hull.append(hull_urut[i][1])

x_titik = []
y_titik = []
for i in range(len(list_titik)) :
    x_titik.append(list_titik[i][0])
    y_titik.append(list_titik[i][1])

plt.scatter(x_titik, y_titik)
plt.plot(x_hull, y_hull)
plt.scatter(x_hull, y_hull)
plt.ylabel('Ordinat')
plt.xlabel('Absis')
plt.show()
