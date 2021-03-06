from django.db import models
from django.db.transaction import atomic

from enumchoicefield import EnumChoiceField

from app.common.enums import MembershipType
from app.content.models import User
from app.group.models import Group
from app.util.models import BaseModel
from app.util.utils import today


class MembershipHistory(BaseModel):
    """Model for a Group Membership History"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    membership_type = EnumChoiceField(MembershipType, default=MembershipType.MEMBER)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        unique_together = ("user", "group", "end_date")
        verbose_name = "Membership History"
        verbose_name_plural = "Membership Histories"

    def __str__(self):
        return f"{self.user} - {self.group} - {self.membership_type} - {self.end_date}"

    @staticmethod
    def from_membership(membership):
        """Creates a Membership History object from a Membership object"""
        MembershipHistory.objects.create(
            user=membership.user,
            group=membership.group,
            membership_type=membership.membership_type,
            start_date=membership.created_at,
            end_date=today(),
        )


class Membership(BaseModel):
    """Model for a Group Membership"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    membership_type = EnumChoiceField(MembershipType, default=MembershipType.MEMBER)
    expiration_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "group")

    def __str__(self):
        return f"{self.user} - {self.group} - {self.membership_type}"

    def is_leader(self):
        return self.membership_type == MembershipType.LEADER

    def is_board_member(self):
        return self.membership_type in MembershipType.board_members

    def clean(self):
        if self.membership_type in MembershipType.board_members():
            self.swap_board()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Membership, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        MembershipHistory.from_membership(self)
        return super().delete(*args, **kwargs)

    @atomic
    def swap_board(self):
        previous_board_member = (
            Membership.objects.select_for_update()
            .filter(group=self.group, membership_type=self.membership_type)
            .first()
        )

        if previous_board_member and previous_board_member.user != self.user:
            MembershipHistory.from_membership(membership=previous_board_member)
            previous_board_member.membership_type = MembershipType.MEMBER
            previous_board_member.save()

        current_membership = (
            Membership.objects.select_for_update()
            .filter(group=self.group, user=self.user)
            .first()
        )

        if current_membership:
            MembershipHistory.from_membership(membership=current_membership)
