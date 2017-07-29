get:
	./FetchmailSES.py		
	mu index --maildir=/usr/home/psmith/NAS/Backups/Maildir

clean:
	rm -fr ls  /usr/home/psmith/NAS/Backups/Maildir/*
