from flask import request, session
from app import db
from app import app, executor
from app import models

from app import email_template

import time
from datetime import date

from send_email import send_message
from app import send_generated_files

from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
import pytz

def payment_received():

    task_id = send_generated_files.background_runner.retrieve_drive_data_asynch()

    while send_generated_files.background_runner.task_status(task_id) != "completed":
        pass

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
        
        send_message(request.email, "AAAAAAAAAAAA PAYMENT SLIP RECEIVED", "TEST AAAAA")

        current_dt = datetime.now(pytz.timezone('Singapore')).replace(microsecond = 0)

        request.payment_date = current_dt
        db.session.commit()



