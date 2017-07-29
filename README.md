This solves a little problem for me. I have mail being recieved by Amazon's SES and stored in an S3 bucket. I then want to get that mail into my local mailsystem, so ...

Download any files in the bucket (their should only be mail files there), and save it first as a tmp file in my Maildir. Then move it to the cur directory in the Maildir (this seems like good practice). Finally, delete the orginal file on S3.

There is not a lot of error checking going on, but hopefully there is enough.

### Installation

This assumes you have installed the boto3 library and configured it correctly (with your AWS access codes, however you like to do that).

You'll need to configure the particular directory you want to use and the S3 bucket. In my case it is:

``` python
options_maildir = '~/NAS/Backups/Maildir'
options_s3bucket = 'mailbox.petersmith.org'
options_keepmail = True 
```


Setting the options keepmail to False will delete all the mail once it has been transferred. Alternatively, you can use the `--keepmail` option when running the programme.

### Usuage
Easy, it's just

```bash
FetchmailSES.py
```

Be warey of using the Makefile to run the code (like what I do), `make clean` will delete pretty much everything in your Maildir, which could be a very bad thing.
