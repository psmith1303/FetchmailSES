#!/usr/bin/env python3
#
#
#
import boto3
from datetime import datetime
import os
import errno
import argparse
import pdb

#
# Some basic definitions
#
api_base_url = 'https://api.smashrun.com/v1/my/'


#
# Command-line variables
#
options_verbose = 0
options_maildir = '~/NAS/Backups/Maildir'
options_s3bucket = 'mailbox.petersmith.org'
options_keepmail = True # If True then the mail of the server is not deleted after it is downloaded



def vlog(level, message):
    """ print out a message if needed """
    if level <= options_verbose:
        print(message)
    return(True)


def check_positive(value):
    """ Check if an option is a positive integer """
    ivalue = int(value)
    
    if ivalue <= 0:
         raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


def ensure_dir(dirname):
    """
    Ensure that a named directory exists; if it does not, attempt to create it.
    """

    vlog(2, 'Creating Maildir: [{}]'.format(dirname))

    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def parse_args():
    """ parse any commandline arguments """
    global options_bucket
    global options_maildir
    global options_verbose
    global options_keepmail


    parser = argparse.ArgumentParser(description='Fetch emails from Amazon SES and store them in a Maildir.')

    parser.add_argument('-b', '--bucket', help='the S3 bucket that has the mail messages',
                        action='store')
    parser.add_argument('-k', '--keepmail', help='keep the mail on the server after downloading it',
                        action='store_true')
    parser.add_argument('-m', '--maildir', help='the path to the Maildir. e.g., "~/NAS/Maildir"',
                        action='store')
    parser.add_argument('-v', '--verbose', help='Increase output verbosity', 
                        type=check_positive, default=0, const=1, nargs='?', action='store')

    args = parser.parse_args()

    if args.maildir:
        options_maildir = args.maildir
    #
    # Make sure the maildir is fully expanded (no ~ and the like)
    #
    options_maildir = os.path.expanduser(options_maildir)
        
    if args.bucket:
        options_s3bucket = args.bucket

    if args.keepmail:
        options_keepmail = True
    else:
        options_keepmail = False
        


    if args.verbose:
        options_verbose = args.verbose
    else:
        options_verbose = 0
        
    return(True)


def fetch_mail():
    s3 = boto3.resource('s3')
    print(options_s3bucket)
    bucket = s3.Bucket(options_s3bucket)
    # Iterates through all the objects, doing the pagination for you. Each obj
    # is an ObjectSummary, so it doesn't contain the body. You'll need to call
    # get to get the whole body.
    vlog(1, 'Processing {} messages'.format(len(list(bucket.objects.all()))))
    for obj in bucket.objects.all():
        dirname = '{}/tmp'.format(options_maildir)
        ensure_dir(dirname)
        tmpfilename = '{}/{}.{}.{}'.format(dirname, int(obj.last_modified.timestamp()), obj.key, options_s3bucket)
        vlog(2, 'Filename: {}'.format(tmpfilename))
        
        try:
            s3.meta.client.download_file(options_s3bucket, obj.key, tmpfilename)
        finally:
            vlog(1, 'File copied')

        #
        # Move the file to it's final place
        dirname = '{}/cur'.format(options_maildir)
        ensure_dir(dirname)
        destfilename = '{}/{}.{}.{}'.format(dirname, int(obj.last_modified.timestamp()), obj.key, options_s3bucket)
        os.rename(tmpfilename, destfilename)

        if options_keepmail == False:
            vlog(1, 'Deleting: {} from {}'.format(obj.key, options_s3bucket))
            obj.delete()
            
    return(True)


def main():
    """ process  runs from SmashRun into blog posts """
    parse_args()
    fetch_mail()

    return(True)



if __name__ == "__main__":
    main()
