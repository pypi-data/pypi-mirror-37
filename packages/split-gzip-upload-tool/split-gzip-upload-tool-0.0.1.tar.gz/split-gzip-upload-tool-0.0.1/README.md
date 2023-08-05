### split-gzip-upload

#### Description
Tool to split stdin, gzip it and upload to s3.

#### Prerequisites
AWS [CLI](https://aws.amazon.com/cli/) should be installed and 
[configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration)

#### Installation
```
pip install split-gzip-upload-tool
```

#### Usage examples
Let's say you need to move big amount of data from AWS Aurora Postgres to AWS Redshift.
You can do it with just:
```
psql -c '\copy some_big_table TO PROGRAM "aws s3 cp - s3://your-bucket/some_big_table.csv"'
```
to copy all your data as CSV file (big one).  
Or you can compress it with gzip (or bzip2 etc.) first:
```
psql -c '\copy some_big_table TO PROGRAM "gzip | aws s3 cp - s3://your-bucket/some_big_table.csv.gz"'
```
But this will give you 1 compressed file, instead of N files, as Redshift documentation [recommends](https://docs.aws.amazon.com/redshift/latest/dg/c_best-practices-use-multiple-files.html)  
So, you can use the tool to split the `psql`'s `\copy` output to N parts and upload it to S3:
```
psql -c '\copy some_big_table TO PROGRAM "split-gzip-upload --bucket=your-bucket --path=some_big_table --slices=12"'
```
which will upload your data gzipped a little bit faster, and, what is more valuable, split to N near-to-equal-length parts, which is good for loading to Redshift, as it can load them in parallel.  

#### Help
```
split-gzip-upload --help
usage: split-gzip-upload [-h] --bucket BUCKET --path PATH [--slices SLICES]
                         [--batch-size BATCH_SIZE]

optional arguments:
  -h, --help            show this help message and exit
  --bucket BUCKET       S3 bucket name
  --path PATH           path in S3 bucket, some/path will be converted to
                        something like some/path.123.csv.gz, where 123 is a
                        slice number
  --slices SLICES       number of output slices
  --batch-size BATCH_SIZE
                        number of lines in a batch
```

#### FAQ
**Q:** What is it for?   
**A:** It's an all-in-one tool to split the STDIN, compress each part with Gzip, and upload compressed parts in parallel to S3

**Q:** How is this different from linux [`split`](http://man7.org/linux/man-pages/man1/split.1.html) command with `--filter` 
option, like [here](https://stackoverflow.com/posts/23701140/revisions)? Why reinvent the wheel?    
**A:** Technically, if you can use `split` with `--filter`, better use `split`. But when using you have to specify the number of lines per file. 
It's good if you know how many lines in your source file and you just divide the total number of lines in a source file by number of files you want to produce. 
But the tool allows you just specify the number of lines per batch (portion of data written to compressed file) and don't think about calculations.

**Q:** What is faster - gzip and upload with aws cli or use the tool?    
**A:** The tool is a little bit faster:
```
ll ~/Downloads/hmnist_28_28_RGB.csv
-rwxr-xr-x@ 1 andrii  staff    41M Sep 19 14:24 /Users/andrii/Downloads/hmnist_28_28_RGB.csv
```
And with not so fast internet connection on MBP, first using the tool:
```
time cat ~/Downloads/hmnist_28_28_RGB.csv | split-gzip-upload --bucket=<bucket> --path=test-sgu --slices=5 --batch-size=100
...
cat ~/Downloads/hmnist_28_28_RGB.csv  0.00s user 0.05s system 1% cpu 3.449 total
split-gzip-upload --bucket=<bucket> --path=test-sgu --slices=5   3.40s user 0.31s system 31% cpu 11.955 total
```
and using the aws cli:
```
time cat ~/Downloads/hmnist_28_28_RGB.csv | gzip | aws s3 cp - s3://<bucket>/test-sgu.csv.gz   
cat ~/Downloads/hmnist_28_28_RGB.csv  0.00s user 0.03s system 0% cpu 5.609 total
gzip  4.95s user 0.01s system 88% cpu 5.621 total
aws s3 cp - s3://<bucket>/test-sgu.csv.gz  0.58s user 0.23s system 5% cpu 15.091 total
```
