# QA Test Planı

| Alan | Değer |
|---|---|
| Proje | Abonelik ve Fatura Hatırlatıcı Mobil Uygulaması |
| Sorumlu rol | Quality Assurance ve Test Automation Engineer |
| Durum | Taslak - PO ve Architect incelemesi bekliyor |
| Kapsam | Sprint 1 hazırlığı ve sonraki sprintler için test yaklaşımı |

## 1. Amaç ve mevcut durum

Bu plan, test senaryolarını backlog ile izlemek ve uygulama hazır olduğunda testleri yürütmek için kullanılır. Sprint 1 puanlanan teslimleri ayrı bir otomatik test paketi istemiyor. Bu aşamadaki QA çalışması kabul kriterlerini ve API sözleşmesini test edilebilirlik açısından incelemektir.

Bu belge bir test planıdır, test sonucu raporu değildir. Senaryoların çalıştırılma durumu ve kanıtları ilgili PR veya CI raporunda kaydedilmelidir. API yanıtları ve iş kuralları onaylı OpenAPI sözleşmesi ile PO kararlarına göre kesinleştirilmelidir.

Atanan US-03, US-05, US-06 ve US-08 için senaryo → beklenen HTTP sonucu → planlanan otomatik test eşlemesi [QA Test Senaryoları](test-cases.md#atanan-storyler-icin-izlenebilirlik) belgesinde yer alır. Eşleme görev ekranındaki gereksinimlere dayanır; planlanan testler henüz kodlanmış testler değildir.

Mevcut `main` checkout'unda `api/openapi.yaml` ve `backend/` bulunmuyor; ancak `origin/develop` branch'inde OpenAPI 3.0.3 sözleşmesi ile yenileme ve health testleri var. Test senaryoları belgesindeki işlem matrisi bu sözleşmedeki tüm operasyonları kapsar. `origin/develop` içindeki API uygulaması henüz yalnızca health endpoint'ini içerdiğinden API senaryoları çalıştırılamaz ve gerçek kapsam yüzdesi ölçülemez. En az %50 birim kapsamı hedefi korunmuştur; uygulama ve testler tamamlandığında CI/coverage raporuyla kanıtlanmalıdır.

PR #4'te (`chore: repo iskeleti ve next_renewal`) bulunan yenileme fonksiyonu ve mevcut birim testlerini inceledim. `backend/tests/test_renewal.py` içinde tarih hesabına yönelik yedi test var; kaynak kodu incelendi, test komutları bu incelemede çalıştırılmadı. Ayrıntılı kapsam eşlemesi ve görülen boşluk [QA Test Senaryoları](test-cases.md) belgesinde yer alıyor.

## 2. Test kapsamı

İlk sürüm için test edilecek temel davranışlar:

- E-posta/şifre ile kayıt ve giriş; korumalı işlemlerde JWT doğrulaması.
- Abonelik ekleme, listeleme, görüntüleme ve iptal etme.
- Aylık ve yıllık yenileme tarihi hesabı; ay sonu ve artık yıl davranışı.
- Aynı kullanıcıda aynı servis ve periyot için aktif abonelik çakışmasının engellenmesi.
- Yenilemeden üç gün ve bir gün önce hatırlatma üretilmesi; her eşikte tekillik, geç eklemede yalnızca kalan eşikler ve iptalden sonra yeni hatırlatma üretmeme.
- Kullanıcılar arası veri izolasyonu ve API hata davranışları.

İlk sürüm kapsamı dışında kalan gerçek push/cihaz kaydı, haftalık periyot, ödeme/banka bağlantısı ve harcama grafikleri bu planın fonksiyonel kapsamına dahil değildir.

## 3. Test yaklaşımı

| Seviye | Amaç | Örnekler | Zamanlama |
|---|---|---|---|
| Birim | Saf alan kurallarını ve uç durumları hızlı doğrulamak | Yenileme hesabı, abonelik doğrulaması, durum geçişi, hatırlatma tekilliği | İlgili kod PR'larında ve CI'da |
| API | HTTP sözleşmesini, doğrulamayı, yetkilendirmeyi ve hata yanıtlarını doğrulamak | Kayıt/giriş, abonelik CRUD işlemleri, `400/401/404/409` davranışları | API işlemleri geliştirildikçe |
| Entegrasyon | API, veritabanı ve mock bildirim sınırlarının birlikte çalışmasını doğrulamak | Kalıcı kayıt, benzersiz kısıt, hatırlatma üretimi | MVP entegrasyonunda |
| Uçtan uca | Ana kullanıcı yolculuğunu çalışan ürün üzerinden doğrulamak | Kayıt/giriş, abonelik ekleme, hatırlatma kaydını görme | Final teslim ve demo öncesi |

Birim kapsamı ders gereksinimi olan en az **%50** seviyesinde tutulmalıdır. Ekip, kapsam ölçümünün hangi modülleri kapsadığını ve hariç tutulan kodu raporda açıkça belirtmelidir. QA testleri ve raporu sahiplenir; başarısız üretim kodunu ilgili implementasyon sahibi düzeltir.

## 4. Senaryolar ve izlenebilirlik

Ayrıntılı ön koşullar, veri örnekleri, adımlar ve beklenen sonuçlar [QA Test Senaryoları](test-cases.md) belgesindedir. Senaryolar teknik belge v4, `api/openapi.yaml` ve US-01–US-10 issue'larına dayanır. PO tarafından karara bağlanan kurallar senaryolara işlenmiştir; e-posta büyük/küçük harf ve servis adı boşluk normalizasyonu için yazılı karar beklenmektedir.

Testler çalıştırıldığında her senaryonun durumu (PASS/FAIL/BLOCKED), uygulanan build/commit ve kanıt ilgili PR/CI raporunda kaydedilmelidir.

## 5. Teste hazır olma ve kabul koşulları

Bir story test geliştirmeye hazır sayılmadan önce:

- Kullanıcı, amaç, gerekli alanlar ve gözlenebilir sonuç açık olmalı.
- Olumlu akışın yanında geçersiz girdi ve ilgili hata/çakışma davranışı belirtilmeli.
- API etkisi ve beklenen HTTP yanıtları onaylı `api/openapi.yaml` ile tutarlı olmalı.
- Tarih, saat dilimi, para ve kullanıcı sahipliği kuralları karara bağlanmış olmalı.
- Test verisi ve çalıştırma yöntemi belirlenebilir olmalı.

Bir story QA açısından tamamlanmış sayılmadan önce:

- İlgili otomatik testler geçmeli; kapsam eşiği %50'nin altına düşmemeli.
- Davranış OpenAPI sözleşmesi ve kabul kriterleriyle tutarlı olmalı.
- PR'da çalıştırma kanıtı ve ilişkili issue bağlantısı bulunmalı.
- Bulunan hatalar düzeltilmiş veya PO tarafından önceliklendirilmiş açık issue olarak kaydedilmiş olmalı.

## 6. Bug ve test kanıtı kaydı

Her hata için issue'da en az şunlar bulunmalı: başlık, etkilenen story/API işlemi, ortam ve build/commit, yeniden üretme adımları, beklenen sonuç, gerçek sonuç, önem/öncelik ve log/rapor/ekran görüntüsü bağlantısı. QA düzeltmeyi aynı senaryoyla yeniden çalıştırıp sonucu issue ve PR'a bağlar.

Test çalıştırma kaydı şablonu:

```text
Story / issue:
Build veya commit:
Ortam:
Test ID'leri:
Sonuç: PASS / FAIL / BLOCKED / NOT RUN
Çalıştırma komutu veya yöntem:
Kanıt (CI raporu, log, ekran görüntüsü):
İlgili hata issue'ları:
```

## 7. Açık kararlar

Basit ilk sürüm için aşağıdaki davranışları öneriyorum; PO ve Architect onayıyla kesinleştirilmeleri gerekir:

- Uygulama abonelik satın almaz, ödeme yapmaz ve servis sağlayıcısından yenilenme bilgisi almaz. `active` kayıt, kullanıcının izlemeye devam ettiği tekrarlayan abonelik anlamına gelir. Tarih geçince mevcut teknik taslağa göre uygulama bir sonraki dönemin tarihini hesaplar; kullanıcı uygulamada iptal ederse sonraki hatırlatmalar durur.
- İptal fiziksel silme değildir. Kayıt `cancelled` durumuna alınır ve saklanır; ilk sürümde listede “İptal edildi” durumu gösterilir. Aynı servis/periyot daha sonra yeniden eklenirse yeni kayıt açılır.
- Her aktif yenileme döngüsü için yenilemeden üç gün önce bir hatırlatma kaydı ve mock gönderim oluşturulur. Gerçek push ve birden fazla hatırlatma ilk sürümde yoktur.

Kesinleştirilecek teknik kararlar:

- İptal kayıtlarının listede gösterim biçimi ve varsayılan liste sıralaması.
- Kapsam raporunda hangi dosya/modüllerin ölçüleceği ve test dışı bırakılma gerekçeleri.

Karara bağlanan kurallar: geçersiz girdi `400`; JWT ömrü 24 saat ve yenileme akışı yok; hatırlatmalar yenilemeden 3 ve 1 gün önce üretilir. Eşik kaçırılmışsa geçmiş hatırlatma gönderilmez; abonelik geç eklenirse yalnızca kalan eşikler üretilir.

