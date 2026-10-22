# QA Test Senaryoları

**İlgili plan:** [QA Test Planı](test-plan.md)  
**Durum:** Planlandı; uygulama üzerinde henüz çalıştırılmadı  
**Kaynak:** Teknik belge v4, `api/openapi.yaml`, US-01–US-10 issue'ları ve ders proje yönergesi

Bu senaryolar, mevcut proje kurallarına göre hazırlanmıştır. Beklenen sonuçlar uygulama ve onaylı `api/openapi.yaml` ile doğrulanmadan kesin kabul kriteri sayılmaz. Açık ürün kararları belgenin son bölümündedir. Bir test başarısız olursa gerçek sonuç, build/commit bilgisi ve kanıt ilgili issue/PR'a eklenmelidir.

## PR #4 incelemesi

PR #4, `backend/app/domain/renewal.py` içindeki `add_months` ve `next_renewal` fonksiyonlarını ve `backend/tests/test_renewal.py` dosyasını eklemiş. Kaynak kodu ve test adları incelendi; bu incelemede testler çalıştırılmadı.

| Mevcut test | Bu plandaki karşılığı | İnceleme notu |
|---|---|---|
| `test_add_months_clamps_to_month_end` | QA-DATE-01 | Normal yılda 31 Ocak → 28 Şubat yardımcı fonksiyon düzeyinde kapsanıyor. |
| `test_add_months_leap_year` | QA-DATE-02 | Artık yılda 31 Ocak → 29 Şubat yardımcı fonksiyon düzeyinde kapsanıyor. |
| `test_add_months_crosses_year` | QA-DATE-09 | Ay eklemenin yıl geçişi kapsanıyor. |
| `test_monthly_31st_returns_to_31st_after_short_month` | QA-DATE-01 | 31 Ocak → 28 Şubat → 31 Mart zinciri kapsanıyor. |
| `test_renewal_day_itself_is_not_next` | QA-DATE-08 | `after` yenileme gününe eşitse sonraki dönemin seçilmesi kapsanıyor. |
| `test_yearly_feb_29` | QA-DATE-05, QA-DATE-06 | 29 Şubat başlangıcının normal yılda 28 Şubat'a inmesi ve sonraki artık yıla dönmesi kapsanıyor. |
| `test_after_far_in_the_future` | QA-DATE-09 | Birden fazla dönemi atlayıp gelecekteki ilk tarihin bulunması kapsanıyor. |

## Atanan story'ler için izlenebilirlik

Aşağıdaki eşleme görevde özellikle istenen US-03, US-05, US-06 ve US-08 senaryolarını QA senaryo kimliklerine ve planlanan otomatik testlere bağlar. Otomatik test adları plan niteliğindedir; bu çalışma alanında `backend/tests/` bulunmadığı için henüz uygulanmış veya çalıştırılmış test oldukları anlamına gelmez.

| Story | Girdi / durum | QA senaryosu | Beklenen HTTP sonucu | Planlanan otomatik test |
|---|---|---|---|---|
| US-03 | Tutar `0` ile abonelik oluşturma | QA-SUB-05 | `400`; abonelik oluşturulmaz | `backend/tests/test_subscriptions_api.py::test_create_subscription_zero_amount_returns_400` |
| US-04 | Olmayan veya başka kullanıcıya ait aboneliği görüntüleme | QA-SUB-16 | `404`; başka kullanıcının kaydı açığa çıkmaz | `backend/tests/test_subscriptions_api.py::test_get_missing_or_foreign_subscription_returns_404` |
| US-05 | İptal edilmiş aboneliği yeniden iptal etme | QA-SUB-18 | `409`; kayıt durumu değişmez | `backend/tests/test_subscriptions_api.py::test_cancel_already_cancelled_subscription_returns_409` |
| US-05 | Olmayan veya başka kullanıcıya ait aboneliği iptal etme | QA-SUB-18 | `404`; kayıt durumu değişmez | `backend/tests/test_subscriptions_api.py::test_cancel_missing_or_foreign_subscription_returns_404` |
| US-06 | Aynı kullanıcıda aynı servis ve periyotla ikinci aktif abonelik | QA-SUB-10 | `409`; ikinci kayıt oluşmaz | `backend/tests/test_subscriptions_api.py::test_duplicate_active_subscription_returns_409` |
| US-08 | Yenilemeden 3 gün ve 1 gün önce hatırlatma | QA-REM-01/16 | Her eşik için bir hatırlatma; tekrar üretim yok | `backend/tests/test_reminders.py::test_reminders_generated_at_three_and_one_days` |
| US-08 | Geç eklemede yalnızca kalan hatırlatma günleri | QA-REM-17 | Geçmiş eşikler atlanır; kalan eşikler için birer hatırlatma | `backend/tests/test_reminders.py::test_late_added_subscription_gets_only_remaining_reminders` |
| US-08 | İptalden sonra yeni hatırlatma üretmeme | QA-REM-08 | Yeni hatırlatma oluşmaz, notifier çağrılmaz | `backend/tests/test_reminders.py::test_cancelled_subscription_does_not_create_reminder` |

US-03 için `400` ve US-05/US-06 için `404`/`409` görev ekranındaki kabul ölçütlerine göre yazılmıştır. Başkasının aboneliğini görüntüleme US-04 kapsamındadır. US-08 hatırlatma üretimini kapsar; iptal senaryoları US-05'e aittir.

## OpenAPI işlem → senaryo → otomatik test eşlemesi

Bu eşleme, yerel checkout'taki `main` değil, depodaki `origin/develop` branch'inde bulunan `api/openapi.yaml` sürümüne göre hazırlandı. `origin/develop` sözleşmesi OpenAPI 3.0.3 kullanıyor. Aşağıdaki otomatik test adları önerilen eşlemelerdir; yalnızca yenileme tarihine ait yedi test ve health testi şu anki `origin/develop` ağacında mevcut. Endpoint uygulaması ve API testleri henüz bu branch'te bulunmuyor.

