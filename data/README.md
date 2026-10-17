# data/ — bilgi tabanı

Kodun değil, verinin yaşadığı yer. Kural eklemek = satır eklemek; kod değişmez (karar belgesi K5, §4).

| Klasör / dosya | Ne | Biçim | Sahibi |
|---|---|---|---|
| `sozluk/` | Kavramlar (`concept`) ve eşanlamlılar (`alias`, ilişki türüyle) | CSV | Ozan |
| `kurallar/` | Kural tablosu (`rule`): varlık · miktar · beyan | CSV | Hilal |
| `kanit/` | CTD/JECFA çıkarımları (`evidence`), yalnız bilgi | CSV | Hilal |
| `kaynaklar.md` | Her kaynağın sürümü, lisansı, alınan alanlar | Markdown | Hilal |

Sütunlar karar belgesi §4'teki şemayı izler. Lisansı `kaynaklar.md`'ye yazılmamış veri buraya girmez.
