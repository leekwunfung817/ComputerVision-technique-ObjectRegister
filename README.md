# ComputerVision-technique-ObjectRegister

This project will run varies of thread, each one have their own functions.

## Function List
<pre>
1. Capture the moving object which is able to see, will skip the remarked irrelevant area.
2. Simulate the object's movement with timestamp after the object was captured.
3. Simulate a map to display the location of the captured objects.
</pre>

config file:
<pre>
Image configuration file (.icfg)
    id_position.icfg - define captured area align with car-parking position. (For function 3)
        1.red 
        2.orange 
        3.yellow 
        4.green 
        5.blue 
        6.purple 
        7.pink 
        8.brown 
        9.black 
        10.white 
        11.gray
    ignore.icfg - ignore area. (green as concentrate, black as ignore) (For function 1)
    sys.cfg (For function 1)
        Camera Name - e.g. Left Corner Area
        Camera ID - e.g. LCA
        
        background - minimum area pixels - e.g. 30 px
        background - capture per second - e.g. 180 sec
        background - movement timeout - e.g. 30 sec
        
        movement - minimum area pixels - e.g. 30px
        movement - thresholds value - e.g. 20%
        movement - video timeout - e.g. 10 sec
        
        db - query frequent - e.g. 10 sec
        remove - check frequent - e.g. 180 sec
        
        red_id= - e.g. position1
        red_name= - e.g. Position 1
        orange_id=
        orange_name=
        yellow_id=
        yellow_name=
        green_id=
        green_name=
        blue_id=
        blue_name=
        purple_id=
        purple_name=
        pink_id=
        pink_name=
        brown_id=
        brown_name=
        black_id=
        black_name=
        white_id=
        white_name=
        gray_id=
        gray_name=

</pre>

## Program Main Thread

<pre>
Boolean is_moving
run thread 1
run thread 2
While haveNewChecking
    run Thread 3 - checking-in or check-out data

</pre>

## Program Thread 1 - Background extraction
image array with 3 background image - for thread 2
<pre>
Capture 3 photos into a buffer, each 3 minutes will capture a photo to append to this buffer and remove the eariest one.

Pseudo code
image array with 3 image
While loop each 3 minutes
    if !is_moving
        append current capture
        remove eariest capture
</pre>

##  Program Thread 2 - Movement capture and save
extract moving object and save with datetime by folder path - for thread 3
<pre>
three_image_not_match_matrix = None

While true
    Capture photo
    three_image_not_match_matrix = \
        cv2.absdiff - compare with three image in an array (pixels that different with all three image, image with 1, 2 and 3)
    is_moving=(diff more then 20% area) three_image_not_match_matrix
    if is_moving
        meta_data = extractMovingObjectAndSaveWithDatetime ( three_image_not_match_matrix )
        similar_images = imageSearch(meta_data)
        analysisAndOutputLog(meta_data)
</pre>


##  Program Thread 3 - Record alignment and database communication
check database table, check-in and check-out record which is nearby the moving datetime - for map display
<pre>
sleep 3 second
dead loop until "if (!is_moving)"
begin_datetime = check_datetime--(seconds) loop until nothing to move (datetime as folder path = have movement)
end_datetime = check_datetime++(seconds) loop until nothing to move (datetime as folder path = have movement)
imagesWithPaths = get image between begin_datetime and end_datetime
SaveWithFolder( car_id, card_id, imagesWithPaths ) - paths, car_id, card_id
alignRecordAndMovement()
</pre>

##  Program Thread 4
combine too similiar object image and remove old files

