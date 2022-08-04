import json
from datetime import datetime
from datetime import timedelta
from lib.resy import Resy
import time

resy_api_key = ""
resy_auth_token = ""

day = datetime.now() + timedelta(days=30)
party_size = 2
venue_id = 975

resy = Resy(resy_api_key, resy_auth_token)

def attemptBooking():
    reservations = resy.findReservations(day, party_size, venue_id)
    if reservations == []:
        print("No reservations available.")
        return False
    print("Got One!!!")
    
    reservationDetail = resy.getReservationDetails(
        config_id = reservations[0]['config']['token'],
        day = day,
        party_size= party_size
    )

    for payment_method in reservationDetail['user']['payment_methods']:
        if payment_method['is_default']:
            payment_method_id = payment_method['id']
            break

    booking = resy.bookReservation(
        book_token= reservationDetail['book_token']['value'],
        payment_method_id= payment_method_id
    )
    print("Reservation Confirmed!")
    return True

bookingConfirmed = False

while not bookingConfirmed:
    nextHour = datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    print ("Next execution at " + nextHour.strftime("%H:%M"))
    timeToWait = nextHour - datetime.now()
    secondsToWait = timeToWait.total_seconds()
    print(f"Sleeping for {secondsToWait} seconds")
    time.sleep(secondsToWait)
    print("Lets get this bread")
    while not bookingConfirmed:
        bookingConfirmed = attemptBooking()
        stopTime = nextHour + timedelta(seconds=15)
        if datetime.now() > stopTime:
            break
        time.sleep(0.5)