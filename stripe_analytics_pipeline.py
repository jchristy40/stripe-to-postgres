from typing import Optional, Tuple
from datetime import datetime
import argparse
from dotenv import load_dotenv

import dlt
from pendulum import DateTime, from_format, timezone
from stripe_analytics import (
    ENDPOINTS,
    INCREMENTAL_ENDPOINTS,
    incremental_stripe_source,
    stripe_source,
)

PIPELINE_NAME = 'stripe_to_postgres'
DESTINATION_NAME = 'postgres'
DEFAULT_DATASET_NAME = 'dlt_stripe'


def full_load(
        endpoints: Tuple[str, ...] = ENDPOINTS + INCREMENTAL_ENDPOINTS,
        start_date: Optional[DateTime] = None,
        end_date: Optional[DateTime] = None,
        dataset_name=DEFAULT_DATASET_NAME
) -> None:
    pipeline = dlt.pipeline(
        pipeline_name=PIPELINE_NAME,
        destination=DESTINATION_NAME,
        dataset_name=dataset_name,
    )
    source = stripe_source(
        endpoints=endpoints, start_date=start_date, end_date=end_date
    )
    load_info = pipeline.run(source)
    print(load_info)


def incremental_load(
        endpoints: Tuple[str, ...] = INCREMENTAL_ENDPOINTS,
        initial_start_date: Optional[DateTime] = None,
        end_date: Optional[DateTime] = None,
        dataset_name=DEFAULT_DATASET_NAME
) -> None:
    pipeline = dlt.pipeline(
        pipeline_name=PIPELINE_NAME,
        destination=DESTINATION_NAME,
        dataset_name=dataset_name,
    )
    source = incremental_stripe_source(
        endpoints=endpoints,
        initial_start_date=initial_start_date,
        end_date=end_date,
    )
    load_info = pipeline.run(source)
    print(load_info)


def cli():
    parser = argparse.ArgumentParser(description="CLI for loading data from Stripe to PostgreSQL.")
    parser.add_argument(
        "--dataset-name",
        type=str,
        required=False,
        help=f"Name of the schema where the data will be stored. Default: {DEFAULT_DATASET_NAME}",
        default=DEFAULT_DATASET_NAME
    )
    subparsers = parser.add_subparsers(dest="pipeline_type")

    # Full Load Parser
    parser_full_load = subparsers.add_parser(
        "full_load",
        help="Reloads the data from all the endpoints using their primary key. "
             "If start and end date are passed, it loads only data that was created during the specified period"
    )
    parser_full_load.add_argument("--start-date", type=str, help="Start date in YYYY-MM-DD format (Included)")
    parser_full_load.add_argument("--end-date", type=str, help="End date in YYYY-MM-DD format (Not included)")
    parser_full_load.add_argument("--skip-incremental-endpoints", action="store_true",
                                  help=f"Skip loading non-editable (incremental) endpoints: "
                                       f"{', '.join(INCREMENTAL_ENDPOINTS)}. "
                                       "Useful if you load these endpoints using 'incremental_load' option.")

    # Incremental Load Parser
    parser_incremental_load = subparsers.add_parser(
        "incremental_load",
        help=f"Load data incrementally using non-editable endpoints: {', '.join(INCREMENTAL_ENDPOINTS)}"
    )
    parser_incremental_load.add_argument(
        "--initial_start_date",
        type=str,
        help="An optional parameter that specifies the initial value for the incremental pipeline. "
             "If parameter is not None, then load only data that were created after initial_start_date on the "
             "first run. Format: YYYY-MM-DD"
    )
    parser_incremental_load.add_argument("--end-date",
                                         type=str,
                                         help="An optional end date to limit the data retrieved. Format: YYYY-MM-DD"
                                         )
    args = parser.parse_args()

    if args.pipeline_type == "full_load":
        start_date = from_format(args.start_date, "YYYY-MM-DD").in_tz("UTC") if args.start_date else None
        end_date = from_format(args.end_date, "YYYY-MM-DD").in_tz("UTC") if args.end_date else None
        endpoints = ENDPOINTS
        if not args.skip_incremental_endpoints:
            endpoints = endpoints + INCREMENTAL_ENDPOINTS
        full_load(endpoints=endpoints, start_date=start_date, end_date=end_date, dataset_name=args.dataset_name)

    elif args.pipeline_type == "incremental_load":
        initial_start_date = from_format(args.initial_start_date, "YYYY-MM-DD").in_tz("UTC") \
            if args.initial_start_date else None
        end_date = from_format(args.end_date, "YYYY-MM-DD").in_tz("UTC") if args.end_date else None
        incremental_load(
            initial_start_date=initial_start_date,
            end_date=end_date,
            dataset_name=args.dataset_name
        )

    else:
        parser.print_help()


if __name__ == "__main__":
    load_dotenv()
    cli()