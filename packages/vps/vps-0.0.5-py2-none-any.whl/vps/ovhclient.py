#!/usr/bin/env python2

import argparse
import datetime
import logging
import json
import ovh
import os
import sys
import time

DRY_RUN=False

class OvhClient(ovh.Client):
   def __init__(self, *args, **kwargs):
      super(OvhClient,self).__init__(*args, **kwargs)

   def get(self, *args, **kwargs):
      try:
         return super(OvhClient,self).get(*args, **kwargs)
      except ovh.exceptions.APIError as err:
         argList = list(args)
         for key in kwargs:
            value = kwargs[key]
            if isinstance(kwargs[key], str):
               # Wrap single quotes around strings
               value = "'{}'".format(value)
            argList.append('{}={}'.format(key,value))
         argStr=','.join(argList)
         logging.exception("get({}) exception:\n{}".format(argStr,err))
         raise
   def post(self, *args, **kwargs):
      try:
         return super(OvhClient,self).post(*args, **kwargs)
      except ovh.exceptions.APIError as err:
         argList = list(args)
         for key in kwargs:
            argList.append('{}={}'.format(key,kwargs[key]))
         argStr=','.join(argList)
         logging.exception("post({}) exception:\n{}".format(argStr,err))
         raise
   def put(self, *args, **kwargs):
      try:
         return super(OvhClient,self).put(*args, **kwargs)
      except ovh.exceptions.APIError as err:
         argList = list(args)
         for key in kwargs:
            argList.append('{}={}'.format(key,kwargs[key]))
         argStr=','.join(argList)
         logging.exception("put({}) exception:\n{}".format(argStr,err))
         raise
   def delete(self, *args, **kwargs):
      try:
         return super(OvhClient,self).delete(*args, **kwargs)
      except ovh.exceptions.APIError as err:
         argList = list(args)
         for key in kwargs:
            argList.append('{}={}'.format(key,kwargs[key]))
         argStr=','.join(argList)
         logging.exception("delete({}) exception:\n{}".format(argStr,err))
         raise

   def getServerTimestamp(self):
      return int(self.get('/auth/time', _need_auth=False))

   def getCK(self, perms, endpoint, recursive):

      ck = super(OvhClient,self).new_consumer_key_request()
      if recursive:
         ck.add_recursive_rules(perms, endpoint)
      else:
         ck.add_rules(perms, endpoint)

      # Request token
      validation = ck.request()

      print("You must visit this URL to authenticate the key:\n{}".format(validation['validationUrl']))
      return validation['consumerKey']

   # Returns JSON list of existing service dicts
   def vpsGetServices(self):
      svcs = self.get('/vps')

      # Get details on VPSs
      details = []
      for s in svcs:
         detail = self.get('/vps/{}'.format(s))

         # Ignore stopped/expired services
         if detail['state'] != 'stopped':
            ips = self.get('/vps/{}/ips'.format(s))
            for ip in ips:
               # Pick out v4 IP address
               ipDetails = self.get('/vps/{}/ips/{}'.format(s,ip))
               if ipDetails['version'] == 'v4':
                  # NOTE: assuming only one v4 IP
                  detail['ip'] = ip
                  break
            details.append(detail)

      return details

   def deleteCart(self, cartId):
      self.delete('/order/cart/{}'.format(cartId))

   # Gets an existing cart with `description` or creates a new one
   def getCart(self, description):

      # TODO don't just delete existing cart with this description
      existing = self.get('/order/cart', description=description)
      if existing:
         logging.warning("Existing cart with description {}".format(description))
         for cart in existing:
            self.deleteCart(cart)

      # Get a new one
      expireTime = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(weeks=1)
      result = self.post('/order/cart',
          description=description,
          expire=expireTime.isoformat(timespec='seconds'),
          ovhSubsidiary='CA',
      )
      cartId = result['cartId']
      return cartId

   def getCatalog(self, product):
      catalog = self.get('/order/catalog/formatted/{}'.format(product),
                           _need_auth=False,
                           ovhSubsidiary='CA')
      return catalog

   # Returns list of VPS offers for this cart
   def getOffers(self, product, cartId=None):
      if not cartId:
         cartId = self.getCart('offers')

      offers = self.get('/order/cart/{}/{}'.format(cartId, product), _need_auth=False)
      return offers

   def vpsFindOffer(self, maxPrice, **minSpecs):
      catalog = self.getCatalog('vps')
      # This will throw if no 'ssd' family
      ssdPlans = next(family['plans'] for family in catalog['plansFamily'] if family['family'] == 'ssd')

      # Find candidate models
      candidates=[]
      for plan in ssdPlans:
         candidate=True

         # Compare plan specs to minimum required specs
         planSpecs = plan['details']['product']['technicalDetails']
         for k,minValue in minSpecs.items():
            planValue=0
            if k in planSpecs:
               planValue = float(''.join(filter(lambda c: c.isdigit() or c=='.', planSpecs[k])))
            if planValue < minValue:
               candidate=False
               break

         if candidate:
            candidates.append(plan)

      # Sort candidates' 1-month pricings
      for c in candidates:
         monthlyPricing = [pricing for pricing in c['details']['pricings']['default'] if pricing['interval'] == 1]
         c['details']['pricings']['default'] = sorted(monthlyPricing, key=lambda pricing: pricing['price']['value'])
      # Sort candidates by best pricing
      candidates = sorted(candidates, key=lambda candidate: candidate['details']['pricings']['default'][0]['price']['value'])

      # Find corresponding offer
      offers = self.getOffers('vps')
      offer = None
      for plan in candidates:
         offer = next(iter([o for o in offers if o['planCode']==plan['planCode']]), None)
         if offer:
            break
      if not offer:
         logging.error("Could not find offer matching 1 of {} candidates".format(len(candidates)))
         return None,None

      # Get cheapest price for this planCode
      deal = sorted(offer['prices'], key=lambda k: k['price']['value'])[0]
      if deal['price']['value'] > maxPrice:
         # Too expensive
         logging.error('Cannot fulfill {}. Price {} > {}, '.format(offer['planCode'], deal['price']['value'], maxPrice))
         return None,None

      return offer['planCode'],deal['pricingMode']

   # NOTE: it seems only prepaid account (ovhAccount) works as payment method via API
   def completeOrder(self, orderId, paymentMean='ovhAccount', paymentMeanId=None):
      logging.info("Pay for order {}".format(orderId))

      try:
         self.post('/me/order/{}/payWithRegisteredPaymentMean'.format(orderId), paymentMean=paymentMean, paymentMeanId=paymentMeanId)
         return True
      except:
         return False

   def vpsOrder(self, qty, price, **minSpecs):
      global DRY_RUN

      planCode,pricingMode = self.vpsFindOffer(price)
      if not planCode or not pricingMode:
         logging.error("Could not find a suitable model. price={}, {}".format(price, ', '.join(['{}={}'.format(k,v) for k,v in minSpecs.items()])))
         return
      logging.info("Ordering {}x {} (pricingMode {})".format(qty, planCode, pricingMode))

      cartId = self.getCart('order')
      logging.debug("cartId: {}".format(cartId))

      # Order VPS for one month
      result = self.post('/order/cart/{}/vps'.format(cartId),
                           duration='P1M',
                           planCode=planCode,
                           pricingMode=pricingMode,
                           quantity=1)
      logging.debug(json.dumps(result,indent=4))
      itemId = result['itemId']

      # Configure VPS
      config = self.post('/order/cart/{}/item/{}/configuration'.format(cartId,itemId),
                           label='vps_ssd_datacenter',
                           value='bhs')
      logging.debug(json.dumps(config,indent=4))
      config = self.post('/order/cart/{}/item/{}/configuration'.format(cartId,itemId),
                           label='vps_ssd_os',
                           value='linux--ubuntu1604-server--64--en')
      logging.debug(json.dumps(config,indent=4))

      # Checkout
      self.post('/order/cart/{}/assign'.format(cartId))
      if DRY_RUN:
         result = self.get('/order/cart/{}/checkout'.format(cartId))
         orderId = 'dryrunorderid'
         logging.info("\n---Checkout Result---\n")
         logging.info(json.dumps(result,indent=4))
      else:
         result = self.post('/order/cart/{}/checkout'.format(cartId))
         orderId = result['orderId']
         self.completeOrder(orderId)
      return orderId

   def vpsTerminate(self, service, token=None):
      global DRY_RUN

      # ensure svc exists
      serviceDetail = next(svc for svc in self.vpsGetServices() if svc['name'] == service)
      if not serviceDetail:
         logging.error('vps: tried to terminate inactive/nonexisting service {}'.format(service))
         return

      if not token:
         # Initiate termination
         ep = '/vps/{}/terminate'.format(service)
         if DRY_RUN:
            logging.info('post({})'.format(ep))
         else:
            self.post(ep)
      else:
         # Confirm termination
         ep = '/vps/{}/confirmTermination'.format(service)
         if DRY_RUN:
            logging.info('post({}, token={})'.format(ep,token))
         else:
            self.post(ep,token=token)

