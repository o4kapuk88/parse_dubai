from twocaptcha import TwoCaptcha

api_key = '786bd7a8b6822e21b9e1138b14c49e44'
solver = TwoCaptcha(api_key)

result = solver.solve_captcha(
    site_key='dd6e16a7-972e-47d2-93d0-96642fb6d8de',
    page_url='https://dubai.dubizzle.com/property-for-sale/residential/?neighborhood=57505&neighborhood=193&neighborhood=52&neighborhood=87&neighborhood=63&page=1'
)

print(result)