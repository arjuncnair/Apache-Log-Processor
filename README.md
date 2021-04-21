# Apache-Log-Processor | How to Use logProcessory.py ?

## Before you start, Please make sure to have minimum requirements met:

- Python 2.7

## Apache Access Logs Formatting:

Apache Access Logs that needs to be processed should be in the format mentioned below:

    "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\""

where:
- **%h** – Remote host (client IP address)
- **%l** – User identity, or dash, if none (often not used)
- **%u** – Username, via HTTP authentication, or dash if not used
- **%t** – Timestamp of when Apache received the HTTP request
- **\”%r\** – The actual request itself from the client
- **%>s** – The status code Apache returns in response to the request
- **%b** – The size of the request in bytes.
- \”%{Referer}i\” – Referrer header, or dash if not used  (In other words, did they click a URL on another site to come to your site)
- \”%{User-agent}i\ – User agent (contains information about the requester’s browser/OS/etc)

For logs that does not follow above format, the script will not parse your log file and will store the same in `Error.Log`

## How to Use logProcessor.py
Using the tool is an easy process. Please follow below steps:
- Clone this Repo
- Use Below Command to Process Log

Syntax:

    python logProcessor.py <ApacheAccessLogFile>
    
Example:

    python logProcessory.py access.log
    python logProcessory.py /root/access.log
    python logProcessory.py /var/log/apache/access.log

- The tool give you options to chose [ 0 - 6 ]:

    * Option 1 | Top 10 Requested Pages and Number of requests made for each (Includes both succesful/Unsuccesfull Page Requests)
    * Option 2 | Top 10 Successful page requests
    * Option 3 | Top 10 Unsuccessful page requests
    * Option 4 | The top 10 hosts making the most requests, displaying the IP address and number of requests made.
    * Option 5 | Percentage of successful requests (anything in the 200s and 300s range)
    * Option 6 | Percentage of unsuccessful requests (anything that is not in the 200s or 300s range)
    * Option 0 | Exit

## Sample Output
