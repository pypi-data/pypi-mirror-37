# Utility for quick test python script

[![Build Status](https://travis-ci.org/xudifsd/cmdcall.svg?branch=master)](https://travis-ci.org/xudifsd/cmdcall)

After you finished coding your script just call cmdcall like `cmdcall.handle(sys.modules[__name__])`,
then, your script is callable immediately. Call your script like `python script.py foo 1 2 --c 3 --d 4`
and cmdcall will parse cmdline args and provide them to `foo` function of your module.

See [entry script](test/entry.py) and [test case](test/test_cmdcall.py) for more info.
