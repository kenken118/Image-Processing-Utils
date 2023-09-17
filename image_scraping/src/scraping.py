import argparse
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from PIL import Image
import os
import time
import datetime
import io
import requests
import pytz


def is_valid_search_word(search_word):
    """検索ワードが適切な形式かどうかをチェックする

    Args:
        search_word (str): 検索ワードとなる文字列

    Returns:
        bool: 検索ワードが適切な形式の場合 -> True
              検索ワードが無効な形式の場合 -> False

    Note:
        検索ワードが空文字列、または使用できない文字（\ / : * ? " < > | _）が含まれている場合、無効な形式とする
    """
    invalid_chars = r'[\\/:*?"<>|_]'

    if not search_word.strip():
        return False

    if re.search(invalid_chars, search_word):
        return False

    return True

def download_images_with_selenium(search_word, num_images, image_size, save_directory):
    """Google画像検索を使用して、指定された検索ワードに関連する画像をダウンロードする

    Args:
        search_word (str): 検索ワードとなる文字列
        num_images (int): ダウンロードする画像の枚数
        image_size (tuple): 保存する画像サイズ（width, height)
        save_directory (str): 画像を保存するディレクトリのパス
    Note:
        必要に応じ画像のリサイズを行い、リサイズされた画像はJPEG形式で保存される
    """
    ts = pytz.timezone("Asia/Tokyo")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    
    try:
        if not is_valid_search_word(search_word):
            print("Scraping failed. The search_word contains invalid characters.")
            return

        driver.get(f"https://www.google.com/search?q={search_word}&tbm=isch")
        # ページが完全にロードされるのを待つ
        time.sleep(2)

        scroll_down = 0
        count = 0
        while count < num_images:
            # ページを一番下までスクロールするための処理
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            scroll_down += 1
            if scroll_down == 5:
                break

        # SeleniumのWebDriverを使用して取得したWebページのHTMLソースコードに対し
        # BeautifulSoupライブラリを使用して解析し、ページ内の全てのimgタグを取得する
        soup = BeautifulSoup(driver.page_source, "html.parser")
        images = soup.find_all("img")

        final_save_directory = os.path.join("..", "save_images", save_directory)

        if not os.path.exists(final_save_directory):
            os.makedirs(final_save_directory)

        for img in images:
            img_url = img.get("src")
            if img_url and img_url.startswith("http"):
                try:
                    img_data = requests.get(img_url).content
                    img_pil = Image.open(io.BytesIO(img_data))
                    img_pil = img_pil.convert("RGB")
                    
                    # 画像の`alt`属性に検索ワードが含まれているかをチェックする
                    # これにより、特定のキーワードが画像に関連付けられている場合のみ、その画像をダウンロードする
                    if search_word.lower() in img.get("alt", "").lower():
                        count += 1
                        timestamp = datetime.datetime.now(tz=ts).strftime('%Y%m%d_%H%M%S')
                        file_name = f"{search_word}_{timestamp}_{count}"
                        file_path = os.path.join(final_save_directory, f"{file_name}.jpg")
                        img_pil_resized = img_pil.resize(image_size, Image.LANCZOS)
                        img_pil_resized.save(file_path, "JPEG", quality=95)
                except Exception as e:
                    print(f"Error downloading image {count}: {e}")

                if count == num_images:
                    break
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        driver.quit()

def main():
    parser = argparse.ArgumentParser(description="Download images from Google image search")
    parser.add_argument("--search_word", type=str, nargs='?', default="car", help="Keyword to search for")
    parser.add_argument("--num_images", type=int, nargs='?', default=10, help="Number of images to download")
    parser.add_argument("--image_width", type=int, nargs='?', default=224, help="Width of the saved images")
    parser.add_argument("--image_height", type=int, nargs='?', default=224, help="Height of the saved images")
    parser.add_argument("--save_directory", type=str, nargs='?', default="/content/drive/MyDrive/ImageProcessingUtils/image_scraping/car", help="Directory to save the images")

    args = parser.parse_args()

    image_size = (args.image_width, args.image_height)

    download_images_with_selenium(args.search_word, args.num_images, image_size, args.save_directory)

if __name__ == "__main__":
    main()
