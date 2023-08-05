from datetime import datetime, timedelta

import boto3
import pytz


class CertificatePruner(object):

    def __init__(self, days_old, profile=None):
        self.profile = profile
        self.session = boto3.Session(profile_name=profile)
        self._iam_client = self.session.client('iam')
        self._elb_client = self.session.client('elb')
        self._elbv2_client = self.session.client('elbv2')
        self.days_old = days_old

    def _list_elb_certificates(self):
        """
        List all certificates ARNs on all classic ELBs

        :return: Set of certificate ARNs
        :rtype: set of str
        """
        marker = None
        certificates = set()

        while True:
            # Fetch the data
            if marker:
                lbs = self._elb_client.describe_load_balancers(Marker=marker)
            else:
                lbs = self._elb_client.describe_load_balancers()

            # Loop through results and save all certificates attached to a listener
            for lb in lbs['LoadBalancerDescriptions']:
                for listener_description in lb['ListenerDescriptions']:
                    # Check if this listener has an associated certificate
                    cert = listener_description['Listener'].get('SSLCertificateId')
                    if cert:
                        certificates.add(cert)

            # Check for the next marker
            if lbs.get('NextMarker'):
                marker = lbs['NextMarker']
            else:
                break

        return certificates

    def _list_elbv2_certificates(self):
        """
        List all certificate ARNs on all ELBv2 load balancers

        :return: Set of certificate ARNs
        :rtype: set of str
        """
        marker = None
        certificates = set()

        while True:
            # Fetch the data
            if marker:
                lbs = self._elbv2_client.describe_load_balancers(Marker=marker)
            else:
                lbs = self._elbv2_client.describe_load_balancers()

            # Loop through results and save all certificates attached to a listener
            for lb in lbs['LoadBalancers']:
                for cert in self._get_elbv2_listener_certificates(lb['LoadBalancerArn']):
                    certificates.add(cert)

            # Check for the next ALB marker
            if lbs.get('NextMarker'):
                marker = lbs['NextMarker']
            else:
                break

        return certificates

    def _get_elbv2_listeners(self, arn):
        """
        Get all listener ARNs for a particular ELBv2 load balancer

        :param arn: Load balancer ARN
        :return: Set of listener ARNs
        :rtype: set of str
        """
        listeners = list()
        marker = None

        while True:
            # Fetch the data
            if marker:
                listener_descriptions = self._elbv2_client.describe_listeners(
                    LoadBalancerArn=arn,
                    Marker=marker
                )
            else:
                listener_descriptions = self._elbv2_client.describe_listeners(
                    LoadBalancerArn=arn
                )

            # Loop through results and save all listener arns
            for listener in listener_descriptions['Listeners']:
                listeners.append(listener['ListenerArn'])

            # Check for the next listener marker
            if listener_descriptions.get('NextMarker'):
                marker = listener_descriptions['NextMarker']
            else:
                break

        return listeners

    def _get_elbv2_listener_certificates(self, arn):
        """
        Get all unique certificates ARNs for a given ELBv2 listener

        :param arn: Listener ARN
        :return: Set of certificate ARNs
        :rtype: set of str
        """
        certificates = set()

        for listener_arn in self._get_elbv2_listeners(arn):

            marker = None

            while True:
                # Fetch the data
                if marker:
                    certificate_descriptions = self._elbv2_client.describe_listener_certificates(
                        ListenerArn=listener_arn,
                        Marker=marker
                    )
                else:
                    certificate_descriptions = self._elbv2_client.describe_listener_certificates(
                        ListenerArn=listener_arn
                    )

                # Loop through results and save all certificates attached to a listener
                for cert in certificate_descriptions.get('Certificates', []):
                    certificates.add(cert['CertificateArn'])

                # Check for the next listener marker
                if certificate_descriptions.get('NextMarker'):
                    marker = certificate_descriptions['NextMarker']
                else:
                    break

        return certificates

    def _list_iam_certificates(self):
        """
        List all IAM server certificate ARNs

        :return: List of certificate dictionaries
        :rtype: list of dict
        """
        certificates = list()
        marker = None

        while True:
            # Fetch the data
            if marker:
                certs = self._iam_client.list_server_certificates(Marker=marker)
            else:
                certs = self._iam_client.list_server_certificates()

            # Loop through results
            for cert in certs['ServerCertificateMetadataList']:
                certificates.append(cert)

            # Check for the next marker
            if certs.get('Marker'):
                marker = certs['Marker']
            else:
                break

        return certificates

    def prune(self, delete=False):
        """
        Perform the certificate pruning operation

        :param bool delete: Whether to perform a dry run or actually start the deletion
        """
        attached_certs = set()
        prune_certs = []

        # Find all attached certificates on ELBs
        for cert in self._list_elb_certificates():
            attached_certs.add(cert)

        # Find all attached certificates on ALBs
        for cert in self._list_elbv2_certificates():
            attached_certs.add(cert)

        # Check each IAM certificate to see if it is in the attached certificates set
        print('Unattached Certificates:')
        for cert in self._list_iam_certificates():
            if cert['Arn'] not in attached_certs:
                prune_certs.append(cert)
                print('\tUNATTACHED: Expiring %s - %s' % (cert['Expiration'], cert['ServerCertificateName']))

        print('-' * 80)

        # Perform the deletion
        delete_certs = []
        keep_certs = []
        for cert in prune_certs:

            # Check if the certificate has already expired or if it was uploaded more than days_old days ago
            now = datetime.now(pytz.utc)
            expired = cert['Expiration'] < now
            if expired:
                expire_word = 'Expired '
            else:
                expire_word = 'Expiring'

            if expired or (self.days_old >= 0 and now - cert['UploadDate'] > timedelta(days=self.days_old)):
                delete_certs.append({'cert': cert, 'expire_word': expire_word})
            else:
                keep_certs.append({'cert': cert, 'expire_word': expire_word})

        # Sort the results
        keep_certs = sorted(keep_certs, key=lambda x: x['cert']['UploadDate'])
        delete_certs = sorted(delete_certs, key=lambda x: x['cert']['Expiration'])

        print('Certificates Kept:')
        for cert in keep_certs:
            print('\t%sKEEPING: Uploaded <= %d days ago: %s, %s %s - %s' % (
                '[DRY RUN] ' if not delete else '',
                self.days_old,
                cert['cert']['UploadDate'],
                cert['expire_word'],
                cert['cert']['Expiration'],
                cert['cert']['ServerCertificateName']
            ))
        print('')

        print('Certificates Deleted:')
        for cert in delete_certs:
            if delete:
                # Perform the deletion
                self._iam_client.delete_server_certificate(
                    ServerCertificateName=cert['ServerCertificateName']
                )

                print('\tDELETED: Uploaded %s, %s %s - %s' % (
                    cert['cert']['UploadDate'],
                    cert['expire_word'],
                    cert['cert']['Expiration'],
                    cert['cert']['ServerCertificateName']
                ))
            else:
                print('\t[DRY RUN] DELETE: Uploaded %s, %s %s - %s' % (
                    cert['cert']['UploadDate'],
                    cert['expire_word'],
                    cert['cert']['Expiration'],
                    cert['cert']['ServerCertificateName']
                ))
        print('')

        print('Total certificates: %d' % len(prune_certs))
        print('Certificates kept: %d' % len(keep_certs))
        print('Certificates deleted: %d' % len(delete_certs))
