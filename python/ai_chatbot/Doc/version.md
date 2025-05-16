Version edit history.

0.1.0 : First stable build
0.2.0 : Memory modes
0.2.1 : stt.py rebuilt to pipe std.err away from runtime terminal (for non runtime critical errors).
0.2.2 : post executable error handling (file not found error)
0.2.3 : Fixed exit() not recognized in executable
0.2.4 : IP changed from hardcoded to runtime. No error handling (yet).
0.2.5 : Tested TTS module to work. Implemented it in speech
0.2.6 : Language argument passed for stt (Needs work, needs tts config call)
0.3.0 : Language is getting passed across the executable and is reconfigurable together with IP. (Major). Testbench also (Major)
0.3.1 : Code cleanup, no major functionality
0.3.2 : Changed order of execution inside caller. Was an oopsie.
0.3.3 : Added functionality to add and remove configurations from config.json
0.3.4 : Added Docker file. Python2 works. Adding Dockerfile to VC. GUI breaks still.
0.4.0 : Built a cli (not_really.py) & changed main.py to server. MAJOR. A lot of shit not working.
0.4.1 : dev mess. A lot of broken functions. Its own branch, not pushed to main
0.5.0 : Server "works". With all old functionality. Skeleton gui. (MAJOR)
0.5.1 : Code cleanup
0.5.2 : Further code cleanup
0.5.3 : Bug fixes
0.5.4 : Moving functions from caller outside to reduce dependancies on application.
0.5.5 : Single command memory speech call. Led control for eyes. Led functionality needs to be tested.
0.5.6 : Restructuring of code, single command debug payload for testing functionality
0.5.7 : Led test function for changing eyes works, needs to be implemented across the code.
