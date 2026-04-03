# ai-kuafor-chatbot
AI destekli randevu sistemi kuaförler için (google calendar + ollama)
# 💇‍♀️ AI Kuaför Chatbot (Nida Kuaför)

Bu proje, küçük işletmeler (özellikle kadın kuaförleri) için geliştirilmiş **yapay zeka destekli randevu chatbotudur**.

Chatbot, kullanıcıyla doğal Türkçe konuşarak:

* 📅 Randevu oluşturur
* ⏰ Uygun saatleri kontrol eder
* 💰 Fiyat bilgisi verir
* 📍 İşletme konumunu paylaşır

Tüm sistem **lokalde çalışır** ve internet bağlantısına ihtiyaç duymadan (LLM tarafı) kullanılabilir.

---

## 🚀 Özellikler

* 🧠 Yerel LLM (Ollama + Gemma)
* 💬 WhatsApp tarzı doğal konuşma
* 📅 Google Calendar entegrasyonu
* ⛔ Dolu saat kontrolü
* 📌 FAQ + fiyat + işletme bilgisi entegrasyonu
* 🇹🇷 Türkçe optimize edilmiş chatbot

---

## 🛠️ Kullanılan Teknolojiler

* Python
* Ollama (Gemma LLM)
* Google Calendar API
* Requests

---

## ⚙️ Kurulum

### 1. Projeyi klonla

```bash
git clone https://github.com/M-Halil-kiral/ai-kuafor-chatbot.git
cd ai-kuafor-chatbot
```

### 2. Gerekli paketleri yükle

```bash
pip install -r requirements.txt
```

### 3. Ollama çalıştır

```bash
ollama serve
```

### 4. Modeli indir

```bash
ollama pull gemma
```

### 5. Uygulamayı başlat

```bash
python chatbot.py
```

---

## 📌 Notlar

* `credentials.json` ve `token.json` güvenlik nedeniyle paylaşılmamıştır
* Google Calendar API kullanmak için kendi API anahtarınızı eklemeniz gerekir

---

## 🎯 Proje Amacı

Bu proje, küçük işletmeler için:

* düşük maliyetli
* offline çalışabilen
* kolay entegre edilebilir

bir yapay zeka çözümü sunmayı amaçlar.

---

## 📷 Geliştirilecek Özellikler

* Web arayüzü (Flask / React)
* WhatsApp entegrasyonu
* Sesli chatbot
* Çoklu müşteri yönetimi

---

## 👨‍💻 Geliştirici

Bu proje bireysel olarak geliştirilmiştir ve portföy amaçlıdır.
