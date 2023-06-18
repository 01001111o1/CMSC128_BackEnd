from flask import request, session, redirect
from app import db
from app import app, executor
from app import models
from app import email_template
import time
from datetime import date
from send_email import send_message
from app import background_runner
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
import pytz
from app import email_template
from GoogleDriveAutomation import retrieve_drive_data
"""

payment_received: function

Function that first retrieves all subfolders from the designated google drive that contains all proof of payments. 
Then, for every ID in that list of subfolders, The payment date for each of those is updated and an appropriate email is sent
as a response.

"""

def payment_received():

    retrieve_drive_data()

    with open('payment_list.txt') as f:
        session["payment_id"] = [line for line in f.readlines()]

    if len(session["payment_id"]) == 0:
        return redirect(session["url"])

    session["payment_id"] =  [line.replace('\n', '') for line in session["payment_id"]]

    for order_number in session["payment_id"]:
        try:
            request = models.Request.query.get(order_number)  
        except NoResultFound:
            request = None
            continue

        current_dt = datetime.now(pytz.timezone('Singapore')).replace(microsecond = 0)

        request.payment_date = current_dt
        db.session.commit()

        subject, content = email_template.email_template(request.first_name, order_number, "payment_received")        

        send_message(request.email, subject, content)