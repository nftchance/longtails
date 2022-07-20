import datetime

from django.db import models

class TransactionIdentifier(models.Model):
    name = models.CharField(max_length=256)
    args = models.CharField(max_length=256)

    machine_rule = models.TextField()
    machine_timeout = models.PositiveIntegerField(default=0)


class Transaction(models.Model):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.machine_at = self.set_machine_at()

    identifier = models.ForeignKey(
        TransactionIdentifier, on_delete=models.SET_NULL)
    data = models.TextField()

    ran_at = models.DateTimeField()

    machine_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def machine_at(self):
        return (
            self.ran_at +
            datetime.timedelta(seconds=self.machine_rule.seconds_after)
        )

    class Meta:
        ordering = ['-updated_at']


class Opportunity(models.Model):
    contract_address = models.CharField(max_length=256)
    contract_abi = models.TextField()

    identifiers = models.ManyToManyField(TransactionIdentifier)
    transactions = models.ManyToManyField(Transaction)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# we run a clock
# we catch up on every transaction
# for every transaction identifier that matches `.identifier`
#   store the response data into `.data`
#   determine when the machine will need to process the rule
