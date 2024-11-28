from libs.UI.page_object_models.sample.google import Google


def test_google_search(context, variables):
    page = context.new_page()
    google_page = Google(page, host=variables['host']).open()
    google_page.search_default("Youtube")