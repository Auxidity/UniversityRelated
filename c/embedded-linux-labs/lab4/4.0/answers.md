1 . in git

2 . cron_blink.txt is in git

3 . I had crontabbed a shell script, for debugging reasons I made it happen every minute and shell script turns it off after 30 seconds. 

Instead of that, to get the desired output, you would edit the wrapper.sh with 600s sleep (instead of 30 that was used to demonstrate it working).

and crontab would be */30 * * * * ./wrapper.sh

instead of runtimes * * * * * ./wrapper.sh

4.

outside of september rule
*/30 0-3,6-23 * * * ./wrapper.sh

september rule
*/15 0-3,6-23 1-30 9 * ./wrapper.sh
