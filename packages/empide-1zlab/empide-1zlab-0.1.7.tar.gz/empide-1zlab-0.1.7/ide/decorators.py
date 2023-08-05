from ide import models


def visit_record(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        models.VisitCounts.today_add_one()
        # print(request.META)
        visitor = models.Visitors(
            ip=request.META.get("REMOTE_ADDR"), url=request.path)
        visitor.save()

        return func(*args, **kwargs)

    return wrapper
