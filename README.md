# TubeUnmix
Opt out of YouTube remixes/shorts for all of your videos.  

I don't have a large channel to test this on, so extended runs could potentially be timed out/throttled by YouTube, so multiple, spaced out attempts may be required in these cases.

There is also only support for Windows at the moment with the pre-compiled EXE file, but the code itself is platform agnostic.

## Getting Started
Head on over to the [Releases tab](https://github.com/Gunsmithy/TubeUnmix/releases) and download the latest tube_unmix-vX.X.X.zip file and extract it somewhere convenient on your PC.  

All you need to do to is simply run the included `tube_unmix.exe` and it will prompt you for the rest!  

If pre-compiled binaries sketch you out, feel free to download the source file and run the Python script directly instead.

## Required Input
All of the below inputs assume you are on your YouTube Studio Content page.  
The instructions also follow that of Google Chrome, but should work similarly in other browser developer tools.

#### Channel ID
This is simply the ID of your YouTube channel, which can be found in the address bar when in YouTube Studio.
![Channel ID Image](/../resources/images/channel_id.png?raw=true "Channel ID")

#### Path/Authorization/Cookie Headers
These are request headers from the request for listing videos. This can be found in Google Chrome DevTools.  
Go to your Content list in YouTube Studio, hit `Ctrl + Shift + I` to enter Chrome's developer tools, and go the to `Network` tab at the top.  
![Network Button Image](/../resources/images/network_button.png?raw=true "Network Button")

From there you should see a text box with the placeholder word "Filter" inside. 
![Filter Blank Image](/../resources/images/filter_blank.png?raw=true "Filter Blank")

Here, simply type `list_creator_videos` and only one request should show up in the list below.  
If nothing shows up, refresh your page and wait a moment until it does.  
![Filter List Image](/../resources/images/filter_list.png?raw=true "Filter List")  
![List Request Image](/../resources/images/list_request.png?raw=true "List Request")

Now ensure you are on the `Headers` tab, then copy and paste the values under `Request Headers` as prompted by the program.  
Whether you copy just the value to the right of the colon or triple click and select the whole line, the program should accept it fine.  
![Request Headers Image](/../resources/images/request_headers.png?raw=true "Request Headers")

#### Session Token
The Session Token is also retrieved in a similar manner to the above Headers, using developer tools, but instead we are filtering for a request called `esr`.  
![ESR Request Image](/../resources/images/esr_request.png?raw=true "ESR Request")

Once you have found this request, go to the `Response` tab, scroll to the bottom, and copy everything within the quotes as blurred in the image below:  
![Session Token Image](/../resources/images/session_token.png?raw=true "Session Token")

## Enjoy!
Feel free to create a [Github Issue or Feature Request](https://github.com/Gunsmithy/TubeUnmix/issues) if you have any problems using this or if there's something you'd like added!  
