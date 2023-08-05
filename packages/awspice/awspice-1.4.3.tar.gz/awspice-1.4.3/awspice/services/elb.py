# -*- coding: utf-8 -*-
from base import AwsBase
import dns.resolver


class ElbService(AwsBase):
    '''
    Class belonging to the Load Balancers service.
    '''

    loadbalancer_filters = {
        'domain': '',
        'tagname': '',
        'cname': '',
    }

    @classmethod
    def _get_cname_from_domain(cls, domain):
        '''
        Get CNAME from a domain

        Raises:
            dns.resolver.NXDOMAIN: DNS Name not registered.
            dns.resolver.NoAnswer: DNS Name not found.

        Return:
            str: String with DNS Canonical Name.
        '''
        try:
            cname = str(dns.resolver.query(domain, "CNAME")[0]).rstrip('.')
            if 'aws.com' not in cname: raise ValueError('Domain %s is not in AWS' % domain)
            return cname
        except (dns.resolver.NXDOMAIN):
            raise dns.resolver.NXDOMAIN("Couldn't find any records(NXDOMAIN)")
        except (dns.resolver.NoAnswer):
            raise dns.resolver.NoAnswer("Couldn't find any records (NoAnswer)")


    def get_loadbalancers(self, regions=[]):
        '''
        Get all Elastic Load Balancers for a region

        Args:
            regions (list): Regions where to look for this element

        Returns:
            LoadBalancers (list): List of dictionaries with the load balancers requested
        '''
        results = list()
        regions = self.parse_regions(regions=regions)
        for region in regions:
            self.change_region(region['RegionName'])

            elbs = self.client.describe_load_balancers()['LoadBalancerDescriptions']
            results.extend(self.inject_client_vars(elbs))

        return results


    def get_loadbalancer_by(self, filter_key, filter_value, regions=[]):
        '''
        Get a load balancer for a region that matches with filter

        Args:
            filter_key (str): Name of the filter
            filter_value (str): Value of the filter
            regions (list): Regions where to look for this element

        Raises:
            dns.resolver.NXDOMAIN: DNS Name not registered.
            dns.resolver.NoAnswer: DNS Name not found.

        Return:
            LoadBalancer (dict): Dictionary with the load balancer requested
        '''
        self.validate_filters(filter_key, self.loadbalancer_filters)

        if filter_key == 'tagname':
            for region in self.parse_regions(regions=regions):
                self.change_region(region)
                elbs = self.client.describe_load_balancers(LoadBalancerNames=[filter_value])
                elbs = elbs['LoadBalancerDescriptions']

        elif filter_key == 'domain' or filter_key == 'cname':

            if filter_key == 'domain':
                cname = self._get_cname_from_domain(filter_value)
            else:
                cname = filter_value

            self.change_region(cname.split('.')[1])
            elbs = [elb for elb in self.get_loadbalancers() if elb['DNSName'].lower() == cname.lower()]

        if elbs:
            return elbs[0]
        return None


    def __init__(self):
        AwsBase.__init__(self, 'elb')