def main():
   global DRY_RUN
   parser = argparse.ArgumentParser()
   parser.add_argument('-l', '--log', help='Log level',
                                      choices=['debug','info','warning','error','critical'],
                                      dest='loglevel',
                                      default='warning')
   parser.add_argument('-c', '--config', help='OVH Config File',
                                         dest='config',
                                         default='./ovh.conf')
   parser.add_argument('-a', '--action', help='Action to take.',
                                         choices=['list','getkey','order','terminate'],
                                         default='list')
   parser.add_argument('-d', '--dry-run', help="See what would've happened.",
                                          dest='dry',
                                          action='store_true',
                                          default=False)
   parser.add_argument('-e', '--key-endpoint', help='Key endpoint',
                                               dest='endpoint')
   parser.add_argument('-s', '--service', help='Service name',
                                          dest='service')
   parser.add_argument('-t', '--token', help='Token',
                                        dest='token')
   parser.add_argument('-r', '--key-recursive', help='Key endpoint is recursive',
                                                dest='recursive',
                                                action='store_true',
                                                default=False)
   parser.add_argument('--key-rw', help='Key read/write permission',
                                   action='store_true',
                                   dest='write',
                                   default=False)
   parser.add_argument('-q', '--quantity', help='Quantity to order',
                                           type=int,
                                           dest='qty',
                                           default=1)
   args = parser.parse_args()
   logging.basicConfig(level=getattr(logging, args.loglevel.upper(), logging.WARNING))
   DRY_RUN=args.dry

   try:
      if not os.path.isfile(args.config):
         logging.exception("{} does not exist".format(args.config))
         sys.exit(1)
      client = OvhClient(config_file=args.config)
      if args.action=='getkey':
         if not args.endpoint:
            logging.exception('Please specify an endpoint.')
            sys.exit(1)
         perm=ovh.API_READ_ONLY
         if args.write:
            perm=ovh.API_READ_WRITE
         print(client.getCK(perm, args.endpoint, args.recursive))
      elif args.action=='list':
         svcs = client.vpsGetServices()
         print(json.dumps(svcs,indent=3))
      elif args.action=='order':
         client.vpsOrder(args.qty, 6.01, cores=1, core_frequency=2.4, ram=2 , disk_space=20)
      elif args.action=='terminate':
         if not args.service:
            logging.exception('Please specify the service name to terminate.')
            sys.exit(1)
         client.vpsTerminate(args.service, args.token)

   except ovh.exceptions.APIError as err:
      logging.exception(err)
      sys.exit(1)


if __name__ == '__main__':
   main()

