from mailchimp_marketing import Client

mailchimp = Client()
mailchimp.set_config({
  "api_key": "263dc0f69ff8bd52e7018ec27d72770b-us2",
  "server": "us2"
})

response = mailchimp.ping.get()
print(response)