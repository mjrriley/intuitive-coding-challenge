# Code Challenge

This my (Matthew Riley) solution to the coding challenge.

## Build

To build the project:
    make

Build can be cleaned by running:
    make clean

## PEP 8 Checker

To verify code is PEP 8 compliant:
    make style

## Unit Test

To run tests:
    make test

I was unable to create unit tests for client.py in time.

## Testing Responsiveness

To verify that status request were responsive and not blocking,
I created client.py and server.py to communication with each other.
By running server.py first and then client.py, you will see the
server will write parameters without block status requests.

For convenience, test\_async.sh was provided to run the scripts
noted above
