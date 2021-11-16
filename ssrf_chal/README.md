Python 3 webserver challenge.

This challenge is based on abusing SSRF. It will reject attempts to 
specify IP addresses (so folks can't just plug in 169.254.169.254) but 
still allow folks to enter domains that resolve to those endpoints.

### requirements
pip install -r requirements.txt

### run
python3 main.py

