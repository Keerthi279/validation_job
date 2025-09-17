from db import fetch_data, run_update_query
from logger import logger

WAIT_TIME = 3600

def send_emails_for_completed_jobs():
    while True:
        logger.log("Started email job for completed jobs.")
        fetch_and_send_emails()


def fetch_and_send_emails():
    jobs = fetch_records("data_comp_request_master", ["*"], {"STATUS": "COMPLETED", "EMAIL_STATUS": "PENDING"})
    logger.log(f"Fetched {len(jobs)} jobs to send emails.")

    if len(jobs) == 0:
        logger.log("No jobs found. Exiting email job.")
        time.sleep(WAIT_TIME)

    for job in jobs:
        logger.log(f"Sending email for job ID: {job['id']}")
        response = send_email(job)
        if response:
            logger.log(f"Email sent for job ID: {job['id']}")
            result = update_email_status(job['id'])
            if result != -1: 
                logger.log(f"Updated email status for job ID: {job['id']} to SENT.")
            else:
                logger.log(f"Updated email status for job ID: {job['id']} failed.")
        else:
            logger.log(f"Failed to send the email for job ID: {job['id']}")

    logger.log("Email job completed.")


def update_email_status(job_id):
    update_sql = """
        UPDATE data_comp_request_master
        SET email_status = :EMAIL_STATUS
        WHERE id = :JOB_ID
    """
    
    update_params = {
        'EMAIL_STATUS': "SENT",
        'JOB_ID': job_id
    }

    return run_update_query(update_sql, update_params)


def send_email(job):
    logger.log("Triggered Job")

    return True


if __name__ == "__main__":
    send_emails_for_completed_jobs()
    print("Email job completed.")