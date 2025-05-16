# This will consist of documentation written in free form. Plans, ToDo, Ventured option, etc.

## Goal
The goal of the project is to create an embedded software that allows the user to interact with social media services or communication services using speech. The project is targeted at people with disabilities who find the normal use of said services difficult or outright impossible.

The potential services include services such as Telegram, WhatsApp, Facebook, TikTok, Instagram. This list is not final, and some services may be added or dropped depending on potential future limitations.

Another goal of the project is to figure out if the solution can be done in embedded environment. Due to resource limitations, it is possible that the solution would need to be partially done with a desktop. Finding out how much can be done in embedded environment (if entirely) and balancing the two if there proves to be a need to create a hybrid solution.

Third objective would be to inspect the security aspects of the project, and take a look at how client data is handled.

## Plans
Currently, the following are being considered:

- ~~How plausible it is to implement WhatsApp functionality~~ Not worth it, telegram is a mess already.

- Expand scope depending on how difficult it proves to be to implement above functionality

- Create frontend on react, ~~backend on python using mqtt + flask (check notes on discord)~~. We need something else than just flask + mqtt. Flask approach for reddit oauth 2.0 flow is neccesary, but thats about all we want to use it for. Limited functionality is going to be behind that part aswell, perhaps scope it out entirely honestly? There is a working authflow already but its not great (live session only). Look into FSM, strong contender.

- ~~Start implementing the API functionality~~ Partially done.

- Look into the feasibility of using AI to handle situations in which keywords aren't being detected?

- Potentially have AI responses.

- ~~When handling Reddit calls, searching for topics could use user input for subreddit finding, and if no subreddit is found with keyword, loop it through AI to get "similliar" hits and prompt user if it would like to search for topics from those? Potentially open webview.~~ Partially Handled

- Look into data handling. Few things need to be made "less accessible". E.g. openai key, user credentials to ~~telegram~~ & reddit (if we choose to allow reddit user post / comment functionality).

- ~~Reddit api needs OAuth 2.0 flow if we wish to add post/comment functionality.~~ Done, but only live session currently.

## Ventured options

#### Regarding WhatsApp functionality, the following difficulties have been observed:

- It is against ToS to emulate WhatsApp. The allowed use of software is only in official platforms they provide. Hence, the useage of WhatsApp is entirely limited to API useage or webclient
- API useage costs money per conversation. API useage is primarily targeted at businesses. It is most likely not in the potential customers interest to pay extra for basic functionality

#### Regarding Speech recognition, the following has been observed:

- Using online API based solutions introduce lag which is not preferrable.
- Whisper is heavily resource intensive (openai-whisper and torch are big, both of which are dependancies. CPU based torch is also slower than GPU based, but since we're looking into embedded devices we don't have the option of using GPU based options)
- Ventured online speech recognition methods : Google cloud, Amazon, CMU Sphinx, IBM, OpenAI Whisper, Mozilla DeepSpeech
- Ventured offline speech recognition methods : VOSK (Current), pocketsphinx

A note about the different speech recognition methods, most of them perform in very similliar ways or are too resource intensive or extremely inaccurate. However, VOSK is very clearly ahead of its competition with simplicity to implement and resource management as secondary points, but major benefit is the speed you achieve with offline solutions. Compared to pocketsphinx, the accuracy of predictions is way better than pocketsphinx. A downside of vosk is that all languages don't have an existing model, limiting language options.

- Note on VOSK: It is poor in identifying names. Potentially problematic later when handling names on different APIs. Potential solution to change model to a more comprehensive one, albeit it does apparently increase lag. Needs further investigation.

- Note on Speech Processing: Attempted to use noisereduce, numpy and librose libraries for audio processing (noise filtering, MFCC, audio level normalization). We run into audio format conversion issues, breaks functionality. 
    Reasons for this is that the recognizer is expecting different data format than what the audio processing libraries want. VOSK is built on using PyAudio streams, whereas librosa needs numpy.int16 and noisereduce needs it aswell.
    Converting back and forth isn't an issue, but getting any output after conversion is. Identifying whats going wrong might not be worth the venture. Potential solution if desired is to work with raw audio data directly, but it seems
    at first glance extremely deep topic. It will be problematic to convert the audio data since most speech recognition solutions are handling raw audio data.

