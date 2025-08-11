# Subdomain Finder & Resolver

This Python script automates **subdomain enumeration** and **IP resolution** using multiple free public sources.  
It gathers subdomains from:

- [crt.sh](https://crt.sh) (Certificate Transparency logs)
- [finder.tools](https://finder.tools) API
- [HackerTarget](https://hackertarget.com)

It then resolves each subdomain to its corresponding IP address (if possible) using multithreading for speed.  
The results are saved in both **CSV** and **JSON** formats.

---

## 📌 Features
- Fetch subdomains from **3 public APIs**.
- Combine and deduplicate results.
- Resolve subdomains to IP addresses.
- Save results to **CSV** and **JSON**.
- **Threaded IP resolution** for faster execution.

---

## 🛠️ Installation & Requirements

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo
```
### 2. Install dependencies
The script requires Python 3.8+ and the following packages:

```bash
pip install requests
```

### 3. Create the output folder
Before running the script, create a folder for storing results:

```bash
mkdir subdomains
```

### 🚀 Usage
Run the script:

```bash
python subdomain_finder.py
```
Example:

```less
Enter the domain (e.g. example.com): testphp.vulnweb.com

[+] Fetching from crt.sh...
[+] Fetching from finder.tools...
[+] Fetching from HackerTarget...

[+] Total unique subdomains found: 12

[~] Resolving 12 subdomains to IPs with threading...

[+] www.testphp.vulnweb.com -> 192.168.0.1
[-] mail.testphp.vulnweb.com -> Unresolved

[✓] Results saved to: subdomains/testphp.vulnweb.com_subdomains.csv and subdomains/testphp.vulnweb.com_subdomains.json
```

### ⚙️ How It Works (Step-by-Step)
User Input
The script prompts for a domain name (e.g. example.com).

Fetch Subdomains from APIs

get_crtsh_subdomains() → Queries crt.sh JSON endpoint.

get_finder_subdomains() → Uses finder.tools API.

get_hackertarget_subdomains() → Uses HackerTarget hostsearch API.

Merge & Deduplicate
All subdomains from the 3 sources are combined and duplicates are removed.

Resolve to IPs

Uses socket.gethostbyname() to resolve each subdomain.

Threading with ThreadPoolExecutor speeds up the process.

Save Results

save_to_csv() → Saves subdomain & IP pairs in CSV format.

save_to_json() → Saves the same data in JSON format.

Output Files
Files are saved in the subdomains/ folder:

example.com_subdomains.csv

example.com_subdomains.json

### 📂 Example Output
CSV:

```csv
Subdomain,IP
www.example.com,93.184.216.34
mail.example.com,Unresolved
```

JSON:

```json
[
    {
        "subdomain": "www.example.com",
        "ip": "93.184.216.34"
    },
    {
        "subdomain": "mail.example.com",
        "ip": null
    }
]
```

### ⚠️ Notes
API endpoints used in this script are public but may have rate limits.

If some APIs are unreachable, the script will continue using available sources.

Always have permission before scanning or enumerating subdomains for a domain.
