# Dream Media Dreambox

Using Enigma2:WebInterface REST API to control decoder.
Library to control Dream Media Dreambox.
Tested on DM800 HD se
Please let me know if it works on other models too

### Methods

##### get_current_channel
- Get's current channel name e2servicename

##### get_current 
Gets following info for the current channel:

- e2servicename
- e2providername
- e2servicevideosize
- e2eventservicereference
- e2eventname
- e2eventdescriptionextended

##### get_audio_status
Returns following data:

- worked
- volume_status
- mute_status

##### get_audio_tracks
Lists info about current audio tracks

- e2audiotrackdescription
- e2audiotrackid
- e2audiotrackpid
- e2audiotrackactive

##### recording_list
Returns list of recordings in dictionary format

##### volume_set
Set's volume to requested value and returns:
- confirmation
- volume_status
- mute_status

##### goto_channel
Sets channel to  channel #

##### record_now
Set's recording timmer to record current program

##### get_timerlist
Returns information about timer:
- e2servicereference
- e2servicename
- e2name
- e2timebegin
- e2timeend
- e2duration

##### timer_cleanup
Clears timers, returns e2statetext

##### recording_delete
Requires e2servicereference
Deletes movie from the disk

##### del_timer
Requires (timer_id, begin, end)
Deletes the timer

##### stream_curent_channel
Returns m3u playlist for current channel

##### change_audio_channel
Requires track_nr
Switching audio channel to track_nr

##### volume_up
Sets volume up

##### volume_down
Sets volume down

##### mute
Muts audio

##### ok
Button OK

##### power
Power toggle

##### info
Button info

##### pause
Pause button

##### play
Play button

##### exit
Exit button
