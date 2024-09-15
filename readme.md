# Step It Up Bot

Here's a program that automates the process for Step it Up Kids!

## Setup

Create an environment if you wwould like, then run `pip install -r requirements.txt`
Rename `config.json.example` to `config.json`, fill in the values.
(stepitup does have a ratelimit, which will result in a 403 error)
(you also might need to update the proxy list)

### Configuration Info

- `domains` - The domains are a list of tld's or subdomains that you have mail for.
- `tempmail` - Whether or not to use a disposable mail website.
- `tempmailkey` - API Key for .
- `familyAuthKey` - The sort of "login" used on the stepItUp website, you can obtain this from your cookies, it should be around 7 digits. You can also put multiple accounts and the bot will evenly spread out the emails to them. Another thing to note, since these are just digits, it's quite easy to impersonate people.
- `schoolPath` - stepItUp will provide you with a link  (ex. https://stepitupkids.com/RealNotFakeHighSchoolName) for each school you want to participate in, in this case provide RealNotFakeHighSchoolName.

## Contribution

You can do stuff, whatever really.

### Credit

https://github.com/TheSpeedX/PROXY-List

https://proxyscrape.com/free-proxy-list

Whoever made the libraries I used