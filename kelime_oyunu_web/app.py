from flask import Flask, render_template, request, redirect, session, url_for
import random

app = Flask(__name__)
app.secret_key = "gizli-anahtar"  # Session için gerekli

kategoriler = {
    "Programlama": [
        ("python", "Popüler bir programlama dili"),
        ("variable", "Değişken anlamına gelir"),
        ("loop", "Tekrar eden yapı"),
    ],
    "Hayvanlar": [
        ("aslan", "Ormanlar kralı"),
        ("zebra", "Siyah beyaz çizgili"),
        ("fil", "Uzun hortumlu büyük hayvan"),
    ],
    "Ülkeler": [
        ("japonya", "Teknolojisiyle ünlü ada ülkesi"),
        ("mısır", "Piramitleriyle ünlü"),
        ("fransa", "Eyfel kulesi burada"),
    ]
}
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        kategori = request.form["kategori"]
        kelime, ipucu = random.choice(kategoriler[kategori])
        session["kelime"] = kelime
        session["ipucu"] = ipucu
        session["kategori"] = kategori
        session["tahmin_edilen"] = ["_"] * len(kelime)
        session["hak"] = 6
        session["skor"] = 0
        session["tahminler"] = []
        return redirect(url_for("oyun"))
    return render_template("index.html", kategoriler=kategoriler.keys())
@app.route("/oyun", methods=["GET", "POST"])
def oyun():
    kelime = session["kelime"]
    ipucu = session["ipucu"]
    tahmin_edilen = session["tahmin_edilen"]
    hak = session["hak"]
    skor = session["skor"]
    tahminler = session["tahminler"]
    mesaj = ""
    if request.method == "POST":
        giris = request.form["tahmin"].lower()
        if len(giris) == 1:
            if giris in tahminler:
                mesaj = "Bu harfi zaten denedin."
            elif giris in kelime:
                for i in range(len(kelime)):
                    if kelime[i] == giris:
                        tahmin_edilen[i] = giris
                tahminler.append(giris)
                skor += 10
                mesaj = "Doğru harf!"
            else:
                tahminler.append(giris)
                hak -= 1
                skor -= 5
                mesaj = "Yanlış harf!"
        else:
            if giris == kelime:
                tahmin_edilen = list(kelime)
                skor += 50
                return redirect(url_for("sonuc", durum="kazandın"))
            else:
                hak -= 1
                skor -= 10
                mesaj = "Yanlış kelime!"

    if "_" not in tahmin_edilen:
        return redirect(url_for("sonuc", durum="kazandın"))
    if hak <= 0:
        return redirect(url_for("sonuc", durum="kaybettin"))
    # Güncelle session
    session["tahmin_edilen"] = tahmin_edilen
    session["hak"] = hak
    session["skor"] = skor
    session["tahminler"] = tahminler
    return render_template("oyun.html", kelime=tahmin_edilen, ipucu=ipucu, hak=hak, skor=skor, mesaj=mesaj)
@app.route("/sonuc/<durum>")
def sonuc(durum):
    return render_template("sonuc.html", durum=durum, kelime=session["kelime"], skor=session["skor"])
if __name__ == "__main__":
    app.run(debug=True)