- Process kill / start handling using File I/O IPC. We can expand upon this with a different solution, this is a placeholder for now due to simplicity to implement


#### MQTT -,,-
- Graceful message handling is possible, actions based on keywords are also possible and implemented.
- Single command operations to multiple scripts are possible and implemented without using SIGINT.

#### Reddit API -,,-
- Topic specification will be an issue with user inputs alone. Potentially solved by AI loop to verify inputs, and running the script through both inputs. Second alternative is using more precise speech recognition. Some hybrid solution might be the best?

- FSM implementation will change how data needs to be handled. Possible solution is to import the module directly in FSM, alternatively we can serialize the data and pass it around

- String vs Array keyword handling performs differently. In order to use multiple keywords, using arrays seems to be the preferred option. Passing arrays around with IPC is more troublesome however, which can be solved with serialization.

- API account needs to "stay alive" for functionality. If it gets terminated for whatever reason, functionality will break entirely.

- Handling accurate vs inaccurate search needs design decision that won't be all encompassing no matter what.

- Speech recognition limitations might affect ability to search accurately for desired content. Potential solution is to provide interface in which you can manually input (how? tbd) search parameters. Also potential solution is to run two different speech recognitions, one for fast operations on FSM state switching, and another for more accurate speech recognition for operations which require precision. Accurate speech recognition does need testing.

- Multiple subreddits can be searched for keywords. No logic as to how to obtain them yet, but that falls outside of the reddit_apis responsibilities.

- Simple sorting algorithm to order the posts based on keywords found. Still return entire list and handle the case where user isn't happy with initial match in the FSM

#### Telegram API -,,-
- Authentication is very unfriendly to do in a web server approach, but since we're actively trying to avoid that anyway its not that big of an issue. Authentication requires a few input()'s, which should be feasible to hook up 
in GUI. Extremely unlikely we wish to use speech recognition for this. Trying to get +358 12 3456789 through speech recognition is a hassle, and verification code is going to run into same issue.

- Contact fetching is done. A bit of a pain, but for now we store it into a json file to load from for non async operations.  Theres a lot of junk in the actual contacts object, manually going through it is a pain in the arse.

- We maintain a session file so further api calls in different sessions do not require the entire authentication process.

- Contact searching return an array of dicts now. 

- Send message, fetch history functions work.

#### FSM -,,-
- Main loop execution is very particular about how everything works. Currently, each check_transition_conditions() call needs access to self.buffer (so that we can clear the buffer when initializing a new state, which is a fix to a weird
infinite loop bug).  On top of that, we need to return a state object on each check_transition_conditions() call, even if we don't wish to change states (e.g. initial state). If we want to make conditional logic on state switching, which
is neccesary, it can be handled with multiple if else statements that are resolved in handle_transition(). Any loop where we wish to start appending messages to buffer and conditionally progress states can be achieved by creating and 
deleting the killswitch file. Extra attention needs to be paid to avoid deadlocks (which happen all the time).

- Any unique to state functions we wish to create need to be called as nested functions inside either check_transition_conditions(), __init__(), or handle_transition(). Handling the speech recognition threads life span is best handled
within inits, by moving between listening states and non_listening states (it would be nice to pass keywords as an argument to a blueprint state, but its likely a lot easier to duplicate similliar working states since the destination state is likely unique to each set of keywords).  Passing buffer around seems dangerous aswell, due to easily creating infinite state switch loops. Theres potentially race condition bullshit happening aswell, further complicating the use of shared buffer between states.

- A potential use case in a "stay or move" state to observe is returning self on check_transition_conditions() on else clause, while in if clause we move to handle_transition(). E.g. if buffer contains keyword, move to if, else keep appending messages to buffer. NOT TESTED FULLY.

