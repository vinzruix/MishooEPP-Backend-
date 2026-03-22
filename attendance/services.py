from attendance.models import WorkerArrival


def register_attendance_successfully(worker, image):
    attendance = WorkerArrival()
    attendance.worker = worker
    attendance.arrival_image = image
    attendance.save()
