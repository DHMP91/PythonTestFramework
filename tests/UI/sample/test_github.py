from libs.UI.page_object_models.sample.github import GitHubUserPage


def test_partial_url(context, variables):
    page = context.new_page()
    GitHubUserPage(page, USER_ID="DHMP91").open()
    print("Welcome to my github page")
