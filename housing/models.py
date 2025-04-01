from django.db import models

# Create your models here.


from django.db import models

class User(models.Model):
    STUDENT = 'Student'
    LANDLORD = 'Landlord'
    ADMIN = 'Admin'
    
    USER_TYPES = [
        (STUDENT, 'Student'),
        (LANDLORD, 'Landlord'),
        (ADMIN, 'Admin'),
    ]

    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)

    def __str__(self):
        return self.name

class Accommodation(models.Model):
    accommodation_id = models.AutoField(primary_key=True)
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Landlord'})
    description = models.TextField()
    location = models.CharField(max_length=255)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Available', 'Available'), ('Booked', 'Booked')])
    created_at = models.DateTimeField(auto_now_add=True)
    building_images = models.ImageField(upload_to='accommodations/', blank=True, null=True)

    def __str__(self):
        return self.description

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Student'})
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
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Student'})
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=[('Read', 'Read'), ('Unread', 'Unread')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification {self.notification_id} - {self.status}"
