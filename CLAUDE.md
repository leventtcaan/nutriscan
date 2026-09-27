@AGENTS.md

## Claude Code'a özgü
- Kişisel katman `CLAUDE.local.md` (gitignore) ayrıca yüklenir; oradaki kurallar yalnız o kişi içindir.
- Ortak skill'ler `.claude/skills/` altında (`.agents/skills/` klasörüne symlink): `pbi-baslat`, `pbi-kapat`, `pr-incele`,
  `karar-yaz`, `tarif-ekle`, `arayuz-tasarim`, `frontend-design`, `expo-design-system`, `expo-native-ui`.
- Büyük işte önce plan modu. Azure Boards MCP (`ado`) salt okunur kullanılır: PAT yalnız okuma yetkili; board değişikliği `plan/board/pbi.yaml` PR'ıyla.