| OpenAPI işlemi | Başarı senaryosu / yanıt | Hatalı girdi veya yetki senaryosu / yanıt | Çakışma / bulunamadı | Planlanan test eşlemesi |
|---|---|---|---|---|
| `POST /auth/register` (`registerUser`) | QA-AUTH-01 → `201` | QA-AUTH-02/03 → `400` | QA-AUTH-04 → `409` | `test_auth_api.py::test_register_valid_user`; `::test_register_invalid_credentials_returns_400`; `::test_register_duplicate_email_returns_409` |
| `POST /auth/login` (`login`) | QA-AUTH-05 → `200` | QA-AUTH-10 → `400`; QA-AUTH-06 yanlış kimlik bilgisi → `401` | Sözleşmede conflict yanıtı yok | `test_auth_api.py::test_login_valid_user`; `::test_login_invalid_body_returns_400`; `::test_login_wrong_credentials_returns_401` |
| `POST /subscriptions` (`createSubscription`) | QA-SUB-01/02/08/22 → `201` | QA-SUB-03/05/07/09 → `400`; QA-AUTH-07 → `401` | QA-SUB-10/11/19 → `409` | `test_subscriptions_api.py::test_create_subscription_valid`; `::test_create_subscription_invalid_input_returns_400`; `::test_create_subscription_unauthorized_returns_401`; `::test_duplicate_active_subscription_returns_409`; `::test_future_start_date_is_accepted` |
| `GET /subscriptions` (`listSubscriptions`) | QA-SUB-14/15 → `200` | QA-AUTH-07 → `401` | Sözleşmede `404`/`409` yanıtı yok | `test_subscriptions_api.py::test_list_subscriptions`; `::test_list_subscriptions_unauthorized_returns_401` |
| `GET /subscriptions/{id}` (`getSubscription`) | QA-SUB-16 → `200` (US-04) | QA-AUTH-07 → `401` | QA-SUB-16 → `404` (US-04) | `test_subscriptions_api.py::test_get_subscription`; `::test_get_subscription_unauthorized_returns_401`; `::test_get_missing_or_foreign_subscription_returns_404` |
| `POST /subscriptions/{id}/cancel` (`cancelSubscription`) | QA-SUB-17 → `200` (US-05) | QA-AUTH-07 → `401` | QA-SUB-18 → `404` veya `409` (US-05) | `test_subscriptions_api.py::test_cancel_subscription_marks_cancelled`; `::test_cancel_unauthorized_returns_401`; `::test_cancel_missing_or_foreign_subscription_returns_404`; `::test_cancel_already_cancelled_subscription_returns_409` |
| `GET /reminders` (`listReminders`) | QA-REM-12 → `200` | QA-AUTH-07 → `401` | Sözleşmede `404`/`409` yanıtı yok | `test_reminders_api.py::test_list_reminders`; `::test_list_reminders_unauthorized_returns_401` |

Sözleşmede tanımlanmayan bir conflict yanıtı olan listeleme ve giriş işlemleri için conflict senaryosu eklenmedi. `401` yetkisiz erişimdir; `409` conflict yanıtları kayıt çakışması veya aboneliğin zaten iptal edilmiş olması için ayrı tutulmuştur.

İstenen işlem/girdi/beklenen yanıt senaryo özeti:

| İşlem | Senaryo | Girdi | Beklenen yanıt |
|---|---|---|---|
| `POST /auth/register` | QA-AUTH-01 | Yeni e-posta ve en az 8 karakter parola | `201` ve kullanıcı |
| `POST /auth/register` | QA-AUTH-02/03 | Eksik alan veya geçersiz e-posta | `400`, kullanıcı oluşmaz |
| `POST /auth/register` | QA-AUTH-04 | Kayıtlı e-posta ile tekrar kayıt | `409`, ikinci kullanıcı oluşmaz |
| `POST /auth/login` | QA-AUTH-05 | Geçerli e-posta/parola | `200` ve JWT |
| `POST /auth/login` | QA-AUTH-10 | Eksik alan veya geçersiz gövde | `400`, token dönmez |
| `POST /auth/login` | QA-AUTH-06 | Hatalı parola veya bulunmayan e-posta | `401`, token dönmez |
| `POST /subscriptions` | QA-SUB-01/02 | Geçerli abonelik alanları, geçerli JWT | `201` ve abonelik |
| `POST /subscriptions` | QA-SUB-05 | `amountKurus: 0` | `400`, kayıt oluşmaz |
| `POST /subscriptions` | QA-SUB-10/11 | Aynı kullanıcı, servis ve periyot için ikinci aktif abonelik | `409`, ikinci kayıt oluşmaz |
| `POST /subscriptions` | QA-AUTH-07 | Geçerli gövde, token yok/bozuk | `401`, kayıt oluşmaz |
| `GET /subscriptions` | QA-SUB-14/15 | Geçerli JWT; boş veya dolu liste | `200`, yalnızca kullanıcının kayıtları |
| `GET /subscriptions` | QA-AUTH-07 | Token yok/bozuk | `401` |
| `GET /subscriptions/{id}` | QA-SUB-16 | Kullanıcıya ait mevcut UUID ve geçerli JWT | `200` ve abonelik |
| `GET /subscriptions/{id}` | QA-SUB-16 | Olmayan veya başka kullanıcıya ait UUID | `404` |
| `GET /subscriptions/{id}` | QA-AUTH-07 | Token yok/bozuk | `401` |
| `POST /subscriptions/{id}/cancel` | QA-SUB-17 | Aktif ve kullanıcıya ait abonelik | `200`, durum `cancelled` |
| `POST /subscriptions/{id}/cancel` | QA-SUB-18 | Olmayan/başkasına ait UUID ya da zaten iptal edilmiş kayıt | `404` veya `409` |
| `POST /subscriptions/{id}/cancel` | QA-AUTH-07 | Token yok/bozuk | `401` |
| `GET /reminders` | QA-REM-12 | Geçerli JWT | `200`, yalnızca kullanıcının hatırlatmaları |
| `GET /reminders` | QA-AUTH-07 | Token yok/bozuk | `401` |

