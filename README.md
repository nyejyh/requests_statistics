# requests_statistics
Obtain information by ELK and make calculations based on it.

This script assumes that the user has two levels of directories.  The first level contains the folders.  The second level contains the text files.  Script will open text files with the format "YYYYMMDDHHMMSS".

The script will tally requests started, requests complete, and requests failed.  It will make appropriate additional calculations with this data, such as percentages of requests successful.  

## Content Sent and Encapsulation Data
For this script, it has a value of "Progress Bar."  The progress bar only accounts for actual file contents in the data, but not for the additional extra data such as headers and other encapsulation information. (For more information, see [Encapsulation](https://en.wikipedia.org/wiki/Encapsulation_(networking)https://en.wikipedia.org/wiki/Encapsulation_(networking))).  The "totalByte" accounts for this instead.  In order to account for an approximate level where we know that the content was never sent, even if only the non-content was sent instead, a threshold of 500 byte was implemented.
