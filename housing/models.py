from django.db import models
from django.contrib.auth.models import AbstractUser





class CustomUser(AbstractUser):
    STUDENT = 'Student'
    LANDLORD = 'Landlord'
    
    USER_TYPES = [
        (STUDENT, 'Student'),
        (LANDLORD, 'Landlord'),
    ]

    username = models.EmailField(max_length=150, unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['user_type']
    

    def __str__(self):
        return self.username


class Accommodation(models.Model):
    
    PROPERTY_TYPE_CHOICES = [
    ('Apartment', 'Apartment'),
    ('Hostel', 'Hostel'),
    ('Single Room', 'Single Room'),
    ('Shared Room', 'Shared Room'),
]
    accommodation_id = models.AutoField(primary_key=True)
    landlord = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Landlord'})
    
    title = models.CharField(max_length=255)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, default=" ")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    address = models.CharField(max_length=255, default="notwane road")
    city = models.CharField(max_length=100, default="Gaborone")
    state = models.CharField(max_length=100, default="South East")
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    square_footage = models.PositiveIntegerField(default=0)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('Available', 'Available'), ('Booked', 'Booked'), ('Coming Soon', 'Coming Soon')], default='Available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.property_type} in {self.city} - {self.price}"
    
    
class AccommodationImage(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='accommodations/')

    def __str__(self):
        return f"Image for {self.accommodation}"


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Student'})
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.booking_id} - {self.accommodation}"


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')])
    transaction_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_id} - {self.payment_status}"


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Student'})
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)

    def __str__(self):
        return f"Review {self.review_id}"


class ReviewDetails(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.review.review_id} - {self.rating} Stars"


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=[('sent', 'sent'), ('failed', 'failed')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification {self.notification_id} - {self.status}"
