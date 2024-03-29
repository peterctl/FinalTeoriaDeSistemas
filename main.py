#!/usr/bin/env python3

from control import config
from control.guards import conn_guard, cache_guard
from control.scripts import *

def main():
    with cache_guard(config.MEMCACHED_HOST) as cache:
        # Clear all keys to run the simulation
        cache.flush_all()

        with conn_guard(**config.MYSQL_CONFIG) as conn:
            # Get initial values
            setpoint = ask_for_setpoint()
            record_count = get_record_count(conn)

            # Main loop which emulates a do while loop
            iteration = 0
            while True:
                tests, cache_hits, db_hits = test_convergence(cache, record_count)

                cache_hit_percentage = cache_hits / tests
                db_hit_percentage = db_hits / tests

                print("Results for iteration %s" % iteration)
                print("    setpoint               = %s" % setpoint)
                print("    tests_done             = %s" % config.TESTS)
                print("    record_count           = %s" % record_count)
                print("    db_hits                = %s" % db_hits)
                print("    db_hit_percentage      = %s" % db_hit_percentage)
                print("    cache_hits             = %s" % cache_hits)
                print("    cache_hit_percentage   = %s" % cache_hit_percentage)
                print("    error                  = %s" % (setpoint - cache_hit_percentage))
                print()

                if cache_hit_percentage >= setpoint:
                    break
                else:
                    iteration += 1
                    add_to_cache(conn, cache, record_count)

if __name__ == "__main__":
    main()