- Made buffer transfer & predecessor state information optional to be passed (in some cases we might want to hop states, in which case returning to a previous state information is vital. We also wish to return to prev. state in a lot of "yes/no" situations, with the yes or no as direct input on how to traverse states)

- Passing state objects around includes a LOT of computational overhead, no clue why

- State switching creates an insane amount of computational overhead, which was introduced when state objects were being passed around. However, Im not entirely certain that is the case. Interestingly, initializing the first state doesn't kill the cpu, but when we do run into state switching from thereon out, regardless of where we try to move, every state switch eats the entire CPU. Potential issue with the file I/O signals? Absolutely no clue. Execution is in SECONDS between most operations. MQTT runs fine after that couple seconds, and the SR thread being alive only amounts to ~5-10% CPU useage when we are actively listening, but for a dynamic program to take seconds between each state transition while the "difficult" task of SR doesn't eat anything (since we kill the thread during state init()). And not only that, seemingly the calling of functions after initializing (when we are certain that SR is passive) a state also take extremely long to do the sequential run_pre_transition() -> handle_transition(). Needs further research as to why.

- From FSM we built a killswitch for both the main and sub threads. Also handling main thread kill command without having to pass the fsm information to the states (which would be dumb alternative). Instead we raise a custom exception which when caught will result in a kill & clean up outcome.

