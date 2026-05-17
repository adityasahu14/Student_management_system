from .models import Attendance

LOW_ATTENDANCE_THRESHOLD = 75

def calculate_attendance_percentage(student, subject, start_date=None, end_date=None):
    qs = Attendance.objects.filter(subject=subject, student=student)
    if start_date:
        qs = qs.filter(date__gte=start_date)
    if end_date:
        qs = qs.filter(date__lte=end_date)
    total_classes = qs.count()
    present_classes = qs.filter(status='present').count()
    if total_classes == 0:
        return 0
    return round((present_classes / total_classes) * 100, 2)

def get_cumulative_attendance(student, start_date=None, end_date=None):
    qs = Attendance.objects.filter(student=student)
    if start_date:
        qs = qs.filter(date__gte=start_date)
    if end_date:
        qs = qs.filter(date__lte=end_date)
    total = qs.count()
    present = qs.filter(status='present').count()
    if total == 0:
        return 0
    return round((present / total) * 100, 2)

def get_monthly_attendance(student, subject, month, year):
    return Attendance.objects.filter(
        student=student,
        subject=subject,
        date__month=month,
        date__year=year
    )
