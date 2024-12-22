# Wczytaj zmienne z pliku .env
include .env
export $(shell sed 's/=.*//' .env)

# Domyślna nazwa pliku backupu (z datą)
BACKUP_FILE ?= backup_$(shell date +%Y-%m-%d_%H:%M:%S).sql

# Reguła: Tworzenie backupu
backup:
	@echo "Tworzenie backupu bazy danych: $(DATABASE)"
	PGPASSWORD=$(PASSWORD) pg_dump -U $(USERNAME) -h $(HOSTNAME) -p $(DATABASE_PORT) -d $(DATABASE) > $(BACKUP_FILE)
	@echo "Backup zapisany do: $(BACKUP_FILE)"

# Reguła: Usuwanie wszystkich backupów
# clean:
# 	@echo "Usuwanie wszystkich plików backupu..."
# 	rm -f backup_*.sql
# 	@echo "Pliki backupu usunięte."
