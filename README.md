# Removing duplicate files, recursively removing empty folders
Программа сравнивает две папки и удаляет одинаковые файлы во второй папке (сравнение папок разных версий)

ВНИМАНИЕ!!! 

**Сравнение не точное**, создается CRC32 сумма для первых 65536 байт файла

```
remove_duplicate.py /папка1 /папка2_в_которой_нужно_удалить_дубликаты
```