**Kod incelemesinde görülen boşluk:** `next_renewal` içinde `MONTHLY` olmayan her değer 12 ay olarak ele alınıyor. Böylece yanlışlıkla "weekly" gibi bir değer fonksiyona ulaşırsa sessizce yıllık hesap yapılabilir. API/domain sınırında yalnızca `Period.MONTHLY` ve `Period.YEARLY` kabul edildiğini doğrulayan bir test eklenmeli; fonksiyonun doğrudan çağrıldığı yerde de beklenmeyen periyot için kontrollü hata davranışı kararlaştırılmalı.

## 1. Kayıt, giriş ve kimlik doğrulama

### QA-AUTH-01 - Geçerli bilgilerle kayıt

- **Tür:** API, entegrasyon
- **Ön koşul/veri:** Daha önce kullanılmamış geçerli e-posta ve parola.
- **Adımlar:** Kayıt uç noktasına zorunlu alanlarla istek gönder; ardından veritabanında kullanıcı kaydını kontrol et.
- **Beklenen:** Yanıt `201`; kullanıcı bir kez oluşturulur; parola hash olarak saklanır, düz metin saklanmaz. Yanıtta parola veya hash dönmez.

### QA-AUTH-02 - Zorunlu kayıt alanları

- **Tür:** API
- **Ön koşul/veri:** E-posta veya parola ayrı ayrı eksik, boş ya da yalnızca boşluk karakterlerinden oluşan istekler.
- **Adımlar:** Her alan eksikliği için ayrı istek gönder.
- **Beklenen:** Her istek `400` döndürür, kullanıcı oluşturulmaz ve hata gövdesi OpenAPI'deki Error şemasına uyar.

### QA-AUTH-03 - E-posta biçimi doğrulama

- **Tür:** API
- **Ön koşul/veri:** E-posta alanında hatalı biçimler: `plain-text`, eksik `@`, eksik alan adı.
- **Adımlar:** Her değerle kayıt isteği gönder.
- **Beklenen:** Geçersiz adresler reddedilir ve kullanıcı oluşturulmaz. Kabul edilen e-posta biçiminin sınırları sözleşmede tanımlıdır.

### QA-AUTH-04 - Yinelenen e-posta

- **Tür:** API, entegrasyon
- **Ön koşul/veri:** Aynı e-posta ile kayıtlı kullanıcı.
- **Adımlar:** Aynı adresle tekrar kayıt isteği gönder; ayrıca e-posta büyük/küçük harf farkıyla tekrar dene.
- **Beklenen:** Aynı hesabın ikinci kez oluşturulması engellenir. Mevcut mimari taslağı aynı e-posta için `409` bekliyor. E-posta karşılaştırmasının büyük/küçük harf duyarlılığı PO/Architect tarafından karara bağlanmalıdır.

### QA-AUTH-05 - Geçerli bilgilerle giriş

- **Tür:** API
- **Ön koşul/veri:** QA-AUTH-01 ile oluşturulmuş kullanıcı.
- **Adımlar:** Doğru e-posta ve parola ile giriş yap.
- **Beklenen:** Yanıt `200`; geçerli bir JWT döner. Token yanıtta ve korumalı isteklerde beklenen biçimde kullanılabilir.

### QA-AUTH-06 - Hatalı giriş bilgileri

- **Tür:** API
- **Ön koşul/veri:** Mevcut kullanıcı için hatalı parola; ayrıca kayıtlı olmayan e-posta.
- **Adımlar:** İki durum için ayrı giriş istekleri gönder.
- **Beklenen:** Giriş başarısız olur, token dönmez, yanıt `401` olur. Kullanıcı varlığını gereksiz yere açığa çıkaran farklı hata mesajları kullanılmaması güvenlik açısından gözden geçirilir.

### QA-AUTH-07 - Korunan uç noktada eksik/geçersiz token

- **Tür:** API
- **Ön koşul/veri:** Token olmadan, bozuk token ile ve desteklenmeyen kimlik doğrulama şemasıyla istek.
- **Adımlar:** Her durumla abonelik listeleme ve değiştirme uç noktalarını çağır.
- **Beklenen:** Her istek `401` ile reddedilir; veri okunmaz veya değiştirilmez.

### QA-AUTH-08 - Başka kullanıcı token'ı ve sahiplik kontrolü

- **Tür:** API, güvenlik
- **Ön koşul/veri:** Kullanıcı A ve B; A'ya ait abonelik, iki geçerli token.
- **Adımlar:** B token'ıyla A'nın aboneliğini görüntüleme, iptal etme ve listeleme işlemlerini dene.
- **Beklenen:** B, A'nın kaydını göremez veya değiştiremez. Tekil kayıt erişiminde mevcut mimari taslağı `404` bekliyor; listeleme yalnızca B'nin verisini döndürür.

### QA-AUTH-09 - 24 saat sonra süresi dolmuş token

- **Tür:** API, güvenlik
- **Ön koşul/veri:** Oluşturulmasının üzerinden 24 saat geçmiş JWT.
- **Adımlar:** Süresi dolmuş token ile korumalı uç noktayı çağır.
- **Beklenen:** Token `401` ile reddedilir ve veri erişimi olmaz. Token yenileme akışı yoktur; kullanıcı yeniden giriş yapar.

### QA-AUTH-10 - Giriş isteğinde geçersiz veya eksik alan

- **Tür:** API
- **Ön koşul/veri:** Eksik e-posta, eksik parola veya e-posta biçimi geçersiz JSON gövdesi.
- **Adımlar:** Her gövdeyle `POST /auth/login` isteği gönder.
- **Beklenen:** Sözleşmeye göre `400`; token dönmez ve hata gövdesi ortak Error şemasına uyar.

## 2. Abonelik oluşturma ve veri doğrulama

### QA-SUB-01 - Aylık abonelik oluşturma

