from django.contrib.auth.models import User
from django.db.models import Model, CharField, ForeignKey, ImageField, IntegerField

gender_choices = ('m', 'f')


female = 'f'
male = 'm'
unknown_gender = 'u'

GENDER_CHOICES = (
    (female, 'Girl'),
    (male, 'Boy'),
    (unknown_gender, 'Unknown Gender')
)

small = 's'
medium = 'm'
large = 'l'
extra_large = 'xl'
unknown_size = 'u'

SIZE_CHOICES = (
    (small, 'Small'),
    (medium, 'Medium'),
    (large, 'Large'),
    (extra_large, 'Extra Large'),
    (unknown_size, 'Unknown Size')
)

baby = 'b'
young = 'y'
adult = 'a'
senior = 's'

AGE_CHOICES = (
    (baby, 'Baby'),
    (young, 'Young'),
    (adult, 'Adult'),
    (senior, 'Senior'),
)

liked = 'l'
disliked = 'd'
undecided = 'u'

STATUS_CHOICES = (
    (liked, 'Liked'),
    (disliked, 'Disliked'),
    (undecided, 'Undecided')
)


class Dog(Model):
    name = CharField(
        max_length=155,
    )
    image_path = ImageField(
        upload_to='dogs/',
        null=True,
        blank=True,
    )
    breed = CharField(
        max_length=155,
        null=True,
    )
    age = IntegerField()
    gender = CharField(
        max_length=1,
        choices=GENDER_CHOICES,
    )
    size = CharField(
        max_length=2,
        choices=SIZE_CHOICES,
    )

    class Meta:
        unique_together = ('name', 'breed', 'age', 'gender')

    def __str__(self):
        return "{} - {}".format(self.name, self.breed)


class UserDog(Model):
    user = ForeignKey(User)
    dog = ForeignKey(Dog)
    status = CharField(
        max_length=1,
        choices=STATUS_CHOICES,
    )

    class Meta:
        unique_together = ('user', 'dog')

    def __str__(self):
        return "{} - {} ({})".format(
            self.user.username, self.dog.name, self.dog.breed
        )


class UserPref(Model):
    user = ForeignKey(User)
    age = CharField(
        max_length=len(AGE_CHOICES) * 2,
        choices=AGE_CHOICES,
        default=", ".join([x[0] for x in AGE_CHOICES])
    )
    gender = CharField(
        max_length=len(GENDER_CHOICES) * 2,
        choices=GENDER_CHOICES,
        default=", ".join([x[0] for x in GENDER_CHOICES if x != 'u'])
    )
    size = CharField(
        choices=SIZE_CHOICES,
        max_length=len(SIZE_CHOICES) * 2,
        default=", ".join([x[0] for x in SIZE_CHOICES if x != 'u'])
    )

    def __str__(self):
        return self.user.username
