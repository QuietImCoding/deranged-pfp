# deranged-pfp
Little bot to make your PFP do horrifying things 

# Usage
- install dependencies with pipenv install or pip install -r requirements.txt (pipenv is great)
- set up the environment variables CONSUMER\_KEY, CONSUMER\_SECRET, ACCESS\_KEY, ACCESS\_SECRET from twitter dev console. these should be set in your .env file or in the ~cloud~ config
- if you want to use railway to deploy, do railway init and set up the project
- run (pipenv run) ```python facemaker.py <your username (no @)> <image to use as pfp> [center x] [center y]```
  - if it works locally, import your .env into railway and edit the procfile to match the command you used locally 
- Congrats! Your pfp should now do some absolutely disgusting things!

## Todo ##

- Literally no error handling has been implemented so it might just fail bc of twitter being evil
- Have not written a single comment? 
- Figure out if i need to have the magick binary bundled for it to work in the cloud... i suspect i do, but truly have no evidence to support that 

