# Ekran Taslakları ve API Eşleşmeleri

Bu belge, abonelik yönetim uygulamasının temel ekran taslaklarını, bileşenlerini ve tetikledikleri API uç noktalarını tanımlar.

---

## 1. Giriş ve Kayıt Ekranı (Auth Screen)

Kullanıcının sisteme kaydolmasını ve mevcut hesabı ile oturum açmasını sağlayan ekrandır.

### Ekran Bileşenleri
* E-posta giriş alanı (`email`)
* Şifre giriş alanı (`password` - gizli metin)
* "Giriş Yap" butonu
* "Kayıt Ol" butonu
* Hata bildirim alanı (geçersiz format, hatalı şifre vb.)

### Tetiklenen API İşlemleri
* **Kayıt Ol:** `POST /auth/register`
  * Gövde: `{"email": "...", "password": "..."}`
  * Başarılı Yanıt: `201 Created`
* **Giriş Yap:** `POST /auth/login`
  * Gövde: `{"email": "...", "password": "..."}`
  * Başarılı Yanıt: `200 OK` (Dönen `accessToken` JWT istemcide güvenli şekilde saklanır)

---

## 2. Abonelik Listesi Ekranı (Subscription List Screen)

Giriş yapmış kullanıcının aktif ve geçmiş aboneliklerini, yaklaşan yenileme tarihlerini ve hatırlatıcı durumlarını listelediği ana ekrandır.

### Ekran Bileşenleri
* Abonelik kartları listesi:
  * Servis Adı (örn. Netflix, Spotify)
  * Tutar ve Para Birimi (TRY)
  * Sonraki Yenileme Tarihi (`nextRenewalDate`)
  * Periyot (Aylık/Yıllık)
  * Yaklaşan Hatırlatıcılar rozeti (`reminders`)
* "Yeni Abonelik Ekle" (+) butonu (Ekleme Formu ekranını açar)
* Abonelik Kartı Detayı / İptal Aksiyonu:
  * "Aboneliği Listeden Kaldır / İptal Et" butonu

### İptal Uyarısının Yeri (Kritik UI Kuralı)
* **Konum:** Kullanıcı bir abonelik kartında "İptal Et" butonuna bastığında açılan onay modal/diyalog penceresinin içinde yer alır.
* **Uyarı Metni:** *"Servisteki gerçek aboneliğiniz iptal edilmez."*
* Kullanıcı bu uyarıyı içeren onay penceresinde "Onayla" dediğinde işlem gerçekleştirilir.

### Tetiklenen API İşlemleri
* **Listeleme:** `GET /subscriptions`
  * Başarılı Yanıt: `200 OK` (Kullanıcıya ait abonelik dizisi)
* **Tekil Detay:** `GET /subscriptions/{id}`
  * Başarılı Yanıt: `200 OK`
* **Abonelik İptali:** `POST /subscriptions/{id}/cancel`
  * Başarılı Yanıt: `200 OK` (`status: "cancelled"`, `cancelledAt` güncellenir)

---

## 3. Abonelik Ekleme Formu Ekranı (Add Subscription Screen)

Kullanıcının yeni bir abonelik tanımladığı form ekranıdır.

### Ekran Bileşenleri
* Servis Adı metin kutusu (`serviceName`)
* Tutar giriş alanı (`amountKurus` - arayüzde TL girilip arka planda kuruşa dönüştürülür)
* Para Birimi seçimi (varsayılan: `TRY`)
* Periyot seçimi (Aylık / Yıllık - `monthly` / `yearly`)
* Başlangıç Tarihi seçici (`startDate` - YYYY-MM-DD)
* "Kaydet" butonu
* Form doğrulama ve çakışma hata mesajı alanı (409 Conflict durumunda "Bu servis ve periyot için aktif bir abonelik zaten var." uyarısı)

### Tetiklenen API İşlemleri
* **Abonelik Oluşturma:** `POST /subscriptions`
  * Gövde: `{"serviceName": "...", "amountKurus": ..., "currency": "TRY", "period": "...", "startDate": "..."}`
  * Başarılı Yanıt: `201 Created` (Hesaplanmış `nextRenewalDate` ve otomatik türetilen `reminders` ile döner)