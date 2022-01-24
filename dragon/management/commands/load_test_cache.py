import random
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.cache import caches


class Command(BaseCommand):
    help = "Loads cache with test objects"

    def add_arguments(self, parser):
        parser.add_argument("-c", "--cache", nargs="+", type=str)
        parser.add_argument("-k", "--keys", type=int, default=50)

    def handle(self, *args, **options):
        caches_to_populate = []
        test_data_file = settings.BASE_DIR / "dragon" / "management" / "commands" / "random_words.txt"

        with open(test_data_file, "r", encoding='utf-8') as fh:
            self.stdout.write(f"Reading test data from file")
            test_data = fh.read().split("\n")

        if "caches" in options:
            caches_to_populate = [(c, caches[c]) for c in options["caches"] if c in settings.CACHES.keys()]
        else:
            caches_to_populate = [(c, caches[c]) for c in settings.CACHES.keys()]
        
        self.stdout.write(
            f"Populating {len(caches_to_populate)} caches with {len(test_data)} random words of test data: " +
            ", ".join([c[0] for c in caches_to_populate])
        )

        for cache_name, cache in caches_to_populate:
            self.stdout.write(f"Populating cache '{cache_name}' with {options['keys']} items")

            try:
                for _ in range(options["keys"]):
                    cache.set(
                        random.choice(test_data),
                        random.choice(test_data)
                    )
            except Exception as e:
                self.stderr.write(f"Unable to populate {cache_name} due to error: {e}")
