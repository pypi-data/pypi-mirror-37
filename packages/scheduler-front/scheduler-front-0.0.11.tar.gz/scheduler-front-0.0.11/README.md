# How to schedule a job easily

## Install the scheduler front

To install the scheduler run the code below in the commandline

````
pip install git@gitlab.criteois.com:j.gajardo/scheduler_front.git 
````

## Clone the scheduled jobs repo

### get the repo
Go to the repo where the scheduled jobs are hosted (at the time of this tutorial it is [latam automation](https://gitlab.criteois.com/c.camilli/latam_automations))
![alt text](img/01 latam automations.png)

### clone the repo

To clone the repo, run the code below in the commandline

````
git clone git@gitlab.criteois.com:c.camilli/latam_automations.git
````

![alt text](img/02 git clone.png)


### create a new branch

create a new branch with a descriptive name for your job to be scheduled

````
git branch new_cool_report
git checkout new_cool_report
````

![alt text](img/03 git branch.png)


## Create your scheduled job

### run the command to start the front end

run the code below in a command line

````
create-scheduled-job
````

![alt text](img/04 run.png)

### copy the address of your recently cloned automation folder
![alt text](img/05 automation folder.png)


### fill the form

![alt text](img/06 front01.png)
![alt text](img/07 front02.png)
![alt text](img/08 front03.png)

### check that your job has been created
![alt text](img/09 automation folder 02.png)


## Push the changes to the repo

### commit the changes
![alt text](img/10 commit.png)

### push the changes to the automation repo
![alt text](img/11 push.png)

### make a merge request
![alt text](img/12 merge01.png)

![alt text](img/13 merge02.png)

![alt text](img/14 merge03.png)