- **Tür:** API, entegrasyon
- **Ön koşul/veri:** Giriş yapmış kullanıcı; geçerli servis adı, pozitif TRY tutarı, aylık periyot ve geçerli başlangıç/yenileme girdisi.
- **Adımlar:** Abonelik oluştur; yanıtı ve kayıtlı veriyi kontrol et.
- **Beklenen:** Yanıt `201`; abonelik doğru kullanıcıya bağlanır, `active` durumundadır ve istek/yanıt şemaya uyar.

### QA-SUB-02 - Yıllık abonelik oluşturma

- **Tür:** API, entegrasyon
- **Ön koşul/veri:** QA-SUB-01'deki gibi, periyot yıllık.
- **Adımlar:** Abonelik oluştur ve kaydedilen periyot ile tarih alanlarını kontrol et.
- **Beklenen:** Yanıt `201`; periyot yıllık olarak saklanır, sonraki yenileme hesabı yıllık kurala göre yapılır.

### QA-SUB-03 - Zorunlu alan eksikliği

- **Tür:** API
- **Ön koşul/veri:** Her zorunlu alanı sırayla eksik bırakan istekler.
- **Adımlar:** Servis, tutar, periyot ve tarih alanlarını ayrı ayrı çıkararak istek gönder.
- **Beklenen:** Her istek reddedilir, kısmi abonelik kaydı oluşmaz ve hata yanıtı sözleşmeye uyar.

### QA-SUB-04 - Boş veya boşluklardan oluşan servis adı

- **Tür:** API, birim
- **Ön koşul/veri:** `""`, yalnızca boşluklar ve başta/sonda boşluk içeren servis adları.
- **Adımlar:** Her değerle abonelik ekle.
- **Beklenen:** Boş ad reddedilir. Baş/son boşluğun kırpılıp kırpılmayacağı karara bağlanmalı; farklı boşluk biçimleriyle yinelenen kayıt oluşmamalıdır.

### QA-SUB-05 - Sıfır ve negatif tutar

- **Tür:** API, birim
- **Ön koşul/veri:** Sıfır, negatif tam sayı ve negatif ondalıklı tutar.
- **Adımlar:** Her değerle abonelik eklemeyi dene.
- **Beklenen:** Sıfır tutar için görev ölçütüne göre yanıt `400` olur ve abonelik kaydı oluşmaz. Negatif tutar da reddedilir; veritabanı kuralı `amount_kurus > 0` koşulunu korur. Hata gövdesi onaylı OpenAPI şemasına uyar.

### QA-SUB-06 - amountKurus tamsayı doğrulaması

- **Tür:** API, birim, entegrasyon
- **Ön koşul/veri:** Tamsayı `amountKurus: 1234`; ondalıklı `amountKurus: 1234.5`.
- **Adımlar:** İki değeri ayrı abonelik oluşturma isteklerinde gönder.
- **Beklenen:** Tamsayı kuruş değeri kabul edilir; ondalıklı değer `400` ile reddedilir. API kuruş cinsinden tamsayı alır, ondalıklı TL tutarı almaz.

### QA-SUB-07 - Desteklenmeyen periyot ve istekte bulunmayan currency alanı

- **Tür:** API
- **Ön koşul/veri:** Haftalık periyot; ayrıca OpenAPI istek şemasında tanımlı olmayan `currency` alanı.
- **Adımlar:** Haftalık periyotla istek gönder. `currency` alanı davranışını yalnızca sözleşme ek alanları reddediyorsa kontrol et.
- **Beklenen:** Haftalık periyot `400` ile reddedilir. İstekte `currency` alanı yoktur; yanıt para birimini `TRY` olarak taşır. Bilinmeyen alan davranışı sözleşmede tanımlı olmadığından tek başına başarısızlık ölçütü değildir.

### QA-SUB-08 - Aboneliği geç ekleme ve sonraki yenileme tarihini hesaplama

- **Tür:** API, birim
- **Ön koşul/veri:** Saat sabitlenmiş testte bugün `2026-10-22`; aboneliğin `startDate` değeri `2026-01-31`, periyodu `monthly`.
- **Adımlar:** Geçmiş başlangıç tarihiyle abonelik oluştur; yanıtı ve kaydedilen kaydı kontrol et.
- **Beklenen:** Geçmiş `startDate` geç eklenen bir abonelik için kabul edilir ve yanıt `201` olur. `nextRenewalDate` `2026-10-31` olur (başlangıç gününden türetilen bugünden sonraki ilk aylık tarih); tarih hesabı doğrudan saf fonksiyon testiyle de doğrulanır. API gövdesinde istemci tarafından gönderilen `nextRenewalDate` alanı yoktur.

### QA-SUB-09 - Tarih biçimi ve sınırları

- **Tür:** API
- **Ön koşul/veri:** Geçersiz takvim tarihi, yanlış format, saat dilimi içeren timestamp ve kabul edilen tarih biçimi.
- **Adımlar:** Her örneği abonelik oluşturma isteğinde kullan.
- **Beklenen:** Geçersiz tarihler reddedilir; kabul edilen format OpenAPI ile tutarlıdır. Yenileme günü timestamp değil takvim tarihi olarak ele alınır.

### QA-SUB-22 - Gelecek startDate

- **Tür:** API, birim
- **Ön koşul/veri:** Saat sabitlenmiş testte bugün `2026-10-22`; `startDate` `2026-11-15`, periyot aylık.
- **Adımlar:** Gelecek başlangıç tarihiyle abonelik oluştur; dönen `nextRenewalDate` alanını kontrol et.
- **Beklenen:** İstek `201` olur; gelecek başlangıç tarihi kabul edilir ve ilk yenileme `2026-12-15` olarak hesaplanır.

## 3. Yinelenen kayıtlar, listeleme ve durum geçişleri

### QA-SUB-10 - Aynı aktif aboneliğin tekrar eklenmesi

