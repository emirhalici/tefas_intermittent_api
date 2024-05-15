# tefas_intermittent_api

> See [README-EN](README-EN.md) for English version of this markdown.

TEFAS üzerindeki fonların temel bilgilerini Github Workflow Actions üzerinden düzenli olarak çekmeye yarar. Bu operasyon Python scripti ile TEFAS'taki ilgili fon sayfasını scrape ederek uygulanır. 

# Nasıl Kullanılır

Bu repository'de [scraper.yml](.github/workflows/scraper.yml) aksiyonu her gün Türkiye saatiyle 12PM'de çalışma üzerine programlandı. [scraper.py](scraper.py) script'inde `INPUTS` kısmında tanımlanmış kodlu fonları otomatik olarak çekip `data` branch'ine yazılıyor. Herhangi bir anda bu verileri json veya csv formatında değişiklik yapmadan okuyabilirsiniz.

CSV formatında ham dosya için [tıklayın](https://raw.githubusercontent.com/emirhalici/tefas_intermittent_api/data/fund_data.csv).

JSON formatında ham dosya için [tıklayın](https://raw.githubusercontent.com/emirhalici/tefas_intermittent_api/data/fund_data.json).

# Nasıl Özelleştirilir

Farklı fonları ekleyip çıkarmak için projeyi klonlamanız gerekir. 

### 1. Projeyi klonlayın

### 2. Script'i düzenleyin

Script dosyasında `INPUTS` değişkenine farklı fon kodları ekleyip çıkararak istediğiniz fon listesini oluşturun. 

> Dikkat: Çok fazla fon kodunu girmek rate limit'e takılarak tool'un dengesiz çalışmasına sebep olabilir.

### 2. Workflow Action'ı düzenleyin

Workflow dosyasının çektiği veriyi `data` branch'ine yazabilmesi için commit iznine ihtiyacı var. Proje ayarlarından `GH_TOKEN` adında bir token oluşturup bu tokene repository yetkilerini verin. 