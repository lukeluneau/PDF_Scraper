'''
Copies files from one directory to a zipfile in the downloads directory
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from types import FunctionType
from lxml import html
from urllib.request import *
import time
import os
import shutil
import requests
from tkinter import *
import datetime
import pdfx #for CRC
import inspect

try: # python 2.7
    from urlparse import urlparse
except:# python 3.4
    from urllib.parse import urlparse
try: # 2.7
    from httplib import HTTPConnection
except: # 3.4
    from http.client import HTTPConnection


# Location of this GUI file.
file = (inspect.getfile(inspect.currentframe()).split('\\')[-1])
SOURCE_DIR = os.path.abspath(os.path.dirname(file))

# Location of SDS Library sorted by company name --> ex) c:\dir\path\PDF_Location
PDF_Location = 'C:\\Users\\lluneau\\Desktop\\Fetch2.0\\PDF_Location'
#PDF_Location = "\\192.168.2.120\\Documents\\Fetch PDFs"  #NASS

class Scrapers():

    def Test():
        start_time = time.time()
        driver = webdriver.Firefox()
        driver.get('http://images.salsify.com/image/upload/s--Pzzd_Dp6--/jce4amrfskpxuxr2pw9l.pdf')
        Downloader.Download("Example.pdf", driver.current_url)
        driver.quit()
        print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator("Test").Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))

    def SherwinWilliams():
        start_time = time.time()
        driver = webdriver.Firefox()
        url_list = []
        driver.get('http://www.sherwin-williams.com/search/?itemsPerPage=80&siteSection=painting-contractors&Ntt=msds')
        time.sleep(2)
        count = 0
        while count < 4:
            count += 1
            element = 0
            for view in driver.find_elements_by_link_text("View Data Sheets"): 
                view.click()
            item = 0
            for sds in driver.find_elements_by_link_text('GHS-SDS'):
                sds.click()
                item += 1
                try:
                    window_after = driver.window_handles[1]
                    driver.switch_to_window(window_after)
                    current_url = driver.current_url
                    url_list.append(current_url)
                    print(current_url)
                    print("--- %s seconds ---" % (time.time() - start_time)), ('---%d---' % (item)), ('---%d---' % a)
                    driver.close()
                    window_original = driver.window_handles[0]
                    driver.switch_to_window(window_original)
                except:
                    pass
            driver.quit()
            driver = webdriver.Firefox()
            driver.get('http://www.sherwin-williams.com/search/?itemsPerPage=80&siteSection=painting-contractors&Ntt=msds')
            time.sleep(2)
            try:
                for i in range(count):
                    driver.find_element_by_link_text('Next').click()
                    time.sleep(5)
            except:
                pass
        driver.quit()
        num = 0
        for url in url_list:
            num += 1
            print(url)
            name = "%30d.pdf" % num
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('SherwinWilliams').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))

    def ScienceLab():
        start_time = time.time()
        connection = urlopen('https://www.sciencelab.com/msdsList.php')
        domain = html.fromstring(connection.read())
        url_list = []
        for url in domain.xpath('//a/@href'):
            url_list.append("http://www.sciencelab.com"+url)
        num = 0
        for url in url_list:
            print(url)
            num += 1
            name = "%04d.pdf" % num
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('ScienceLab').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Rustoleum():
        start_time = time.time()
        url_list = []
        def Rust(num):
            connection = urlopen('http://www.rustoleum.com/pages/find-a-product?mode=msds&sku=%s' % num)
            domain = html.fromstring(connection.read())
            for url in domain.xpath('//a/@href'):
                if url not in url_list and "MSDS/ENGLISH" in url:
                    url_list.append(url)
            print("--- %s seconds ---" % (time.time() - start_time), "---%s---" % num)  
        for num in range(10, 100):
            Rust(num)
        for url in url_list:
            print(url)
            try:
                name = '%s' % url.split('/')[-1]
                Downloader.Download(name, url)
            except:
                print("Could not download: %s" % url)
        PDF_Relocator('Rustoleum').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def SeymourPaint():
        start_time = time.time()
        driver = webdriver.Firefox()
        url_list = []
        driver.get("http://www.seymourpaint.com/msdstds/")
        for el in driver.find_elements_by_xpath("//select[@onchange]/option[@value]"):
            if ".pdf" in el.get_attribute("value").lower() and 'tds' not in el.get_attribute("value").lower():
                if el.get_attribute("value").lower().split('/')[-1][0].isdigit() == True:
                    url_list.append(el.get_attribute("value"))
        driver.quit()
        for url in url_list:
            print(url)
            try:
                name = '%s' % url.split('/')[-1]
                Downloader.Download(name, url)
                print("--- %s seconds ---" % (time.time() - start_time))
            except:
                pass    
        PDF_Relocator('SeymourPaint').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def RSC():
        start_time = time.time()
        driver = webdriver.Firefox()
        driver.get("http://www.rscbrands.com/products/msds.asp")
        driver.find_element_by_name("msds_field").clear()
        driver.find_element_by_name("msds_field").send_keys("%")
        driver.find_element_by_name("submit").click()
        num = 0
        url_list = []
        for i in range(len(driver.find_elements_by_xpath("//a[contains(@class, 'img-icon')]"))):
            if num % 70 == 0 and num != 0:
                driver.close()
                print ("Restarting Firefox -- Memory Overload.")
                time.sleep(3)
                driver = webdriver.Firefox()
                driver.get("http://www.rscbrands.com/products/msds.asp")
                driver.find_element_by_name("msds_field").clear()
                driver.find_element_by_name("msds_field").send_keys("%")
                driver.find_element_by_name("submit").click()
            driver.find_element_by_xpath("(//a[contains(@class, 'img-icon')])[%d]" % (i+1)).click()
            current_url = driver.current_url
            print (current_url)
            url_list.append(current_url)
            print("--- %s seconds ---" % (time.time() - start_time))
            driver.back()
            num += 1
        driver.quit()
        for url in url_list:
            print(url)
            name = '%s' % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('RSC').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Roche():
        start_time = time.time()
        driver = webdriver.Firefox()
        url_list = []
        driver.get('http://www.roche.com/sustainability/what_we_do/for_communities_and_environment/environment/safety_data_sheets-row.htm?sdssearch_name=%25&sdssearch_sum=&sdssearch_cas= ')
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="id-sdssearch_name"]').clear()
        driver.find_element_by_xpath('//*[@id="id-sdssearch_name"]').send_keys("%")
        driver.find_element_by_xpath('//*[@id="content"]/article/div[1]/form/div/p/button').click()
        time.sleep(3)
        for sds in driver.find_elements_by_link_text('English'):
            sds.send_keys("\n")
            window_after = driver.window_handles[1]
            driver.switch_to_window(window_after)
            current_url = driver.current_url
            url_list.append(current_url)
            print("--- %s seconds ---" % (time.time() - start_time))
            driver.close()
            window_original = driver.window_handles[0]
            driver.switch_to_window(window_original)
        driver.quit()
        for url in url_list:
            print(url)
            name = url[44:56] = '.pdf'
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('Roche').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Praxair():
        start_time = time.time()
        url_list = []
        connection = urlopen('http://www.praxair.com/resource-library/sds?s={%22k%22:%22%22,%22ps%22:1000}')
        domain = html.fromstring(connection.read())
        for url in domain.xpath('//a/@href'):
            if '.pdf' in url and url not in url_list:
                url_list.append(url)
        for url in url_list:
            print(url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('Praxair').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Randolph():
        start_time = time.time()
        connection = urlopen('http://www.randolphproducts.com/msds/')
        domain = html.fromstring(connection.read())
        url_list = []
        for url in domain.xpath('//a/@href'):
            if url.lower().endswith('.pdf'):
                url_list.append(url)
        for url in url_list:
            print(url)
            name = '%s' % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('Randolph').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def PPG():
        start_time = time.time()
        num = 0
        url_list = []
        driver = webdriver.Firefox()
        driver.get('https://buyat.ppg.com/ehsdocumentmanagerpublic/documentSearchInnerFrame.aspx?NameCondition=BeginsWith&NameValue=%25&CodeCondition=BeginsWith&CodeValue=&CompCondition=BeginsWith&CompValue=&Form=53bd5d15b2c796a10000&SortBy=ProductName&Language=en-US&SBU=&From=&To=&SuppressSearchControls=False&AlwaysShowSearchResults=False&PageSize=20&FolderID1=0&FolderID2=0&FolderID3=0&FolderID4=0&FolderID5=0&FolderID6=0&FolderID7=0&FolderID8=0&FolderID9=0&FolderID10=0&SearchAllPublicFolders=True&PageNumber=1')
        for i in range(2827):
            driver.find_element_by_link_text("%s" %(i+1)).click()
            num += 1
            for elt in driver.find_elements_by_xpath("//td[@class='whitebold']/a"):
                elt.click()
                window_after = driver.window_handles[1]
                driver.switch_to_window(window_after)
                current_url = driver.current_url
                url_list.append(current_url)
                driver.close()
                window_original = driver.window_handles[0]
                driver.switch_to_window(window_original)
            print("--- %s seconds ---" % (time.time() - start_time))
            if num % 15 == 0 and num != 0:
                driver.quit()
                driver = webdriver.Firefox()
                driver.get('https://buyat.ppg.com/ehsdocumentmanagerpublic/documentSearchInnerFrame.aspx?NameCondition=BeginsWith&NameValue=%25&CodeCondition=BeginsWith&CodeValue=&CompCondition=BeginsWith&CompValue=&Form=53bd5d15b2c796a10000&SortBy=ProductName&Language=en-US&SBU=&From=&To=&SuppressSearchControls=False&AlwaysShowSearchResults=False&PageSize=20&FolderID1=0&FolderID2=0&FolderID3=0&FolderID4=0&FolderID5=0&FolderID6=0&FolderID7=0&FolderID8=0&FolderID9=0&FolderID10=0&SearchAllPublicFolders=True&PageNumber=1')
        for url in url_list:
            print(url)
            name = "SDS_%03d.pdf" % num
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('PPG').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Permatex():
        start_time = time.time()
        connection = urlopen('https://www.permatex.com/tech-documents/sds/?sds_doc=01010,01013,01020,01406,09100,09101,09102,09103,09116,09117,09128,09973,09974,09975,09976,09977,09978,09979,09980,13104,13106,13126,14104,14106,14126,14600,15022,15045,15650,15717,16067,19962,19967,19968,20353,20356,20539,21222,21309,21351,21425,22058,22071,22072,22074,22340,22700,22701,22705,22732,22755,23108,23122,23217,23218,23319,24005,24010,24024,24026,24027,24105,24110,24125,24163,24200,24206,24210,24240,24250,24283,24300,24350,25050,25051,25108,25122,25217,25219,25223,25224,25229,25238,25247,25575,25616,25618,25905,25909,26210,26240,26250,26629,26705,26801,26805,26810,26825,26832,26855,26900S,26901S,26905S,26932,26955,27005,27010,27100,27110,27140,27150,27183,27200,27218,27240,27725,27740,27828,27901,27932,27955,28192,29000,29040,29132,29208,29520,30058,30232,31163,33013,33694,34310,34311,35013,35406,49450,49550,51031,51531,51580,51813,51817,51845,54540,56521,59214,59235,60950,64000,64040,65108,65115,65217,68050,77124,77134,77164,80003,80007,80008,80011,80015,80016,80017,80018,80019,80022,80025,80030,80036,80037,80038,80043,80045,80050,80052,80057,80060,80062,80063,80064,80065,80070,80071,80072,80073,80074,80075,80077,80078,80208,80279,80328,80331,80332,80333,80334,80335,80338,80345,80369,80370,80577,80628,80631,80632,80633,80638,80645,80652,80697,80729,80855,80902,81150,81153,81158,81159,81160,81173,81180,81182,81184,81343,81409,81422,81464,81724,81725,81730,81731,81737,81742,81756,81773,81775,81781,81786,81833,81840,81844,81849,81850,81860,81878,81915,81943,81950,81981,82019,82080,82099,82112,82135,82180,82190,82191,82194,82195,82220,82450,82565,82588,82606,84101,84107,84109,84115,84145,84160,84201,84209,84330,84331,84332,84333,84334,85080,85084,85120,85144,85188,85224,85409,85420,85519,85742,85913,85915,87701,87705,87732,87755')
        domain = html.fromstring(connection.read())
        url_list = []
        for url in domain.xpath('//a/@href'):
            if url.lower().endswith('.pdf') and "USA-English" in url:
                url_list.append(url)
        num = 0
        for url in url_list:
            print(url)
            num += 1
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))    
        PDF_Relocator('Permatex').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def NationalGypsum():
        start_time = time.time()
        connection = urlopen('https://www.nationalgypsum.com/products/product.aspx?doctype=SDS')
        domain = html.fromstring(connection.read())
        url_list = []
        for url in domain.xpath("//a/@href"):
            url = url[2:]
            s = list(url)
            for spot in s:
                if spot == '\\':
                    s[0] = '/'
                    s[5] = '/'
            url = ''.join(s)
            if url.lower().endswith('.pdf'):
                url_list.append("https://www.nationalgypsum.com" + url)
        del url_list[0]
        for url in url_list:
            print(url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('NationalGypsum').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def MOC():
        start_time = time.time()
        for i in range(330, 662):
            url = 'http://msds.mocauto.com/index.php/sds-subscriptionss?task=document.viewdoc&id=%s' % i
            print(url)
            name = "SDS%s.pdf" % url.split('id=')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('MOC').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def LPSLabs():
        start_time = time.time()
        driver = webdriver.Firefox()
        url_list = []
        driver.get('http://www.lpslabs.com/search-results')
        time.sleep(1)
        for product in range(len(driver.find_elements_by_xpath("//table[@class='search-results']//a"))):
            driver.find_elements_by_xpath("//table[@class='search-results']//a")[product].click()
            driver.find_element_by_link_text('US Safety Data Sheet').click()
            time.sleep(1)
            driver.find_element_by_link_text('English').send_keys("\n")
            time.sleep(1)
            try:
                driver.find_element_by_link_text('Aerosol').send_keys("\n")
                window_after = driver.window_handles[1]
                driver.switch_to_window(window_after)
                current_url = driver.current_url
                if current_url not in url_list:
                    url_list.append(current_url)
                driver.close()
                window_original = driver.window_handles[0]
                driver.switch_to_window(window_original)
                print("--- %s seconds ---" % (time.time() - start_time))
                time.sleep(5)
            except:
                pass
            try:
                driver.find_element_by_link_text('Non-Aerosol').click()
                window_after = driver.window_handles[1]
                driver.switch_to_window(window_after)
                current_url = driver.current_url
                if current_url not in url_list:
                    url_list.append(current_url)
                driver.close()
                window_original = driver.window_handles[0]
                driver.switch_to_window(window_original)
                print("--- %s seconds ---" % (time.time() - start_time))
                time.sleep(5)
            except:
                pass
            driver.get('http://www.lpslabs.com/search-results')
        driver.quit()
        for url in url_list:
            print(url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('LPSLabs').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Lubriplate():
        start_time = time.time()
        url_list = []
        connection = urlopen('https://www.lubriplate.com/Technical/SDS.html')
        domain = html.fromstring(connection.read())
        for url in domain.xpath('//a/@href'):
            if 'sds' in url.lower() and 'pdf' in url.lower():
                url_list.append('https://www.lubriplate.com' + url)
        num = 0
        for url in url_list:
            print(url)
            num +=1
            name = "%s.pdf" % num
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('Lubriplate').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def LORD():
        start_time = time.time()
        driver = webdriver.Firefox()
        url_list = []
        page_list = ['adhesives', 'coatings', 'electronic-materials']
        page_url = []
        for page in page_list:
            driver.get('http://www.lord.com/products-and-solutions/' + page)
            if page == page_list[0]:
                print(len(driver.find_elements_by_link_text('View Products')))
                connection = urlopen(driver.current_url)
                domain = html.fromstring(connection.read())
                for url in domain.xpath('//a/@href'):
                    if '/products-and-solutions/adhesives' in url and len(url) > len('/products-and-solutions/adhesives'):
                        if url not in page_url:
                            page_url.append(url)
            if page == page_list[1]:
                for i in range(11):
                    time.sleep(2)
                    driver.find_element_by_xpath('//*[@id="block-system-main"]/div/div/section[2]/div/div/div[2]/div/div[2]/div/div/div/div/div[1]/div/div/p/a[%s]' % (i+1)).send_keys('\n')
                    page_url.append(driver.current_url)
                    driver.back()
            if page == page_list[2]:
                page_url.append('http://www.lord.com/products-and-solutions/electronic-materials/potting-and-encapsulation?keyword=&items_per_page=100')
                page_url.append('http://www.lord.com/products-and-solutions/electronic-materials/semiconductor-packaging-and-circuit-assembly?keyword=&items_per_page=100')
                page_url.append('http://www.lord.com/products-and-solutions/electronic-materials/thick-film-materials?keyword=&items_per_page=100')
                page_url.append('http://www.lord.com/products-and-solutions/specialty-chemicals/specialty-chemicals-product-search-emulsion')
        driver.quit()

        def Get_URL(url):
            connection = urlopen(url)
            domain = html.fromstring(connection.read())
            for url in domain.xpath('//a/@href'):
                if 'pdf' in url.lower() and 'DS' not in url:
                    url_list.append(url)
        for url in page_url:
            if url[1] == "p":
                url = "http://www.lord.com/" + url[1:] + '?keyword=&items_per_page=100'
            if url[6] == "p":
                url = "http://www.lord.com/" + url[6:] + '?keyword=&items_per_page=100'
        Get_URL(url)
        for url in set(url_list):
            print(url)
            url = 'http://www.lord.com/%s' % url
            try:
                name = '%s' % url.split('/')[-1]
                Downloader.Download(name, url)
            except:
                print("Could not download: %s" % url)
        PDF_Relocator('LORD').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Lenco():
        start_time = time.time()
        driver = webdriver.Firefox()
        driver.get("http://www.lencocanada.com/msds.html")
        for i in range(len(driver.find_elements_by_xpath("//div[@class='right_content_body']//a"))):
            try:
                driver.implicitly_wait(1)
                driver.find_element_by_xpath("(//div[@class='right_content_body']//a)[%d]" % (i+1)).click()
                current_url = driver.current_url
                print (current_url)
                url_list.append(current_url)
                driver.back()
            except:
                pass
            print("--- %s seconds ---" % (time.time() - start_time))
        driver.quit()
        for url in url_list:
            print(url)
            name = '%s' % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('Lenco').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def JohnsonDiversey():
        start_time = time.time()
        driver = webdriver.Firefox()
        url_list = []
        driver.get('https://sds.sealedair.com/default.aspx')
        driver.find_element_by_xpath('//*[@id="ddlCountry"]').send_keys('UN')
        driver.find_element_by_xpath('//*[@id="btnCountry"]').click()
        driver.find_element_by_xpath('//*[@id="ctlMasterPage_pageContent"]/table[4]/tbody/tr[4]/td[2]/select').send_keys('E')
        driver.find_element_by_xpath('//*[@id="ctlMasterPage_pageContent"]/table[6]/tbody/tr[2]/td[3]/a').click()
        time.sleep(2)
        for page in range(30):
            if page % 6 == 0 and page != 0:
                driver.quit()
                print("Memory Overload -- Resetting Firefox")
                driver = webdriver.Firefox()
                driver.get('https://sds.sealedair.com/default.aspx')
                driver.find_element_by_xpath('//*[@id="ddlCountry"]').send_keys('UN')
                driver.find_element_by_xpath('//*[@id="btnCountry"]').click()
                driver.find_element_by_xpath('//*[@id="ctlMasterPage_pageContent"]/table[4]/tbody/tr[4]/td[2]/select').send_keys('E')
                driver.find_element_by_xpath('//*[@id="ctlMasterPage_pageContent"]/table[6]/tbody/tr[2]/td[3]/a').click()
                time.sleep(2)
                for i in range(page):
                    driver.find_element_by_link_text('Next').send_keys('\n')
                    time.sleep(1)
            for sds in range(50):
                try:
                    driver.find_element_by_xpath('//*[@id="tlbResults"]/tbody/tr[%s]/td[1]/a' % (sds + 2)).click()
                    window_after = driver.window_handles[1]
                    driver.switch_to_window(window_after)
                    current_url = driver.current_url
                    if current_url not in url_list:
                        url_list.append(current_url)
                    print("--- %s seconds ---" % (time.time() - start_time), '------%s------' % ((page*50)+(sds+1)))
                    driver.close()
                    window_original = driver.window_handles[0]
                    driver.switch_to_window(window_original)
                except:
                    print("--- %s seconds ---" % (time.time() - start_time), 'Could not click on %s' % ((page*50)+(sds+1)))
            try:
                driver.find_element_by_link_text('Next').send_keys('\n')
            except:
                print("No More Pages.")
                break
            print ("Clicked on next page: %s" % (page+1))
        driver.quit()
        for url in url_list:
            print(url)
            name = "%s.pdf" % url.split('prd=')[-1].split('%7E%7EPDF')[0]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('JohnsonDiversey').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def LawsonProducts():
        start_time = time.time()
        reset = 0
        driver = webdriver.Firefox()
        url_list = []
        KeyWords = ['Adhesive', 'Chemical', 'Acid', 'Solution', 'Liquid', 'Wire', 'Weld', 'Tape', 'Battery', 'Treatment', 'Wood', 'Steel', 'Copper', 'Water', 'Jel', 'Spray', 'Earth', 'Cleaner', 'Compound', 'Gal', 'Q', 'J', 'Dirt', 'Pro', 'Foam', 'oz', 'os', 'Glass', 'Paint', 'Core', 'Solder', 'Aerosol', 'Safety', 'General', 'Purpose', 'ae']
        for KeyWord in KeyWords:
            driver.get("https://www.lawsonproducts.com/msds/msds-search.jsp")
            driver.find_element_by_id("productName_search").clear()
            driver.find_element_by_id("productName_search").send_keys('%s' % KeyWord)
            driver.find_element_by_name('/lp/msds/MsdsFormHandler.msdsSearch').click()
            time.sleep(2)
            for i in range(len(driver.find_elements_by_xpath("//table[@class='msds-table']//a"))):
                driver.find_element_by_xpath("(//table[@class='msds-table']//a)[%d]" % (i+1)).click()
                try:
                    window_after = driver.window_handles[1]
                    driver.switch_to_window(window_after)
                    current_url = driver.current_url
                    if current_url not in url_list:
                        url_list.append(current_url)
                    print("--- %s seconds ---" % (time.time() - start_time)), "------%d------" % i, "---%s---" % KeyWord
                    driver.close()
                    window_original = driver.window_handles[0]
                    driver.switch_to_window(window_original)
                except:
                    pass
                reset += 1
                if reset % 400 == 0 and reset != 0:
                    driver.close()
                    print("Restarting Firefox -- Memory Overload.")
                    time.sleep(3)
                    driver = webdriver.Firefox()
                    driver.get("https://www.lawsonproducts.com/msds/msds-search.jsp")
                    driver.find_element_by_id("productName_search").clear()
                    driver.find_element_by_id("productName_search").send_keys('%s' % KeyWord)
                    driver.find_element_by_name('/lp/msds/MsdsFormHandler.msdsSearch').click()
                    time.sleep(2)
        driver.quit()
        for url in url_list:
            print(url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('LawsonProducts').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def HP():
        start_time = time.time()
        url_list = []
        page_url = []
        connection = urlopen('http://www8.hp.com/us/en/hp-information/environment/msds-specs.html')
        domain = html.fromstring(connection.read())
        for url in domain.xpath('//a/@href'):
            if 'productdata' in url and 'http' in url:
                page_url.append(url)
        for i in range(3):
            del page_url[-1]
        page_url.append('http://www8.hp.com/us/en/hp-information/global-citizenship/environment/productdata/msdsmaintsupp.html')
        for url in page_url:
            connection = urlopen('%s' % url)
            domain = html.fromstring(connection.read())
            for url in domain.xpath('//a/@href'):
                if 'pdf' in url and 'http' in url:
                    url_list.append(url)
                if 'pdf' in url and 'http' not in url:
                    url_list.append('http://www.hp.com' + url)
        for url in url_list:
            print(url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('HP').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def IPS():
        start_time = time.time()
        connection = urlopen('http://www.ipscorp.com/plumbing/weldon/weldon_spec')
        domain = html.fromstring(connection.read())
        url_list = []
        for url in domain.xpath('//a/@href'):
            if 'pdf' in url and 'SP' not in url:
                if 'http' not in url:
                    url_list.append('http://www.ipscorp.com' + url)
                else:
                    url_list.append(url)
        for url in url_list:
            print(url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('IPS').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Hexis():
        start_time = time.time()
        connection = urlopen('http://www.hexis.co.uk/hexis/MSDS.html')
        domain = html.fromstring(connection.read())
        url_list = []
        for url in domain.xpath('//a/@href'):
            if "MSDS" in url:
                url_list.append("http://www.hexis.co.uk/hexis/"+url)
        num = 0
        for url in url_list:
            print(url)
            name = '%s' % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('Hexis').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def GWJ():
        start_time = time.time()
        driver = webdriver.Firefox()
        url_list = []
        driver.get('http://www.gwjcompany.com/index.php?main_page=advanced_search_result&search_in_description=1&keyword=sds')
        time.sleep(1)
        for tab in range(61):
            driver.find_element_by_xpath('//*[@id="catList"]/div[%s]/div[1]/a/img' % (tab+1)).click()
            try:
                driver.find_element_by_link_text('Click to Download The MSDS For This Product').click()
                window_after = driver.window_handles[1]
                driver.switch_to_window(window_after)
                current_url = driver.current_url
                url_list.append(current_url)
                print("--- %s seconds ---" % (time.time() - start_time))
                driver.close()
                window_original = driver.window_handles[0]
                driver.switch_to_window(window_original)
            except:
                pass
            driver.back()
            time.sleep(1)
        driver.quit()
        num = 0
        for url in url_list:
            print(url)
            num += 1
            name = "%02d.pdf" % num
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('GWJ').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def GOJO():
        start_time = time.time()
        driver = webdriver.Firefox()
        url_list = []
        driver.get('https://www.gojo.com/')
        time.sleep(1)
        driver.find_element_by_link_text('SDS').click()
        window_after = driver.window_handles[1]
        driver.switch_to_window(window_after)
        time.sleep(15)
        for sds in driver.find_elements_by_link_text('English'):
            try:
                time.sleep(1)
                sds.click()
                sds_window = driver.window_handles[2]
                driver.switch_to_window(sds_window)
                current_url = driver.current_url
                if current_url not in url_list:
                    url_list.append(current_url)
                print("--- %s seconds ---" % (time.time() - start_time))
                driver.close()
                driver.switch_to_window(window_after)
            except:
                print('could not click on %s' % sds)
        driver.quit()
        num = 0
        for url in url_list:
            print(url)
            num += 1
            name = "%02d" % num
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('GOJO').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Gelest():
        start_time = time.time()
        driver = webdriver.Firefox()
        url_list = []
        driver.get('http://www.gelest.com/product-search/?wpsolr_q=')
        time.sleep(1)
        for page in range(7):
            for sds in driver.find_elements_by_link_text('SDS'):
                sds.send_keys('\n')
                window_after = driver.window_handles[1]
                driver.switch_to_window(window_after)
                current_url = driver.current_url
                if current_url not in url_list:
                    url_list.append(current_url)
                print("--- %s seconds ---" % (time.time() - start_time))
                driver.close()
                window_original = driver.window_handles[0]
                driver.switch_to_window(window_original)
            driver.find_element_by_link_text('%s' % (page+2)).send_keys("\n")
        driver.quit()
        new_list = []
        for url in url_list:
            print(url)
            a = url[50:]
            new_list.append(a)
        for url in new_list:
            print(url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('Gelest').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def ExxonMobil():
        start_time = time.time()
        def SetUp():
            download_to = PDF_Location + "\\ExxonMobil"
            Actions.Ensure_Dir(download_to)
            global driver
            profile = webdriver.FirefoxProfile()
            profile.set_preference("browser.download.folderList", 2)
            profile.set_preference("browser.download.manager.showWhenStarting", False)
            profile.set_preference("browser.download.dir", download_to)
            profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/rtf")
            profile.set_preference("browser.helperApps.alwaysAsk.force", False)             
            profile.set_preference("pdfjs.disabled", True)
            driver = webdriver.Firefox(firefox_profile=profile)
        url_list = []
        SetUp()
        driver.get('http://www.msds.exxonmobil.com/IntApps/psims/psims.aspx')
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="drpCountry"]').click()
        driver.find_element_by_xpath('//*[@id="drpCountry"]').send_keys("USA")
        driver.find_element_by_xpath('//*[@id="txtProd"]').clear()
        driver.find_element_by_xpath('//*[@id="txtProd"]').send_keys("%")
        driver.find_element_by_xpath('//*[@id="drpPerPage"]').click()
        driver.find_element_by_xpath('//*[@id="drpPerPage"]').send_keys(Keys.ARROW_DOWN)
        driver.find_element_by_xpath('//*[@id="drpPerPage"]').send_keys(Keys.RETURN)
        driver.find_element_by_xpath('//*[@id="btnSearch"]').click()
        time.sleep(3)
        page = 1
        for i in range(9):
            for sds in range(30):
                try:
                    driver.find_element_by_xpath('//*[@id="gvResults"]/tbody/tr[%d]/td[1]/a' % (sds+3)).click()
                    print("Last SDS was: %s" % (sds+1))
                except:
                    driver.back()
            time.sleep(1)
            try:
                driver.find_element_by_link_text('%d' % (page+1)).send_keys("\n")
            except:
                print ("---Could not click on next page---")
            page += 1
            time.sleep(2.5)
        driver.quit()
        PDF_Relocator("ExxonMobil").Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Enlight():
        start_time = time.time()
        connection = urlopen('http://www.ormco.com/resources/msds.php')
        domain = html.fromstring(connection.read())
        url_list = []
        for url in domain.xpath('//a/@href'):
            if 'pdf' in url and 'msds' in url:
                if url[0] == '.':
                    url = url[2:]
                url_list.append("http://www.ormco.com"+url)
        lang_list = ['canada', 'danish', 'german', 'dutch', 'eu-spanish', 'french', 'italian', 'polish', 'slovenian', 'finnish', 'swedish']
        for lang in lang_list:
            for url in url_list:
                if url.lower().endswith('%s.pdf' % lang):
                    url_list.remove(url)
        time.sleep(5)
        for url in url_list:
            print(url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('Enlight').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def EMDMillipore():
        start_time = time.time()
        def SetUp():
            download_to = PDF_Location + '\\EMDMillipore'
            Actions.Ensure_Dir(download_to)
            global driver
            profile = webdriver.FirefoxProfile()
            profile.set_preference("browser.download.folderList", 2)
            profile.set_preference("browser.download.manager.showWhenStarting", False)
            profile.set_preference("browser.download.dir", download_to)
            profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
            profile.set_preference("browser.helperApps.alwaysAsk.force", False)     
            profile.set_preference("pdfjs.disabled", True)
            driver = webdriver.Firefox(firefox_profile=profile)
        url_list = []
        SetUp()
        driver.get('http://www.emdmillipore.com/Web-US-Site/en_CA/-/USD/ViewParametricSearch-ProductPaging?PageNumber=0&PageSize=20&SortingAttribute=&TrackingSearchType=filter&SingleResultDisplay=SFProductSearch&SearchTerm=*&SelectedSearchResult=SFProductSearch&SearchContextPageletUUID=_dWb.qB.SiUAAAFA8pIEM3P1&SearchParameter=%26%40QueryTerm%3D*%26channels%3DUS_or_GLOBAL%26ContextCategoryUUIDs%3D3Vyb.qB.B4YAAAE_0AZ3.Lxj%257Cda.b.qB.DRMAAAE_.d53.L6L%26MERCK_FF.defaultSimilarity%3D9000%26MERCK_FF.enabledFilters%3D')
        time.sleep(1)
        for page in range(63): #63
            time.sleep(5)
            current_url = driver.current_url
            try:
                driver.find_element_by_xpath('//*[@id="fsrOverlay"]/div/div/div/div/div/div[2]/div[2]/a').send_keys("\n")
            except:
                pass
            for sds in range(20):
                try:
                    time.sleep(2)
                    try:
                        driver.find_element_by_xpath('//*[@id="fsrOverlay"]/div/div/div/div/div/div[2]/div[2]/a').send_keys("\n")
                    except:
                        pass
                    try:
                        driver.find_element_by_xpath('//*[@id="Products"]/div[2]/section[%s]/div[3]/ul/li[1]/a' % (sds+1)).click()
                        time.sleep(1)
                        print ("sds %s" % (sds+1))
                        driver.find_element_by_xpath('//*[@id="msdsDownloadbtn"]').click()
                        driver.back()
                    except:
                        driver.get(current_url)
                except:
                    print('Could not do %s.' % (sds+1))
                    driver.get(current_url)
            time.sleep(1)
            try:
                driver.find_element_by_xpath('//*[@id="fsrOverlay"]/div/div/div/div/div/div[2]/div[2]/a').send_keys("\n")
            except:
                pass
            driver.get(current_url)
            time.sleep(3)
            try:
                driver.find_element_by_xpath('//*[@id="Products"]/div[2]/div[1]/div[3]/div/ul/li[6]/a').send_keys('\n')
                print("Supposed To Be On Page: % s" % (page+2))
            except:
                print("Could NOT Click On Next Page")
                driver.get(current_url)
                try:
                    driver.find_element_by_xpath('//*[@id="Products"]/div[2]/div[1]/div[3]/div/ul/li[6]/a').send_keys('\n')
                    print("Tried To Click Again")
                    print("Click was Successful")
                except:
                    print("Second Try Was Not Successful.")
        time.sleep(3)   
        driver.quit()
        PDF_Relocator("EMDMillipore").Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Dap():
        start_time = time.time()
        driver = webdriver.Firefox()
        url_list = []
        driver.get('http://www.dap.com/')
        time.sleep(1)
        page_url = []
        current_url = driver.current_url
        connection = urlopen('%s' % current_url)
        domain = html.fromstring(connection.read())
        for url in domain.xpath('//a/@href'):
            if '/products/' in url and 'http' not in url and len(url) > 12:
                page_url.append('http://www.dap.com' + url)
        product_list = []
        for page in page_url:
            connection = urlopen('%s' % page)
            domain = html.fromstring(connection.read())
            for url in domain.xpath('//a/@href'):
                if 'dap-products-ph' in url and url not in product_list:
                    product_list.append('http://www.dap.com' + url)
        num = 0
        for product in set(product_list):
            print(product)
            if num % 100 == 0 and num != 0:
                driver.quit()
                time.sleep(5)
                driver = webdriver.Firefox()
            driver.get('%s' % product)
            try:
                driver.find_element_by_partial_link_text('SDS').click()
                time.sleep(1)
                for sds in driver.find_elements_by_link_text('ENGLISH'):
                    try:
                        sds.click()
                        window_after = driver.window_handles[1]
                        driver.switch_to_window(window_after)
                        current_url = driver.current_url
                        url_list.append(current_url)
                        driver.close()
                        window_original = driver.window_handles[0]
                        driver.switch_to_window(window_original)
                    except:
                        print('Could not click on SDS')
            except:
                print("Page does not exist")
        for url in url_list:
            x = url.split('/')[-1]
            result = ''.join([i for i in x if i.isdigit()])
            if len(result) <= 9:
                url_list.remove(url)
        driver.quit()
        for url in url_list:
            print (url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('Dap').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Dell():
        start_time = time.time()
        connection = urlopen('http://www.dell.com/learn/us/en/vn/product-info-msds-batteries')
        domain = html.fromstring(connection.read())
        url_list = []
        for url in domain.xpath('//a/@href'):
            if "Documents/sds" in url:
                url_list.append(url)
        ###################################################################
        #       Downloads from the printers/ink/other sds from Dell
        #       Dell puts them in two categories
        ###################################################################
        connection = urlopen('http://www.dell.com/learn/us/en/vn/product-info-msds-printer-ink-toner')
        domain = html.fromstring(connection.read())
        url_list = []
        for url in domain.xpath('//a/@href'):
            if "solutions/en/Documents/print_" in url:
                url_list.append(url)
        for url in url_list:
            print(url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('Dell').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def DadeBehring():
        start_time = time.time()
        connection = urlopen('https://www.healthcare.siemens.com/doclib/jsp_doclib_public/doclib_homePage.jsp?tabId=5&msdsSR=yes&gotoMSDS=1&doclibId=1&locale=en_US&msdsSearchFormDescription=%25&msdsSearchFormLanguageCountry=United+States+of+America_Eng&msdsSearchFormProductLine=&continue=true')
        domain = html.fromstring(connection.read())
        url_list = []
        for url in domain.xpath('//a/@href'):
            if 'pdf' in url:
                url_list.append(url)
        for url in set(url_list):
            print (url)
            name = url.upper().split('/')[-1].split('_SIEMENS')[0] + '.pdf'
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('DadeBehring').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def CRC():
        start_time = time.time()
        global_PDF = ['http://crcindustries.com/ei/files/CRC-GHS-Update-for-SDS-2015-12.pdf']
        target_directory = '%s\\CRC' % PDF_Location
        for pdf in global_PDF:
            pdf = pdfx.PDFx("%s" % pdf)
            metadata = pdf.get_metadata()
            references_list = pdf.get_references()
            references_dict = pdf.get_references_as_dict()
            pdf.download_pdfs(target_directory)
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def ConocoPhillips():
        start_time = time.time()
        connection = urlopen('http://www.conocophillips.com/sustainable-development/safety-health/Pages/safety-data-sheets.aspx')
        domain = html.fromstring(connection.read())
        url_list = []
        for url in domain.xpath('//a/@href'):
            if url.lower().endswith('.pdf'):
                url_list.append("http://www.conocophillips.com"+url)
        for url in url_list:
            print(url)
            name = '%s' % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time)) 
        PDF_Relocator('ConocoPhillips').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Colgate():
        start_time = time.time()
        driver = webdriver.Firefox()
        url_list = []
        page_list = []
        connection = urlopen('http://www.colgatecommercial.com/SDS-Sheets.aspx')
        domain = html.fromstring(connection.read())
        for url in domain.xpath('//a/@href'):
            if url.endswith('.aspx'):
                page_list.append("http://www.colgatecommercial.com" + url)
        page_list = page_list[25:-6]
        for page in page_list:
            driver.get(page)
            try:
                driver.find_element_by_link_text('SDS Sheets').send_keys('\n')
                window_after = driver.window_handles[1]
                driver.switch_to_window(window_after)
                current_url = driver.current_url
                if current_url not in url_list:
                    url_list.append(current_url)
                driver.close()
                window_original = driver.window_handles[0]
                driver.switch_to_window(window_original)
            except:
                print('This page does not have an SDS: %s' % page[32:])
        driver.quit()
        for url in url_list:
            print (url)
            name = url[-11:]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('Colgate').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Citgo():
        start_time = time.time()
        driver = webdriver.Firefox()
        url_list = []
        driver.get('https://www.citgo.com/CITGOforYourBusiness/SDS.jsp')
        time.sleep(1)
        page_url_list = []
        for i in range(3):
            xpath = '//*[@id="allcopy"]/div/div/p[3]/a[%s]' % (i+1)
            driver.find_element_by_xpath(xpath).send_keys('\n')
            page_url = driver.current_url
            page_url_list.append(page_url)
            time.sleep(1)
            driver.back()
            time.sleep(1)
        for page in page_url_list:
            connection = urlopen('%s' % page)
            domain = html.fromstring(connection.read())
            for url in domain.xpath('//a/@href'):
                if 'pdf' in url and 'msds' in url:
                    url_list.append(url)
        driver.quit()
        num = 0
        for url in url_list:
            print (url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('Citgo').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Clorox():
        start_time = time.time()
        connection = urlopen('https://www.thecloroxcompany.com/products/sds/')
        domain = html.fromstring(connection.read())
        url_list = []
        lang_list = ['canada', 'uk(english)', 'japan', 'malaysia', 'puertorico', 'sg', 'korea' ]
        for url in domain.xpath('//a/@href'):
            if '.pdf' in url:
                url_list.append('http://wilkopaintinc.com/' + url)
        temp_list = []
        for url in url_list:
            for lang in lang_list:
                if lang in url:
                    temp_list.append(url)
        for url in temp_list:
            if url in url_list:
                url_list.remove(url)
        for url in url_list:
            print(url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('Clorox').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Chemtronics():
        start_time = time.time()
        driver = webdriver.Firefox()
        driver.get("https://www.chemtronics.com/msds.aspx")
        url_list = []
        count = 0
        for elt in range(15):
            for i in range(len(driver.find_elements_by_xpath("//tbody//td[4]//ul[@class='docs-list']//a"))):
                button = driver.find_element_by_xpath("(//tbody//td[4]//ul[@class='docs-list']//a)[%d]" % (i+1))
                button.click()
                window_after = driver.window_handles[1]
                driver.switch_to_window(window_after)
                current_url = driver.current_url
                print(current_url)
                if "English" in current_url and "United" in current_url:
                    url_list.append(current_url)
                driver.close()
                window_original = driver.window_handles[0]
                driver.switch_to_window(window_original)
                count += 1
                if count % 60 == 0:
                    driver.quit()
                    time.sleep(1)
                    driver = webdriver.Firefox()
                    driver.get("https://www.chemtronics.com/msds.aspx")
            driver.find_element_by_xpath('//*[@id="aspnetForm"]/div[4]/div[5]/ul[3]/li/a').click()
        driver.quit()
        num = 0
        for url in url_list:
            print (url)
            num += 1
            name = "SDS_%03s.pdf" % num
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('Chemtronics').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def CastleProducts():
        start_time = time.time()
        driver = webdriver.Firefox()
        driver.get("http://www.castlepackspower.com/search.cfm?Page=Search")
        driver.find_element_by_name("SearchTerm").clear()
        driver.find_element_by_name("SearchTerm").send_keys("%")
        driver.find_element_by_name("SearchTerm").send_keys(Keys.RETURN)
        url_list = []
        for i in range(len(driver.find_elements_by_xpath("//div[@id='content']//a"))):
            try:
                driver.find_element_by_xpath("(//div[@id='content']//a)[%d]" % (i+1)).click()
                current_url = driver.current_url
                connection = urlopen('%s' % current_url)
                domain = html.fromstring(connection.read())
                for url in domain.xpath('//a/@href'):
                    if url.lower().endswith('.pdf'):
                        url_list.append(url)
                driver.implicitly_wait(5)
                driver.back()
            except:
                driver.get("http://www.castlepackspower.com/search.cfm?Page=Search")
                driver.find_element_by_name("SearchTerm").clear()
                driver.find_element_by_name("SearchTerm").send_keys("%")
                driver.find_element_by_name("SearchTerm").send_keys(Keys.RETURN)
        driver.quit()
        temp_list = []
        for url in url_list:
            Crop_list = list(url)
            for num in range(14):
                del Crop_list[0]
            temp_list.append(''.join(Crop_list))
        url_list = []
        for url in temp_list:
            url_list.append('http://www.castlepackspower.com' + url)
        for url in url_list:
            print (url)
            name = url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('CastleProducts').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def CarrollCo():
        start_time = time.time()
        driver = webdriver.Firefox()
        driver.get("http://carrollco.com/sds/page/search")
        url_list = []
        for elt in range(15):
            for i in range(20):
                try:
                    driver.find_element_by_xpath("(//table[@class='msdst']//a)[%d]" % (i+1)).click()
                except:
                    continue
                window_after = driver.window_handles[1]
                driver.switch_to_window(window_after)
                current_url = driver.current_url
                print(current_url)
                url_list.append(current_url)
                print("--- %s seconds ---" % (time.time() - start_time))
                driver.close()
                window_original = driver.window_handles[0]
                driver.switch_to_window(window_original)
            print("Attempt to Click.", "Now on page %s" % (elt + 2))        
            try:
                driver.find_element_by_link_text('%s' % (elt + 2)).click()
            except:
                continue
        driver.quit()
        for url in url_list:
            print(url)
            name = '%s' % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('CarrollCo').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Carboline():
        start_time = time.time()
        def SetUp():
            download_to = PDF_Location + '\\Carboline'
            Actions.Ensure_Dir(download_to)
            global driver
            profile = webdriver.FirefoxProfile()
            profile.set_preference("browser.download.folderList", 2)
            profile.set_preference("browser.download.manager.showWhenStarting", False)
            profile.set_preference("browser.download.dir", download_to)
            profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
            profile.set_preference("browser.helperApps.alwaysAsk.force", False)     
            profile.set_preference("pdfjs.disabled", True)
            driver = webdriver.Firefox(firefox_profile=profile)
        url_list = []
        SetUp()
        driver.get('http://www.carboline.com/products/')
        time.sleep(1)
        for p in range(10, 100):
            driver.get("http://www.carboline.com/products/")
            time.sleep(1)
            driver.find_element_by_id("ap-prod").clear()
            driver.find_element_by_id("ap-prod").send_keys(p)
            driver.find_element_by_xpath("//input[@name='searchButtonprod']").click()
            time.sleep(5)
            a =  len(driver.find_elements_by_partial_link_text('SDS'))
            num = 0
            for sds in driver.find_elements_by_partial_link_text('SDS'):
                num += 1
                sds.send_keys('\n')
                print("--- %s seconds ---" % (time.time() - start_time), "---%s/%s---" % (num, a))
                time.sleep(1)
            if p % 20 == 0:
                time.sleep(3)
                driver.quit()
                print('Memory overload -- Restarting Firefox')
                time.sleep(3)
                SetUp()
                time.sleep(5)
        time.sleep(5)
        driver.quit()
        PDF_Relocator('Carboline').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Canon():
        start_time = time.time()
        def SetUp():
            download_to = PDF_Location + '\\Canon'
            Actions.Ensure_Dir(download_to)
            global driver
            global profile
            profile = webdriver.FirefoxProfile()
            profile.set_preference("browser.download.folderList", 2)
            profile.set_preference("browser.download.manager.showWhenStarting", False)
            profile.set_preference("browser.download.dir", download_to)
            profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "binary/octet-stream")
            profile.set_preference("browser.helperApps.alwaysAsk.force", False)     
            profile.set_preference("pdfjs.disabled", True)
            driver = webdriver.Firefox(firefox_profile=profile)
        url_list = []
        SetUp()
        driver.quit()
        SetUp()
        driver.get('http://downloads.oce.com/MaterialsSafetyDataDownloads/')
        driver.find_element_by_xpath('//*[@id="SEDCountryID"]').send_keys("United States")
        driver.find_element_by_xpath('//*[@id="SEDCountryID"]').send_keys(Keys.RETURN)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="SEDLangID"]').send_keys("English-US")
        driver.find_element_by_xpath('//*[@id="SEDLangID"]').send_keys(Keys.RETURN)
        time.sleep(1)
        Categories = ['Developer', 'Ink', 'Other Supplies', 'Photoconductor', 'Toner']
        for category in Categories:
            driver.find_element_by_xpath('//*[@id="SEDCategoryID"]').send_keys("%s" % category)
            driver.find_element_by_xpath('//*[@id="SEDCategoryID"]').send_keys(Keys.RETURN)
            time.sleep(2)
            print(len(driver.find_elements_by_partial_link_text('MSDS')))
            for sds in driver.find_elements_by_partial_link_text('MSDS'):
                try:
                    sds.send_keys('\n')
                    print("--- %s seconds ---" % (time.time() - start_time))
                    time.sleep(1)
                    for i in range(3):
                        try:
                            driver.find_element_by_xpath('//*[@id="ajax-modal"]/div/button').click()
                        except:
                            time.sleep(1)
                    time.sleep(1)
                except:
                    driver.quit()
                    SetUp()
                    driver.quit()
                    SetUp()
                    driver.get('http://downloads.oce.com/MaterialsSafetyDataDownloads/')
                    driver.find_element_by_xpath('//*[@id="SEDCountryID"]').send_keys("United States")
                    driver.find_element_by_xpath('//*[@id="SEDCountryID"]').send_keys(Keys.RETURN)
                    time.sleep(1)
                    driver.find_element_by_xpath('//*[@id="SEDLangID"]').send_keys("English-US")
                    driver.find_element_by_xpath('//*[@id="SEDLangID"]').send_keys(Keys.RETURN)
                    time.sleep(1)
                    driver.find_element_by_xpath('//*[@id="SEDCategoryID"]').send_keys("%s" % category)
                    driver.find_element_by_xpath('//*[@id="SEDCategoryID"]').send_keys(Keys.RETURN)
                    time.sleep(2)
        driver.quit()
        PDF_Relocator('Canon').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Bostik():
        start_time = time.time()
        connection = urlopen('http://www.bostik.co.uk/support/safetyData/construction/search/1/44/All')
        domain = html.fromstring(connection.read())
        url_list = []
        for url in domain.xpath('//a/@href'):
            if url.lower().endswith('.pdf'):
                url_list.append("http://www.bostik.co.uk"+url)
        num = 0
        for url in url_list:
            print(url)
            num +=1
            name = str(num) + url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('Bostik').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def BioRad():
        start_time = time.time()
        driver = webdriver.Firefox()
        url_list = []
        driver.get('http://www.bio-rad.com/evportal/evolutionPortal.portal?_nfpb=true&_pageLabel=LiteratureLibraryLanding&searchString=MSDS&database=faqs%2Bliteratures%2Bmsds%2Binserts&sfStartNumber=1&sfPageResize=true&sfMode=search&sfDim=&sfRetrievalFieldText=MATCH%7B0%7D%3A*%2FNoPDFLink%2BAND%2BMATCH%7Ben_US%2CUS%7D%3ALOCALE_KEY&sfRetrievalFilter=&sfRetrievalFilterText=&sfRetrievalFilterAction=&searchVertical=&catID=&jumpToAction=y&selection=MSDS%2C&divisionSelect=&sfResultsPerPage=30 ')
        driver.find_element_by_link_text('USA').click()
        time.sleep(10)
        while len(driver.find_elements_by_link_text('Next')) >= 1:
            page += 1
            if page % 10 == 0:
                driver.quit()
                print("Memory Overload -- Restarting Firfox")
                driver = webdriver.Firefox()
                driver.get('http://www.bio-rad.com/evportal/evolutionPortal.portal?_nfpb=true&_pageLabel=LiteratureLibraryLanding&searchString=MSDS&database=faqs%2Bliteratures%2Bmsds%2Binserts&sfStartNumber=1&sfPageResize=true&sfMode=search&sfDim=&sfRetrievalFieldText=MATCH%7B0%7D%3A*%2FNoPDFLink%2BAND%2BMATCH%7Ben_US%2CUS%7D%3ALOCALE_KEY&sfRetrievalFilter=&sfRetrievalFilterText=&sfRetrievalFilterAction=&searchVertical=&catID=&jumpToAction=y&selection=MSDS%2C&divisionSelect=&sfResultsPerPage=30 ')
                time.sleep(3)
                driver.find_element_by_link_text('USA').click()
                time.sleep(7)
                i = 5
                while i <= page:
                    try:
                        driver.find_element_by_link_text("%s" % i).click()
                        i += 5
                    except:
                        try:
                            driver.find_element_by_link_text("Take survey next time").click()
                        except:
                            print ("Could not click or skip survey")
            time.sleep(2.5)
            try:
                driver.find_element_by_link_text("Take survey next time").click()
            except:
                pass
            print ("-----%s-----" % page)
            for sds in range(len(driver.find_elements_by_class_name('imageIcons'))):
                driver.find_elements_by_class_name('imageIcons')[sds].click()
                window_after = driver.window_handles[1]
                driver.switch_to_window(window_after)
                current_url = driver.current_url
                if current_url not in url_list:
                    url_list.append(current_url)
                print("--- %s seconds ---" % (time.time() - start_time)), ("Page: %d" % page,'---%s---' % (sds+1))
                driver.close()
                window_original = driver.window_handles[0]
                driver.switch_to_window(window_original)
            time.sleep(2.5)
            try:
                driver.find_element_by_link_text("Take survey next time").click()
            except:
                pass
            driver.find_element_by_link_text("%s" % (page+1)).click()
            time.sleep(2.5)
        driver.quit()
        for url in url_list:
            print (url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('BioRad').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Bayer():
        start_time = time.time()
        driver = webdriver.Firefox()
        url_list = []
        driver.get('http://bayeres.ca/environmental-sciences/en/resources/labels-msds/')
        time.sleep(1)
        for sds in range(11):
            driver.find_element_by_xpath('//*[@id="templatewrapper"]/div[1]/div[2]/div[2]/div[3]/div/table/tbody/tr[%s]/td[3]/a' % (sds+2)).click()
            current_url = driver.current_url
            if current_url not in url_list and 'pdf' in current_url:
                url_list.append(current_url)
            time.sleep(1)
            driver.back()
            time.sleep(1)
        driver.quit()
        for url in url_list:
            print (url)
            name = '%s' % url.split('/')[-1]
            if name[-1] != "/":
                Downloader.Download(name, url)
                print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('Bayer').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Betco():
        start_time = time.time()
        for num in range(1000):
            a = '%03d' % num
            try:
                url = "http://sds.betco.com/docs/default-source/sds/%s.pdf" % a 
                print(url)
                name = '%s.pdf' % a
                Downloader.Download(name, url)
                print("--- %s seconds ---" % (time.time() - start_time))
            except:
                pass
        PDF_Relocator('Betco').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def AvantorMaterials():
        start_time = time.time()
        driver = webdriver.Firefox()
        url_list = []
        driver.get('http://www.avantormaterials.com/search.aspx?searchtype=msds')
        for num in range(1000, 10000):
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="ctl00_MainContent_MSDSSearch1_UCTxtSearchBox"]').clear()
            driver.find_element_by_xpath('//*[@id="ctl00_MainContent_MSDSSearch1_UCTxtSearchBox"]').send_keys("%s" % num)
            driver.find_element_by_xpath('//*[@id="ctl00_MainContent_MSDSSearch1_UCTxtSearchBox"]').send_keys(Keys.RETURN)
            time.sleep(2)
            number = len(driver.find_elements_by_xpath("//a[@href and @target='_\"new\"']"))
            print (number)
            for i in range(len(driver.find_elements_by_xpath("//a[@href and @target='_\"new\"']"))):
                driver.find_element_by_xpath("(//a[@href and @target='_\"new\"'])[%d]" % (i+1)).click()
                window_after = driver.window_handles[1]
                driver.switch_to_window(window_after)
                current_url = driver.current_url
                if current_url not in url_list:
                    url_list.append(current_url)
                print(current_url)
                print(("--- %s seconds ---" % (time.time() - start_time)), "---%s---%s/%s---" % (num, (i+1), number))
                driver.close()
                window_original = driver.window_handles[0]
                driver.switch_to_window(window_original)
            if num % 20 == 0 and num != 0:
                driver.quit()
                time.sleep(3)
                driver = webdriver.Firefox()
                driver.get('http://www.avantormaterials.com/search.aspx?searchtype=msds')
        time.sleep(1)
        driver.quit()
        for url in url_list:
            print (url)
            try:
                name = '%s' % url.split('/')[-1]
                Downloader.Download(name, url)
            except:
                print("Could not download: %s" % url)
        PDF_Relocator('AvantorMaterials').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Astrazeneca():
        start_time = time.time()
        url_list = []
        connection = urlopen('http://www.astrazeneca.com.au/healthcare-professionals/material-safety-data-sheets')
        domain = html.fromstring(connection.read())
        for url in domain.xpath('//a/@href'):
            if 'pdf' in url:
                url_list.append('http://www.astrazeneca.com.au/'+ url)
        num = 0
        for url in url_list:
            print (url)
            num += 1
            name = "%02d.pdf" % num
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time)) 
        PDF_Relocator('Astrazeneca').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def ArdexWax():
        start_time = time.time()
        connection = urlopen('http://www.ardexwax.com/MSDS_Links.html')
        domain = html.fromstring(connection.read())
        url_list = []
        for url in domain.xpath('//a/@href'):
            if 'pdf' in url:
                url_list.append('http://www.ardexwax.com/' + url)
        for url in url_list:
            print (url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('ArdexWax').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Aplicare():
        start_time = time.time()
        url_list = []
        connection = urlopen('https://www.cloroxprofessional.com/sds/')
        domain = html.fromstring(connection.read())
        for url in domain.xpath('//a/@href'):
            if 'pdf' in url and url not in url_list:
                url_list.append(url)
        for url in url_list:
            print (url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('Aplicare').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Amresco():
        start_time = time.time()
        driver = webdriver.Firefox()
        url_list = []
        site_url_list = []
        driver.get('http://www.amresco-inc.com/home/products/products-home.cmsx')
        Application_list = ['DNA', 'RNA', 'Protein', 'Cell Culture', 'Histology', 'Biochemicals']
        for application in Application_list:
            print (application)
            driver.find_element_by_link_text('%s' % application).click()
            current_url = driver.current_url
            connection = urlopen('%s' % current_url)
            domain = html.fromstring(connection.read())
            for site_url in domain.xpath('//a/@href'):
                if "products/products-by-application/%s" % application.lower() in site_url and site_url not in site_url_list:
                    site_url_list.append('http://www.amresco-inc.com' + site_url)
        for url in site_url_list:
            driver.get(url)
            for num in range(15):
                try:
                    driver.find_element_by_xpath('//*[@id="department_product_display"]/div[%s]/h2/a' % (num+1)).click()
                    driver.find_element_by_xpath('//*[@id="tab_header"]/ul/li[2]/a').click()
                    driver.find_element_by_link_text('Safety Data Sheet').click()
                    window_after = driver.window_handles[1]
                    driver.switch_to_window(window_after)
                    current_url = driver.current_url
                    if current_url not in url_list:
                        url_list.append(current_url)
                    print("--- %s seconds ---" % (time.time() - start_time)), len(url_list)
                    driver.close()
                    window_original = driver.window_handles[0]
                    driver.switch_to_window(window_original)
                    driver.back()
                except:
                    print("No more PDFs. ---%s---" % (num+1))
                    print("--- %s seconds ---" % (time.time() - start_time))
        driver.quit()
        for url in url_list:
            print (url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))    
        PDF_Relocator('Amresco').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Zep():
        start_time = time.time()
        url_list = []
        connection = urlopen('http://www.zepcommercial.com/sds')
        domain = html.fromstring(connection.read())
        for url in domain.xpath('//a/@href'):
            if 'sds' in url and 'https' in url:
                url_list.append(url)
        for url in url_list:
            print (url)
            name = url.split('C013=')[-1].split("&")[0] + '.pdf'
            Downloader.Download(name, url) 
            print("--- %s seconds ---" % (time.time() - start_time))    
        PDF_Relocator('Zep').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Xerox():
        start_time = time.time()
        driver = webdriver.Firefox()
        url_list = []
        page_list = []
        count = 0
        driver.get('http://www.xerox.com/about-xerox/environment/search/enus.html')
        for i in range(100):
            try:
                driver.find_element_by_xpath('//*[@id="m1"]/option[%s]' % (i+1)).click()
                for j in range(100):
                    try:
                        print("--- %s seconds ---" % (time.time() - start_time))    
                        time.sleep(2)
                        driver.find_element_by_xpath('//*[@id="m2"]/option[%s]' % (j+1)).click()
                        current_url = driver.current_url
                        page_list.append(current_url)
                        driver.back()
                        count += 1
                        time.sleep(3)
                        driver.find_element_by_xpath('//*[@id="m1"]/option[%s]' % (i+1)).click()
                    except:
                        break
                    if count % 50 == 0 and count != 0:
                        driver.quit()
                        time.sleep(2)
                        driver = webdriver.Firefox()
                        driver.get('http://www.xerox.com/about-xerox/environment/search/enus.html')
                        driver.find_element_by_xpath('//*[@id="m1"]/option[%s]' % (i+1)).click()
            except:
                break
        driver.quit()
        for page in page_list:
            connection = urlopen('%s' % page)
            domain = html.fromstring(connection.read())
            for url in domain.xpath('//a/@href'):
                if 'download/ehs/msds' in url:
                    url_list.append(url)
            print("--- %s seconds ---" % (time.time() - start_time))
        for url in set(url_list):
            print (url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('Xerox').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def WilkoPaint():
        start_time = time.time()
        connection = urlopen('http://wilkopaintinc.com/downloads/')
        domain = html.fromstring(connection.read())
        url_list = []
        for url in domain.xpath('//a/@href'):
            if "SDS" in url and '.pdf' in url:
                url_list.append('http://wilkopaintinc.com/' + url)
        for url in url_list:
            print (url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('WilkoPaint').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def WD40():
        start_time = time.time()
        url_list = []
        connection = urlopen('http://www.wd40company.com/partners/msds/usa/')
        domain = html.fromstring(connection.read())
        for url in domain.xpath('//a/@href'):
            if 'sds' in url.lower() and 'pdf' in url.lower():
                url_list.append('http://www.wd40company.com' + url)
        for url in url_list:
            print (url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('WD40').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def VWR():
        start_time = time.time()
        driver = webdriver.Firefox()
        url_list = []
        driver.get('https://us.vwr.com/store/')
        driver.find_element_by_xpath('//*[@id="keyword"]').click()
        driver.find_element_by_link_text('SDS').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="maincontent"]/div[4]/form/table/tbody/tr[3]/td[2]/input[1]').clear()
        driver.find_element_by_xpath('//*[@id="maincontent"]/div[4]/form/table/tbody/tr[3]/td[2]/input[1]').send_keys("%")
        driver.find_element_by_xpath('//*[@id="maincontent"]/div[4]/form/table/tbody/tr[4]/td[3]/input[3]').click()
        time.sleep(3)
        page = 1
        driver.find_element_by_link_text('64').click()
        for i in range(7):
            time.sleep(5)
            for sds in driver.find_elements_by_link_text('View SDS'):
                try:
                    sds.click()
                    window_after = driver.window_handles[1]
                    driver.switch_to_window(window_after)
                    current_url = driver.current_url
                    if current_url not in url_list:
                        url_list.append(current_url)
                    print(current_url)
                    driver.close()
                    window_original = driver.window_handles[0]
                    driver.switch_to_window(window_original)
                except:
                    print("Could not click on this")
            time.sleep(1)
            try:
                driver.find_element_by_link_text('%d' % (page+1)).send_keys("\n")
            except:
                pass
            page += 1
            time.sleep(2.5)
        driver.quit()
        for url in url_list:
            print(url)
            name = "%s.pdf" % url.split('/')[-2]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('VWR').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def VolvoTrucks():
        start_time = time.time()
        driver = webdriver.Firefox()
        url_list = []
        driver.get('http://www.volvotrucks.us/parts-and-services/parts/material-safety-data-sheets/')
        print(len(driver.find_elements_by_link_text('English')))
        for sds in range(len(driver.find_elements_by_link_text('English'))):
            try:
                driver.find_elements_by_link_text('English')[sds].click()
                current_url = driver.current_url
                url_list.append(current_url)
                print(current_url)
                url_list.append(current_url)
                print("--- %s seconds ---" % (time.time() - start_time))
                driver.back()
                time.sleep(3)
            except:
                pass
        driver.quit()
        num = 0
        for url in url_list:
            print(url)
            num += 1
            name = "%02d.pdf" % num
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))    
        PDF_Relocator('VolvoTrucks').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Ventana():
        start_time = time.time()
        url_list = []
        driver = webdriver.Firefox()
        driver.get("http://www.ventana.com/msds/us")
        for i in range(len(driver.find_elements_by_xpath("//div[@id='yw0']//ul//a"))):
            if i % 230 == 0 and i != 0:
                driver.close()
                print("Restarting Firefox -- Memory Overload.")
                time.sleep(3)
                driver = webdriver.Firefox()
                driver.get("http://www.ventana.com/msds/us")        
            driver.find_element_by_xpath("(//div[@id='yw0']//ul//a)[%d]" % (i+1)).click()
            window_after = driver.window_handles[1]
            driver.switch_to_window(window_after)
            print("--- %s seconds ---" % (time.time() - start_time))
            current_url = driver.current_url
            url_list.append(current_url)
            driver.close()
            window_original = driver.window_handles[0]
            driver.switch_to_window(window_original)
        driver.quit()
        for url in url_list:
            print(url)
            name = "%s" % url.split("/")[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('Ventana').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def TCI():
        start_time = time.time()
        def SetUp():
            download_to = PDF_Location + '\\TCI'
            Actions.Ensure_Dir(download_to)
            global driver
            profile = webdriver.FirefoxProfile()
            profile.set_preference("browser.download.folderList", 2)
            profile.set_preference("browser.download.manager.showWhenStarting", False)
            profile.set_preference("browser.download.dir", download_to)
            profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
            profile.set_preference("browser.helperApps.alwaysAsk.force", False)     
            profile.set_preference("pdfjs.disabled", True)
            driver = webdriver.Firefox(firefox_profile=profile)
        count = 0
        page_list = []
        alphabet = "ABCDEFGHIJKLMNOPQRSTUPQXYZ"
        for letter in list(alphabet):
            for num in range(10000):
                url = 'http://www.tcichemicals.com/eshop/en/us/commodity/%s%04d/' % (letter, num)
                print (url)
                print (CheckUrl.checkUrl(url))
                print("--- %s seconds ---" % (time.time() - start_time))
                print("-------------------------")
                if CheckUrl.checkUrl(url) == True:
                    page_list.append(url)
        SetUp()
        num = 0
        for page in page_list:
            driver.get(page)
            time.sleep(1)
            try:
                print(page.split('/')[-1])
                driver.find_element_by_xpath('//*[@id="side"]/div/div/div[1]/div/ul/li/a/span').click()
            except:
                print('Could not click on page: %s' % page.split('/')[-2])
            print("--- %s seconds ---" % (time.time() - start_time))
            time.sleep(1)
            num += 1
            if num % 120 == 0:
                driver.quit()
                time.sleep(1)
                SetUp()
        driver.quit()
        PDF_Relocator('TCI').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))        


    def TaylorTechnologies():
        start_time = time.time()
        url_list = []
        driver = webdriver.Firefox()
        driver.get("http://www.taylortechnologies.com/products_msds_results.asp?Type=ReagentSearch&Number=%")
        for i in range(len(driver.find_elements_by_xpath("//tr[@class='tableline']//a"))):
            driver.find_element_by_xpath("(//tr[@class='tableline']//a)[%d]" % (i+1)).click()
            window_after = driver.window_handles[1]
            driver.switch_to_window(window_after)
            print("--- %s seconds ---" % (time.time() - start_time))
            current_url = driver.current_url
            url_list.append(current_url)
            driver.close()
            window_original = driver.window_handles[0]
            driver.switch_to_window(window_original)
        driver.quit()
        for url in url_list:
            print(url)
            name = '%s' % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('TaylorTechnologies').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Steris():
        start_time = time.time()
        driver = webdriver.Firefox()
        url_list = []
        driver.get('https://www.steris.com/healthcare/support/msds/search.cfm')
        time.sleep(1)
        try:
            driver.find_element_by_xpath('//*[@id="fsrOverlay"]/div/div/div/a').click()
            driver.find_element_by_id("btnSubmit").click()
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="fsrOverlay"]/div/div/div/a').click()
        except:
            pass
        time.sleep(2)
        total = driver.find_elements_by_xpath("//table[@id='document-list']//a")
        au = driver.find_elements_by_partial_link_text('AU')
        ca = driver.find_elements_by_partial_link_text('CA')
        nl = driver.find_elements_by_partial_link_text('NL')
        fr = driver.find_elements_by_partial_link_text('FR')
        it = driver.find_elements_by_partial_link_text('IT')
        pt = driver.find_elements_by_partial_link_text('PT')
        es = driver.find_elements_by_partial_link_text('ES')
        ch = driver.find_elements_by_partial_link_text('CH')
        uk = driver.find_elements_by_partial_link_text('UK')
        de = driver.find_elements_by_partial_link_text('DE')
        lang = au + ca + nl + fr + it + pt + es + ch + uk + de
        for link in total:
            if link in lang:
                total.remove(link)
        language_list = ['CANADIAN', 'SPANISH', 'AUSTRALIAN', 'CHINESES', 'TURKISH', 'FINNISH', 'SWEDISH', 'RUSSIAN', 'POLISH', 'LITHUANIAN', 'DANISH', 'CZECH', 'HUNGARIAN', 'FRENCH', 'ITALIAN', 'PORTUGUESES', 'SWISS', 'KINGDOM', 'GERMAN']
        for sds in total:
            sds.click()
            window_after = driver.window_handles[1]
            driver.switch_to_window(window_after)
            current_url = driver.current_url
            for language in language_list:
                if language.lower() not in current_url.lower():
                    if current_url not in url_list:
                        url_list.append(current_url)
            print("--- %s seconds ---" % (time.time() - start_time))
            driver.close()
            window_original = driver.window_handles[0]
            driver.switch_to_window(window_original)
        driver.quit()
        num = 0
        for url in url_list:
            print(url)
            num += 1
            name = "%04d.pdf" % num
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))    
        PDF_Relocator('Steris').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def SpartanChemical():
        start_time = time.time()
        url_list = []
        for page in range(41):
            connection = urlopen('https://www.spartanchemical.com/search/?page=%d&tab=SDS' % (page+1))
            domain = html.fromstring(connection.read())
            for url in domain.xpath('//a/@href'):
                if "AGHS/EN" in url:
                    url_list.append(url)
        for url in url_list:
            print(url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('SpartanChemical').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def Spectrum():
        start_time = time.time()
        driver = webdriver.Firefox()
        driver.get("https://www.spectrumchemical.com/OA_HTML/index.jsp?section=10565&language=US&minisite=10020&respid=22372")
        url_list = []
        for letter in ["a", "e", "i", "o", "u"]: #iterate over vowels
            print(letter)
            driver.find_element_by_id("sli_search_1").clear()
            driver.find_element_by_id("sli_search_1").send_keys(letter)
            driver.find_element_by_id('search-btn').click()
            num = 0
            while len(driver.find_elements_by_link_text("Next")) == 1:
                time.sleep(2)
                for j in range(len(driver.find_elements_by_link_text("Pricing & More Info"))):
                    time.sleep(1)
                    driver.find_element_by_id("sli_search_1").clear()
                    driver.find_element_by_id("sli_search_1").send_keys(letter)
                    driver.find_element_by_id("sli_search_1").send_keys(Keys.RETURN)
                    for page in range(num):
                        driver.find_element_by_link_text("%s" % (num+1)).send_keys('\n')
                    time.sleep(4)
                    driver.find_elements_by_link_text("Pricing & More Info")[j].click()
                    try:
                        driver.find_element_by_xpath('//*[@id="container"]/div[4]/div/div[10]/div[1]/div/table/tbody/tr[2]/td/a').click()
                        try:
                            for msds in range(len(driver.find_elements_by_link_text("MSDS"))):
                                driver.find_elements_by_link_text("MSDS")[msds].click()
                                window_after = driver.window_handles[1]
                                driver.switch_to_window(window_after)
                                current_url = driver.current_url
                                if current_url not in url_list:
                                    url_list.append(current_url)
                                    print("--- %s seconds ---" % (time.time() - start_time))
                                driver.close()
                                window_original = driver.window_handles[0]
                                driver.switch_to_window(window_original)
                        except:
                            pass
                    except:
                        pass
                    if (j+1) == 16:
                        num += 1
                driver.find_element_by_id("sli_search_1").clear()
                driver.find_element_by_id("sli_search_1").send_keys(letter)
                driver.find_element_by_id('search-btn').click()
        driver.quit()
        for url in url_list:
            print(url)
            name = "%s" % url.split('/')[-1]
            Downloader.Download(name, url)
            print("--- %s seconds ---" % (time.time() - start_time))
        PDF_Relocator('Spectrum').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


    def PGProducts():
        def SetUp():
            download_to = PDF_Location + '\\PGProducts'
            mime_types = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document, application/pdf, binary/pdf, application/octet-stream, binary/octet-stream'
            Actions.Ensure_Dir(download_to)
            global driver
            profile = webdriver.FirefoxProfile()
            profile.set_preference("browser.download.folderList", 2)
            profile.set_preference("browser.download.manager.showWhenStarting", False)
            profile.set_preference("browser.download.dir", download_to)
            profile.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
            profile.set_preference("browser.helperApps.alwaysAsk.force", False)     
            profile.set_preference("pdfjs.disabled", True)
            driver = webdriver.Firefox(firefox_profile=profile)
        start_time = time.time()
        SetUp()
        driver.get('http://pgpro.com/')
        driver.find_element_by_link_text('SDS').click()
        time.sleep(4)
        home_url = driver.current_url
        for page in range(1, 24):
            driver.find_element_by_xpath('//*[@id="select2-category-container"]').click()
            time.sleep(1)
            for i in range(page):
                driver.find_element_by_xpath('//*[@id="pg_main"]/div[1]/div[5]/div/div/form/div/div[2]/ul/li/span/span[1]/span').send_keys(Keys.ARROW_DOWN)
            driver.find_element_by_xpath('//*[@id="pg_main"]/div[1]/div[5]/div/div/form/div/div[2]/ul/li/span/span[1]/span').send_keys(Keys.RETURN)
            driver.find_element_by_xpath('//*[@id="pg_main"]/div[1]/div[5]/div/div/form/p/button').click()
            for elt in range(len(driver.find_elements_by_class_name('modal'))/2):
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="pg_main"]/div[1]/div[5]/div[2]/div/table/tbody/tr[%s]/td[2]/a' % (elt+1)).click()
                time.sleep(2)
                for sds in driver.find_elements_by_link_text('english'):
                    try:
                        sds.click()
                    except:
                        try:
                            time.sleep(3)
                            sds.click()
                        except:
                            pass
                print("--- %s seconds ---" % (time.time() - start_time))
                time.sleep(1)
                driver.refresh()
            if page % 8 == 0 and page != 0:
                driver.quit()
                time.sleep(3)
                SetUp()
            driver.get(home)
            time.sleep(2)
        driver.quit()
        PDF_Relocator('PGProducts').Relocator()
        print("**Finished** -- %s seconds --" % (time.time() - start_time))


###################################################################################################################################
#   Classes and functions for the Scrapers
###################################################################################################################################


class PDF_Relocator(object):
    ''' 
    Class for all location/relocation based functions
    '''
    def __init__(self, company):
        self.company = company

    def Relocator(self):
        
        company = "Test"
        DEST_DIR = '%s\\%s' % (PDF_Location, self.company)
        
        Actions.Ensure_Dir(DEST_DIR)

        self.Dedup()        
        for doc_id in os.listdir(SOURCE_DIR):
            if doc_id.lower().endswith('.pdf'):
                try:
                    shutil.move(os.path.join(SOURCE_DIR, doc_id), os.path.join(DEST_DIR, doc_id))
                except:
                    print("%s already exists" % doc_id)
                    os.remove(doc_id)
            if doc_id.lower().endswith('.docx'):
                shutil.move(os.path.join(SOURCE_DIR, doc_id), os.path.join(DEST_DIR, doc_id))
            if doc_id.lower().endswith('.asp'):
                os.remove(doc_id)
            if doc_id.lower().endswith('.pyc'):
                os.remove(doc_id)
            if doc_id.lower().endswith('.html'):
                os.remove(doc_id)
        
    
    def Dedup(self):

        company = "Test"
        special_company = ['PG']
        if self.company not in special_company:
            for doc_id in os.listdir(SOURCE_DIR):
                for num in range(10):
                    if doc_id.split('.')[0][-3:] == ('(%s)' % num):
                        os.remove(doc_id)
                        print(doc_id)
    
# Use next line for testing
#PDF_Relocator("Test").Relocator()  #Relocator("Your Company")


class CheckUrl():
    '''
    Verifies that the url is valid with readable content
    '''

    def checkUrl(url):
        p = urlparse(url)
        conn = HTTPConnection(p.netloc)
        conn.request('HEAD', p.path)
        resp = conn.getresponse()
        return resp.status < 400    

class Downloader():
    '''
    Downlaoder that works for HTTPS and HTTP.
    When given the PDFs url, the Downloader will download the file
    in the same directory as the Downloader.
    '''

    def Download(name, url):
        r = requests.get(url, auth=('usrname', 'password'), verify=False,stream=True)
        r.raw.decode_content = True
        with open(name, 'wb') as f:
            shutil.copyfileobj(r.raw, f) 

#Scrapers.Test()

###################################################################################################################################
#   Classes and functions for the GUI
###################################################################################################################################



class Relocators():

    def CopyFile(src, dst):
        # Copy src to dst. (cp src dst)
        shutil.copy(src, dst)

    def MoveFile(src, dst):
        # Copy files, but preserve metadata (cp -p src dst)
        shutil.copy2(src, dst)

    def CopyDir(src, dst):
        # Copy directory tree (cp -R src dst)
        shutil.copytree(src, dst)

    def MoveDir(src, dst):
        # Move src to dst (mv src dst)
        shutil.move(src, dst)

class Actions():

    def add_item(ALL = False):
        """
        add the text in the Entry widget to the end of the listbox
        """
        global Queue
        try:
            if enter1.get() not in Queue:
                Queue.append(enter1.get())
                listbox2.insert(END, enter1.get())
            else:
                print("%s is already in Queue" % enter1.get())
        except:
            pass


    def delete_item():
        """
        delete a selected line from the listbox
        """
        global Queue
        try:
            index = listbox2.curselection()[0]
            listbox2.delete(index)
            del Queue[index]
        except:
            pass
       

    def get_list1(event):
        """
        function to read listbox1 selection
        and put the result in an entry widget
        """
        # get selected line index
        index = listbox1.curselection()[0]
        # get the line's text
        seltext = listbox1.get(index)
        # delete previous text in enter1
        enter1.delete(0, 50)
        # now display the selected text
        enter1.insert(0, seltext)
     
    def get_list2(event):
        """
        function to read listbox2 selection
        and put the result in an entry widget
        """
        try:
            # get selected line index
            index2 = listbox2.curselection()[0]
            # get the line's text
            seltext2 = listbox2.get(index2)
            # delete previous text in enter1
            enter2.delete(0, 50)
            # now display the selected text
            enter2.insert(0, seltext2)
        except:
            pass

    def Quit():
        global root
        root.quit()


    def Queue_All():
        """
        Function that adds every company to the queue
        """
        global Queue
        for company in Company_list:
            if company not in Queue:
                Queue.append(company)
                listbox2.insert(END, company)


    def Empty_Queue():
        """
        Functions that removes overy company in queue
        """
        global Queue
        for company in Company_list:
            try:
                del Queue[0]
                listbox2.delete(0)
            except:
                pass


    def Ensure_Dir(f):
        d = os.path.dirname(f)
        if not os.path.exists(d):
            os.makedirs(d)

    def Check_Location():
        if enter3.get() != 'Default':
            print('Downloading to %s' % enter3.get())
            Actions.Ensure_Dir(enter3.get())
            Fetch.Fetch_Files()
        else:
            Actions.Ensure_Dir("C:\\Fetch Downloads")
            Fetch.Fetch_Files()


    def Call_Both():
        Scrape.Scrape_Files(Empty=False)
        Fetch.Fetch_Files(Empty=True)

class Fetch():

    def Fetch_Files(Empty=True):
        """
        Function to iniate the scraping command
        """
        global Queue
        print("Fetching %s companie(s)." % len(Queue))
        today = datetime.date.today()
        date = today.strftime("%m-%d-%Y")
        
        for company in sorted(set(Queue)):
            print(company)
            name = company + " " + date
            try:
                Relocators.CopyDir('%s\\%s' % (PDF_Location, company), '%s' % name)
                if enter3.get() != 'Default':
                    Relocators.MoveDir('%s\\%s' % (SOURCE_DIR, name), '%s\\%s' % (enter3.get(), name))
                else:
                    Relocators.MoveDir('%s\\%s' % (SOURCE_DIR, name), 'C:\\Fetch Downloads\\%s' %  name)
                listbox2.delete(0)
            except:
                print('We do not have a file directory made yet.  Scrape to make one.')
        if Empty == True:
            Actions.Empty_Queue()

        print("Fetch Completed")
        



class Scrape():
    def Scrape_Files(Empty=True):
        """
        Function to iniate the scraping command
        """
        global Queue
        print("Scraping %s companie(s)." % len(Queue))
        for company in sorted(set(Queue)):
           try:
              print(company)
              func = getattr(Scrapers, company)
              func()
              PDF_Relocator(company).Relocator()
           except:
              pass
        if Empty == True:
            Actions.Empty_Queue()
        print("Scrape Completed")

###################################################################################################################################
#   GUI Layout Modules
###################################################################################################################################
root = Tk()
root.title("Fetch2.0")
root.minsize(340,490);
root.maxsize(340,600);
#  ***** Main Menu *****
menu = Menu(root)
root.config(menu=menu)
subMenu = Menu(menu)
menu.add_command(label="Exit", command=Actions.Quit)
menu.add_command(label="Queue All", command=Actions.Queue_All)
menu.add_command(label="Empty Queue", command=Actions.Empty_Queue)


# create the sample data file
# list is based on number of functions in Scraper Class
Company_list = ([x for x, y in Scrapers.__dict__.items() if type(y) == FunctionType])
Company_list = sorted(Company_list)

# create the listbox (note that size is in characters)
listbox1 = Listbox(root, width=50, height=10)
listbox1.grid(row=0, column=0)
 
# create a vertical scrollbar to the right of the listbox
yscroll = Scrollbar(command=listbox1.yview, orient=VERTICAL)
yscroll.grid(row=0, column=1, sticky=N+S)
listbox1.configure(yscrollcommand=yscroll.set)

# use entry widget to display/edit selection
enter1 = Entry(root, width=50)
enter1.grid(row=1, column=0)

enter2 = Entry(root, width=50)
enter2.grid(row=4, column=0)

# button to add a line to the listbox
addButt = Button(root, text='Add company to queue bellow', command=Actions.add_item)
addButt.grid(row=2, column=0, sticky=E)
# button to delete a line from listbox
delButt = Button(root, text='     Delete selected line     ', command=Actions.delete_item)
delButt.grid(row=5, column=0, sticky=E)
# load the listbox with data
for item in Company_list:
    listbox1.insert(END, item)
 
# left mouse click on a list item to display selection
listbox1.bind('<ButtonRelease-1>', Actions.get_list1)

listbox2 = Listbox(root, width=50, height=10)
listbox2.grid(row=3, column=0)

listbox2.bind('<ButtonRelease-1>', Actions.get_list2)

#   ***** Fetch and Scrape Buttoms *****

status3 = Label(root, text="Fetch Will Download Files 'C:\\Fetch Documents' By Default", bd=1, anchor=W)
status3.grid(row=8, column=0)

enter3 = Entry(root, width=50)
enter3.insert(0, r'Default')
enter3.grid(row=9, column=0, sticky=W)

f1 = Frame(root)

fetchButt = Button(f1, text='Fetch Only', command=Actions.Check_Location)
#fetchButt.grid(row=9, column=0, sticky=N)
fetchButt.pack(side=RIGHT)

ScrapeButt = Button(f1, text='Scrape Only', command=Scrape.Scrape_Files)
#ScrapeButt.grid(row=8, column=0, sticky=N) 
ScrapeButt.pack(side=RIGHT)

f1.grid(row=10, column=0, sticky=E)

bothButt = Button(root, text='  Scrape And Fetch Files   ', command=Actions.Call_Both)
bothButt.grid(row=11, column=0, sticky=E)

Queue = []

#################################################
#Saved rows to add more buttons.
#When adding buttons, re-adjust window size.
#################################################

# label to inform user that everything is working
f2 = Frame(root)

status0 = Label(f2, text="  ", bd=1, anchor=W)
status0.pack()

status1 = Label(f2, text="Module will be 'NOT RESPONSIVE' while performing task.")
status1.pack()

status2 = Label(f2, text="WARNING: Fetching may take a couple minutes.", bd=1, anchor=W)
status2.pack()

status3 = Label(f2, text="WARNING: Scraping will average 45 minutes PER company.", bd=1, anchor=W)
status3.pack()

# row=100 so always at the bottom of the GUI
f2.grid(row=100, column=0, sticky=N)


root.mainloop()
