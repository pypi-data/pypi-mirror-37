===============================
Gingerit
===============================

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/Azd325/gingerit
   :target: https://gitter.im/Azd325/gingerit?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. image:: https://img.shields.io/travis/Azd325/gingerit.svg
        :target: https://travis-ci.org/Azd325/gingerit

.. image:: https://img.shields.io/pypi/v/gingerit.svg
        :target: https://pypi.python.org/pypi/gingerit


Correcting spelling and grammar mistakes based on the context of complete sentences. Wrapper around the gingersoftware.com API

* Free software: MIT license
* Documentation: https://gingerit.readthedocs.org.

Installation:
-------------

::

    pip install gingerit

Usage:
------

::

    from gingerit.gingerit import GingerIt

    text = 'The smelt of fliwers bring back memories.'

    parser = GingerIt()
    parser.parse(text)

TODO:
-----

 - More tests
 - Commandline Tool

Contributing:
-------------

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

Thanks
------

Thank you for [Ginger Proofreader](http://www.gingersoftware.com/) for such awesome service. Hope they will keep it free :)

Thanks to @subosito for this inspriration https://github.com/subosito/gingerice (Ruby Gem)
