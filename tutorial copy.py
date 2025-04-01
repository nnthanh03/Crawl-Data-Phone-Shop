from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import requests
import io
from PIL import Image
import time

s = Service(r"D:\CodeUIT\Data\Crawl-Data-Phone-Shop\chromedriver.exe")

wd = webdriver.Chrome(service=s)

def get_images_from_google(wd, delay, max_images):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)

	url = "https://www.lazada.vn/dien-thoai-di-dong/samsung/"
	wd.get(url)

	image_urls = set()
	skips = 0

	while len(image_urls) + skips < max_images:
		scroll_down(wd)
		images = wd.find_elements(By.CLASS_NAME , "jBwCF ")
		for image in images:
			if image.get_attribute('src') in image_urls and image.get_attribute('type') == 'product' and image.get_attribute('src').count("data:image") <=0:
				max_images += 1
				skips += 1
				break

			if image.get_attribute('src') and 'http' in image.get_attribute('src'):
				image_urls.add(image.get_attribute('src'))
				print(f"Found {len(image_urls)}")

	return image_urls


def download_image(download_path, url, file_name):
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_path = download_path + file_name

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Success")
	except Exception as e:
		print('FAILED -', e)

urls = get_images_from_google(wd, 1, 6)

download_path = r'C:\Users\ngoct\Downloads\Image-Scraper-And-Downloader-main\imgs'

# for i, url in enumerate(urls):
# 	download_image(download_path, url, str(i) + ".jpg")

print(urls)

wd.quit()