- **Tür:** API, entegrasyon
- **Ön koşul/veri:** Aynı kullanıcıda aktif `Netflix` aylık aboneliği.
- **Adımlar:** Aynı servis adı ve periyotla ikinci kez ekle.
- **Beklenen:** Yanıt `409`; ikinci aktif kayıt oluşmaz.

### QA-SUB-11 - Servis adı normalizasyonu ile yinelenme

- **Tür:** API, entegrasyon
- **Ön koşul/veri:** `Netflix` adlı aktif kayıt; varyasyonlar `netflix`, ` NETFLIX `.
- **Adımlar:** Her varyasyonu aynı kullanıcı ve periyotla ekle.
- **Beklenen:** Mimari taslağı servis adının küçük harfli karşılaştırmasını öngörüyor; eşleşen varyasyonlar yinelenen aktif kayıt sayılır. Boşluk kırpma davranışı ayrıca onaylanmalıdır.

### QA-SUB-12 - Farklı periyot veya farklı kullanıcı

- **Tür:** API, entegrasyon
- **Ön koşul/veri:** Kullanıcı A'da aktif Netflix aylık aboneliği.
- **Adımlar:** A için Netflix yıllık; ardından kullanıcı B için Netflix aylık aboneliği oluştur.
- **Beklenen:** Aynı kullanıcı+servis için farklı periyot ve farklı kullanıcı için ayrı kayıt, diğer kurallara uygunsa kabul edilir. Benzersizlik yanlış kapsamda uygulanmaz.

### QA-SUB-13 - İptal sonrası yeniden abonelik

- **Tür:** API, entegrasyon
- **Ön koşul/veri:** Kullanıcının aktif servis aboneliği.
- **Adımlar:** Aboneliği iptal et; aynı servis ve periyotla yeni kayıt oluştur.
- **Beklenen:** Eski kayıt `cancelled` kalır ve silinmez; yeni abonelik ayrı kayıt olarak oluşturulabilir. İptal edilmiş kayıt yeniden aktive edilmez.

### QA-SUB-14 - Boş abonelik listesi ve yalnızca kullanıcı verileri

- **Tür:** API
- **Ön koşul/veri:** Bir hesabın aboneliği yok; diğer senaryoda iki kullanıcıda farklı abonelikler var.
- **Adımlar:** Her kullanıcının listesini çağır.
- **Beklenen:** Boş hesap boş liste alır; her kullanıcı yalnızca kendi kayıtlarını görür. Yanıt `200` ve liste şemasıyla uyumludur.

### QA-SUB-15 - İptal edilmiş kayıtların listelenmesi

- **Tür:** API
- **Ön koşul/veri:** Aynı kullanıcıda aktif ve iptal edilmiş abonelik.
- **Adımlar:** Listeleme uç noktasını çağır.
- **Önerilen beklenen:** Basit MVP'de kayıt listede kalır ve “İptal edildi” durumu gösterilir; silme veya ek filtre gerektirmez. PO farklı karar verirse test ve API sözleşmesi güncellenir.

### QA-SUB-16 - Kayıt görüntüleme

- **Tür:** API
- **Ön koşul/veri:** Kullanıcı A'ya ait mevcut kayıt, olmayan bir kimlik ve kullanıcı B'ye ait kayıt.
- **Adımlar:** A token'ıyla her kimliği ayrı ayrı çağır.
- **Beklenen:** A'nın kaydı `200`; olmayan ve B'ye ait kimlikler `404`. B'ye ait kaydın varlığı açığa çıkmaz.

### QA-SUB-17 - Aktif aboneliği iptal etme

- **Tür:** API, entegrasyon
- **Ön koşul/veri:** Kullanıcıya ait aktif abonelik.
- **Adımlar:** İptal işlemini çağır; yanıtı ve kalıcı durumu yeniden okuyarak kontrol et.
- **Beklenen:** Yanıt `200`; durum `cancelled` olur ve iptal zamanı kaydedilir (alan varsa). Kayıt fiziksel olarak silinmez ve iptal durumu görünür.

### QA-SUB-18 - İkinci iptal ve iptal yetkisi

- **Tür:** API
- **Ön koşul/veri:** Bir kez iptal edilmiş kayıt; başka kullanıcıya ait aktif kayıt; olmayan kimlik.
- **Adımlar:** Aynı kaydı tekrar iptal et; diğer kullanıcı ve olmayan kimlik için iptal isteği gönder.
- **Beklenen:** Tekrar iptal taslağa göre `409`; başka kullanıcı kaydı ve olmayan kimlik `404`. Yetkisiz işlem durumu değiştirmez.

### QA-SUB-19 - Eşzamanlı yinelenen abonelik isteği

- **Tür:** Entegrasyon
- **Ön koşul/veri:** Aynı kullanıcıda henüz bulunmayan servis/periyot çifti; eşzamanlı istek gönderebilen test ortamı.
- **Adımlar:** Aynı abonelik oluşturma isteğini paralel olarak iki kez gönder.
- **Beklenen:** Benzersiz veritabanı kısıtı nedeniyle yalnızca bir aktif kayıt oluşur; diğer istek belgelenen çakışma yanıtını alır (`409`). Uygulama beklenmeyen `500` üretmez.

### QA-SUB-20 - Kalıcılık

- **Tür:** Entegrasyon
- **Ön koşul/veri:** Oluşturulmuş kullanıcı ve abonelik; test veritabanı yeniden başlatılabilir.
- **Adımlar:** Kaydı oluştur; API/veritabanı servisini test ortamında yeniden başlat; kayıtları tekrar oku.
- **Beklenen:** Kalıcı veritabanında kullanıcı ve abonelik kaydı korunur; uygulama yeniden başladı diye tekrar kayıt oluşmaz veya durum değişmez.

### QA-SUB-21 - İptal fiziksel silme yapmaz

- **Tür:** API, entegrasyon
- **Ön koşul/veri:** Aktif abonelik.
- **Adımlar:** Aboneliği iptal et; aynı kimlikle detayını veya liste kaydını yeniden oku.
- **Beklenen:** Kayıt saklanır, durumu `cancelled` görünür. İptal işlemi geçmiş kaydı silmez.

