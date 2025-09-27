1 Initial Setup 

1.1.1 R
1.1.2 

1.2 Configure Software Updates 
1.2.1
1.2.2 R

2 Basic Configuration 

3 Logging 

4 Encryption 

5 Request Filtering and Restrictions 



1 Initial Setup 
1.1 Installation 
1.1.1 Ensure NGINX is installed (Automated)   
1.1.2 Ensure NGINX is installed from source (Manual)   
1.2 Configure Software Updates 
1.2.1 Ensure package manager repositories are properly 
configured (Manual) 
1.2.2 Ensure the latest software package is installed (Manual)   
2 Basic Configuration 
2.1 Minimize NGINX Modules 
2.1.1 Ensure only required modules are installed (Manual)   
2.1.2 Ensure HTTP WebDAV module is not installed 
(Automated) 
2.1.3 Ensure modules with gzip functionality are disabled 
(Automated) 
2.1.4 Ensure the autoindex module is disabled (Automated)   
2.2 Account Security 
2.2.1 Ensure that NGINX is run using a non-privileged, 
dedicated service account (Automated) 
2.2.2 Ensure the NGINX service account is locked 
(Automated) 
2.2.3 Ensure the NGINX service account has an invalid shell 
(Automated)
2.3 Permissions and Ownership 
2.3.1 Ensure NGINX directories and files are owned by root 
(Automated) 
2.3.2 Ensure access to NGINX directories and files is 
restricted (Automated) 
2.3.3 Ensure the NGINX process ID (PID) file is secured 
(Automated) 
2.3.4 Ensure the core dump directory is secured (Manual)   
2.4 Network Configuration 
2.4.1 Ensure NGINX only listens for network connections on 
authorized ports (Manual) 
2.4.2 Ensure requests for unknown host names are rejected 
(Automated) 
2.4.3 Ensure keepalive_timeout is 10 seconds or less, but not 
0 (Automated)
2.4.4 Ensure send_timeout is set to 10 seconds or less, but 
not 0 (Automated) 
2.5 Information Disclosure 
2.5.1 Ensure server_tokens directive is set to `off` 
(Automated) 
2.5.2 Ensure default error and index.html pages do not 
reference NGINX (Automated) 
2.5.3 Ensure hidden file serving is disabled (Manual)   
2.5.4 Ensure the NGINX reverse proxy does not enable 
information disclosure (Automated) 
3 Logging
3.1 Ensure detailed logging is enabled (Manual)   
3.2 Ensure access logging is enabled (Manual)   
3.3 Ensure error logging is enabled and set to the info 
logging level (Automated) 
3.4 Ensure log files are rotated (Automated)   
3.5 Ensure error logs are sent to a remote syslog server 
(Manual) 
3.6 Ensure access logs are sent to a remote syslog server 
(Manual) 
3.7 Ensure proxies pass source IP information (Manual)   
4 Encryption 
4.1 TLS / SSL Configuration 
4.1.1 Ensure HTTP is redirected to HTTPS (Manual)   
4.1.2 Ensure a trusted certificate and trust chain is installed 
(Manual) 
4.1.3 Ensure private key permissions are restricted 
(Automated) 
4.1.4 Ensure only modern TLS protocols are used 
(Automated) 
4.1.5 Disable weak ciphers (Manual)   
4.1.6 Ensure custom Diffie-Hellman parameters are used 
(Automated) 
4.1.7 Ensure Online Certificate Status Protocol (OCSP) 
stapling is enabled (Automated) 
4.1.8 Ensure HTTP Strict Transport Security (HSTS) is 
enabled (Automated)
4.1.9 Ensure upstream server traffic is authenticated with a 
client certificate (Automated) 
4.1.10 Ensure the upstream traffic server certificate is trusted 
(Manual) 
4.1.11 Ensure your domain is preloaded (Manual)   
4.1.12 Ensure session resumption is disabled to enable perfect 
forward security (Automated) 
4.1.13 Ensure HTTP/2.0 is used (Automated)   
4.1.14 Ensure only Perfect Forward Secrecy Ciphers are 
Leveraged (Manual) 
5 Request Filtering and Restrictions 
5.1 Access Control 
5.1.1 Ensure allow and deny filters limit access to specific IP 
addresses (Manual) 
5.1.2 Ensure only approved HTTP methods are allowed 
(Manual) 
5.2 Request Limits 
5.2.1 Ensure timeout values for reading the client header and 
body are set correctly (Automated) 
5.2.2 Ensure the maximum request body size is set correctly 
(Automated) 
5.2.3 Ensure the maximum buffer size for URIs is defined 
(Automated) 
5.2.4 Ensure the number of connections per IP address is 
limited (Manual) 
5.2.5 Ensure rate limits by IP address are set (Manual)
5.3 Browser Security 
5.3.1 Ensure X-Frame-Options header is configured and 
enabled (Automated) 
5.3.2 Ensure X-Content-Type-Options header is configured 
and enabled (Automated) 
5.3.3 Ensure that Content Security Policy (CSP) is enabled 
and configured properly (Manual) 
5.3.4 Ensure the Referrer Policy is enabled and configured 
properly (Manual) 
6 Mandatory Access Control