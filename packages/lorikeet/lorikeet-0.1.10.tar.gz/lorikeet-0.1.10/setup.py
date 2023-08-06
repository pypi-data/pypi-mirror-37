# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['lorikeet',
 'lorikeet.extras',
 'lorikeet.extras.email_invoice',
 'lorikeet.extras.starshipit',
 'lorikeet.extras.starshipit.migrations',
 'lorikeet.extras.stripe',
 'lorikeet.extras.stripe.migrations',
 'lorikeet.migrations',
 'lorikeet.templatetags']

package_data = \
{'': ['*']}

install_requires = \
['django-model-utils>=2.6,<3.0',
 'django>=1.8,<1.11',
 'djangorestframework>=3.5.3,<3.6.0']

extras_require = \
{'email_invoice': ['premailer>=3.0.1,<4.0.0'],
 'starshipit': ['requests>=2.13.0,<3.0.0'],
 'stripe': ['stripe>=1.44.0,<2.0.0']}

setup_kwargs = {
    'name': 'lorikeet',
    'version': '0.1.10',
    'description': 'A simple, generic, API-only shopping cart framework for Django',
    'long_description': "Lorikeet\n========\n\n⚠️ **Note:** Lorikeet is a work in progress. It may change at any time,\nand you shouldn't use it in production yet.\n\nLorikeet is a simple, generic, API-only shopping cart framework for\nDjango.\n\nLorikeet currently supports Django 1.8 to 1.10 on Python 3.4+. New versions of Lorikeet will support `Django versions that currently have extended support <https://www.djangoproject.com/download/#supported-versions>`_.\n\nWhy use Lorikeet?\n-----------------\n\nE-commerce apps are divided into two types: simple ones that work well so long as what you're selling is simple, and complex ones that try to be all things to all people by way of a maze of checkboxes and dropdowns.\n\n**Lorikeet isn't an e-commerce app; it's a shopping cart framework.** With Lorikeet, you define models for line items (the things that go in your cart), delivery addresses and payment methods yourself. For complex shops, this means you can model exactly the functionality you need without fighting the system. For simple shops, this is a simple process that requires way less code than you'd expect, and gives you a system without unnecessary bloat, but with room to grow.\n\n**Lorikeet only cares about the cart itself**; everything outside of that, including your navigation and product pages, is directly under your control, so you're free to use a simple ``ListView`` and ``DetailView``, Wagtail, Mezzanine, Django CMS, or something totally bespoke. There's not a single line of HTML or CSS in Lorikeet's codebase either, so Lorikeet gives you total control over your visuals too.\n\nLorikeet line items, delivery addresses and payment methods are designed to be orthogonal, so you can package them as reusable apps and share them internally between sites in your company, or with the world as open-source packages. In fact, **Lorikeet already includes an optional Stripe payment method plugin**, totally separate from the rest of the codebase and written against the same public API as your own apps.\n\nBecause most modern payment providers require JavaScript anyway, **Lorikeet is API-only**. This lets you build a fast, frictionless shopping experience where users can add to and change their shopping carts without the entire page refreshing each time, and Lorikeet's API is designed to allow logged-in repeat users to check out in a single click.\n\n\nWhy use something else?\n-----------------------\n\n- **Lorikeet isn't turnkey.** For simple sites, you won't need to write much Python code; for complex ones, the time it takes to get up and running will probably be comparable to the time it takes to figure out how to bend e-commerce apps to your will. But the total control over the frontend that Lorikeet gives you means you'll need to write a fair bit of HTML, CSS and JavaScript to get up and running, so if you need to go from zero to shop quickly, it's best to look somewhere else.\n- **Lorikeet sites will require JavaScript.** Lorikeet doesn't provide regular HTML-form-based views for adding items to the cart and checking out; if you need this, Lorikeet isn't for you.\n",
    'author': 'Adam Brenecki',
    'author_email': 'adam@brenecki.id.au',
    'url': 'https://lorikeet.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.4',
}


setup(**setup_kwargs)