## 4. Yenileme tarihi hesaplama

Bu bölüm saf tarih fonksiyonu için birim testlerini kapsar. Tarihlerin saat içermediği ve `after` parametresinden **sonra gelen ilk** yenilemenin beklendiği teknik taslakla doğrulanmalıdır.

### QA-DATE-01 - 31 Ocak başlangıç, normal yıl

- **Tür:** Birim
- **Veri:** Başlangıç 31 Ocak 2025, periyot aylık.
- **Adımlar:** Şubat yenilemesini hesapla; `after` değerini 28 Şubat'tan önce tutarak sonraki yenilemeyi; sonra `after=28 Şubat` ile bir sonrakini hesapla.
- **Beklenen:** 28 Şubat 2025, ardından 31 Mart 2025. Şubat'a kısalan gün başlangıç tarihi olarak kalıcı değişmez.

### QA-DATE-02 - 31 Ocak başlangıç, artık yıl

- **Tür:** Birim
- **Veri:** Başlangıç 31 Ocak 2024, periyot aylık.
- **Adımlar:** Şubat ve Mart yenilemelerini sırasıyla hesapla.
- **Beklenen:** 29 Şubat 2024, ardından 31 Mart 2024.

### QA-DATE-03 - 30 Ocak başlangıç, artık yıl

- **Tür:** Birim
- **Veri:** Başlangıç 30 Ocak 2024, periyot aylık.
- **Adımlar:** Şubat ve Mart yenilemelerini sırayla hesapla.
- **Beklenen:** 29 Şubat, ardından 30 Mart; tarih Şubat'ın 29'una kalıcı kaymaz.

### QA-DATE-04 - Ayın 29'u ve 28'i

- **Tür:** Birim
- **Veri:** Başlangıç günleri 29 ve 28 olan aylık abonelikler; artık ve normal Şubat.
- **Adımlar:** Şubat ve takip eden ay yenilemelerini hesapla.
- **Beklenen:** Gün mevcutsa korunur; mevcut değilse o ayın son gününe iner; sonraki ayda başlangıç gününe döner.

### QA-DATE-05 - Yıllık 29 Şubat başlangıcı

- **Tür:** Birim
- **Veri:** Başlangıç 29 Şubat 2024, periyot yıllık.
- **Adımlar:** 2025 yenilemesini hesapla.
- **Beklenen:** 28 Şubat 2025.

### QA-DATE-06 - Yıllık 29 Şubat başlangıcından sonraki artık yıla geçiş

- **Tür:** Birim
- **Veri:** Başlangıç 29 Şubat 2024, `after` 28 Şubat 2027.
- **Adımlar:** `after` tarihinden sonraki ilk yıllık yenilemeyi hesapla.
- **Beklenen:** 29 Şubat 2028; önceki kısa yıl tarihi başlangıç gününü kalıcı olarak değiştirmez.

### QA-DATE-07 - `after` ilk yenilemeden önce

- **Tür:** Birim
- **Veri:** Başlangıç 15 Ocak 2025, aylık periyot, `after=14 Ocak 2025`.
- **Adımlar:** İlk sonraki yenilemeyi hesapla.
- **Beklenen:** 15 Şubat 2025 (ilk yenileme `start` gününden sonraki dönemdir; başlangıç günü yenileme sayılıp sayılmadığı PO/Architect tarafından doğrulanmalıdır).

### QA-DATE-08 - `after` tam yenileme gününe eşit

- **Tür:** Birim
- **Veri:** Başlangıç 15 Ocak 2025, aylık periyot, `after=15 Şubat 2025`.
- **Adımlar:** `after` tarihinden sonraki ilk yenilemeyi hesapla.
- **Beklenen:** Fonksiyon sözleşmesindeki “sonraki ilk tarih” tanımına göre 15 Mart 2025; eşit tarih yeniden döndürülmez.

### QA-DATE-09 - Birden fazla dönemi atlama

- **Tür:** Birim
- **Veri:** Başlangıç 10 Ocak 2026, aylık periyot, `after=10 Ocak 2027`.
- **Adımlar:** İlk sonraki yenilemeyi hesapla.
- **Beklenen:** 10 Şubat 2027. Hesaplama atlanan dönemlerin üzerinden doğru geçer ve `after` tarihinden sonraki ilk günü döndürür.

### QA-DATE-10 - Desteklenmeyen periyot

- **Tür:** Birim
- **Veri:** Enum dışında bir periyot değeri.
- **Adımlar:** Yenileme fonksiyonunu geçersiz periyotla çağır.
- **Beklenen:** Geçersiz değer sessizce aylık/yıllık sayılmaz; doğrulama veya kontrollü hata oluşur.

### QA-DATE-11 - Tarih ve timestamp saklama

- **Tür:** API, entegrasyon
- **Ön koşul/veri:** Europe/Istanbul gün sınırına yakın işlem zamanı ve geçerli yenileme tarihi.
- **Adımlar:** Abonelik oluştur; veritabanı ve API yanıtındaki yenileme günü ile oluşturulma zamanını karşılaştır.
- **Beklenen:** Yenileme günü saat dilimi dönüşümüyle bir gün ileri/geri kaymaz; takvim tarihi olarak saklanır. Timestamp alanları UTC saklanır ve yanıt sözleşmesine göre serileştirilir.

## 5. Hatırlatma üretimi, zamanlama ve tekillik

### QA-REM-01 - Yenilemeden üç gün önce hatırlatma

- **Tür:** Birim, entegrasyon
- **Ön koşul/veri:** Aktif abonelik; yenileme tarihi bugünden üç takvim günü sonrası; ilgili yenileme için hatırlatma yok.
- **Adımlar:** Saat 09:00 Europe/Istanbul'da günlük işi çalıştır.
- **Beklenen:** Yenilemeden üç gün önce tek hatırlatma kaydı oluşur; aynı eşik yinelenmez.

