import requests
import csv
from bs4 import BeautifulSoup

CSV_NAME = "vacancies.csv"
url = "https://www.python.org/jobs"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    job_list = soup.find("ol", class_="list-recent-jobs")

    if not job_list:
        job_items = []
    else:
        job_items = job_list.find_all("li")

    vacancies = []

    for item in job_items:

        h2 = item.find("h2", class_="listing-company")
        if not h2:
            continue

        link_tag = h2.find("a")
        title = link_tag.text.strip()
        link = "https://www.python.org" + link_tag["href"]

        company = "—"
        company_span = h2.find("span", class_="listing-company-name")
        if company_span:
            text_parts = company_span.get_text("\n", strip=True).split("\n")
            if text_parts:
                company = text_parts[-1]

        location = "—"
        location_span = h2.find("span", class_="listing-location")
        if location_span:
            location = location_span.text.strip()

        vacancies.append({
            "title": title,
            "company": company,
            "location": location,
            "link": link
        })

    print(f"найдено {len(vacancies)} вакансий")
    for v in vacancies[:3]:
        print(f"{v['title']} — {v['company']} ({v['location']})")
        print(f"Ссылка: {v['link']}\n")

    with open("vacancies.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "company", "location", "link"])
        writer.writeheader()
        writer.writerows(vacancies)
    print(f"данные сохранены в {CSV_NAME}")
else:
    print(f"ошибка: {response.status_code}")
#сделано за 1.5 часа