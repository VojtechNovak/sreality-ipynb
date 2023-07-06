1. Program scrapuje data z https://www.sreality.cz/hledani/prodej/byty (sreality.py)
2. Program uloží data do csv a z csv je načte do Postgres db (sreality.py)
3. Program zobrazí data na lokálním serveru v tabulce http://127.0.0.1:8080/ (server.py)
4. TO DO – docker-compose up doesnt work with selenium (ERROR selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH
even though the driver is in path)
Starting ChromeDriver 114.0.5735.90 (386bc09e8f4f2e025eddae123f36f6263096ae49-refs/branch-heads/5735@{#1052}) on port 9515
Only local connections are allowed.)

  ✔ Container ipynb-db-1       Created                                                                                     
  ✔ Container ipynb-server-1   Created                                                                                  
  ✔ Container ipynb-scraper-1  Created  