### QA-REM-02 - Üç günlük eşikten önce

- **Tür:** Birim
- **Ön koşul/veri:** Yenileme tarihi bugünden beş gün sonrası; hatırlatma yok.
- **Adımlar:** Günlük üretim fonksiyonunu bugün tarihiyle çalıştır.
- **Beklenen:** Henüz hatırlatma oluşturulmaz.

### QA-REM-03 - Kaçırılmış hatırlatma eşiği

- **Tür:** Birim, entegrasyon
- **Ön koşul/veri:** Hatırlatma eşiği dünden geçmiş; bu yenileme için hatırlatma yok.
- **Adımlar:** Günlük işi çalıştır.
- **Beklenen:** Kaçırılmış geçmiş eşik için hatırlatma gönderilmez; yalnızca gelecekte kalan eşikler için hatırlatma oluşturulur.

### QA-REM-04 - Aynı yenilemeye ikinci üretim

- **Tür:** Birim, entegrasyon
- **Ön koşul/veri:** Aynı abonelik ve yenileme tarihi için hatırlatma kaydı mevcut.
- **Adımlar:** Üretim işini tekrar çalıştır.
- **Beklenen:** İkinci kayıt oluşmaz; kullanıcıya ikinci mock gönderim yapılmaz.

### QA-REM-05 - İşin aynı gün iki kez çalışması

- **Tür:** Entegrasyon
- **Ön koşul/veri:** Uygun, henüz hatırlatılmamış aktif abonelik.
- **Adımlar:** Günlük işi aynı tarih için ardışık iki kez çalıştır.
- **Beklenen:** `(subscription_id, renewal_date)` benzersizliği korunur; veritabanında ve mock gönderim kaydında çift oluşmaz.

### QA-REM-06 - Eşzamanlı iş çalıştırma

- **Tür:** Entegrasyon
- **Ön koşul/veri:** QA-REM-01 ile aynı; iki worker/job aynı anda başlatılabilir test ortamı.
- **Adımlar:** İki üretim işlemini eşzamanlı başlat.
- **Beklenen:** Benzersiz veritabanı kısıtı çift kaydı engeller; beklenen yarış durumu kontrollü ele alınır ve uygulama beklenmeyen 500 hatası üretmez.

### QA-REM-07 - Bir sonraki yenileme döngüsü

- **Tür:** Birim, entegrasyon
- **Ön koşul/veri:** Aynı aboneliğin önceki yenilemesine ait reminder var; sonraki yenileme tarihi farklı.
- **Adımlar:** Sonraki döngü için hatırlatma eşiğine gelindiğinde üretim işini çalıştır.
- **Beklenen:** Yeni `renewal_date` için yeni bir hatırlatma oluşur; önceki kaydın tekilliği yeni döngüyü engellemez.

### QA-REM-08 - İptal edilmiş abonelik

- **Tür:** Birim, entegrasyon
- **Ön koşul/veri:** İptal edilmiş aboneliğin yenileme tarihi hatırlatma eşiğine gelmiş.
- **Adımlar:** Günlük hatırlatma işini çalıştır.
- **Beklenen:** İptal edilmiş abonelik için yeni hatırlatma oluşturulmaz ve notifier çağrılmaz.

### QA-REM-09 - Birden çok uygun abonelik

- **Tür:** Entegrasyon
- **Ön koşul/veri:** Aynı kullanıcıda iki uygun abonelik; başka kullanıcıda bir uygun abonelik.
- **Adımlar:** Günlük işi bir kez çalıştır; kayıtları kullanıcı ve abonelik bazında incele.
- **Beklenen:** Her uygun abonelik için kendi yenilemesine bağlı bir kayıt oluşur; kayıtlar kullanıcılar/abonelikler arasında karışmaz.

### QA-REM-10 - Yenileme gününden sonra tarihi ilerletme

- **Tür:** Birim, entegrasyon
- **Ön koşul/veri:** Aktif aboneliğin `next_renewal_date` değeri bugünden önce.
- **Adımlar:** Günlük işi çalıştır; aboneliğin yeni tarihini ve reminder kayıtlarını kontrol et.
- **Beklenen:** Kullanıcı kaydı `active` tuttuğu sürece yeni tarih `next_renewal(start_date, period, bugün)` ile bugünden sonraki ilk yenileme olur. Başlangıç gününe dayalı ay sonu kuralı korunur. Bu tarih hesabı ödeme veya servis sağlayıcıda gerçek yenileme yapıldığı anlamına gelmez; kullanıcı uygulamada iptal ederse sonraki hatırlatmalar durur.

### QA-REM-11 - Bildirim sağlayıcısının mock olması

- **Tür:** Entegrasyon
- **Ön koşul/veri:** Uygun abonelik ve mock notifier.
- **Adımlar:** Hatırlatma üretim işini çalıştır; ağ çağrılarını/çıkışları gözle.
- **Beklenen:** Mock gönderim kaydı oluşur; gerçek push servisine veya cihaz token'ına ihtiyaç duyulmaz.

### QA-REM-12 - Hatırlatma listeleme ve kullanıcı izolasyonu

- **Tür:** API
- **Ön koşul/veri:** Kullanıcı A ve B için hatırlatma kayıtları.
- **Adımlar:** İki kullanıcı ayrı ayrı listeleme uç noktasını çağırır; ayrıca tokensız çağrı yapılır.
- **Beklenen:** Her kullanıcı yalnızca kendi hatırlatmalarını görür; başarılı listeleme `200`, tokensız istek `401` olur.

### QA-REM-13 - Zamanlayıcı saati ve test edilebilirlik

- **Tür:** Birim, entegrasyon
- **Ön koşul/veri:** Sahte saat/kontrol edilebilir tarih; Europe/Istanbul zaman dilimi.
- **Adımlar:** Günlük iş fonksiyonunu sabit tarihle doğrudan çağır; gerçek saat beklemeden zamanlama koşulunu sınırın öncesi, tam sınır ve sonrası için çalıştır.
- **Beklenen:** Birim testleri duvar saatine veya gerçek scheduler beklemesine bağlı kalmaz; üretim planı günde bir kez 09:00 Europe/Istanbul kuralını izler.

