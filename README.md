# About

At Verkada you will be required to apply your knowledge and skills to continually expand and scale the infrastructure that underpins our applications. This assignment is a miniaturized example of a real system that we have to communicate with our cameras. Your goal is to take some existing code and change, adapt, stack and modify it to meet the needs of a scalable system.

# Initial state

Our initial system is functional but can't scale beyond a single process. Let's look at it in more detail.

It has three endpoints. The first endpoint is a long poll endpoint for sending requests to the camera. The second endpoint is a response endpoint for sending responses back from camera. The third endpoint is an app-facing endpoint for requesting and receiving the camera response.

Here is the API:

`GET /camera/accept/${cameraId}`

`PUT /camera/response/${cameraId}/${requestId}`

`GET /app/request/${cameraId}`

The initial system can only work in a single process because it uses a blocking queue for inter-thread communication and all cameras and apps need to connect to that same process.

# Desired state

We want to adapt the software and the stack so that there is NO single point of failure or vertically scaled component. It should theoretically be able to handle an unlimited number of cameras. Although a fully deployed system would of course have auto scaling, it is okay to set fixed parameters for the number of each component deployed, as long as there is no real reason it could not be increased arbitrarily.

You can assume that an infinitely scalable dumb round-robin DNS or TCP load balancer exists in front of whatever you have.


