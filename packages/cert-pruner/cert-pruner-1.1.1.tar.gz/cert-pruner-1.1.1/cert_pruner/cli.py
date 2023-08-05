from argparse import ArgumentParser

from cert_pruner.pruner import CertificatePruner


def main():
    parser = ArgumentParser(
        description='Prune IAM Server Certificates that are not attached to an ELB',
        usage=
        '''
        Determine which certificates will be pruned:
            cert-pruner

        Look for unattached certificates at least 60 days old:
            cert-pruner --days 60
        
        Look for unattached, expired certificates:
            cert-pruner --days -1
        
        Perform the pruning operation:
            cert-pruner --delete
        '''
    )

    parser.add_argument(
        '--delete',
        '-d',
        help='Perform a dry run of the operations',
        action='store_true'
    )

    parser.add_argument(
        '--profile',
        '-p',
        help='AWS profile to use for authentication',
        default=None
    )

    parser.add_argument(
        '--days',
        '-n',
        help='Number of days old an newly uploaded, but unattached certificate must be to be '
             'considered for deletion. Defaults to 30 days. Set to -1 to disable and only delete expired certificates.',
        type=int,
        default=30
    )

    # Parse arguments
    options = parser.parse_args()

    # Create the pruner
    pruner = CertificatePruner(days_old=options.days, profile=options.profile)
    pruner.prune(delete=options.delete)


if __name__ == '__main__':
    main()
