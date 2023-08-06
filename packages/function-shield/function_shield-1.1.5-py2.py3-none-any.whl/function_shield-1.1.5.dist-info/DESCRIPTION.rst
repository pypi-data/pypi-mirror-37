
FunctionShield
--------------

   AWS Lambda Security Library for Developers. Regain Control over Your
   Serverless Runtime.

How FunctionShield helps With AWS Lambda Security?
--------------------------------------------------

-  By monitoring (or blocking) outbound network traffic from your
   function, you can be certain that your data is never leaked
-  By disabling read/write operations on the /tmp/ directory, you can
   make your function truly ephemeral
-  By disabling the ability to launch child processes, you can make sure
   that no rogue processes are spawned without your knowledge by
   potentially malicious packages
-  By disabling the ability to read the function’s (handler) source code
   through the file system, you can prevent handler source code leakage,
   which is oftentimes the first step in a serverless attack

Get a free token
----------------

Please visit: https://www.puresec.io/function-shield-token-form

Install
-------

.. code:: sh

   $ pip install function-shield

Super simple to use
-------------------

.. code:: python

   import function_shield

   function_shield.configure({
       "policy": {
           # 'block' mode => active blocking
           # 'alert' mode => log only
           # 'allow' mode => allowed, implicitly occurs if key does not exist
           "outbound_connectivity": "block",
           "read_write_tmp": "block",
           "create_child_process": "block",
           "read_handler": "block"
       },
       "token": os.environ['FUNCTION_SHIELD_TOKEN']
   })

   def handler(event, context):
       # Your Code Here #

Logging & Security Visibility
-----------------------------

FunctionShield logs are sent directly to your function’s AWS CloudWatch
log group. Here are a few sample logs, demonstrating the log format you
should expect:

.. code:: js

   // Log example #1:
   {
       "function_shield": true,
       "policy": "outbound_connectivity",
       "details": {
           "host": "google.com"
       },
       "mode": "alert"
   }

   // Log example #2:
   {
       "function_shield": true,
       "policy": "read_write_tmp",
       "details": {
           "path": "/tmp/node-alert"
       },
       "mode": "alert"
   }

   // Log example #3:
   {
       "function_shield": true,
       "policy": "create_child_process",
       "details": {
           "path": "/bin/sh"
       },
       "mode": "block"
   }

   // Log example #4:
   {
      "function_shield": true,
      "policy": "read_handler",
      "details": {
          "path": "/var/task/handler.js"
      },
      "mode": "alert"
   }

Custom Security Policy (whitelisting)
-------------------------------------

Custom security policy is only supported with the PureSec SSRE full
product.

`Get PureSec`_

.. _Get PureSec: https://www.puresec.io/product

