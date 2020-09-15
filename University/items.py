# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UniversityItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    course_name=scrapy.Field()

    course_category=scrapy.Field()

    course_webiste=scrapy.Field()

    duration=scrapy.Field()

    duration_term=scrapy.Field()

    study_mode=scrapy.Field()

    degree_level=scrapy.Field()

    intake_day=scrapy.Field()

    intake_month=scrapy.Field()

    apply_day=scrapy.Field()

    apply_month=scrapy.Field()

    city=scrapy.Field()

    domestic_only=scrapy.Field()

    international_fee=scrapy.Field()

    domestic_fee=scrapy.Field()

    fee_term=scrapy.Field()

    fee_year=scrapy.Field()

    currency=scrapy.Field()

    study_load=scrapy.Field()

    ielts_overall=scrapy.Field()

    ielts_listening=scrapy.Field()

    ielts_speaking=scrapy.Field()

    ielts_reading=scrapy.Field()

    ielts_writing=scrapy.Field()

    pte_overall=scrapy.Field()

    pte_listening=scrapy.Field()

    pte_speaking=scrapy.Field()

    pte_reading=scrapy.Field()

    pte_writing=scrapy.Field()

    toefl_overall=scrapy.Field()

    toefl_listening=scrapy.Field()

    toefl_speaking=scrapy.Field()

    toefl_reading=scrapy.Field()

    toefl_writing=scrapy.Field()

    course_description=scrapy.Field()

    course_structure=scrapy.Field()

    career=scrapy.Field()

    other_requirements=scrapy.Field()


    


