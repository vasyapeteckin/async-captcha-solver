# Async Captcha Solver

`async-captcha-solver` is a Python library designed for solving various types of CAPTCHA challenges using popular third-party CAPTCHA-solving services such as 2Captcha, AntiCaptcha, and CapMonster. It provides an easy-to-use abstraction layer for interacting with these services in a unified and efficient way.

---

## Key Features

- Support for popular CAPTCHA-solving services (e.g., 2Captcha, AntiCaptcha, CapMonster).
- Unified interface for handling CAPTCHA tasks.
- Asynchronous API for scalable and high-performance applications.
- Extensible framework allowing custom CAPTCHA-solving providers.
- Built-in HTTP client abstraction for flexibility.

---

## Installation

Ensure you have Python 3.12 or newer installed on your system. Then, install the package using `pip`:

```bash
uv add async-captcha-solver
```
or
```bash
pip install async-captcha-solver
```

---

## Usage

### Quick Start

```python
import asyncio
import logging

from captcha_solver import CaptchaSolver


async def main():
    logging.basicConfig(level=logging.DEBUG)
    solver = CaptchaSolver(service='capmonster', api_key='API_KEY')

    # optional
    solver.client.retry_count = 20
    solver.client.delay = 7

    status, result = await solver.client.recaptcha_v2(website_url='https://app.getgrass.io/register/',
                                                      website_key='6LeeT-0pAAAAAFJ5JnCpNcbYCBcAerNHlkK4nm6y')
    print("result", result)

    if status:
        token = result.get('solution').get('gRecaptchaResponse')
        print("token", token)


if __name__ == '__main__':
    asyncio.run(main())

```

## Acknowledgments

- [AntiCaptcha](https://anti-captcha.com/apidoc)
- [CapMonster](https://docs.capmonster.cloud/docs)
- [2captcha](https://anti-captcha.com/api-docs)
- [aiohttp](https://docs.aiohttp.org/)
---
