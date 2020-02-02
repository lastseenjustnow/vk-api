if __name__ == '__main__':
    from access_token import access_token
    message = ''.join('''Greetings! You are running vk_toolkit first draft demonstration ... :)

Your access token is: ''' + access_token + '''

There are 2 demonstration options:
1. Find matches of passed people's names and surnames within particular groups
2. Collect data posted within particular group

Which option do you want to test? Select a number: 
''')
    print(message)
    option = None
    while option is None:
        option = input("Number: ")
        if option == "1":
            import data.find_people_in_groups
        elif option == "2":
            import data.crawl_group_posts
        else:
            print("You'd better be certain! Choose 1 or 2 option...")
            option = None
            continue
