# txtHumanizer

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.5.0-blue)](https://github.com/LangeVC/txtHumanizer/releases/tag/v0.5.0)
[![Status](https://img.shields.io/badge/status-production%20ready-green)](https://github.com/LangeVC/txtHumanizer)
[![Capacium](https://img.shields.io/badge/Capacium-Install%20via%20cap-0B1020?style=flat-square)](https://github.com/Capacium/capacium)
[![CI](https://github.com/LangeVC/txtHumanizer/actions/workflows/ci.yml/badge.svg)](https://github.com/LangeVC/txtHumanizer/actions/workflows/ci.yml)

[ ![Deutsch](https://img.shields.io/badge/🇩🇪-Deutsch-0969da?style=flat-square) ](README.md)
[ ![English](https://img.shields.io/badge/🇬🇧-English-0969da?style=flat-square) ](README.en.md)
[ ![Français](https://img.shields.io/badge/🇫🇷-Français-0969da?style=flat-square) ](README.fr.md)
[ ![Español](https://img.shields.io/badge/🇪🇸-Español-0969da?style=flat-square) ](README.es.md)
[ ![Italiano](https://img.shields.io/badge/🇮🇹-Italiano-0969da?style=flat-square) ](README.it.md)
[ ![Português](https://img.shields.io/badge/🇵🇹-Português-0969da?style=flat-square) ](README.pt.md)
[ ![Tiếng Việt](https://img.shields.io/badge/🇻🇳-Tiếng%20Việt-238636?style=flat-square) ](README.vi.md)

Framework mô-đun, đa ngôn ngữ và nhạy bén với các biến thể phương ngữ để nhận diện và nhân văn hóa văn bản do AI tạo ra, đi kèm giao diện **Terminal CLI** hoàn chỉnh (không phụ thuộc bên thứ ba, 100% Python tiêu chuẩn).

---

## ⚡ Hướng dẫn nhanh CLI

```bash
# Chạy trực tiếp
./bin/txt-humanizer --help

# Nhận diện ngôn ngữ, phương ngữ (Bắc, Trung, Nam) và tín hiệu con người
txt-humanizer detect "Chúng tôi phân tích hành vi và kiểm tra tính nhất quán."

# Đánh giá văn bản với điểm số và trích dẫn bằng chứng
txt-humanizer check van-ban.md
```

---

## 📜 Giấy phép

Được phát hành theo [Giấy phép Apache, Phiên bản 2.0](LICENSE).
