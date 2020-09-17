import scrapy
import logging,re,traceback
import re
import requests
from lxml import html

from University.items import UniversityItem

class AucklanduniversitySpider(scrapy.Spider):
    name='AucklandUniversity'
    allowed_domains=['www.auckland.ac.nz/']
    start_urls=['https://www.auckland.ac.nz/en/study/study-options/find-a-study-option.html?programmeType=bachelors-honours,doctorates,masters,postgraduate-diploma-and-certificates&programmeFaculty=auckland-bioengineering-institute,arts,business,creative-arts-and-industries,education-and-social-work,engineering,law,medical-and-health-sciences,science,liggins-institute&_charset_=UTF-8#list']

    def parse(self, response):
        study_options=response.xpath('//main[@id="main"]/div/div[@class="container"]/div[@class="row"]/div[@class="col-xs-12"]/div[@class="browse-area"]/ul[@class="browse-area__list"]/li[@class="browse-area__list-items"]/a/@href').extract()
        # 
        logging.info('Auckland University :Scrapping started :Url {}'.format(response.url))
        # print(study_options)
        for base_url in study_options:
            yield scrapy.Request(base_url,callback=self.parse_program_url)

    def parse_program_url(self,response):
        all_programs=response.xpath('//*[@id="main"]/div[2]/div[3]/div/div[1]/div/div/ul/li/a/@href').extract()
        logging.info('Auckland University :Scrapping staretd finding all programs :Url {}'.format(response.url))
        print(len(all_programs))
        for course in all_programs:
            yield scrapy.Request(course,callback=self.parse_course)

    def parse_course(self,response):
        logging.info('Auckland University :Scrapping started course page :Url {}'.format(response.url))
        try:
            item=UniversityItem()
            # 1 course name
            course_name=response.xpath('//main[@id="main"]/div[@class="embed-section"]/div/div[@class="banner banner--detail"]/div[@class="banner__content"]/h1[@class="banner__heading"]/text()').extract_first()
            item["course_name"]=course_name
            # print(course_name)

            # 2 course category
            course_category=response.xpath('//main[@id="main"]/div[@class="embed-section"]/div/div[@class="banner banner--detail"]/div[@class="banner__content"]/p[@class="banner__faculty"]/text()').extract_first()
            item["course_category"]=course_category
            # print(course_category)

            # 4 course website
            course_webiste=response.url
            item["course_webiste"]=course_webiste
            # print(course_webiste)
            
            # 5 and 6 duration and duration term
            duration_words=response.xpath('//*[@id="main"]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/dl[1]/dd[1]/text()').extract_first()
            if duration_words:
                output=duration_words.split(':')
                use_regex=output[1]
                # print(use_regex)
                year=re.findall(r'\d+',use_regex)
                if year is not None:
                    item["duration"]=year
                    # print(year[0])
                else:
                    item["duration"]=""
                term=re.sub('[^A-Z a-z\n]+','',use_regex)
                if term is not None:
                    item["duration_term"]=" ".join(term.split())
                    # print(term)
                    # print(term)
                else:
                    item["duration_term"]=""       
            # print(duration_words)
            # 7 study mode not available

            # 9 degree level
            degree_level=response.xpath('//*[@id="main"]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/dl[5]/dd[1]/text()').extract_first()
            if degree_level is not None:
                item["degree_level"]=degree_level
            else:
                item["degree_level"]=degree_level
            # print(degree_level)

            # 10 and 11 intake day and month
            intake_day=[]
            intake_month=[]
            intake1=response.xpath('//*[@id="main"]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/dl[2]/dd/text()').extract_first()
            days=[i for i in range(1,31)]
            months=['january','february','march','april','may','jun','july','august','september','october','november','december']
            if intake1:
                output=re.findall(r'\d+',intake1)
                day=[]
                for value in output:
                    number=(int(value))
                    day.append(number)
                for j in days:
                    for k in day:
                        if k==j:
                            intake_day.append(k)
                            break
                find_month=re.sub('[^A-Z a-z\n]+','',intake1)
                month=" ".join(find_month.split())
                def _string_to_list(month):
                    list_to_find_month=list(month.split(" "))
                    return list_to_find_month
                list_to_find_month=_string_to_list(month)
                lower_list_items=[]
                for value in list_to_find_month:
                    string=value.lower()
                    lower_list_items.append(string)
                for j in months:
                    for k in lower_list_items:
                        if k == j:
                            intake_month.append(k)
                            break
            
            # print(intake_day)
            # print(intake_month)
            intake2=response.xpath('//*[@id="main"]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/dl[2]/dd[2]/text()').extract_first()
            if intake2:
                output=re.findall(r'\d+',intake2)
                day=[]
                for value in output:
                    number=(int(value))
                    day.append(number)
                for j in days:
                    for k in day:
                        if k==j:
                            intake_day.append(k)
                            break
                find_month=re.sub('[^A-Z a-z\n]+','',intake2)
                month=" ".join(find_month.split())
                def _string_to_list(month):
                    list_to_find_month=list(month.split(" "))
                    return list_to_find_month
                list_to_find_month=_string_to_list(month)
                lower_list_items=[]
                for value in list_to_find_month:
                    string=value.lower()
                    lower_list_items.append(string)
                for j in months:
                    for k in lower_list_items:
                        if k == j:
                            intake_month.append(k)
                            break
            converted_intake_day=[str(element) for element in intake_day]
            joined_intake_day=",".join(converted_intake_day)
            item["intake_day"]=joined_intake_day
            item["intake_month"]=intake_month
            # print(intake_day)
            # print(intake_month)

            # 12 and 13 apply_day and apply month
            apply_day=[]
            apply_month=[]
            apply1=response.xpath('//*[@id="section5"]/div[1]/div[2]/div[1]/div[1]/div[1]/dl/dd/text()').extract_first()
            if apply1:
                output=re.findall(r'\d+',apply1)
                day=[]
                for value in output:
                    number=(int(value))
                    day.append(number)
                for j in days:
                    for k in day:
                        if k==j:
                            apply_day.append(k)
                            break
                find_month=re.sub('[^A-Z a-z\n]+','',apply1)
                month=" ".join(find_month.split())
                def _string_to_list(month):
                    list_to_find_month=list(month.split(" "))
                    return list_to_find_month
                list_to_find_month=_string_to_list(month)
                lower_list_items=[]
                for value in list_to_find_month:
                    string=value.lower()
                    lower_list_items.append(string)
                for j in months:
                    for k in lower_list_items:
                        if k == j:
                            apply_month.append(k)
                            break
            apply2=response.xpath('//*[@id="section5"]/div[1]/div[2]/div/div/div[2]/dl/dd/text()').extract_first()
            if apply2:
                output=re.findall(r'\d+',apply2)
                day=[]
                for value in output:
                    number=(int(value))
                    day.append(number)
                for j in days:
                    for k in day:
                        if k==j:
                            apply_day.append(k)
                            break
                find_month=re.sub('[^A-Z a-z\n]+','',apply2)
                month=" ".join(find_month.split())
                def _string_to_list(month):
                    list_to_find_month=list(month.split(" "))
                    return list_to_find_month
                list_to_find_month=_string_to_list(month)
                lower_list_items=[]
                for value in list_to_find_month:
                    string=value.lower()
                    lower_list_items.append(string)
                for j in months:
                    for k in lower_list_items:
                        if k == j:
                            apply_month.append(k)
                            break
            item["apply_month"]=apply_month
            converted_day=[str(element) for element in apply_day]
            joined_day=",".join(converted_day)
            item["apply_day"]=joined_day
            
            # 14 city
            city=response.xpath('//*[@id="main"]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/dl[3]/dd[1]/text()').extract_first()
            if city:
                find_city=re.sub('[^A-Z a-z\n]+','',city)
                if find_city:
                    item["city"]=find_city
                else:
                    item["city"]=""
            # print(city)

            # 16  domestic fee 
            domestic=response.xpath('//*[@id="section4"]/div[3]/div[1]/div[1]/dl/dd/text()').extract_first()
            if domestic:
                m=re.findall(r'\d+\,\d\d\d\.\d+',domestic)
                if not m:
                    n=re.findall(r'\d+\,\d\d\d',domestic)
                    if len(n)==2 or len(n)==1:
                        item["domestic_fee"]=n[0]
                        # print(n[0])
                else:
                    if len(m)==2 or len(m)==1:
                        item["domestic_fee"]=m[0]
                        # print(m[0])
            international=response.xpath('//*[@id="section4"]/div[3]/div[1]/div[2]/dl/dd/text()').extract_first()
            # 15 domestic only
            if international is not None:
                item["domestic_only"]=False
            else:
                item["domestic_only"]=True

            # 17 international fee
            if international:
                m=re.findall(r'\d+\,\d\d\d\.\d+',international)
                if not m:
                    n=re.findall(r'\d+\,\d\d\d',international)
                    if len(n)==2 or len(n)==1:
                        item["international_fee"]=n[0]
                        # print(n[0])
                else:
                    if len(m)==2 or len(m)==1:
                        item["international_fee"]=m[0]
                        # print(m[0])
        
            # 18 fee term
            fee_term="year"
            item["fee_term"]=fee_term
            # 19 fee year
            fee_year= response.xpath('//*[@id="section4"]/div[1]/div[1]/h3/text()').extract_first()
            if fee_year:
                m=re.findall(r'\d+',fee_year)
                # print(m)
                if len(m)==1:
                    item["fee_year"]=m[0]
            # 20 currency
            currency="NZD"
            item["currency"]=currency

            # 21 study load
            # full_time
            study_load=set()
            full_time=response.xpath('//*[@id="main"]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/dl[1]/dd/text()').extract_first()
            if full_time:
                f_time=" ".join(full_time.split())
                list_time=f_time.split(":")
                study_load.add(list_time[0].lower())
                # print(study_load)
            part_time=response.xpath('//*[@id="main"]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/dl[1]/dd[2]/text()').extract_first()
            if part_time:
                p_time=" ".join(part_time.split())
                time=p_time.split(":")
                study_load.add(time[0].lower())
            # print(study_load)
            if 'full-time' and not 'part-time' in study_load:
                item["study_load"]="Full Time"
            elif 'part-time' and not 'full-time' in study_load:
                item["study_load"]="Part Time"
            elif 'full-time' and 'part-time' in study_load:
                item["study_load"]="Both"

            # english requirements
            # 22 to 36 english requirements for graduate level
            if degree_level=="Postgraduate" or degree_level=="Doctorate":
                eng_url="https://www.auckland.ac.nz/en/study/applications-and-admissions/entry-requirements/postgraduate-entry-requirements/postgraduate-english-language-requirements.html"
                eng=self._get_english_req_grad(eng_url)
                ielts=eng.get('ielts')
                # print(ielts)
                toefl=eng.get('toefl')
                # print(toefl)
                pte=eng.get('pte')
                # print(pte)

                listening=ielts.get('listening')
                reading=ielts.get('reading')
                speaking=ielts.get('speaking')
                writing=ielts.get('writing')
                overall=ielts.get('overall')
                # ielts data
                item["ielts_listening"]=listening
                item["ielts_reading"]=reading
                item["ielts_speaking"]=speaking
                item["ielts_writing"]=writing
                item["ielts_overall"]=overall
                
                # toefl data
                item["toefl_listening"]=toefl.get('listening')
                item["toefl_reading"]=toefl.get('reading')
                item["toefl_speaking"]=toefl.get('speaking')
                item["toefl_writing"]=toefl.get('writing')
                item["toefl_overall"]=toefl.get('overall')

                # pte data
                item["pte_listening"]=pte.get('listening')
                item["pte_reading"]=pte.get('reading')
                item["pte_speaking"]=pte.get('speaking')
                item["pte_writing"]=pte.get('writing')
                item["pte_overall"]=pte.get('overall')
            # english  requirement for undergraudate
            elif degree_level=="Undergraduate":
                eng_url="https://www.auckland.ac.nz/en/study/applications-and-admissions/entry-requirements/undergraduate-entry-requirements/undergraduate-english-language-requirements.html"
                eng=self._get_english_req_ungrad(eng_url)
                ielts=eng.get('ielts')
                # print(ielts)
                toefl=eng.get('toefl')
                # print(toefl)
                pte=eng.get('pte')
                # print(pte)
                listening=ielts.get('listening')
                reading=ielts.get('reading')
                speaking=ielts.get('speaking')
                writing=ielts.get('writing')
                overall=ielts.get('overall')
                # ielts data
                item["ielts_listening"]=listening
                item["ielts_reading"]=reading
                item["ielts_speaking"]=speaking
                item["ielts_writing"]=writing
                item["ielts_overall"]=overall
                
                # toefl data
                item["toefl_listening"]=toefl.get('listening')
                item["toefl_reading"]=toefl.get('reading')
                item["toefl_speaking"]=toefl.get('speaking')
                item["toefl_writing"]=toefl.get('writing')
                item["toefl_overall"]=toefl.get('overall')

                # pte data
                item["pte_listening"]=pte.get('listening')
                item["pte_reading"]=pte.get('reading')
                item["pte_speaking"]=pte.get('speaking')
                item["pte_writing"]=pte.get('writing')
                item["pte_overall"]=pte.get('overall')
            
            # 37 to 48 not availables
            
            # 49 other requirements
            other_requirements=response.xpath('//*[@id="area-postgraduate-uoa-qualification-further-programme-requirements"]/div').extract_first()
            
            if other_requirements is not None:
                item["other_requirements"]=other_requirements

            else:
                item["other_requirements"]=""
            # print(other_requirements)
            # 50 course description
            course_description=response.xpath('//*[@id="main"]/div[2]/div/div[1]/div/div[1]/div/div[2]/p/text()').extract_first()
            # print(course_description)
            if course_description is not None:
                item["course_description"]=course_description

            else:
                item["course_description"]=""

            # 51 course structure
            course_structure=response.xpath('//*[@id="section1"]/div[1]/div[2]/div/div').extract_first()

            if course_structure is not None: 
                item["course_structure"]=course_structure
            else:
                item["course_structure"]=""

            # print(course_structure)
            # 52
            career=response.xpath('//*[@id="section1"]/div[1]/div[2]/div/div').extract_first()
            if career is not None:
                item["career"]=career
            
            else:
               item["career"]=""
 
            # print(career)
            yield item
        except Exception as ex:
            logging.error("auckland_university; msg=Crawling Failed; URL= %s;Error=%s",response.url,traceback.format_exc())
    # english requirements for graduate 
    def _get_english_req_grad(self,eng_url):
        page=requests.get(eng_url)
        response=html.fromstring(page.content)
        eng={}
		# response=html.fromstring(page.content)
        try:
            ielts_data=response.xpath('//*[@class="text js-responsive-tables"]/table/tbody/tr[1]/td[2]/text()')[0]
            ielts=re.findall(r"[-+]?\d*\.\d+|\d+", ielts_data)
            ielts_o=ielts[0]
            ielts_a=ielts[1]
            eng['ielts']={
                'listening':ielts_a,
                'reading':ielts_a,
                'writing':ielts_a,
                'speaking':ielts_a,
                'overall':ielts_o
            }
        except Exception as ex:
            logging.error("Auckland University: Cannot fetch ielts: {}".format(ex))
        
        try:
            toefl_data=response.xpath('//*[@class="text js-responsive-tables"]/table/tbody/tr[2]/td[2]/text()')[0]
            toefl=re.findall(r'\d+',toefl_data)
            toefl_o=toefl[0]
            toefl_a=toefl[1]
            eng['toefl']={
                'listening':toefl_a,
                'reading':toefl_a,
                'writing':toefl_a,
                'speaking':toefl_a,
                'overall':toefl_o
            }
        except Exception as ex:
            logging.error("Auckland University: Cannot fetch toefl: {}".format(ex))

        try:
            pte_data=response.xpath('//*[@class="text js-responsive-tables"]/table/tbody/tr[8]/td[2]/text()')[0]
            pte=re.findall(r'\d+',pte_data)
            pte_o=pte[0]
            pte_a=pte[1]
            eng['pte']={
                'listening':pte_a,
                'reading':pte_a,
                'writing':pte_a,
                'speaking':pte_a,
                'overall':pte_o
            }
        except Exception as ex:
            logging.error("Auckland University: Cannot fetch pte: {}".format(ex))

        return eng
    # english requirements for undergraduate
    def _get_english_req_ungrad(self,eng_url):
        page=requests.get(eng_url)
        response=html.fromstring(page.content)
        eng={}
		# response=html.fromstring(page.content)
        try:
            ielts_data=response.xpath('//*[@class="text js-responsive-tables"]/table/tbody/tr[1]/td[2]/text()')[0]
            ielts=re.findall(r"[-+]?\d*\.\d+|\d+", ielts_data)
            ielts_o=ielts[0]
            ielts_a=ielts[1]
            eng['ielts']={
                'listening':ielts_a,
                'reading':ielts_a,
                'writing':ielts_a,
                'speaking':ielts_a,
                'overall':ielts_o
            }
        except Exception as ex:
            logging.error("Auckland University: Cannot fetch ielts: {}".format(ex))
        
        try:
            toefl_data=response.xpath('//*[@class="text js-responsive-tables"]/table/tbody/tr[2]/td[2]/text()')[0]
            toefl=re.findall(r'\d+',toefl_data)
            toefl_o=toefl[0]
            toefl_a=toefl[1]
            eng['toefl']={
                'listening':toefl_a,
                'reading':toefl_a,
                'writing':toefl_a,
                'speaking':toefl_a,
                'overall':toefl_o
            }
        except Exception as ex:
            logging.error("Auckland University: Cannot fetch toefl: {}".format(ex))

        try:
            pte_data=response.xpath('//*[@class="text js-responsive-tables"]/table/tbody/tr[8]/td[2]/text()')[0]
            pte=re.findall(r'\d+',pte_data)
            pte_o=pte[0]
            pte_a=pte[1]
            eng['pte']={
                'listening':pte_a,
                'reading':pte_a,
                'writing':pte_a,
                'speaking':pte_a,
                'overall':pte_o
            }
        except Exception as ex:
            logging.error("Auckland University: Cannot fetch pte: {}".format(ex))

        return eng