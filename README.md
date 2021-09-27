
## Intelligent Pothole Detection
## Overview

This is a project that automates detection of potholes on poor quality roads using an iOS app and AWS Lambda Functions. The iOS app is used to collect data from an iPhone placed in a moving vehicle by tracking its location, accelerometer and gyroscope readings. One screen on the app tracks the movement data, and on the other, another person sitting in the passenger seat annotates every time a pothole is encountered against a timestamp. Timestamps from both sets are compared and used to combine the data.


<p class = "aligncenter"
<img src="https://github.com/aneeshjain/Pothole-Detection/blob/master/pics/App_screens.png" width="600">
</p>
<style>
.aligncenter {
    text-align: center;
}
</style>


First this collected data is used to train a model that facilitates pothole detection. The model is deployed to AWS and then realtime data is sent to the model for inferencing when a user is driving. 


<img src="https://github.com/aneeshjain/Pothole-Detection/blob/master/pics/Process%20Flow.jpg" width="600" class="center">


This is used to create a map of potholes which can be displayed to all users so that they can effectively plan their route.

<img src="https://github.com/aneeshjain/Pothole-Detection/blob/master/pics/map.png" width="600" class="center">


#### The repository has the following directory structure contains the following files and directories and files:

* **AccelWithUpload** - This folder contains the Swift code for the iOS app that track the gyroscope and accelerometer data and uploads the csv file to an AWS S3 bucket.
* **inferencing_lambda_deployment_pkg** - This is the deployment package for the AWS Lambda function that inferences the model for pothole predictions
* **model** - contains the final deployed model
* **pre_processing_lambda_deployment_pkg** - This is the deployment package for the AWS Lambda function that pre-processes that data uploaded by the iOS app
* **pre_processed_data** - Contains a sample of the data after it has been pre-processed
* **raw_data** - Contains a sample of the raw data collected by the iOS app
* **utils** - Contains some utility functions


