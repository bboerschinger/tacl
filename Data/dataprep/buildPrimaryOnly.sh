#!/bin/bash

# takes the transcript and introduces stress-marks only for
# primary stress, removing all additional stress info

sed 's/1/ */g; s/0//g; s/2//g' $1
