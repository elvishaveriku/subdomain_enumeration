import requests
import socket
import csv
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_crtsh_subdomains(domain):
    print(f"[+] Fetching from crt.sh...")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        subdomains = set()
        for entry in data:
            for sub in entry['name_value'].split('\n'):
                if sub.endswith(domain):
                    subdomains.add(sub.strip())
        return list(subdomains)
    except Exception as e:
        print(f"[!] crt.sh error: {e}")
        return []

def get_finder_subdomains(domain):
    print(f"[+] Fetching from finder.tools...")
    url = f"https://subdomains.finder.tools/api/subdomain/{domain}"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        return data.get("subdomains", [])
    except Exception as e:
        print(f"[!] finder.tools error: {e}")
        return []

def get_hackertarget_subdomains(domain):
    print(f"[+] Fetching from HackerTarget...")
    url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
    try:
        r = requests.get(url, timeout=10)
        lines = r.text.strip().split("\n")
        subdomains = []
        for line in lines:
            parts = line.split(",")
            if len(parts) == 2:
                subdomains.append(parts[0].strip())
        return subdomains
    except Exception as e:
        print(f"[!] HackerTarget error: {e}")
        return []

def resolve_to_ip(subdomain):
    try:
        ip = socket.gethostbyname(subdomain)
        return ip
    except socket.gaierror:
        return None

def save_to_csv(results, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Subdomain', 'IP'])
        for entry in results:
            writer.writerow([entry['subdomain'], entry['ip'] or 'Unresolved'])

def save_to_json(results, filename):
    with open(filename, 'w') as f:
        json.dump(results, f, indent=4)

def main():
    domain = input("Enter the domain (e.g. example.com): ").strip()

    crtsh = get_crtsh_subdomains(domain)
    finder = get_finder_subdomains(domain)
    hackertarget = get_hackertarget_subdomains(domain)

    all_subs = sorted(set(crtsh + finder + hackertarget))
    print(f"\n[+] Total unique subdomains found: {len(all_subs)}")

    results = []

    print(f"\n[~] Resolving {len(all_subs)} subdomains to IPs with threading...\n")
    with ThreadPoolExecutor(max_workers=25) as executor:
        future_to_sub = {executor.submit(resolve_to_ip, sub): sub for sub in all_subs}
        for future in as_completed(future_to_sub):
            sub = future_to_sub[future]
            ip = future.result()
            print(f"{'[+]' if ip else '[-]'} {sub} -> {ip if ip else 'Unresolved'}")
            results.append({
                "subdomain": sub,
                "ip": ip
            })

    csv_file = f"subdomains/{domain}_subdomains.csv"
    json_file = f"subdomains/{domain}_subdomains.json"
    save_to_csv(results, csv_file)
    save_to_json(results, json_file)

    print(f"\n[✓] Results saved to: {csv_file} and {json_file}")

if __name__ == "__main__":
    main()
