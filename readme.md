
Prerequisites:

- python3
- python libraries: twisted, requests, pickle
- move the tor directory into appdata directory (C:\Users\<user>\AppData\Roaming)


===================================================================


Run the server from TunnelProject directory:
- python -m Server.server


Run the client from TunnelProject directory:
- python -m Client.client


===================================================================


Available Commands:

1. Add new proxy
   - arguments: IP, port, protocol, user, password

2. Remove proxy
   - arguments: IP (should be an IP of proxy added before)

3. Setup Tor
   - no arguments

4. Teardown Tor
   - no arguments

5. Connect URL via proxy
   - arguments: IP (should be an IP of proxy added before), URL
   - if the IP is empty, the server connects to the URL without proxies

6. Connect URL via Tor
   - arguments: URL
   - to use this command, you should setup Tor before

7. Quit from server
   - no arguments

