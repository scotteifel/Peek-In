# Peek-In

<p align="center">
  <img src="https://user-images.githubusercontent.com/34344118/172986936-47beb405-a5d4-4f88-8fca-facb37ad94fd.png"/>
</p>

Hello. This app is meant to help enable parents to monitor what their children are seeing on the internet.  It stores screenshots which can be retrieved later.  It also has a way to run
in the background, so it is not easily detectable.

After creating an account, you set a time delay 
for automatically taking screenshots and you can start using it.

A screenshot will be taken and converted to a text file.  The file will be encrypted,
and it will be saved into a database to add to the security of the information stored.
Only a signed in user can access their screenshots.

This could be turned into an executable program and is developed for Windows OS currently.

WARNING:
I use subprocesses to isolate the program and close it, which may need tweeking in order for it to be more stable.
