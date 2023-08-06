from visma.models import Customer, CustomerInvoiceDraft, Account, \
    CompanySettings

#a = Customer.objects.filter(id='91ff2390-968b-4ef7-877d-dd7aef616ae4').order_by('id')
#a = Customer.objects.filter(name='TestCustomer AB').order_by('id')

#a = Account.objects.all()
#print(len(a))
#for item in a:
#    print(item.id)

c = CompanySettings.objects.all().first()
print(c.name)
print(c.product_variant)

#x = Customer.objects.all()
#for i in x:
#    print(i.name)