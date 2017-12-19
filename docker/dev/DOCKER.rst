Docker
======

Docker integration
------------------
To build the smartPeak docker image, navigate to the smartPeak/py directory

:code:`docker build -t dmccloskey/smartPeak:latest .`

To run the smartPeak docker image after building, navigate to the smartPeak/py directory

:code:`docker-compose up`

To restart the smartPeak docker image

:code:`docker-compose restart`

To remove the smartPeak docker image

:code:`docker-compose down`

Remote debugging with vscode
----------------------------
- change the luanch.json file in the .vscode directory to match your system settings
by changing the "localRoot" directory of "Attach (Remote Debug)" to match your system.

- you can then dynamically debug your application using the debug_remote.py file and
debugging using the "Attach (Remote Debug)" launch setting