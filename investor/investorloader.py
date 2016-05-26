from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity

class InvestorLoader(ItemLoader):

    default_output_processor = TakeFirst()

    summary_in = MapCompose(unicode.strip)
    summary_out = Join()

    investments_in = MapCompose(unicode.strip)
    investments_out = Join()

    skills_in = MapCompose(unicode.strip)
    skills_out = Join(', ')

    locations_in = MapCompose(unicode.strip)
    locations_out = Join(', ')

    what_i_do_in = MapCompose(unicode.strip)
    what_i_do_out = Join(', ')

    achievements_in = MapCompose(unicode.strip)
    achievements_out = Join(', ')

    markets_in = MapCompose(unicode.strip)
    markets_out = Join(', ')

    experience_out = Identity()

