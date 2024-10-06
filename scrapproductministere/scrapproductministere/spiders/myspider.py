import scrapy
import json
import os


class MyspiderSpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ["cnlvc.ci"]
    start_urls = ["https://cnlvc.ci/articles/"]
    json_file_path = 'C:/Users/Uriel-Marie/Documents/self/practice/python/scrapping/ministerecollecteproductfluctuation/scrapproductministere/article.json'
    pdf_folder = 'C:/Users/Uriel-Marie/Documents/self/family/dadsproject/echodesmarches'


    def parse(self, response):
        # Extract link to the archive page
        archive_link = response.css('li.menu-item.menu-item-type-post_type.menu-item-object-page.current-menu-item.page_item.page-item-12036.current_page_item.td-menu-item.td-normal-menu.menu-item-12107  a::attr(href)').get()

        # Follow the archive link
        if archive_link:
            yield response.follow(archive_link, self.parse_page)

    def parse_page(self, response):
        # Load existing articles from the JSON file
        existing_articles = self.load_existing_articles()

        article_links = response.css('div > div.item-details > h3 > a::attr(href)').getall()
        article_text = response.css('div > div.item-details > h3 > a::text').getall()

        new_articles = []  # To store new articles
        for title, link in zip(article_text, article_links):
            # Check if the title already exists
            if title not in existing_articles:
                new_articles.append({'title': title, 'url': link})

        # Write new articles back to the JSON file
        self.save_articles(new_articles)

        for link in article_links:
            if link:
                yield response.follow(link,self.parse_atuality_detail)

    def parse_atuality_detail(self, response):
        # Find the link to the PDF in the page
        pdf_url = response.css('div.td-post-content > div.wp-block-file > a[href$=".pdf"]::attr(href)').get()  # Finds a link ending in .pdf
        if pdf_url:
            pdf_url = response.urljoin(pdf_url)  # Get the full URL if the link is relative
            yield scrapy.Request(pdf_url, callback=self.save_pdf)

    def save_pdf(self, response):
        # Extract the PDF file name from the URL
        pdf_filename = response.url.split('/')[-1]
        pdf_path = os.path.join(self.pdf_folder, pdf_filename)

        # Check if the file already exists
        if os.path.exists(pdf_path):
            self.log(f'PDF already exists: {pdf_path}, skipping download')
            return  # Skip downloading

        # If the file doesn't exist, download and save the PDF
        with open(pdf_path, 'wb') as f:
            f.write(response.body)
        
        self.log(f'Saved PDF file: {pdf_path}')



    def load_existing_articles(self):
        if not os.path.exists(self.json_file_path):
            return []  # Return an empty list if the file doesn't exist

        with open(self.json_file_path, 'r') as file:
            data = json.load(file)
            return [article['title'] for article in data]
        
    def save_articles(self, new_articles):
        if not new_articles:
            return  # No new articles to save

        # Load existing articles
        existing_data = []
        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'r') as file:
                existing_data = json.load(file)

        # Append new articles
        existing_data.extend(new_articles)

        # Write back to the JSON file
        with open(self.json_file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)