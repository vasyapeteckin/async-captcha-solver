import asyncio
import logging

from async_captcha_solver import CapMonsterClient


async def main():
    logging.basicConfig(level=logging.DEBUG)
    solver = CapMonsterClient(api_key='API_KEY')

    # optional
    solver.retry_count = 20
    solver.delay = 7

    status, result = await solver.recaptcha_v2(website_url='https://app.getgrass.io/register/',
                                               website_key='6LeeT-0pAAAAAFJ5JnCpNcbYCBcAerNHlkK4nm6y')
    print("result", result)

    if status:
        token = result.get('solution').get('gRecaptchaResponse')
        print("token", token)


if __name__ == '__main__':
    asyncio.run(main())
