from argparse import ArgumentParser

from log_parser.connected_hostnames import get_connected_hostnames
from log_parser.unlimited_parser import unlimited


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("input_file", type=str, help="Input file to read")
    subparsers = parser.add_subparsers(help="Function to execute", dest="function")
    connected_parser = subparsers.add_parser("connected")
    connected_parser.add_argument("init_timestamp", type=int, help="The beginning of the period")
    connected_parser.add_argument("end_timestamp", type=int, help="The end of the period")
    connected_parser.add_argument("hostname", type=str, help="The host to check connections")
    connected_parser.add_argument("-m", "--multithreading", help="Enable multithreading", action="store_true")
    connected_parser.add_argument("-w", "--workers", type=int, help="Number of workers to use")
    connected_parser.add_argument("-b", "--batch-size", type=int, help="The batch size")
    unlimited_parser = subparsers.add_parser("unlimited")
    unlimited_parser.add_argument("origin_host", type=str, help="Origin host to check")
    unlimited_parser.add_argument("end_host", type=str, help="Destination host to check")
    unlimited_parser.add_argument("-i", "--init_timestamp", type=int, help="The beginning to start check")
    args = parser.parse_args()
    if args.function == "connected":
        get_connected_hostnames(
            args.input_file, args.init_timestamp, args.end_timestamp, args.hostname,
            use_multithread=args.multithreading, workers=args.workers, batch_size=args.batch_size
        )
    if args.function == "unlimited":
        unlimited(args.input_file, args.origin_host, args.end_host, init_timestamp=args.init_timestamp)
