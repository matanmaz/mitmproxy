#!/usr/bin/env python2.7
'''
Replay server for HTTP.
See --help for usage, README.md for solutions to common problems.
'''

from twisted.internet import reactor
import Queue
import sys

sys.path.append('../lib')
import mitmproxy


def main():
    '''
    Parser options, open and read log file, start replay server
    '''
    (opts, _) = mitmproxy.replay_option_parser(8080)

    if opts.inputfile is None:
        print "Need to specify an input file."
        sys.exit(1)
    else:
        log = mitmproxy.Logger()
        if opts.logfile is not None:
            log.open_log(opts.logfile)

        serverq = Queue.Queue()
        clientq = Queue.Queue()
        clientfirst = None

        mitmproxy.logreader(opts.inputfile, serverq, clientq, clientfirst)

        sys.stderr.write(
            'Server running on localhost:%d\n' % opts.localport)
        factory = mitmproxy.ReplayServerFactory(
            log, (serverq, clientq), opts.delaymod, clientfirst)
        reactor.listenTCP(opts.localport, factory)
        reactor.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
