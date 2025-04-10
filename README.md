
# Student Attendance Tracker

![Architecture diagram](https://i.imgur.com/m9aJre2.png)

This is the usage guide for my Student Attendance Tracker

---

## Prerequisites


    - Make sure you have at least one device set up
    (Guide in raspberry_pi/README.md)
    - Some excel files with classgroups
Excel format:
![Excel file format](https://i.imgur.com/vVOpJ99.png)
Make sure you have a title row (Cell A1) and you follow the header names from the image.



---
## Setting up classgroups

First off make sure you have at least one excel file ready like shown in the previous chapter.

![Classgroup overview](https://i.imgur.com/Go3V0kU.png)

To add a new classgroup to the system click the `Import classgroup` button. This will open the following page:

![Upload excel page](https://i.imgur.com/a5IE0Gh.png)

Here you can select the excel file of the classgroup you want to import. After clicking import classgroup it will load all the students from the file. If you go back to the classgroup overview page you will see your classgroup in the list and if you click open your classgroup you can check if all your students are in there:

![Classgroup overview](https://i.imgur.com/tZwgKaR.png)

---

## Configuring the schedule of a device

A device has a specific schedule of sessions. These sessions need to be scheduled before the attendance of a classgroup can be taken. Go to the scheduler page on the website and you will see:

![Device selection](https://i.imgur.com/6paNzTl.png)

Start of by selecting the classroom you want to manage the schedule for:

![](https://i.imgur.com/aDPy0bL.png)

Here you will see an overview of sessions already scheduled only for that classroom. 2 sessions can **not** be scheduled with an overlap. 

If you want to create a new session you click the `+ Add Session` button.

This will open up a form:
![Session form](https://i.imgur.com/xCJaf5C.png)

Here you can select the date, end- and starttime, classgroup and the classroom that the session needs to be created for.
Creating a session that overlaps with another session in that classroom is **not** possible
All the times in this form are in **Europe/Helsinki** time.

After clicking create session the session should be on the schedule:
![New session added](https://i.imgur.com/ZXfDHtL.png)

## Taking attendance for a session

If the device is correctly set up (Check the raspberry_pi/README.MD guide), you should not have to do any more setup to have the attendances working.
If the device is powered on, it will automatically start scanning when a session starts.

If you doubleclick on a session in the schedule you will be able to view able to see an overview off the students attending that session:
![Session overview](https://i.imgur.com/3JjMSDr.png)

To add attendance for a student all they have to do is scan their student id. They have the Tuudo app on their mobile phone. They should go to the QR-code overview but hold the following part in front of the camera:
![](https://i.imgur.com/7lEFYJv.png)

*If they scan more that does not matter, just make sure the Student Id is well visible to the camera*

The phone should be held about 8cm (3") away from the camera. Do not zoom in the screen.

If they scan it correctly they should be displayed as Present on the session overview (after a page refresh):

![](https://i.imgur.com/FYLS4Ns.png)





## Technical Details

| Name | Details |
| ------------- | ------------- |
| Single board computer | Raspberry Pi (3 and up)  |
| Camera  | Raspberry Pi AI Camera  |


## Todo

- Authentication and Authorization for teachers
- Add support for no session devices