### QA-REM-14 - Bildirim gönderimi başarısızlığı

- **Tür:** Entegrasyon
- **Ön koşul/veri:** Mock notifier hata döndürecek şekilde ayarlanmış; uygun abonelik.
- **Adımlar:** Günlük işi çalıştır ve kayıt durumu ile tekrar çalıştırma davranışını incele.
- **Beklenen:** Kayıt durumu, tekrar deneme ve çift gönderim davranışı onaylı hata politikasıyla tutarlı olmalıdır. Bu politika mevcut taslaklarda kesin değil; uygulamadan önce karara bağlanmalıdır.

### QA-REM-15 - Günlük işi aynı yenileme için kayıt durumunu korur

- **Tür:** Entegrasyon
- **Ön koşul/veri:** Reminder kaydı oluşturulmuş ve abonelik yenileme tarihi henüz değişmemiş.
- **Adımlar:** Günlük işi tekrar çalıştır; aboneliğin durumunu ve reminder kayıtlarını kontrol et.
- **Beklenen:** Mevcut reminder korunur, yinelenmez ve hatırlatılmamış yeni bir yenileme döngüsü yoksa gereksiz kayıt oluşturulmaz.

### QA-REM-16 - Yenilemeden bir gün önce hatırlatma

- **Tür:** Birim, entegrasyon
- **Ön koşul/veri:** Aktif abonelik; yenileme tarihi yarın; bir günlük eşik için hatırlatma yok.
- **Adımlar:** Hatırlatma üretimini sabit tarihle çalıştır.
- **Beklenen:** Yenilemeden bir gün önce tek hatırlatma oluşur; yinelenen kayıt veya gönderim yapılmaz.

### QA-REM-17 - Geç eklenen abonelikte yalnızca kalan hatırlatmalar

- **Tür:** Birim, entegrasyon
- **Ön koşul/veri:** Abonelik yenilemeye iki gün kala eklenmiş; üç günlük eşik geçmiş, bir günlük eşik gelecekte.
- **Adımlar:** Hatırlatma üretimini ekleme günü ve bir gün sonra sabit saatle çalıştır.
- **Beklenen:** Geçmiş üç günlük eşik atlanır; yenilemeden bir gün önce kalan hatırlatma bir kez oluşturulur.

## 6. OpenAPI, kalite kapısı ve regresyon

### QA-CONTRACT-01 - OpenAPI yapısal doğrulama

- **Tür:** Sözleşme/CI
- **Ön koşul/veri:** `api/openapi.yaml` mevcut ve güncel.
- **Adımlar:** YAML/OpenAPI doğrulayıcısı ve repo Spectral kurallarını çalıştır.
- **Beklenen:** Belge geçerli YAML ve OpenAPI 3.0.3 olur; operationId ve tags gibi zorunlu kurallar geçer; her endpoint için istek/yanıt/hata şemaları tanımlıdır.

### QA-CONTRACT-02 - Sözleşme ve uygulama yanıt eşleşmesi

- **Tür:** API, sözleşme
- **Ön koşul/veri:** Uygulanmış API ve onaylanmış sözleşme.
- **Adımlar:** Her operasyonun başarı ve hata yanıtlarını API testlerinden gelen gerçek yanıtlarla karşılaştır.
- **Beklenen:** HTTP kodu, zorunlu alanlar ve hata gövdesi sözleşmeyle eşleşir; belgesiz davranış PR'da düzeltilir veya önce sözleşmeye eklenir.

### QA-CI-01 - Test ve kapsam kalite kapısı

- **Tür:** CI
- **Ön koşul/veri:** Test ve coverage komutları CI'a eklenmiş.
- **Adımlar:** Tüm testlerin geçtiği ve birim kapsamının %50'nin altına düştüğü iki örnek build çalıştır.
- **Beklenen:** Test hatası build'i başarısız yapar; kapsam %50 altına düştüğünde zorunlu kalite kontrolü merge'i engeller. Rapor kapsamı ve hariç tutulan dosyalar görünürdür.

### QA-REG-01 - Düzeltme sonrası regresyon

- **Tür:** İlgili test seviyesi
- **Ön koşul/veri:** Önceden kaydedilmiş ve düzeltilmiş bug issue'su.
- **Adımlar:** Hatanın yeniden üretim senaryosunu çalıştır; ilgili abonelik/tarih/hatırlatma regresyonlarını da çalıştır.
- **Beklenen:** Bug artık yeniden oluşmaz; ilgili regresyonlar geçer ve kanıt issue/PR'a eklenir.

## 7. Kapsam dışı ve bu sürümde test edilmeyecekler

- Gerçek FCM/Expo push bildirimi ve cihaz token'ı.
- Haftalık abonelik periyodu.
- Banka/kart verisi, ödeme, çoklu para birimi, harcama grafiği ve aile paylaşımı.
- Sosyal giriş, e-posta doğrulama, parola sıfırlama ve hesap silme.

Bu özellikler kapsam değişikliğiyle ilk sürüme alınırsa önce PO backlog'u ve API sözleşmesi güncellenir; sonra ilgili senaryolar eklenir.

## 8. Netleştirilmesi gereken kararlar

1. E-posta büyük/küçük harf karşılaştırması ve servis adındaki baş/son boşluk normalizasyonu (PO yazılı karar bekleniyor).
2. İptal kayıtlarının listede gösterim biçimi ve varsayılan liste sıralaması.
3. Notifier başarısız olursa retry ve yeniden gönderim davranışı.
4. Kapsam raporunda ölçülecek modüller ve hariç tutma gerekçeleri.
5. `next_renewal` fonksiyonuna geçersiz periyot ulaşırsa kontrollü hata davranışı.

