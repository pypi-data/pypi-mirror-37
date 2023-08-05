import datetime

from django.core.management.base import BaseCommand

from shutter.gps import get_estimate, get_lat_lon_time_from_gpx
from shutter.models import Photo


class Command(BaseCommand):
    help = 'Import user gpx file.'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int)
        parser.add_argument('gpx')
        parser.add_argument('--offset', type=int,
                            help="Timezone offset in hours")
        parser.add_argument('--noop', action='store_true',
                            help='Do not save estimates to DB.')
        parser.add_argument('--delta', type=int, default=1000,
                            help="Max amount of seconds photo time can differ from closest GPX point.")

    def handle(self, *args, **options):

        user_id = options.get('user_id')
        gpx_path = options.get('gpx')
        offset = options.get('offset')
        noop = options.get('noop')
        delta = options.get('delta')
        points = get_lat_lon_time_from_gpx(gpx_path)


        # todo: use offset in start_date and end_date
        start_date = points[0][0].date()
        end_date = points[-1][0].date()

        photos = Photo.objects.filter(user_id=user_id, date_taken__gte=start_date, date_taken__lte=end_date)

        self.stdout.write(
            f'GPX start: {start_date}\n'
            f'GPX end: {end_date}\n'
            f'Num photos in that range: {len(photos)}\n'
            f'Using delta limit of {delta} seconds\n'
        )
        num_imported = 0
        num_failed = 0

        for photo in photos:
            photo_time = datetime.datetime.combine(photo.date_taken, photo.time_taken)
            if offset:
                photo_time += datetime.timedelta(hours=offset)
            try:
                estimate = get_estimate(time=photo_time, points=points, max_dt=delta)
            except ValueError:
                num_failed += 1
                continue
            else:

                lat, lng, bearing, ele = estimate
                photo.latitude = lat
                photo.longitude = lng
                if not noop:
                    photo.save()
                num_imported += 1

        self.stdout.write(
            f"Number of photos with new geodata: {num_imported}\n"
            f"Number failed: {num_failed}\n"
        )
