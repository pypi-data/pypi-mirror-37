from ide import models


def visit_record(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        models.VisitCounts.today_add_one()
        # print(request.META)
        if request.path == '/ide/post/ip/':
            try:
                espip = models.EspIP.objects.get(
                    ip=request.META.get("REMOTE_ADDR"))

                if espip:
                    espip.set_esp_ip(request.GET.get('esp_ip', ''))
            except:
                # print('new espip')
                espip = models.EspIP(
                    ip=request.META.get("REMOTE_ADDR"), esp_ip=request.GET.get('esp_ip', ''))

            finally:
                espip.save()

        elif request.path == "/":
            visitor = models.Visitors(
                ip=request.META.get("REMOTE_ADDR"), url=request.path)
            visitor.save()
            
        return func(*args, **kwargs)

    return wrapper
