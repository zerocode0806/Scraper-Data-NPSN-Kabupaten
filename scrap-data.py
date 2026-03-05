import time
import random
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.sync_api import sync_playwright

# =====================================
# KONFIGURASI
# =====================================
BASE_URL = "https://referensi.data.kemendikdasmen.go.id/pendidikan/dikdas/050200/2/jf/all/all"
OUTPUT_FILE = "data_sekolah_lengkap.xlsx"

MAX_WORKERS = 4
MAX_RETRY = 3
HEADLESS = True


# =====================================
# RETRY LOAD FUNCTION
# =====================================
def goto_with_retry(page, url):
    for attempt in range(MAX_RETRY):
        try:
            page.goto(url, timeout=60000)
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_selector("table tbody tr", timeout=20000)
            return True
        except Exception as e:
            print(f"[Retry {attempt+1}] Gagal load {url} | {e}")
            time.sleep(4)
    return False


# =====================================
# SCRAPE PER KECAMATAN
# =====================================
def scrape_kecamatan(nama_kec, link_kec):

    hasil = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()

        print(f"[START] {nama_kec}")

        if not goto_with_retry(page, link_kec):
            print(f"[FAILED LOAD] {nama_kec}")
            browser.close()
            return hasil

        page_number = 1

        while True:

            print(f"{nama_kec} - Page {page_number}")

            page.wait_for_selector("table tbody tr", timeout=20000)
            rows = page.locator("table tbody tr")
            total_rows = rows.count()

            print(f"Total rows: {total_rows}")

            for i in range(total_rows):
                try:
                    row = rows.nth(i)
                    cols = row.locator("td")

                    if cols.count() < 3:
                        continue

                    # Struktur kolom:
                    # 0 = No
                    # 1 = NPSN
                    # 2 = Nama Satuan Pendidikan

                    npsn = cols.nth(1).inner_text().strip()
                    nama_sekolah = cols.nth(2).inner_text().strip()

                    # Ambil link jika ada
                    link_elem = cols.nth(1).locator("a")
                    link_npsn = link_elem.first.get_attribute("href") if link_elem.count() > 0 else ""

                    hasil.append({
                        "Kecamatan": nama_kec,
                        "NPSN": npsn,
                        "Nama_Satuan_Pendidikan": nama_sekolah,
                        "Link_NPSN": link_npsn
                    })

                except Exception as e:
                    print("Error row:", e)
                    continue

            # ==========================
            # PAGINATION
            # ==========================
            next_button = page.locator("a.paginate_button.next")

            if next_button.count() > 0:
                class_attr = next_button.get_attribute("class")

                if class_attr and "disabled" in class_attr:
                    break
                else:
                    next_button.click()
                    time.sleep(random.uniform(3, 5))
                    page.wait_for_selector("table tbody tr", timeout=20000)
                    page_number += 1
            else:
                break

        browser.close()
        print(f"[DONE] {nama_kec} - Total Data: {len(hasil)}")

    return hasil


# =====================================
# AMBIL SEMUA KECAMATAN (WITH PAGINATION)
# =====================================
def get_all_kecamatan():

    daftar = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()

        print("Mengambil daftar kecamatan...")

        if not goto_with_retry(page, BASE_URL):
            print("Gagal load halaman utama")
            browser.close()
            return daftar

        page_number = 1

        while True:

            print(f"Halaman Kecamatan: {page_number}")

            page.wait_for_selector("td.link1")

            links = page.locator("td.link1 a")
            total = links.count()

            for i in range(total):
                nama = links.nth(i).inner_text().strip()
                link = links.nth(i).get_attribute("href")

                if "/dikdas/" in link:
                    daftar.append((nama, link))

            next_button = page.locator("a.paginate_button.next")

            if next_button.count() > 0:
                class_attr = next_button.get_attribute("class")

                if class_attr and "disabled" in class_attr:
                    break
                else:
                    next_button.click()
                    time.sleep(3)
                    page.wait_for_selector("td.link1")
                    page_number += 1
            else:
                break

        browser.close()

    print(f"Total kecamatan ditemukan: {len(daftar)}")
    return daftar


# =====================================
# MAIN EXECUTION
# =====================================
def main():

    semua_data = []
    daftar_kecamatan = get_all_kecamatan()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

        futures = [
            executor.submit(scrape_kecamatan, nama, link)
            for nama, link in daftar_kecamatan
        ]

        for future in as_completed(futures):
            semua_data.extend(future.result())

    df = pd.DataFrame(semua_data)
    df.to_excel(OUTPUT_FILE, index=False)

    print("\n============================")
    print("SCRAPING SELESAI")
    print(f"Total Data: {len(df)}")
    print(f"File disimpan: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()