- Buffer can now be stored into a cache for the object if for some reason we would need to. Maybe useful though I'd have to ensure that when we move a lot between states, when we enter a state once already created we do enter the old
state instead of creating a new one. The issue is, we currently only store the current and previous state. Im not exactly certain what happens to the states after that (memory ghosts which potentially lead to memory leaks, memory being reserved until it runs out or if the memory is free'd up dynamically), but we do NOT return to an already instanced state unless we explicitly go to the previous state. Topic needs further research.

- We need to create new telegram client using same session_name every time we wish to use any telegram functionality, otherwise we run into a telethon library error (must use same event loop), asyncio related.

More in detail :

Each telegram client instance needs a separate asyncio event loop.  And Im too stupid to know how to pass an asyncio event loop around states and then "run" it without it dying on me (asyncio.run() dies on 2nd run of the event thread by default), so we just create a new event loop every time we need a client for something. This has something to do with asyncio library having natural deadlock issues, and telethon library has built in error handling for this. The issue is, we can pass the old instance of telegram client around, but we run into deadlock situations due to asyncio if we try to use an old event loop (that most of the time isn't even active anymore. Reactivating old event loop seems like a really bad idea too.)

Technically we could create functionality inside one big function (like how the pre prototype function in telegram_api.main() was done), but since my approach is a divide and conquer on the fsm with a lot of small substates, it would require a complete refactoring, and the solution comes with a lot more issues than it solves (which is the original reason why I went with divide and conquer)

- Each functionality in FSM is approached with divide and conquer tactic, where each problem is divided to as small of a problem as humanly possible. This means that if we need to for example search a subreddit, we split acquiring the keywords into its own state, and then acquiring the subreddits to search as a separate state. This allows for a more uniform control flow, with a lot less complicated control logic (in essence, most states consist of less than 10 if statements instead of having 10+ in each). The tradeoff is that there are a lot of substates, which create a lot of code. However inspecting the code is faster, and debugging is infinitely easier. Also creating working code is faster, since each added module doesn't complicate the logic exponentially, but instead its mostly its own dedicated path which adds dedicated control flow to the module, and realistically adding one more if check in the place where the module is selected. 

- Authentication is the only place which is handled a little differently, due to the limitations of the client.start() method. When is_user_authenticated() returns false, we enter a custom "state" which is implemented entirely differently from rest of the code. It enters a similliar while loop as the states, but when I tried to pass a state as an callback function for the client.start() it just wouldn't work. Its a while loop that is exited only if a "yes" is inputted on to the mqtt topic, and the function holds a global buffer unique to the callback function itself. The callback function is entered again if you input wrong code, and telegram will lock you out if you fail the authentication too many times.

## ToDo

#### Regarding WhatsApp, certain things need to be established. Some to mention:

- Verify if there is enough space for a webcrawler in raspberry pi
- Verify if a webcrawler can return contacts as a list that can then be used to automate contact fetching through the webclient

After doing the above, make a gameplan on how to continue.

Outside of WhatsApp, the following needs to be done:

- Cross-compile an executable which handles speech recognition and stringifies the input. That is then used for control
- Provide alternative GUI on desktop environment


#### Regarding Speech recognition

- ~~Control for starting and ending the process (Using GUI. Primitive signal handler is in place which can be expanded upon)~~

- Handling names better. High inconsistency in name identification. Propably an endless issue in modern day with speed / accuracy tradeoff.

- Verify the viability of using multiple different speech recognition methods, fast in FSM state switching & precise when specifying parameters for searches for ui navigation & api calls.

- Run a parallel thread on more accurate SR API. Perform searches on quick for dirty solutions, if user doesn't like output run search through accurate SR (slow) instead. Google or Whisper? If slow performs poorly, allow useage of GUI to manually search. Increases overhead. Perhaps a configuration setting to enable this? Parallel execution vs choice between different SR methods.

#### MQTT -,,-

- ~~Implement API functionality from keywords (Create commands for the FLASK component)~~
- ~~Expand keyword logic to fit the needs~~
- ~~Make the component that handles the blocking of speech recognition when TTS fires up to avoid echo hallucination~~ No part handling this, but the functionality exists with a File I/O IPC (read speech_module.py)
- ~~Create a finite state machine for navigating commands.~~
- ~~Possibility to create aliases, single word & multi word aliases for keywords to mitigate speech recognition issues in places where speech recognition performs poorly, but predictably.~~ Handle with GUI instead?

#### API -,,-
- ~~Create functionality with reddit crawler that returns links to a post if one is present.~~
- ~~Create framework for handling the useage of Telegram & Reddit APIs.~~
- ~~Create ability to move in the FSM between states based on API call results~~

#### Reddit API -,,-
- Create IPC data handling, not just printing the data

#### GUI -,,-
- Open the webviews if so desired by user. 
- Ability to change configs based on user preference?
- Buttons need to publish messages over MQTT so that backend FSM will switch states accordingly.

#### TTS -,,-
- Look into TTS solutions.
- Handle stt thread manipulation so that the stt isn't listening when tts is running. Potential issue arises when the execution is considered "done", but tts is still talking, causing hallucination.

#### FSM -,,-
- ~~Create it.~~
- ~~Create more states based on the existing blueprint, we need to cut each part into smaller pieces. At least the general rough outline is there. Heavily consider dropping the reddit auth~~
- Make some schema on how it works when it works
- Start publishing messages on each state switch over mqtt to a different topic to control GUI so that they stay synced
- ~~Look into handling mqtt messages as interrupts instead of doing a continuous while loop execution~~ Partially done.
- ~~Look into the 90+% CPU useage issue. That needs to be optimized better~~

#### Flask -,,-
- Create all neccesary credential fetching so you can authorize users. Eventually create a db to store credentials to and encrypt it. Throw openai key, reddit api key, etc all there.

- Refactor the authentication and api call functions separate.

#### Telegram API -,,-
- Create ~~send message, fetch message history~~, create group, etc functionality

- ~~In search function, handle emojis somehow. Emojis currently "kill" that field entirely. Allow partial search term like in reddit posts?~~ Handled. Even sending emojis through terminal works. Potentially map some emojis
that can be used in gui? Creating a message out of speech with emojis is probably annoying though, make a prompt at end "would you like to end the message in an emoji?" or something like that. Extra eye-candy after functionality
works.

#### Entire project -,,-
- Create error handling logger, where if we run into errors, they are then logged to a log file. THIS LOGFILE SHOULD NOT BE PACKAGED WITH THE EXECUTABLE.
- Create potential error solutions as exceptions and log them (major refactor)
- Create automated testing for the code.
- Demo the prototype
- Wrap the project into binary